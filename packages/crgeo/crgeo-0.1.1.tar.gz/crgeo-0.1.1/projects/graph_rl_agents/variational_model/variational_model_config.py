# flake8: noqa
# type: ignore

import os

import torch
from commonroad.common.solution import VehicleType
from stable_baselines3 import PPO
from torch import nn

from commonroad_geometric.common.io_extensions.scenario import LaneletAssignmentStrategy
from commonroad_geometric.dataset.extraction.traffic.feature_computers.implementations.lanelet import LaneletGeometryFeatureComputer, LaneletVerticesFeatureComputer
from commonroad_geometric.dataset.extraction.traffic.feature_computers.implementations.lanelet_to_lanelet import LaneletConnectionGeometryFeatureComputer
from commonroad_geometric.dataset.extraction.traffic.feature_computers.implementations.vehicle import AccelerationFeatureComputer, EgoFramePoseFeatureComputer, NumLaneletAssignmentsFeatureComputer, \
    VehicleLaneletConnectivityComputer, VehicleLaneletPoseFeatureComputer, VehicleVerticesFeatureComputer, YawRateFeatureComputer, ft_orientation, ft_orientation_vec, ft_vehicle_shape, ft_velocity
from commonroad_geometric.dataset.extraction.traffic.feature_computers.implementations.vehicle_to_lanelet import VehicleLaneletPoseEdgeFeatureComputer
from commonroad_geometric.dataset.extraction.traffic.feature_computers.implementations.vehicle_to_vehicle import \
    ClosenessFeatureComputer, TimeToCollisionFeatureComputer, ft_rel_state
from commonroad_geometric.dataset.preprocessing.implementations.lanelet_network_subset_preprocessor import LaneletNetworkSubsetPreprocessor
from commonroad_geometric.dataset.preprocessing.implementations.vehicle_filter_preprocessor import VehicleFilterPreprocessor
from commonroad_geometric.learning.reinforcement.rewarder.reward_aggregator.implementations import SumRewardAggregator
from commonroad_geometric.learning.reinforcement.rewarder.reward_computer.implementations import CollisionPenaltyRewardComputer, IncentivizeLaneChangeRewardComputer, ConstantRewardComputer, \
    StillStandingPenaltyRewardComputer
from commonroad_geometric.learning.reinforcement.termination_criteria.implementations import CollisionCriterion, OffroadCriterion
from commonroad_geometric.rendering.plugins import RenderEgoVehicleCloseupPlugin, RenderEgoVehiclePlugin, RenderLaneletNetworkPlugin, RenderObstaclesPlugin, RenderPlanningProblemSetPlugin, \
    RenderTrafficGraphPlugin
from commonroad_geometric.rendering.traffic_scene_renderer import TrafficSceneRendererOptions
from commonroad_geometric.simulation.ego_simulation.control_space.implementations import LongitudinalControlOptions, PIDControlOptions, PIDLaneChangeControlOptions, SteeringAccelerationControlOptions
from commonroad_geometric.simulation.ego_simulation.ego_vehicle import VehicleModel
from commonroad_geometric.simulation.ego_simulation.ego_vehicle_simulation import EgoVehicleSimulationOptions
from commonroad_geometric.simulation.ego_simulation.respawning.implementations.in_between_traffic_respawner import InBetweenTrafficRespawnerOptions
from projects.geometric_models.lane_occupancy.utils.renderer_plugins import RenderLaneletEncodingPlugin, RenderLaneletOccupancyPredictionPlugin

TUTORIALS_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DEFAULT_OUTPUT_DIR = os.path.join(TUTORIALS_DIR, 'output/rl')
SCENARIO_DIR = os.path.join(TUTORIALS_DIR, 'test_scenarios/t_junction_recorded')

#DEFAULT_FEATURE_EXTRACTOR = 'lanelet_graph'
# DEFAULT_CONTROL_SPACE = 'sa'
DEFAULT_CONTROL_SPACE = 'lo'
# DEFAULT_CONTROL_SPACE = 'pidlc'
# SCENARIO_DIR = 'data/other/'
# SCENARIO_DIR = 'data/osm_crawled/DEU_Berlin_2-2341.xml'
# SCENARIO_DIR = 'data/other_recordings/ZAM_Tjunction-1_50_T-1_time_steps_100_V1_0.xml'
# SCENARIO_DIR = 'data/other/DEU_Muehlhausen-14_1_T-1.xml'
# SCENARIO_DIR = 'data/highd-test'
# SCENARIO_DIR = 'data/other'
#SCENARIO_DIR = 'data/intersections_test'
#SCENARIO_DIR = 'data/interaction_sample'
#SCENARIO_DIR = 'data/ind_sample'

