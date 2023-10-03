import os
import sys

current_dir = os.path.dirname(__file__)
framework_dir = os.path.dirname(current_dir)
sys.path.insert(0, framework_dir)

import argparse
import logging
import shutil
import warnings
from pathlib import Path

import torch
from class_resolver import ClassResolver

from commonroad_geometric.common.class_extensions.nested_to_dict import nested_to_dict
from commonroad_geometric.common.config import Config
from commonroad_geometric.dataset.collection.scenario_dataset_collector import ScenarioDatasetCollector
from commonroad_geometric.dataset.extraction.traffic.edge_drawers.implementations import FullyConnectedEdgeDrawer
from commonroad_geometric.dataset.extraction.traffic.traffic_extractor import TrafficExtractorOptions
from commonroad_geometric.dataset.postprocessing.implementations import LaneletSegmentationPostProcessor
from commonroad_geometric.debugging.warnings import debug_warnings
from commonroad_geometric.learning.geometric.base_geometric import MODEL_FILE, OPTIMIZER_FILE, BaseGeometric, MODEL_FILENAME
from commonroad_geometric.learning.geometric.components.encoders.base_encoder import BaseEncoder
from commonroad_geometric.learning.geometric.components.encoders.gcn_encoder import GCNEncoder
from commonroad_geometric.learning.geometric.components.encoders.gru_encoder import GRUEncoder
from commonroad_geometric.learning.geometric.components.encoders.mlp_encoder import MLPEncoder
from commonroad_geometric.learning.geometric.components.encoders.rnn_encoder import RNNEncoder
from commonroad_geometric.learning.geometric.components.encoders.vgae_encoder import VGAEEncoder
from commonroad_geometric.learning.geometric.training.callbacks.callback_computer_container_service import CallbackComputerContainerService, CallbackComputersContainer
from commonroad_geometric.learning.geometric.training.callbacks.implementations.early_stopping_callback import EarlyStoppingCallback
from commonroad_geometric.learning.geometric.training.callbacks.implementations.epoch_checkpoint_callback import EpochCheckpointCallback
from commonroad_geometric.learning.geometric.training.callbacks.implementations.export_latest_model_callback import ExportLatestModelCallback
from commonroad_geometric.learning.geometric.training.callbacks.implementations.log_wandb_callback import LogWandbCallback
from commonroad_geometric.learning.geometric.training.callbacks.implementations.watch_model_callback import WatchWandbCallback
from commonroad_geometric.learning.geometric.training.experiment import GeometricExperiment, GeometricExperimentConfig
from commonroad_geometric.learning.geometric.training.geometric_trainer import GeometricTrainer
from commonroad_geometric.learning.training.git_features.defaults import DEFAULT_GIT_FEATURE_COLLECTORS
from commonroad_geometric.learning.training.git_features.git_feature_collector import GitFeatureCollector
from commonroad_geometric.learning.training.wandb_service import WandbService
from tutorials.train_geometric_model.common import optimizer_service
from tutorials.train_geometric_model.models.generative_model import GenerativeModel
from tutorials.train_geometric_model.models.recurrent_model import RecurrentModel

warnings.filterwarnings("ignore")
logger = logging.getLogger(__name__)

encoder_resolver = ClassResolver(
    [VGAEEncoder, GCNEncoder, RNNEncoder, MLPEncoder, GRUEncoder],
    base=BaseEncoder,
    default=VGAEEncoder,
)

model_resolver = ClassResolver(
    [GenerativeModel, RecurrentModel],
    base=BaseGeometric,
    default=GenerativeModel,
)

DEFAULT_HIDDEN_CHANNELS = 20
DATA_COLLECTOR_CLS = ScenarioDatasetCollector
MAX_SAMPLES = 1000
DATASET_DIR = f'{Config.OUTPUT_DIR}/dataset'
MODEL_DIR = f'{Config.OUTPUT_DIR}/model'
SCENARIO_DIR = 'data/highd' if DATA_COLLECTOR_CLS is ScenarioDatasetCollector else 'data/highway_test'
n_trials = 1000


