# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import pytest

from pyrit.memory.memory_models import PromptDataType
from pyrit.prompt_normalizer import NormalizerRequestPiece
from pyrit.prompt_converter import PromptConverter


class MockPromptConverter(PromptConverter):

    def __init__(self) -> None:
        pass

    def convert(self, *, prompt: str, input_type: PromptDataType = "text") -> str:
        return prompt

    def is_supported(self, input_type: PromptDataType) -> bool:
        return input_type == "text"


def test_prompt_request_piece_init_valid_arguments():
    prompt_converters = [MockPromptConverter()]
    prompt_text = "Hello"
    metadata = "meta"

    prompt = NormalizerRequestPiece(
        prompt_converters=prompt_converters,
        prompt_text=prompt_text,
        prompt_data_type="text",
        metadata=metadata,
    )

    assert prompt.prompt_converters == prompt_converters
    assert prompt.prompt_text == prompt_text
    assert prompt.prompt_data_type == "text"
    assert prompt.metadata == metadata


def test_prompt_init_no_metadata():
    prompt_converters = [MockPromptConverter()]
    prompt_text = "Hello"

    prompt = NormalizerRequestPiece(
        prompt_converters=prompt_converters,
        prompt_text=prompt_text,
        prompt_data_type="text",
    )

    assert prompt.prompt_converters == prompt_converters
    assert prompt.prompt_text == prompt_text
    assert prompt.prompt_data_type == "text"
    assert not prompt.metadata


def test_prompt_request_piece_init_invalid_converter():
    prompt_text = "Hello"
    metadata = "meta"

    with pytest.raises(ValueError):
        NormalizerRequestPiece(
            prompt_converters=["InvalidPromptConverter"],
            prompt_text=prompt_text,
            prompt_data_type="text",
            metadata=metadata,
        )


def test_prompt_init_empty_prompt_converters():
    prompt_text = "Hello"
    metadata = "meta"

    with pytest.raises(ValueError):
        NormalizerRequestPiece(
            prompt_converters=[],
            prompt_text=prompt_text,
            prompt_data_type="text",
            metadata=metadata,
        )


def test_prompt_init_invalid_prompt_text():
    metadata = "meta"

    with pytest.raises(ValueError):
        NormalizerRequestPiece(
            prompt_converters=[],
            prompt_text=123,
            prompt_data_type="text",
            metadata=metadata,
        )
