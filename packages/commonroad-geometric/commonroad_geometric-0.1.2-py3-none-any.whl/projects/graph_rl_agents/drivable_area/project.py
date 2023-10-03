from pathlib import Path

from commonroad.common.solution import VehicleType
from stable_baselines3 import PPO
from stable_baselines3.common.torch_layers import FlattenExtractor
from torch import nn
from torch.optim import Adam

from commonroad_geometric.common.io_extensions.scenario import LaneletAssignmentStrategy
from commonroad_geometric.dataset.extraction.traffic import TrafficExtractorOptions
from commonroad_geometric.dataset.extraction.traffic.edge_drawers.implementations import *
from commonroad_geometric.dataset.extraction.traffic.feature_computers.implementations.lanelet import *
from commonroad_geometric.dataset.extraction.traffic.feature_computers.implementations.lanelet_to_lanelet import *
from commonroad_geometric.dataset.extraction.traffic.feature_computers.implementations.vehicle import *
from commonroad_geometric.dataset.extraction.traffic.feature_computers.implementations.vehicle_to_lanelet import *
from commonroad_geometric.dataset.extraction.traffic.feature_computers.implementations.vehicle_to_vehicle import *
from commonroad_geometric.dataset.extraction.traffic.traffic_extractor import TrafficFeatureComputerOptions
from commonroad_geometric.dataset.postprocessing.implementations import *
from commonroad_geometric.dataset.preprocessing.implementations import *
from commonroad_geometric.dataset.transformation.implementations.feature_normalization.feature_normalization_transformation import FeatureNormalizationTransformation, FeatureUnnormalizationTransformation
from commonroad_geometric.learning.reinforcement import RLEnvironmentOptions
from commonroad_geometric.learning.reinforcement.experiment import RLExperiment, RLExperimentConfig
from commonroad_geometric.learning.reinforcement.observer.flattened_graph_observer import FlattenedGraphObserver
from commonroad_geometric.learning.reinforcement.project.base_rl_project import BaseRLProject
from commonroad_geometric.learning.reinforcement.rewarder.reward_aggregator.implementations import SumRewardAggregator
from commonroad_geometric.learning.reinforcement.rewarder.reward_computer.implementations import *
from commonroad_geometric.learning.reinforcement.rewarder.reward_computer.types import RewardLossMetric
from commonroad_geometric.learning.reinforcement.termination_criteria.implementations import *
from commonroad_geometric.learning.reinforcement.training.rl_trainer import RLModelConfig
from commonroad_geometric.rendering.traffic_scene_renderer import TrafficSceneRendererOptions
from commonroad_geometric.simulation.ego_simulation.control_space.implementations import *
from commonroad_geometric.simulation.ego_simulation.ego_vehicle import VehicleModel
from commonroad_geometric.rendering.plugins import *
from commonroad_geometric.simulation.ego_simulation.ego_vehicle_simulation import EgoVehicleSimulationOptions
from commonroad_geometric.simulation.ego_simulation.respawning.implementations import *
from commonroad_geometric.simulation.interfaces.static.scenario_simulation import ScenarioSimulation, ScenarioSimulationOptions
from projects.geometric_models.drivable_area.project import DrivableAreaFeatureComputers, create_edge_drawer, create_lanelet_graph_conversion_steps, create_scenario_filterers
from projects.graph_rl_agents.drivable_area.utils.encoding_observer import EncodingObserver
from projects.graph_rl_agents.drivable_area.utils.post_processors import EncodingPostProcessor
from projects.geometric_models.drivable_area.models.scenario_models import ScenarioDrivableAreaModel

SCENARIO_PREPROCESSORS = [
    #VehicleFilterPreprocessor(),
    #RemoveIslandsPreprocessor()
    SegmentLaneletsPreprocessor(20.0)
    #(DepopulateScenarioPreprocessor(1), 1),
]

# Control settings
EGO_VEHICLE_SIMULATION_OPTIONS = EgoVehicleSimulationOptions(
    vehicle_model=VehicleModel.KS,
    vehicle_type=VehicleType.BMW_320i
)

# Reinforcement learning problem configuration
REWARDER_COMPUTERS = [
    # AccelerationPenaltyRewardComputer(
    #     weight=0.0,
    #     loss_type=RewardLossMetric.L2
    # ),
    CollisionPenaltyRewardComputer(
        penalty=-0.1,
    ),
    #FrictionViolationPenaltyRewardComputer(penalty=-0.01),
    # TrajectoryProgressionRewardComputer(
    #     weight=0.06,
    #     delta_threshold=0.08
    # ),
    ConstantRewardComputer(reward=0.001),
    #
    ReachedGoalRewardComputer(reward=-0.1),
    #SteeringAnglePenaltyRewardComputer(weight=0.0005, loss_type=RewardLossMetric.L1),
    StillStandingPenaltyRewardComputer(penalty=-0.002, velocity_threshold=2.0),
    LateralErrorPenaltyRewardComputer(weight=0.0001, loss_type=RewardLossMetric.L1),
    #TimeToCollisionPenaltyRewardComputer(weight=0.1), # requires incoming edges
    #YawratePenaltyRewardComputer(weight=0.01),
    OffroadPenaltyRewardComputer(penalty=-0.1),
    # VelocityPenaltyRewardComputer(
    #     reference_velocity=17.0,
    #     weight=0.002,
    #     loss_type=RewardLossMetric.L1,
    #     only_upper=True
    # ),
    HeadingErrorPenaltyRewardComputer(
        weight=0.01,
        loss_type=RewardLossMetric.L2,
        wrong_direction_penalty=-0.01
    )
]

