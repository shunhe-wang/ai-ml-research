from __future__ import annotations

import hashlib
from collections.abc import Mapping, Sequence
from typing import Protocol, cast

from rule_carryover.providers import DecodingValue, ProviderCompletion
from rule_carryover.rendering import Message, RenderedRequest


class _Tokenizer(Protocol):
    def apply_chat_template(self, messages: object, **kwargs: object) -> str: ...

    def encode(self, text: str) -> Sequence[int]: ...


class _GenerateFunction(Protocol):
    def __call__(
        self,
        model: object,
        tokenizer: object,
        *,
        prompt: str,
        max_tokens: int,
        sampler: object,
        verbose: bool,
    ) -> str: ...


class MlxLmProvider:
    """Single-request MLX-LM adapter for an already pinned local snapshot."""

    def __init__(
        self,
        *,
        model: object,
        tokenizer: _Tokenizer,
        generate_function: _GenerateFunction,
        sampler: object,
    ) -> None:
        self._model = model
        self._tokenizer = tokenizer
        self._generate = generate_function
        self._sampler = sampler

    def token_count(self, text: str) -> int:
        return len(self._tokenizer.encode(text))

    def _render_prompt(self, system_block: str, messages: Sequence[Message]) -> str:
        chat_messages = [{"role": "system", "content": system_block}]
        chat_messages.extend(
            {"role": message.role, "content": message.content} for message in messages
        )
        template_kwargs = {
            "tokenize": False,
            "add_generation_prompt": True,
            "enable_thinking": False,
        }
        try:
            return self._tokenizer.apply_chat_template(chat_messages, **template_kwargs)
        except Exception as error:
            if "Conversation roles must alternate" not in str(error):
                raise
            if not messages or messages[0].role != "user":
                raise ValueError(
                    "alternating-only chat template requires an initial user message"
                ) from error
            fallback_messages = [
                {
                    "role": "user",
                    "content": f"{system_block}\n\n{messages[0].content}",
                }
            ]
            fallback_messages.extend(
                {"role": message.role, "content": message.content}
                for message in messages[1:]
            )
            return self._tokenizer.apply_chat_template(
                fallback_messages, **template_kwargs
            )

    def request_token_count(self, request: RenderedRequest) -> int:
        return self.token_count(self._render_prompt(request.system_block, request.messages))

    @classmethod
    def from_path(cls, model_path: str) -> MlxLmProvider:
        try:
            from mlx_lm import generate, load  # type: ignore[import-not-found]
            from mlx_lm.sample_utils import make_sampler  # type: ignore[import-not-found]
        except ImportError as error:
            raise RuntimeError(
                "install the pinned 'mlx' extra in a native arm64 environment"
            ) from error
        model, tokenizer = load(model_path)
        return cls(
            model=model,
            tokenizer=cast(_Tokenizer, tokenizer),
            generate_function=cast(_GenerateFunction, generate),
            sampler=make_sampler(temp=0.0),
        )

    def complete(
        self,
        *,
        system_block: str,
        messages: Sequence[Message],
        model_id: str,
        decoding: Mapping[str, DecodingValue],
    ) -> ProviderCompletion:
        del model_id
        temperature = decoding.get("temperature", 0)
        if isinstance(temperature, bool) or temperature != 0:
            raise ValueError("the local smoke provider is restricted to greedy decoding")
        max_tokens_raw = decoding.get("max_tokens", 128)
        if isinstance(max_tokens_raw, bool) or not isinstance(max_tokens_raw, int):
            raise ValueError("max_tokens must be an integer")

        prompt = self._render_prompt(system_block, messages)
        raw = self._generate(
            self._model,
            self._tokenizer,
            prompt=prompt,
            max_tokens=max_tokens_raw,
            sampler=self._sampler,
            verbose=False,
        )
        return ProviderCompletion(
            raw_response=raw,
            prompt_tokens=self.token_count(prompt),
            completion_tokens=self.token_count(raw),
            provider_prompt=prompt,
            provider_prompt_hash=hashlib.sha256(prompt.encode()).hexdigest(),
        )