# DEFAULT_FEATURE_EXTRACTOR = 'lanelet_graph'
DEFAULT_FEATURE_EXTRACTOR = 'vehicle_graph'
# DEFAULT_FEATURE_EXTRACTOR = 'ego_lanelet'
# EDGE_DRAWER = FullyConnectedEdgeDrawer(dist_threshold=30.0)
# EDGE_DRAWER = NoEdgeDrawer()
# EDGE_DRAWER = VoronoiEdgeDrawer(dist_threshold=30.0)
EDGE_DRAWER_DIST_THRESHOLD = 30.0

# General settings
LANELET_ASSIGNMENT_STRATEGY = LaneletAssignmentStrategy.ONLY_SHAPE
DEFAULT_TOTAL_TIMESTEPS = int(1e9)
MIN_SCENARIO_LENGTH = 50
NUM_RESPAWNS_PER_SCENARIO = 0
SUMO_PRESIMULATION_STEPS = 0
NORMALIZE_FEATURES = False # note: broken
NORMALIZE_REWARDS = True
LANELET_SEGMENTS_MAX_LENGTH = 400

def depopulation_schedule(i: int) -> float:
    return max(0.22, 0.10 + i/5000)

SCENARIO_PREPROCESSORS = [
    #HijackVehiclePreprocessor(),
    LaneletNetworkSubsetPreprocessor(),
    VehicleFilterPreprocessor(),
    #SegmentLaneletsPreprocessor()
    #(DepopulateScenarioPreprocessor(1), 1),
]
POSTPROCESSORS = [
    #VirtualEgoLaneletPostProcessor(lanelet_length=50.0),
    #RemoveEgoLaneletConnectionsPostProcessor()
]
GLOBAL_FEATURES_INCLUDE = {
    'embeddings'
}

RENDERER_OPTIONS = [
    TrafficSceneRendererOptions( # 1. For recording videos
        plugins=[
            RenderLaneletNetworkPlugin(
                render_id=False,
                enable_ego_rendering=True,
                from_graph=False,
                randomize_lanelet_color=False
            ),
            #RenderLaneletEncodingPlugin(y_offset=-20.),
            RenderPlanningProblemSetPlugin(render_trajectory=False),
            RenderTrafficGraphPlugin(),
            RenderObstaclesPlugin(
                randomize_color_from_lanelet=False
            ),
            RenderEgoVehiclePlugin(),
            #RenderEgoVehicleInputPlugin(),
            RenderEgoVehicleCloseupPlugin(),
            # RenderObstaclesEgoFramePlugin()
            # RenderVehicleToLaneletEdges()
        ]
    ),
    TrafficSceneRendererOptions(  # 2. For high-resolution png screenshots
        window_size_multiplier=6.0,
        render_freq=500,
        minimize_window=True,
        disable_overlays=True,
        export_dir=os.path.join(DEFAULT_OUTPUT_DIR, 'images'),
        plugins=[
            RenderLaneletEncodingPlugin(y_offset=-20.),
            RenderLaneletNetworkPlugin(
                render_id=False,
                enable_ego_rendering=True,
                from_graph=False
            ),
            RenderLaneletOccupancyPredictionPlugin(enable_matplotlib_plot=False),
            RenderPlanningProblemSetPlugin(render_trajectory=True),
            RenderTrafficGraphPlugin(),
            RenderObstaclesPlugin(),
            RenderEgoVehiclePlugin(),
        ]
    )
]


# RL Agent configuration
AGENT_CLS = PPO
# Tuning tips: https://arxiv.org/pdf/2006.05990.pdf
DEFAULT_NUM_ROLLOUT_STEPS = 256
AGENT_KWARGS = dict(
    batch_size=2,
    gae_lambda=0.9,
    gamma=0.99,
    n_epochs=4,  # decrease this for stability
    ent_coef=0.01,
    vf_coef=0.5,
    max_grad_norm=0.5,
    learning_rate=3e-4, #get_linear_fn(start=5e-4, end=3e-4, end_fraction=0.5),
    clip_range=0.2, #get_linear_fn(start=0.3, end=0.1, end_fraction=1.0),
    clip_range_vf=None  # TODO test values for this
)
AGENT_NET_ARCH = {'vf': [256, 128], 'pi': [64, 32]}
# AGENT_NET_ARCH = {'vf': [256], 'pi': [256]}
AGENT_ACT_FUN = nn.Tanh
# AGENT_POLICY = CustomActorCriticPolicy # modified MultiInputPolicy with intermediate normalization layers
AGENT_POLICY = 'MultiInputPolicy'
AGENT_POLICY_KWARGS = dict(
    ortho_init=False
)
FEATURE_EXTRACTOR_KWARGS = dict(
    embedding_dim=DEFAULT_EMBEDDINGS_DIM + 1, # Add one since we add boolean flags for each lanelet to indicate existence
    gnn_hidden_dim=256,
    gnn_layers=1,
    gnn_out_dim=256,
    concat_ego_features=True,
    self_loops=False,
    aggr='max',
    activation_fn=AGENT_ACT_FUN,
    normalization=False,
    alpha_hidden_channels = 256,
    alpha_num_layers = 2
)
OPTIMIZER = torch.optim.Adam
OPTIMIZER_KWARGS = dict(
    #weight_decay=5e-5,
    #momentum=0.0,
    #alpha=0.99
)