TERMINATION_CRITERIA = [
    OffroadCriterion(),
    #OffrouteCriterion(),
    CollisionCriterion(),
    ReachedGoalCriterion(),
    TrafficJamCriterion(),
    # FrictionViolationCriterion()
]

class DrivableAreaRLProject(BaseRLProject):
    def configure_experiment(self, cfg: dict) -> RLExperimentConfig:
        occ_model_path = Path(cfg["encoding_model_path"]).resolve()
        enable_representations: bool = cfg["enable_representations"]

        observer = EncodingObserver()
        
        postprocessors = []
        if cfg["enable_feature_normalization"]:
            feature_normalizer_transformation = FeatureNormalizationTransformation(
                params_file_path=cfg["feature_normalization_params_path"]
            )
            postprocessors.append(feature_normalizer_transformation.to_post_processor())
        encoder_post_processor = EncodingPostProcessor(
            model_filepath=cfg["encoding_model_path"],
            reload_freq=10000,
            enable_decoding=cfg["render_decoding"]
        )
        postprocessors.append(encoder_post_processor)
        if cfg["enable_feature_normalization"]:
            feature_unnormalizer_transformation = FeatureUnnormalizationTransformation(
                params_file_path=cfg["feature_normalization_params_path"]
            )
            postprocessors.append(feature_unnormalizer_transformation.to_post_processor())

        lanelet_graph_conversion_steps = create_lanelet_graph_conversion_steps(
            enable_waypoint_resampling=cfg["enable_waypoint_resampling"],
            waypoint_density=cfg["lanelet_waypoint_density"]
        )
        
        renderer_plugins = ScenarioDrivableAreaModel.configure_renderer_plugins()
        renderer_plugins.insert(-2, RenderEgoVehiclePlugin())
        renderer_plugins.insert(-2, RenderPlanningProblemSetPlugin())
        
        experiment_config = RLExperimentConfig(
            simulation_cls=ScenarioSimulation,
            simulation_options=ScenarioSimulationOptions(
                lanelet_assignment_order=LaneletAssignmentStrategy.ONLY_SHAPE,
                lanelet_graph_conversion_steps=lanelet_graph_conversion_steps
            ),
            control_space_cls=SteeringAccelerationSpace,
            control_space_options=SteeringAccelerationControlOptions(
            ),
            respawner_cls=RandomRouteRespawner,
            respawner_options=RandomRouteRespawnerOptions(
                
            ),
            traffic_extraction_options=TrafficExtractorOptions(
                edge_drawer=create_edge_drawer(cfg["edge_range"]),
                feature_computers=TrafficFeatureComputerOptions(
                    v=DrivableAreaFeatureComputers.v(),
                    v2v=DrivableAreaFeatureComputers.v2v(),
                    l=DrivableAreaFeatureComputers.l(),
                    l2l=DrivableAreaFeatureComputers.l2l(),
                    v2l=DrivableAreaFeatureComputers.v2l(),
                    l2v=DrivableAreaFeatureComputers.l2v()
                ),
                postprocessors=postprocessors,
                only_ego_inc_edges=cfg["only_ego_inc_edges"], 
                assign_multiple_lanelets=True,
                ego_map_radius=cfg["ego_map_radius"],
                include_lanelet_vertices=True
            ),
            ego_vehicle_simulation_options=EGO_VEHICLE_SIMULATION_OPTIONS,
            rewarder=SumRewardAggregator(REWARDER_COMPUTERS),
            termination_criteria=TERMINATION_CRITERIA,
            env_options=RLEnvironmentOptions(
                async_resets=True,
                num_respawns_per_scenario=0,
                loop_scenarios=True,
                scenario_preprocessors=SCENARIO_PREPROCESSORS,
                scenario_prefilters=create_scenario_filterers(),
                render_on_step=cfg["render_on_step"],
                render_debug_overlays=cfg["render_debug_overlays"],
                renderer_options=TrafficSceneRendererOptions(
                    plugins=renderer_plugins,
                    camera_follow=True,
                    camera_auto_rotation=False
                ),
                raise_exceptions=False,
                observer=observer
            )
        )
        return experiment_config

    def configure_model(self, cfg: dict, experiment: RLExperiment) -> RLModelConfig:
        enable_representations: bool = cfg["enable_representations"]

        feature_extractor_cls = FlattenExtractor
        feature_extractor_kwargs = {}
        return RLModelConfig(
            agent_cls=PPO,
            agent_kwargs=dict(
                gae_lambda=cfg["gae_lambda"],
                gamma=cfg["gamma"],
                n_epochs=cfg["n_epochs"],
                ent_coef=cfg["ent_coef"],
                n_steps=cfg["n_steps"],
                batch_size=cfg["batch_size"],
                vf_coef=cfg["vf_coef"],
                max_grad_norm=cfg["max_grad_norm"],
                learning_rate=cfg["learning_rate"],
                clip_range=cfg["clip_range"],
                clip_range_vf=None,
                policy='MultiInputPolicy',
                policy_kwargs=dict(
                    ortho_init=False,
                    log_std_init=-1,
                    net_arch={'vf': [256, 128, 64], 'pi': [256, 128, 64]},
                    activation_fn=nn.Tanh,
                    features_extractor_class=feature_extractor_cls,
                    features_extractor_kwargs=feature_extractor_kwargs,
                    optimizer_class=Adam,
                    optimizer_kwargs=dict(
                        eps=1e-5
                    )
                ),
            ),            
        )
