
#!/usr/bin/env python
# coding=utf-8
# Copyright 2021 The HuggingFace Inc. team. All rights reserved.
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
"""
This script is used to train BPE tokenizers for machine translation.

Usage example:
    python cli/create_tokenizer.py \
        --dataset_name=stas/wmt14-en-de-pre-processed \
        --vocab_size=16_384 \
        --save_dir=output_dir
"""
import os
import argparse
import logging
from packaging import version

import datasets
from datasets import load_dataset

import transformers
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace

from transformers import RobertaTokenizer

# Setup logging
logger = logging.getLogger(__file__)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)

datasets.utils.logging.set_verbosity_warning()
transformers.utils.logging.set_verbosity_info()


def parse_args():
    parser = argparse.ArgumentParser(description="Train a tokenizer")

    parser.add_argument(
        "--dataset_name",
        type=str,
        default="spider",
        help="The name of the dataset to use (via the datasets library).",
    )
    parser.add_argument(
        "--dataset_config_name",
        type=str,
        default="spider",
        help=("Many datasets in Huggingface Dataset repository have multiple versions or configs. "
              "For the case of machine translation these usually indicate the language pair like "
              "en-es or zh-fr or similar. To look up possible configs of a dataset, "
              "find it on huggingface.co/datasets."),
    )
    parser.add_argument("--source_lang", type=str, default="en", help="Source language")
    parser.add_argument("--target_lang", type=str, default="es", help="Target language")
    parser.add_argument("--vocab_size", type=int, required=True, help="Size of the vocabulary")
    parser.add_argument("--save_dir", type=str, required=True, help="Directory which will be used to save tokenizer.")

    args = parser.parse_args()

    return args


def main():
    args = parse_args()
    logger.info(f"Starting tokenizer training with args {args}")

    # See more about loading any type of standard or custom dataset (from files, python dict, pandas DataFrame, etc) at
    # https://huggingface.co/docs/datasets/loading_datasets.html.
    logger.info(f"Loading dataset")
    # path = "/".join(os.path.realpath(__file__).split("/")[:-1])
    # print(path)
    # datasets.config.DOWNLOADED_DATASETS_PATH = Path(path)
    raw_datasets = load_dataset("spider")

    if "validation" not in raw_datasets:
        # will create "train" and "test" subsets
        # fix seed to make sure that the split is reproducible
        # note that we should use the same seed here and in train.py
        raw_datasets = raw_datasets.train_test_split(test_size=20, seed=42)

    logger.info(f"Loading pre-trained tokenizer")

    # Optional Task: If you are using a dataset different from stas/wmt14-en-de-pre-processed
    # depending on the dataset format, you might need to modify the iterator (line 109)
    # YOUR CODE STARTS HERE
    source_tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
    source_tokenizer_trainer = BpeTrainer(special_tokens=["[UNK]", "[PAD]", "[BOS]", "[EOS]"], vocab_size=args.vocab_size)
    source_tokenizer.pre_tokenizer = Whitespace()

    source_iterator = (item["question"] for item in raw_datasets["train"])
    source_tokenizer.train_from_iterator(
        source_iterator,
        trainer=source_tokenizer_trainer,
    )

    source_tokenizer = transformers.PreTrainedTokenizerFast(
        tokenizer_object=source_tokenizer,
        bos_token="[BOS]",
        eos_token="[EOS]",
        pad_token="[PAD]",
    )
    logger.info(f"Saving source to {args.save_dir}/english_tokenizer")
    source_tokenizer.save_pretrained(os.path.join(args.save_dir, "english_tokenizer"))
    # YOUR CODE ENDS HERE

    logger.info(f"Building tokenizer for the target SQL queries (might take a couple of minutes)")

    # Task 3.1: by analogy to the source tokenizer above, make a tokenizer for the target language
    # 1. Build a target tokenizer,
    # 2. Train it on args.target_lang
    # 3. Convert to transformers.PreTrainedTokenizerFast and save to save_dir/target_tokenizer.
    #
    # BOS is beginning-of-sequence special token.
    # EOS is end-of-sequence special token.
    # PAD is a padding token.
    #
    # Above every code line leave a short comment explaining what it does.
    # YOUR CODE STARTS HERE (our implementation is 8 lines of code)
    target_tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-base')  # Loading pre-trained tokenizer
    logger.info(f"Saving target to {args.save_dir}/sql_tokenizer")
    target_tokenizer.save_pretrained(os.path.join(args.save_dir, f"sql_tokenizer"))

    # YOUR CODE ENDS HERE


if __name__ == "__main__" :
    if version.parse(datasets.__version__) < version.parse("1.18.0"):
        raise RuntimeError("This script requires Datasets 1.18.0 or higher. Please update via pip install -U datasets.")
    main()