# Control settings
EGO_VEHICLE_SIMULATION_OPTIONS = EgoVehicleSimulationOptions(
    vehicle_model=VehicleModel.KS,
    vehicle_type=VehicleType.BMW_320i
)
PID_CONTROL_SPACE_OPTIONS = PIDControlOptions(
    lower_bound_velocity=0.0,
    upper_bound_steering=0.3,
    use_lanelet_coordinate_frame=True
)
STEERING_ACCELERATION_CONTROL_SPACE_OPTIONS = SteeringAccelerationControlOptions()
PID_LANE_CHANGE_CONTROL_SPACE = PIDLaneChangeControlOptions(
    lower_bound_velocity=30.0,
    #upper_bound_steering=0.3,
    use_lanelet_coordinate_frame=True,
    lower_bound_acceleration=0.0,
    finish_action_threshold=0.2,
)

#LONGITUDINAL_CONTROL_OPTIONS = LongitudinalControlOptions(upper_bound=1.5, lower_bound=1.0)
LONGITUDINAL_CONTROL_OPTIONS = LongitudinalControlOptions(
    upper_bound=10.0,
    #max_velocity=15.0,
    min_velocity=0.0
)

IN_BETWEEN_TRAFFIC_RESPAWNER_OPTIONS = InBetweenTrafficRespawnerOptions(
    init_speed=30,
    max_attempts_outer=100,
    max_respawn_attempts=10,
    start_arclength_offset=20.0,
    min_threshold_diff=45.0
)

# Reinforcement learning problem configuration
REWARDER = SumRewardAggregator([
    # AccelerationPenaltyRewardComputer(weight=0.01, loss_type=LossFunction.L2),
    CollisionPenaltyRewardComputer(penalty=-2.3),
    #FrictionViolationPenaltyRewardComputer(penalty=-0.01),
    #TrajectoryProgressionRewardComputer(weight=0.0025),
    #HeadingErrorPenaltyRewardComputer(weight=0.003, loss_type=LossFunction.L2),
    #LaneChangeRewardComputer(weight=2.0, dense=False),
    #LateralErrorPenaltyRewardComputer(weight=0.0001, loss_type=LossFunction.L1),
    ConstantRewardComputer(reward=0.001),
    #OffroadPenaltyRewardComputer(penalty=-1.0),
    #ReachedGoalRewardComputer(reward=1),
    IncentivizeLaneChangeRewardComputer(weight=0.005),
    #SteeringAnglePenaltyRewardComputer(weight=0.0005, loss_type=LossFunction.L1),
    StillStandingPenaltyRewardComputer(penalty=-0.09, velocity_threshold=32.0),
    #TimeToCollisionPenaltyRewardComputer(weight=0.5),
    #YawratePenaltyRewardComputer(weight=0.01)
    #VelocityPenaltyRewardComputer(reference_velocity=40.0, weight=0.08, loss_type=LossFunction.L1),
])

TERMINATION_CRITERIA = [
    OffroadCriterion(),
    # OffrouteCriterion(),
    CollisionCriterion(),
    #ReachedGoalCriterion(),
    # FrictionViolationCriterion()
]

# Data extraction
V_FEATURE_COMPUTERS = [
    ft_velocity,
    AccelerationFeatureComputer(),
    ft_orientation,
    ft_orientation_vec,
    ft_vehicle_shape,
    VehicleLaneletPoseFeatureComputer(update_exact_interval=10),
    VehicleVerticesFeatureComputer(),
    # GoalAlignmentComputer(
    #     include_goal_distance_longitudinal=False,
    #     include_goal_distance_lateral=False,
    #     include_goal_distance=True,
    #     include_lane_changes_required=True,
    #     logarithmic=False
    # ),
    YawRateFeatureComputer(),
    # VehicleLaneletPoseFeatureComputer(
    #     include_longitudinal_abs=True,
    #     include_longitudinal_rel=True,
    #     include_lateral_left=False,
    #     include_lateral_right=False,
    #     include_lateral_error=True,
    #     include_heading_error=True,
    #     update_exact_interval=10
    # ),
    VehicleLaneletConnectivityComputer(),
    EgoFramePoseFeatureComputer(),
    NumLaneletAssignmentsFeatureComputer(),
    VehicleVerticesFeatureComputer()
]
L_FEATURE_COMPUTERS = [
    LaneletVerticesFeatureComputer(),
    LaneletGeometryFeatureComputer()
]
L2L_FEATURE_COMPUTERS = [
    LaneletConnectionGeometryFeatureComputer()
]
V2V_FEATURE_COMPUTERS = [
    ClosenessFeatureComputer(),
    TimeToCollisionFeatureComputer(),
    ft_rel_state,
]
V2L_FEATURE_COMPUTERS = [
    VehicleLaneletPoseEdgeFeatureComputer()
]
