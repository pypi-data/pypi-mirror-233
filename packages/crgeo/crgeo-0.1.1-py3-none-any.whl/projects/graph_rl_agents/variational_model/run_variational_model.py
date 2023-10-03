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
from typing import Any, Dict, Optional, Type

import torch

import projects.graph_rl_agents.variational_model.variational_model_config as Config
from commonroad_geometric.dataset.extraction.traffic.traffic_extractor import TrafficFeatureComputerOptions
from commonroad_geometric.common.logging import LoggingFormat, setup_logging
from commonroad_geometric.common.utils.seeding import get_random_seed
from commonroad_geometric.dataset.extraction.traffic import TrafficExtractorOptions
from commonroad_geometric.dataset.extraction.traffic.edge_drawers.base_edge_drawer import BaseEdgeDrawer
from commonroad_geometric.dataset.preprocessing.implementations.hijack_vehicle_preprocessor import HijackVehiclePreprocessor
from commonroad_geometric.dataset.preprocessing.implementations.lanelet_network_subset_preprocessor import LaneletNetworkSubsetPreprocessor
from commonroad_geometric.debugging.warnings import debug_warnings
from commonroad_geometric.learning.reinforcement import RLEnvironmentOptions, RLTrainer
from commonroad_geometric.learning.reinforcement.base_geometric_feature_extractor import BaseGeometricFeatureExtractor
from commonroad_geometric.learning.reinforcement.experiment import RLExperiment, RLExperimentConfig
from commonroad_geometric.learning.reinforcement.observer.flattened_graph_observer import FlattenedGraphObserver
from commonroad_geometric.learning.reinforcement.termination_criteria.implementations.timeout_criterion import TimeoutCriterion
from commonroad_geometric.learning.reinforcement.training.rl_trainer import RLTrainerParams
from commonroad_geometric.simulation.base_simulation import BaseSimulation, BaseSimulationOptions
from commonroad_geometric.simulation.ego_simulation.control_space import BaseControlSpace, BaseControlSpaceOptions
from commonroad_geometric.simulation.ego_simulation.control_space.implementations import LongitudinalControlSpace, PIDControlSpace, PIDLaneChangeControlSpace, SteeringAccelerationSpace
from commonroad_geometric.simulation.ego_simulation.respawning import BaseRespawner, BaseRespawnerOptions
from commonroad_geometric.simulation.ego_simulation.respawning.implementations import PlanningProblemRespawner, PlanningProblemRespawnerOptions, RandomRespawner, RandomRespawnerOptions
from commonroad_geometric.simulation.ego_simulation.respawning.implementations.in_between_traffic_respawner import InBetweenTrafficRespawner
from commonroad_geometric.simulation.interfaces.interactive.sumo_simulation import SumoSimulation, SumoSimulationOptions
from commonroad_geometric.simulation.interfaces.interactive.traffic_spawning import BaseTrafficSpawner
from commonroad_geometric.simulation.interfaces.interactive.traffic_spawning.implementations import ConstantPopulationSpawner, ConstantRateSpawner, OrnsteinUhlenbeckSpawner
from commonroad_geometric.simulation.interfaces.static.compressed_scenario_simulation import CompressedScenarioSimulation, CompressedSimulationOptions
from commonroad_geometric.simulation.interfaces.static.scenario_simulation import ScenarioSimulation, ScenarioSimulationOptions
from commonroad_geometric.simulation.interfaces.static.unpopulated_scenario_simulation import UnpopulatedScenarioSimulation
from projects.graph_rl_agents.lane_occupancy.utils.lanelet_graph_feature_extractor import LaneletGraphFeatureExtractor
from projects.graph_rl_agents.lane_occupancy.utils.occupancy_encoding_post_processor import OccupancyEncodingPostProcessor
from projects.graph_rl_agents.v2v_policy.feature_extractor import VehicleGraphFeatureExtractor

logger = logging.getLogger(__name__)

torch.set_printoptions(precision=2, sci_mode=False)


