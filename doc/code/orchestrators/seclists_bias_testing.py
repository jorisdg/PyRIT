# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: pyrit-dev
#     language: python
#     name: python3
# ---

# %% [markdown]
# # SecLists Bias Testing - optional
#
# This notebook demonstrates the process of using SecLists AI LLM Bias Testing examples to evaluate the bias of an AI language model.
# It includes fetching bias testing prompts from the SecLists repository, sending them to the model, and scoring the model's responses based on predefined fairness and bias scales.
# The goal is to assess how well the AI model handles various biases in its responses.


# %%
# Import necessary packages
from pyrit.common import IN_MEMORY, initialize_pyrit
from pyrit.datasets import fetch_seclists_bias_testing_examples
from pyrit.orchestrator import PromptSendingOrchestrator
from pyrit.prompt_target import OpenAIChatTarget
from pyrit.score import LikertScalePaths, SelfAskLikertScorer

initialize_pyrit(memory_db_type=IN_MEMORY)

prompt_target = OpenAIChatTarget()
examples_source = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Ai/LLM_Testing/Bias_Testing/nationality_geographic_bias.txt"

# Set up the Bias Scorer with the same prompt target to ensure consistency
bias_scorer = SelfAskLikertScorer(
    likert_scale_path=LikertScalePaths.FAIRNESS_BIAS_SCALE.value, chat_target=prompt_target
)


# Fetch examples from SecLists Bias Testing dataset
prompt_dataset = fetch_seclists_bias_testing_examples(examples_source, source_type="public_url")

# Use the first 5 examples
prompt_list = [prompt.value for prompt in prompt_dataset.prompts[:4]]

orchestrator = PromptSendingOrchestrator(objective_target=prompt_target, scorers=[bias_scorer])

responses = await orchestrator.send_prompts_async(prompt_list=prompt_list)  # type: ignore
await orchestrator.print_conversations_async()  # type: ignore


# %%
from pyrit.memory import CentralMemory

memory = CentralMemory.get_memory_instance()
memory.dispose_engine()
