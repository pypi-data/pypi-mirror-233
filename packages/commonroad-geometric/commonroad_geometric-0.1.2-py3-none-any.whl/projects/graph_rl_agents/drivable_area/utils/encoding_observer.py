from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import IntEnum, unique
from typing import Optional

import gymnasium
import numpy as np

from commonroad_geometric.common.geometry.helpers import relative_orientation
from commonroad_geometric.common.math import scale_feature
from commonroad_geometric.dataset.commonroad_data import CommonRoadData
from commonroad_geometric.dataset.extraction.traffic.feature_computers.implementations.types import V_Feature
from commonroad_geometric.dataset.extraction.traffic.feature_computers.implementations.vehicle.ego.goal_alignment_feature_computer import GoalAlignmentComputer
from commonroad_geometric.dataset.extraction.traffic.feature_computers.types import VFeatureParams
from commonroad_geometric.learning.reinforcement.observer.base_observer import BaseObserver, T_Observation
from commonroad_geometric.simulation.ego_simulation.ego_vehicle_simulation import EgoVehicleSimulation

logger = logging.getLogger(__name__)


@dataclass
class FeatureScaleOptions:
    fmin: Optional[float]
    fmax: Optional[float]


@unique
class Features(IntEnum):
    GOAL_DISTANCE = 0
    VELOCITY = 1
    ACCELERATION = 2
    STEERING_ANGLE = 3
    STEERING_ANGLE_ABS = 4
    HEADING_ERROR = 5
    HEADING_ERROR_ABS = 6
    LATERAL_ERROR = 7
    LATERAL_ERROR_ABS = 8


class EncodingObserver(BaseObserver):
    FEATURE_SCALING_OPTIONS = {
        Features.GOAL_DISTANCE: FeatureScaleOptions(0.0, 100.0),
        Features.VELOCITY: FeatureScaleOptions(0.0, 22.0),
        Features.ACCELERATION: FeatureScaleOptions(0.0, 20.0),
        Features.STEERING_ANGLE: FeatureScaleOptions(-0.4, 0.4),
        Features.STEERING_ANGLE_ABS: FeatureScaleOptions(0.0, 0.4),
        Features.HEADING_ERROR: FeatureScaleOptions(-np.pi / 4, np.pi / 4),
        Features.HEADING_ERROR_ABS: FeatureScaleOptions(0.0, np.pi / 4),
        Features.LATERAL_ERROR: FeatureScaleOptions(-2.5, 2.5),
        Features.LATERAL_ERROR_ABS: FeatureScaleOptions(0.0, 2.5),
    }

    N_FIXED_EGO_FEATURES = len(FEATURE_SCALING_OPTIONS)

    def __init__(
        self,
    ) -> None:
        self._n_encoding_features: int
        self._goal_alignment_computer = GoalAlignmentComputer(
            include_lane_changes_required=False
        )
        super().__init__()

    def setup(self, dummy_data: CommonRoadData) -> gymnasium.Space:
        self._n_encoding_features = dummy_data.vehicle.encoding.shape[-1]
        observation_space = gymnasium.spaces.Box(
            -np.inf,
            np.inf,
            (EncodingObserver.N_FIXED_EGO_FEATURES + self._n_encoding_features,),
            dtype=np.float32
        )
        return observation_space

    def observe(
        self,
        data: CommonRoadData,
        ego_vehicle_simulation: EgoVehicleSimulation
    ) -> T_Observation:
        opt = EncodingObserver.FEATURE_SCALING_OPTIONS
        F = Features

        try:
            z_ego = data.ego.encoding.squeeze(0).detach().numpy()
        except AttributeError:
            logger.warning("Encoding property 'encoding' missing on data. Setting zeros")
            z_ego = np.zeros((self._n_encoding_features,), dtype=np.float32)

        current_state = ego_vehicle_simulation.ego_vehicle.state
        velocity = current_state.velocity
        steering_angle = current_state.steering_angle
        steering_angle_abs = abs(steering_angle)
        velocity = current_state.velocity
        acceleration = current_state.acceleration

        lanelet_id = ego_vehicle_simulation.simulation.obstacle_id_to_lanelet_id[ego_vehicle_simulation.ego_vehicle.obstacle_id][0]
        path = ego_vehicle_simulation.simulation.get_lanelet_center_polyline(lanelet_id)
        arclength = path.get_projected_arclength(current_state.position)
        path_direction = path.get_direction(arclength)
        heading_error = relative_orientation(
            current_state.orientation,
            path_direction
        )
        heading_error_abs = abs(heading_error)
        lateral_error = path.get_lateral_distance(
            current_state.position
        )
        lateral_error_abs = abs(lateral_error)

        goal_alignment_dict = self._goal_alignment_computer(
            params=VFeatureParams(
                dt=ego_vehicle_simulation.dt,
                time_step=ego_vehicle_simulation.current_time_step,
                obstacle=ego_vehicle_simulation.ego_vehicle.as_dynamic_obstacle,
                state=current_state,
                is_ego_vehicle=True,
                ego_state=current_state,
                ego_route=ego_vehicle_simulation.ego_route
            ),
            simulation=ego_vehicle_simulation.simulation
        )
        goal_distance = goal_alignment_dict[V_Feature.GoalDistanceLongitudinal.value]

        goal_distance = scale_feature(opt[F.GOAL_DISTANCE].fmin, opt[F.GOAL_DISTANCE].fmax, goal_distance)
        velocity = scale_feature(opt[F.VELOCITY].fmin, opt[F.VELOCITY].fmax, velocity)
        acceleration = scale_feature(opt[F.ACCELERATION].fmin, opt[F.ACCELERATION].fmax, acceleration)
        steering_angle = scale_feature(opt[F.STEERING_ANGLE].fmin, opt[F.STEERING_ANGLE].fmax, steering_angle)
        steering_angle_abs = scale_feature(opt[F.STEERING_ANGLE_ABS].fmin, opt[F.STEERING_ANGLE_ABS].fmax, steering_angle_abs)
        heading_error = scale_feature(opt[F.HEADING_ERROR].fmin, opt[F.HEADING_ERROR].fmax, heading_error)
        heading_error_abs = scale_feature(opt[F.HEADING_ERROR_ABS].fmin, opt[F.HEADING_ERROR_ABS].fmax, heading_error_abs)
        lateral_error = scale_feature(opt[F.LATERAL_ERROR].fmin, opt[F.LATERAL_ERROR].fmax, lateral_error)
        lateral_error_abs = scale_feature(opt[F.LATERAL_ERROR_ABS].fmin, opt[F.LATERAL_ERROR_ABS].fmax, lateral_error_abs)

        x_scalars = np.array([
            goal_distance,
            velocity,
            acceleration,
            steering_angle,
            steering_angle_abs,
            heading_error,
            heading_error_abs,
            lateral_error,
            lateral_error_abs
        ])

        x = np.concatenate([
            x_scalars,
            z_ego
        ], axis=-1)

        return x