def setup_trainer(
    output_dir: str,
    interactive: bool,
    unpopulated: bool,
    async_resets: bool,
    use_pickled_trajectories: bool,
    rendering: bool,
    render_debug_overlays: bool,
    random_planning_problems: bool,
    lc_planning_problems: bool,
    control_space_cls: Type[BaseControlSpace],
    control_space_options: BaseControlSpaceOptions,
    traffic_spawner: BaseTrafficSpawner,
    n_rollout_steps: int,
    feature_extractor_cls: Type[BaseGeometricFeatureExtractor] = None,
    feature_extractor_kwargs: Optional[Dict[str, Any]] = None,
) -> RLTrainer:
    respawner_options: BaseRespawnerOptions
    respawner_cls: Type[BaseRespawner]
    if lc_planning_problems:
        respawner_options = Config.IN_BETWEEN_TRAFFIC_RESPAWNER_OPTIONS
        respawner_cls = InBetweenTrafficRespawner
    elif interactive or random_planning_problems:
        respawner_options = RandomRespawnerOptions(
            init_speed=35, 
            start_arclength=40.0, 
            end_offset=50.0, 
            max_attempts_outer=100, 
            max_attempts_inner=50,
            max_respawn_attempts=10
        )
        respawner_cls = RandomRespawner
    else:
        respawner_options = PlanningProblemRespawnerOptions()
        respawner_cls = PlanningProblemRespawner

    simulation_options: BaseSimulationOptions
    simulation_cls: Type[BaseSimulation]
    if interactive:
        simulation_options = SumoSimulationOptions(
            lanelet_assignment_order=Config.LANELET_ASSIGNMENT_STRATEGY,
            traffic_spawner=traffic_spawner,
            presimulation_steps=Config.SUMO_PRESIMULATION_STEPS  # Presimulation steps and ego-vehicle spawning don't play nice at the moment with _CRSumoSimulation
        )
        simulation_cls = SumoSimulation
    elif use_pickled_trajectories:
        simulation_options = CompressedSimulationOptions(
            lanelet_assignment_order=Config.LANELET_ASSIGNMENT_STRATEGY,
            backup_initial_scenario=False,
        )
        simulation_cls = CompressedScenarioSimulation
    else:
        simulation_options = ScenarioSimulationOptions(
            lanelet_assignment_order=Config.LANELET_ASSIGNMENT_STRATEGY
        )
        simulation_cls = UnpopulatedScenarioSimulation if unpopulated else ScenarioSimulation
    if isinstance(simulation_options, ScenarioSimulationOptions) and control_space_cls == LongitudinalControlSpace:
        simulation_options.remove_ego_vehicle_from_obstacles = True

    Config.AGENT_KWARGS["n_steps"] = n_rollout_steps

    if args.hijack_preprocessing:
        Config.SCENARIO_PREPROCESSORS = [HijackVehiclePreprocessor()] + Config.SCENARIO_PREPROCESSORS
    if args.subset_preprocessing:
        Config.SCENARIO_PREPROCESSORS = [LaneletNetworkSubsetPreprocessor()] + Config.SCENARIO_PREPROCESSORS
    if args.max_timesteps_per_episode is not None:
        Config.TERMINATION_CRITERIA.append(TimeoutCriterion(max_timesteps=args.max_timesteps_per_episode))
    if args.hd_videos:
        Config.RENDERER_OPTIONS[0].window_size_multiplier = 3.0
        Config.RENDERER_OPTIONS[0].disable_overlays = True

    if args.embeddings_model_path:
        Config.POSTPROCESSORS.extend([OccupancyEncodingPostProcessor(args.embeddings_model_path, max_lanelet_length=Config.LANELET_SEGMENTS_MAX_LENGTH)])
    
    edge_drawer_cls = BaseEdgeDrawer.resolve(args.edge_drawer)

    experiment = RLExperiment(RLExperimentConfig(
        simulation_cls=simulation_cls,
        simulation_options=simulation_options,
        control_space_cls=control_space_cls,
        control_space_options=control_space_options,
        respawner_cls=respawner_cls,
        respawner_options=respawner_options,
        traffic_extraction_options=TrafficExtractorOptions(
            edge_drawer=edge_drawer_cls(Config.EDGE_DRAWER_DIST_THRESHOLD),
            feature_computers=TrafficFeatureComputerOptions(
                v=Config.V_FEATURE_COMPUTERS,
                v2v=Config.V2V_FEATURE_COMPUTERS,
                l=Config.L_FEATURE_COMPUTERS,
                l2l=Config.L2L_FEATURE_COMPUTERS,
                v2l=Config.V2L_FEATURE_COMPUTERS,
            ),
            postprocessors=Config.POSTPROCESSORS,
            only_ego_inc_edges=False, # set to True to speed up extraction for 1-layer GNNs
            normalize_features=Config.NORMALIZE_FEATURES,
            assign_multiple_lanelets=True
        ),
        ego_vehicle_simulation_options=Config.EGO_VEHICLE_SIMULATION_OPTIONS,
        rewarder=Config.REWARDER,
        termination_criteria=Config.TERMINATION_CRITERIA,
        env_options=RLEnvironmentOptions(
            async_resets=async_resets,
            num_respawns_per_scenario=-1 if interactive else args.respawns_per_scenario,
            loop_scenarios=True,
            scenario_preprocessors=Config.SCENARIO_PREPROCESSORS,
            render_on_step=rendering,
            render_debug_overlays=render_debug_overlays,
            renderer_options=Config.RENDERER_OPTIONS,
            raise_exceptions=args.debug,
            observer=FlattenedGraphObserver(
                data_padding_size=1000,
                global_features_include=Config.GLOBAL_FEATURES_INCLUDE
            )
        )
    ))

    rl_trainer = RLTrainer(
        params=RLTrainerParams(
            experiment=experiment,
            output_dir=output_dir,
            feature_extractor_cls=feature_extractor_cls,
            feature_extractor_kwargs=feature_extractor_kwargs,
            agent_cls=Config.AGENT_CLS,
            agent_kwargs=Config.AGENT_KWARGS,
            net_arch=Config.AGENT_NET_ARCH,
            activation_fn=Config.AGENT_ACT_FUN,
            policy_cls=Config.AGENT_POLICY,
            policy_kwargs=Config.AGENT_POLICY_KWARGS,
            optimizer_class=Config.OPTIMIZER,
            optimizer_kwargs=Config.OPTIMIZER_KWARGS,
            project_name='train_graph_rl_' + args.d.lower(),
        )
    )

    return rl_trainer


