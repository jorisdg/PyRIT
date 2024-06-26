# %% [markdown]
# The `pyrit.memory` module provides functionality to keep track of the conversation history. In a nutshell, this can be used as follows

# %% [markdown]
# The PyRIT DuckDB database comprises of tables defined in the `pyrit.memory.memory_models` module.
#
#
# %%
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from uuid import uuid4
from pyrit.memory import DuckDBMemory
from pyrit.models import PromptRequestPiece

conversation_id = str(uuid4())

memory = DuckDBMemory()
message_list = [
    PromptRequestPiece(
        role="user", original_prompt_text="Hi, chat bot! This is my initial prompt.", conversation_id=conversation_id
    ),
    PromptRequestPiece(
        role="assistant", original_prompt_text="Nice to meet you! This is my response.", conversation_id=conversation_id
    ),
    PromptRequestPiece(
        role="user",
        original_prompt_text="Wonderful! This is my second prompt to the chat bot!",
        conversation_id=conversation_id,
    ),
]

memory.add_request_pieces_to_memory(request_pieces=message_list)


entries = memory.get_chat_messages_with_conversation_id(conversation_id=conversation_id)

for entry in entries:
    print(entry)


# %%

# update based on conversation_id
update_fileds = {"converted_prompt_text": "this is updated field"}
memory.update_entries_by_conversation_id(conversation_id=conversation_id, update_fields=update_fileds)


prompt_entries = memory.get_prompt_entries_with_conversation_id(conversation_id=conversation_id)

for entry in prompt_entries:
    print(entry)

# %%
# Cleanup memory resources
memory.dispose_engine()

# %%
