# Copyright 2023 Komplete AI Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Optional, Tuple

from .. import enums
from ..core.config import HuggingFaceConfig
from ..datasets.base import BaseDataset
from ..types import RawSample
from ..utils.logger import dist_logger


class GeneralDataset(BaseDataset):
    @classmethod
    def download(cls, config: HuggingFaceConfig) -> Optional[Tuple[List[RawSample], Optional[List[RawSample]]]]:
        dist_logger.warning(
            "This is a special type of dataset in which it is not supposed to download anything. "
            "You must pass the data here through __init__, "
            "or through the path in config.train_local_path_to_data and config.eval_local_path_to_data (optional)"
        )
        return None

    def get_sample(self, index: int) -> RawSample:
        text = self.data[index][enums.General.default_sample_field]

        assert isinstance(text, str)

        sample: RawSample = {enums.General.text_parts: [text]}

        return sample
