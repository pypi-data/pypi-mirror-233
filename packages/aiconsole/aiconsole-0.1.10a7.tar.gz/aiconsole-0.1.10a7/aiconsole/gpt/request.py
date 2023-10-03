import decimal
import json
from typing import Dict, List, Literal, Optional, Union

import tiktoken

from aiconsole.gpt.consts import MODEL_DATA, GPTMode, GPTModel, GPTModeLiteral
from aiconsole.gpt.gpt_types import EnforcedFunctionCall, GPTMessage
from aiconsole.gpt.token_error import TokenError

EXTRA_BUFFER_FOR_ENCODING_OVERHEAD = 50


class GPTRequest:
    def __init__(
        self,
        messages: List[GPTMessage],
        mode: GPTModeLiteral,
        functions: List[property] = None,
        function_call: Union[
            Literal["none"], Literal["auto"], EnforcedFunctionCall, None
        ] = None,
        temperature: float = 1,
        max_tokens: int = 0,
    ):
        self.messages = messages
        self.functions = functions or []
        self.function_call = function_call or ""
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.model = self.get_model(mode)
        self.model_data = MODEL_DATA[self.model]

    def get_messages_dump(self):
        return [message.model_dump() for message in self.messages]

    def add_prompt_context(self, system_content):
        self.messages = [
            GPTMessage(
                role="system",
                content=system_content
            ),
            *self.messages,
        ]

    def calculate_costs(
        self, message_content: str, message_function_call: Optional[Dict]
    ) -> tuple[decimal.Decimal, int, int]:

        input_tokens = self.count_tokens()
        output_tokens = self.count_tokens_output(message_content, message_function_call)

        input_cost = (
            input_tokens * decimal.Decimal(0.001)
        ) * self.model_data.input_cost_per_1K
        output_cost = (
            output_tokens * decimal.Decimal(0.001)
        ) * self.model_data.output_cost_per_1K

        total_cost = input_cost + output_cost

        return total_cost, input_tokens, output_tokens

    def count_tokens(self):
        encoding = tiktoken.encoding_for_model(self.model_data.encoding)

        if self.functions:
            functions_tokens = len(
                encoding.encode(",".join(json.dumps(f) for f in self.functions))
            )
        else:
            functions_tokens = 0
        return self.count_messages_tokens(encoding) + functions_tokens

    def count_tokens_for_model(self, model):
        encoding = tiktoken.encoding_for_model(MODEL_DATA[model].encoding)
        return self.count_messages_tokens(encoding)

    def count_messages_tokens(self, encoding):
        messages_str = json.dumps(self.get_messages_dump())
        messages_tokens = len(encoding.encode(messages_str))

        return messages_tokens

    def count_tokens_output(
        self, message_content: str, message_function_call: Optional[Dict]
    ):
        encoding = tiktoken.encoding_for_model(self.model_data.encoding)

        return len(encoding.encode(message_content)) + (
            len(encoding.encode(json.dumps(message_function_call)))
            if message_function_call
            else 0
        )

    def update_max_token(self, min_tokens: int, preferred_tokens: int):
        """
        Checks if the given prompt can fit within a specified range of token lengths for the specified AI model.
        Returns the number of tokens that can be used.
        """
        used_tokens = self.count_tokens() + EXTRA_BUFFER_FOR_ENCODING_OVERHEAD
        available_tokens = self.model_data.max_tokens - used_tokens

        if available_tokens < min_tokens:
            print(
                "Not enough tokens to perform the modification. Used tokens: ",
                used_tokens,
                "  available tokens: ",
                available_tokens,
                "requested tokens: ",
                self.max_tokens,
            )
            raise TokenError(
                "Combination of file size, selection, and your command is too big for us to handle."
            )

        self.max_tokens = min(available_tokens, preferred_tokens)

    def validate_request(self):
        """
        Checks if the prompt can be handled by the model
        """

        used_tokens = self.count_tokens()
        model_max_tokens = self.model_data.max_tokens

        if used_tokens - model_max_tokens >= self.max_tokens:
            print(
                f"Not enough tokens to perform the modification. Used tokens: {used_tokens},"
                f" available tokens: {model_max_tokens},"
                f" requested tokens: {self.max_tokens}"
            )
            raise TokenError(
                "Combination of file size, selection, and your command is too big for us to handle."
            )

    def get_model(self, mode: GPTModeLiteral) -> str:
        model = GPTModel.GPT_4_0613
        if mode == GPTMode.FAST:
            model = GPTModel.GPT_35_TURBO_16k_0613
            used_tokens = self.count_tokens_for_model(model) + self.max_tokens

            if used_tokens < MODEL_DATA[GPTModel.GPT_35_TURBO_0613].max_tokens:
                model = GPTModel.GPT_35_TURBO_0613

        return model