def main(args):
    train_batch_size = 20
    MAX_EPOCHS = 20000
    if args.optimize:
        MAX_EPOCHS = 50
    SCENARIO_DIR = args.scenario_dir
    DATASET_DIR = args.dataset_dir
    if args.pre_process:
        shutil.rmtree(DATASET_DIR, ignore_errors=True)

    experiment = GeometricExperiment(GeometricExperimentConfig(
        traffic_extraction_options=TrafficExtractorOptions(
            edge_drawer=FullyConnectedEdgeDrawer(),
        ),
        data_collector_cls=ScenarioDatasetCollector,
        preprocessors=Config.PREPROCESSORS,
        postprocessors=[LaneletSegmentationPostProcessor(ensure_multiple_nodes_per_sample = True)]
    ))

    dataset =  experiment.collect_traffic_dataset(
        scenario_dir=args.scenario_dir,
        dataset_dir=DATASET_DIR,
        overwrite=args.overwrite,
        pre_transform_workers=args.n_workers,
        cache_data=Config.CACHE_DATA
    )

    logger.info(f"Done exporting graph dataset")

    if args.warmstart:
        latest_model_path = os.path.join(latest_dir, MODEL_FILE)
        latest_optimizer_state_path = os.path.join(latest_dir, OPTIMIZER_FILE)
        model = model_resolver.lookup(args.m).load(latest_model_path)
        optimizer_state = torch.load(latest_optimizer_state_path)
    else:
        model = model_resolver.lookup(args.m)()
        optimizer_state = None
    model.train(True)

    encoder: BaseEncoder = encoder_resolver.lookup(args.e)()

    model_name = f'{type(model).__name__.lower()}-{type(encoder).__name__}'

    hidden_channels = args.hc

    model_kwargs = {'hidden_channels': hidden_channels, 'encoder': encoder, 'raw_dir': SCENARIO_DIR, 'processed_dir': DATASET_DIR}

    wandb_service = WandbService()
    feature_collector = GitFeatureCollector(DEFAULT_GIT_FEATURE_COLLECTORS)
    features = feature_collector()
    #model_name = model_name + ",".join("{}={}".format(*i) for i in features.items())

    optimization_service = optimizer_service(
        wandb_service=wandb_service,
        use_sweeps=args.use_sweeps,
        n_trials=n_trials,
    )

    base_trainer = GeometricTrainer(
        max_epochs=MAX_EPOCHS,
        device='cuda',
        overfit=args.overfit,
        max_optimize_samples=1000,
        validation_freq=20,
        validate_inner=False,
        enable_multi_gpu=False
    )

    wandb_metadata = dict(
        training={
            "epochs": MAX_EPOCHS,
            "batch_size": train_batch_size,
        },
        experiment=nested_to_dict(experiment.config),
        model=nested_to_dict(model.config) if hasattr(model, 'config') else None
    )

    wandb_kwargs = {}
    if base_trainer.multi_gpu():
        wandb_kwargs["group"] = f'{type(model).__name__}-DDP'

    model_name = wandb_service.start_experiment(
        name=model_name,
        metadata=wandb_metadata,
        include_timestamp=False,
        **wandb_kwargs
    )

    BASE_OUTPUT_DIR = f'{Config.OUTPUT_DIR}/{model_name}'
    base_checkpoint_directory = f'{BASE_OUTPUT_DIR}/checkpoints'
    latest_dir = os.path.join(BASE_OUTPUT_DIR , "latest")

    initialize_training_callbacks_params = [WatchWandbCallback(wandb_service=wandb_service)]

    # if not args.optimize:
    #     initialize_training_callbacks_params.append(WarmStartCallback(base_checkpoint_directory))

    callbacks_computers = CallbackComputersContainer(
        initialize_training_callbacks=CallbackComputerContainerService(initialize_training_callbacks_params),
        training_step_callbacks=CallbackComputerContainerService([
            ExportLatestModelCallback(directory=latest_dir),
            LogWandbCallback(wandb_service=wandb_service)
        ]),
        checkpoint_callbacks=CallbackComputerContainerService(
            [EpochCheckpointCallback(directory=base_checkpoint_directory)]),
        early_stopping_callbacks=CallbackComputerContainerService([EarlyStoppingCallback(after_epochs=150)]),
    )

    if not args.optimize:
        dataset, _ = dataset.split(MAX_SAMPLES, True)
    base_trainer.launch_trainer(
        model_dir=MODEL_DIR,
        experiment=experiment,
        dataset=dataset,
        model=model,
        wandb_service=wandb_service,
        train_batch_size=train_batch_size,
        optimizer_service=optimization_service if args.optimize else None,
        model_kwargs=model_kwargs,
        optimizer_state=optimizer_state,
        callbacks_computers=callbacks_computers
    )

    base_trainer.train(
        trial=None,
        model=model,
        experiment=experiment,
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--m',
        type=str,
        default='GenerativeModel',
        const='GenerativeModel',
        nargs='?',
        choices=['GenerativeModel', 'RecurrentModel'],
        help='Model to train'
    )
    parser.add_argument('--e',
        type=str,
        default='VGAEEncoder',
        const='VGAEEncoder',
        nargs='?',
        choices=['VGAEEncoder', 'GCNEncoder', 'RNNEncoder', 'MLPEncoder', 'GRUEncoder'],
        help='Set the encoder function'
    )
    parser.add_argument("--hc", default=DEFAULT_HIDDEN_CHANNELS, type=int, help="Set the hidden channels")
    parser.add_argument("--scenario-dir", default=SCENARIO_DIR, type=str, help="Set the scenario directory")
    parser.add_argument("--dataset_dir", default=DATASET_DIR, type=str, help="Set the dataset directory")
    parser.add_argument("--overfit", default=False, type=bool, action=argparse.BooleanOptionalAction, help="Overfit the model")
    parser.add_argument("--pre-process", default=False, type=bool, action=argparse.BooleanOptionalAction, help="Preprocess and recreate dataset")
    parser.add_argument("--optimize", default=False, type=bool, action=argparse.BooleanOptionalAction, help="Use an optimization service to optimize the model hyperparameters")
    parser.add_argument("--use_sweeps", type=bool, action=argparse.BooleanOptionalAction, help="Use wandb sweeps for optimization. (Requires the user to launch the program via the provided shell script)")
    parser.add_argument("--output-dir", default=Config.OUTPUT_DIR, type=Path, help="output directory for the experiment")
    parser.add_argument("--profile", action="store_true", help="profiles code")
    parser.add_argument("--no-warn", action="store_true", help="disable warnings")
    parser.add_argument("--debug", action="store_true", help="activates debug logging")
    parser.add_argument("--overwrite", action="store_true", help="remove and re-create the output directory before training")
    parser.add_argument("--n-workers", type=int, help="number of processes", default=1)
    parser.add_argument("--warmstart", action="store_true", help="continue from latest checkpoint")
    # Dummy argument to allow argsparse to work in ipython/debugging situations
    parser.add_argument('-f', '--fff', default='1', 
    help='Dummy argument to allow argsparse to work in ipython/debugging situations')

    args: argparse.Namespace = parser.parse_args()
    def run_main() -> None:
        if args.profile:
            from commonroad_geometric.debugging.profiling import profile
            profile(main, dict(args=args))
        else:
            main(args)

    if args.no_warn:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            run_main()
    elif args.debug:
        debug_warnings(run_main)
    else:
        run_main()