def main(args) -> None:
    setup_logging(
        filename=args.log_file,
        level=logging.DEBUG if args.debug else logging.INFO,
        fmt=LoggingFormat.ONLY_FILENAMES_MP
    )

    if args.seed is not None:
        seed = args.seed
    else:
        seed = get_random_seed()
        logger.info(f"Using random seed: {seed}")

    output_dir = os.path.join(args.output_dir, args.d)
    os.makedirs(output_dir, exist_ok=True)

    if args.overwrite:
        shutil.rmtree(output_dir, ignore_errors=True)

    if args.traffic_spawner == 'constant_population':
        traffic_spawner = ConstantPopulationSpawner(args.population_size)  # noqa: 405
    elif args.traffic_spawner == 'constant_rate':
        traffic_spawner = ConstantRateSpawner(args.spawn_rate)  # noqa: 405
    else:
        traffic_spawner = OrnsteinUhlenbeckSpawner()  # noqa: 405

    control_space_cls: Type[BaseControlSpace]
    control_space_options: BaseControlSpaceOptions
    if args.control_space == 'pid':
        control_space_cls = PIDControlSpace
        control_space_options = Config.PID_CONTROL_SPACE_OPTIONS
    elif args.control_space == 'lo':
        control_space_cls = LongitudinalControlSpace
        control_space_options = Config.LONGITUDINAL_CONTROL_OPTIONS
    elif args.control_space == 'sa':
        control_space_cls = SteeringAccelerationSpace
        control_space_options = Config.STEERING_ACCELERATION_CONTROL_SPACE_OPTIONS
    elif args.control_space == 'pidlc':
        control_space_cls = PIDLaneChangeControlSpace
        control_space_options = Config.PID_LANE_CHANGE_CONTROL_SPACE

    if args.feature_extractor == 'vehicle_graph':
        feature_extractor_cls = VehicleGraphFeatureExtractor
    elif args.feature_extractor == 'lanelet_graph':
        feature_extractor_cls = LaneletGraphFeatureExtractor
    elif args.feature_extractor == 'vehicle_embeddings':
        feature_extractor_cls = VehicleEmbeddingsFeatureExtractor
    else:
        raise NotImplementedError(args.feature_extractor)
    feature_extractor_kwargs = Config.FEATURE_EXTRACTOR_KWARGS
    if args.dummy_values:
        feature_extractor_kwargs['dummy_values'] = True
        feature_extractor_kwargs['device'] = args.device

    rl_trainer = setup_trainer(
        output_dir=output_dir,
        interactive=args.interactive,
        unpopulated=args.unpopulated,
        async_resets=not args.no_async_resets,
        use_pickled_trajectories=args.use_pickled_trajectories,
        rendering=args.rendering or args.play,
        render_debug_overlays=not args.no_overlays,
        random_planning_problems=args.random_planning_problems,
        lc_planning_problems=args.lane_change_planning_problems,
        control_space_cls=control_space_cls,
        control_space_options=control_space_options,
        traffic_spawner=traffic_spawner,
        feature_extractor_cls=feature_extractor_cls,
        feature_extractor_kwargs=feature_extractor_kwargs,
        n_rollout_steps=args.n_rollout_steps
    )

    if args.play:
        logger.info("Playing agent")

        def play() -> None:
            rl_trainer.play(scenario_dir=args.scenario_dir)

        if args.profile:
            from commonroad_geometric.debugging.profiling import profile
            profile(play)
        else:
            play()

    else:
        logger.info("Training agent")
        rl_trainer.train(
            scenario_dir=args.scenario_dir,
            total_timesteps=args.total_timesteps,
            n_envs=args.n_envs,
            checkpoint_freq=10000,
            n_eval_episodes=10,
            eval_freq=None if args.no_eval else 20000,
            record_freq=None if (args.no_record or args.rendering) else args.recording_frequency,
            video_length=args.video_length,
            verbose=2,
            device=args.device,
            seed=seed,
            wandb_logging=not args.no_wandb,
            experiment_message=args.m,
            normalize_rewards=Config.NORMALIZE_REWARDS,
            checkpoint=args.checkpoint_dir,
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train reinforcement learning agent.")
    parser.add_argument("-m", type=str, help="experiment message (will be appended to experiment name)", required=True)
    parser.add_argument("-d", type=str, help="dataset suffix allowing storing and training on separate datasets", default='main')
    parser.add_argument("--scenario-dir", type=Path, default=Config.SCENARIO_DIR, help="path to scenario directory used for training")
    parser.add_argument("--output-dir", default=Config.DEFAULT_OUTPUT_DIR, type=Path, help="output directory for the RL experiment")
    parser.add_argument("--overwrite", action="store_true", help="remove and re-create the output directory before training")
    parser.add_argument("--log-file", default="train-rl-agent.log", help="path to the log file")
    parser.add_argument("--seed", type=int, help="integer for seeding the random number generator")
    parser.add_argument("--total-timesteps", type=int, default=Config.DEFAULT_TOTAL_TIMESTEPS, help="total timesteps to train the RL agent for")
    parser.add_argument("--n-envs", type=int, default=1, help="number of parallel training environments to use")
    parser.add_argument("--n-rollout-steps", type=int, default=Config.DEFAULT_NUM_ROLLOUT_STEPS, help="number of rollout steps")
    parser.add_argument("--respawns-per-scenario", type=int, default=Config.NUM_RESPAWNS_PER_SCENARIO)
    parser.add_argument("--interactive", action="store_true", help="whether to train with interactive traffic via SUMO")
    parser.add_argument("--unpopulated", action="store_true", help="whether to train without other traffic participants")
    parser.add_argument("--use-pickled-trajectories", action='store_true', help="whether to look for pickled trajectories in parent directory of scenario dir (../trajectories)")
    parser.add_argument("--random-planning-problems", action="store_true", help="whether to randomize planning problems at each environment reset")
    parser.add_argument("--lane-change-planning-problems", action="store_true", help="whether to randomize create lane change situations")
    parser.add_argument('--feature-extractor',
                        default=Config.DEFAULT_FEATURE_EXTRACTOR,
                        const=Config.DEFAULT_FEATURE_EXTRACTOR,
                        nargs='?',
                        choices=['vehicle_graph', 'lanelet_graph', 'ego_lanelet', 'vehicle_embeddings'],
                        help='type of feature extractor used for RL model')
    parser.add_argument('--traffic-spawner',
                        default='constant_population',
                        const='constant_population',
                        nargs='?',
                        choices=['constant_population', 'constant_rate', 'ornstein_uhlenbeck'],
                        help='type of traffic spawned used for interactive SUMO simulation')
    parser.add_argument('--control-space',
                        default=Config.DEFAULT_CONTROL_SPACE,
                        const=Config.DEFAULT_CONTROL_SPACE,
                        nargs='?',
                        choices=['pid', 'sa', 'lo', 'pidlc'],
                        help='type of control space for RL agent (pid=PIDControlSpace, sa=SteeringAccelerationControlSpace, lo=LongitudinalControlSpace, pidlc=PIDLaneChangeControlSpace)')
    parser.add_argument("--population-size", type=int, default=5, help="population size for constant_population traffic spawner")
    parser.add_argument("--spawn-rate", type=float, default=0.01, help="spawn rate for constant_rate traffic spawner")
    parser.add_argument("--rendering", action="store_true", help="whether to render the environment during training")
    parser.add_argument("--no-overlays", action="store_true", help="whether to disable the rendering of debugging overlays")
    parser.add_argument("--recording-frequency", type=int, default=5000, help="how frequently in terms of time-steps a video of the agent should be recorded")
    parser.add_argument("--video-length", type=int, default=2000, help="how many timesteps to record the agent")
    parser.add_argument("--play", action="store_true", help="play the agent using the keyboard (forces rendering=True)")
    parser.add_argument("--device", type=str, default='auto', help="torch device")
    parser.add_argument("--edge-drawer", type=str, default='NoEdgeDrawer', help="type of edge drawer to use")
    parser.add_argument("--no-warn", action="store_true", help="disables warnings")
    parser.add_argument("--no-wandb", action="store_true", help="disable wandb logging")
    parser.add_argument("--no-record", action="store_true", help="disable video logging")
    parser.add_argument("--hd-videos", action="store_true", help="high res video exports")
    parser.add_argument("--subset-preprocessing", action="store_true", help="extract subsets of lanelet network for training")
    parser.add_argument("--hijack-preprocessing", action="store_true", help="hijack existing vehicles for creating planning problems")
    parser.add_argument("--occ-encodings", action="store_true", help="add postprocessing steps for extracting occupancy encodings")
    parser.add_argument("--occ-model-path", type=str, help="path to pretrained occupancy encoding model")
    parser.add_argument("--embeddings-model-path", type=str, help="path to pretrained occupancy encoding model")
    parser.add_argument("--no-eval", action="store_true", help="disable eval runs")
    parser.add_argument("--no-async-resets", action="store_true", help="disable async episode resets")
    parser.add_argument("--profile", action="store_true", help="profiles code")
    parser.add_argument("--max-timesteps-per-episode", type=int, help="optional upper bound for number of timesteps per episode")
    parser.add_argument("--debug", action="store_true", help="activates debug logging")
    parser.add_argument("--dummy-values", action="store_true", help="activates debug logging")
    parser.add_argument("--checkpoint-dir", type=Path, default=None, help="path to the rl agent checkpoint")
    args = parser.parse_args()

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
