import logging
from copy import deepcopy
from typing import List, Optional

import torch

from commonroad_geometric.dataset.commonroad_data import CommonRoadData
from commonroad_geometric.dataset.postprocessing.base_data_postprocessor import BaseDataPostprocessor
from commonroad_geometric.dataset.transformation.implementations.feature_normalization.feature_normalization_transformation import FeatureNormalizationTransformation
from commonroad_geometric.simulation.base_simulation import BaseSimulation
from commonroad_geometric.simulation.ego_simulation.ego_vehicle import EgoVehicle
from projects.geometric_models.drivable_area.models.scenario_models import ScenarioDrivableAreaModel

logger = logging.getLogger(__name__)


class EncodingPostProcessor(BaseDataPostprocessor):
    """
    Wrapper for obtaining encodings from pretrained drivable area
    representation model.
    """

    def __init__(
        self,
        model_filepath: str,
        reload_freq: Optional[int] = None,
        enable_decoding: bool = False
    ) -> None:

        self._model_filepath = model_filepath
        self._model = self._load_model()
        self._reload_freq = reload_freq
        self._enable_decoding = enable_decoding
        self._call_count = 0

    def _load_model(self) -> ScenarioDrivableAreaModel:
        model = ScenarioDrivableAreaModel.load(
            self._model_filepath,
            device='cpu',
            retries=0,
            from_torch=False
        )
        model.eval()
        return model

    def __call__(
        self,
        samples: List[CommonRoadData],
        simulation: Optional[BaseSimulation] = None,
        ego_vehicle: Optional[EgoVehicle] = None
    ) -> List[CommonRoadData]:
        assert simulation is not None

        self._call_count += 1
        if self._reload_freq is not None and self._call_count % self._reload_freq == 0:
            self._model = self._load_model()

        for data in samples:
            encoding = self._model.encoder.forward(data)
            data.vehicle.encoding = encoding
            if self._enable_decoding:
                prediction = self._model.decoder.forward(data=data, x=encoding)
                data.vehicle.prediction = prediction
        return samples
