from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Protocol

from rule_carryover.rendering import Message

type DecodingValue = str | int | float | bool | None


class TransportError(RuntimeError):
    """A provider transport failure, distinct from a model response."""


@dataclass(frozen=True)
class ProviderCompletion:
    raw_response: str
    provider_request_id: str | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    provider_prompt: str | None = None
    provider_prompt_hash: str | None = None


class Provider(Protocol):
    def complete(
        self,
        *,
        system_block: str,
        messages: Sequence[Message],
        model_id: str,
        decoding: Mapping[str, DecodingValue],
    ) -> ProviderCompletion: ...


class ScriptedProvider:
    """Deterministic provider used to exercise success and failure paths."""

    def __init__(self, responses: Sequence[str | TransportError]) -> None:
        self._responses = list(responses)
        self._index = 0

    def complete(
        self,
        *,
        system_block: str,
        messages: Sequence[Message],
        model_id: str,
        decoding: Mapping[str, DecodingValue],
    ) -> ProviderCompletion:
        del system_block, messages, model_id, decoding
        if self._index >= len(self._responses):
            raise TransportError("scripted provider has no remaining response")
        response = self._responses[self._index]
        self._index += 1
        if isinstance(response, TransportError):
            raise response
        return ProviderCompletion(
            raw_response=response,
            provider_request_id=f"scripted-{self._index:04d}",
        )
