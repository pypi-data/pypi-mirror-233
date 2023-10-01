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

# Thanks to Phil Schmid's post: https://www.philschmid.de/gptq-llama

import json
import os
from typing import Any, Dict, List, Tuple

import torch
from loguru import logger
from optimum.gptq import GPTQQuantizer
from tqdm import tqdm
from transformers import PreTrainedModel, PreTrainedTokenizer

from .. import enums
from ..core.config import HuggingFaceConfig
from ..core.dependencies import build_dataset, build_model, build_tokenizer
from ..datasets.registry import datasets_registry
from ..utils.post_training import push_to_hub_bos_add_bos_token


def gptq_quantize(
    config: HuggingFaceConfig,
) -> Tuple[PreTrainedTokenizer, PreTrainedModel]:
    if not torch.cuda.is_available():
        logger.warning("CUDA is not available")

    config.check_auto_gptq()

    tokenizer = build_tokenizer(config=config, use_fast=False)
    logger.info(f"Tokenizer {config.correct_tokenizer_name_or_path} was built")

    model, _ = build_model(
        config=config,
        quantization_config=None,
    )
    logger.info(f"Model {config.model_name_or_path} was built")

    dataset_id = None
    samples: List[str] = list()

    if config.quantization_dataset_id is not None:
        dataset_id = config.quantization_dataset_id
    else:
        if config.prepare_dataset:
            dataset_cls = datasets_registry.get(config.dataset_key)

            if dataset_cls is None:
                raise ValueError(f"Dataset with key {config.dataset_key} not found")

            dataset_cls.prepare(config=config)

        raw_dataset = build_dataset(config=config, is_train=True)

        if raw_dataset is None:
            raise ValueError("Quantization dataset can't be loaded")

        samples = list()

        for sample_index in tqdm(range(len(raw_dataset)), desc="Loading quantization dataset"):
            sample: Dict[str, Any] = raw_dataset[sample_index]
            text_parts = sample[enums.General.text_parts]
            text = "\n".join(text_parts)
            if isinstance(text, str):
                samples.append(text)

            if 0 < config.quantization_max_samples == len(samples):
                break

    quantizer = GPTQQuantizer(
        bits=config.gptq_bits,
        group_size=config.gptq_group_size,
        dataset=dataset_id or samples,
        model_seqlen=config.max_length,
    )
    logger.info("Quantizer loaded")

    logger.info("Start quantization")
    quantized_model = quantizer.quantize_model(model, tokenizer)
    logger.info("Quantization complete")

    logger.info(f"Saving quantized model to {config.quantized_model_path}")
    model.save_pretrained(
        save_directory=config.quantized_model_path,
        safe_serialization=config.save_safetensors,
    )

    tokenizer = build_tokenizer(config=config)

    tokenizer.save_pretrained(save_directory=config.quantized_model_path)

    with open(
        os.path.join(config.quantized_model_path, "quantize_config.json"),
        "w",
        encoding="utf-8",
    ) as f:
        quantizer.disable_exllama = False
        json.dump(quantizer.to_dict(), f, indent=2)

    with open(os.path.join(config.quantized_model_path, "config.json"), "r", encoding="utf-8") as f:
        model_config = json.load(f)
        model_config["quantization_config"]["disable_exllama"] = False

    with open(os.path.join(config.quantized_model_path, "config.json"), "w", encoding="utf-8") as f:
        json.dump(model_config, f, indent=2)

    if config.quantized_hub_model_id is not None:
        logger.info(f"Push quantized model to the hub {config.quantized_hub_model_id}")
        quantized_model.push_to_hub(
            repo_id=config.quantized_hub_model_id,
            private=config.quantized_hub_private_repo,
            safe_serialization=config.save_safetensors,
        )
        tokenizer.push_to_hub(
            repo_id=config.quantized_hub_model_id,
            private=config.quantized_hub_private_repo,
            safe_serialization=config.save_safetensors,
        )
        if config.push_to_hub_bos_add_bos_token:
            push_to_hub_bos_add_bos_token(repo_id=config.quantized_hub_model_id)
    else:
        logger.warning("hub_model_id is None. Model will stay locally")

    return tokenizer, model
