import hashlib
from collections.abc import Mapping, Sequence

from rule_carryover.mlx_provider import MlxLmProvider
from rule_carryover.rendering import Boundary, Channel, Message, RenderedRequest


class FakeTokenizer:
    def __init__(self) -> None:
        self.last_messages: object = None
        self.last_kwargs: dict[str, object] = {}

    def apply_chat_template(
        self, messages: object, **kwargs: object
    ) -> str:
        self.last_messages = messages
        self.last_kwargs = kwargs
        return "rendered prompt"

    def encode(self, text: str) -> list[int]:
        return list(range(len(text.split())))


class AlternatingOnlyTokenizer(FakeTokenizer):
    def apply_chat_template(self, messages: object, **kwargs: object) -> str:
        assert isinstance(messages, list)
        if messages[0]["role"] == "system":
            raise ValueError(
                "Conversation roles must alternate user/assistant/user/assistant/..."
            )
        self.last_messages = messages
        self.last_kwargs = kwargs
        return "fallback prompt"


def test_mlx_provider_uses_single_request_non_thinking_greedy_path() -> None:
    tokenizer = FakeTokenizer()
    calls: list[dict[str, object]] = []

    def generate(
        model: object,
        tokenizer_arg: object,
        *,
        prompt: str,
        max_tokens: int,
        sampler: object,
        verbose: bool,
    ) -> str:
        calls.append(
            {
                "model": model,
                "tokenizer": tokenizer_arg,
                "prompt": prompt,
                "max_tokens": max_tokens,
                "sampler": sampler,
                "verbose": verbose,
            }
        )
        return '{"decision":"DENY","rule_id":"x","margin":-1}'

    provider = MlxLmProvider(
        model=object(),
        tokenizer=tokenizer,
        generate_function=generate,
        sampler="greedy",
    )
    messages: Sequence[Message] = (Message(role="user", content="case"),)
    decoding: Mapping[str, str | int | float | bool | None] = {
        "temperature": 0,
        "max_tokens": 64,
    }

    completion = provider.complete(
        system_block="rules",
        messages=messages,
        model_id="local/model@revision",
        decoding=decoding,
    )

    assert completion.raw_response.startswith("{")
    assert completion.provider_prompt == "rendered prompt"
    assert completion.prompt_tokens == 2
    assert completion.provider_prompt_hash == hashlib.sha256(b"rendered prompt").hexdigest()
    assert tokenizer.last_kwargs["enable_thinking"] is False
    assert tokenizer.last_kwargs["add_generation_prompt"] is True
    assert len(calls) == 1
    assert calls[0]["max_tokens"] == 64
    assert provider.token_count("one two three") == 3
    request = RenderedRequest(
        system_block="rules",
        target_block="case",
        messages=tuple(messages),
        channel=Channel.NEUTRAL,
        boundary=Boundary.FRESH,
    )
    assert provider.request_token_count(request) == 2


def test_mlx_provider_embeds_system_block_for_alternating_only_template() -> None:
    tokenizer = AlternatingOnlyTokenizer()

    def generate(
        model: object,
        tokenizer_arg: object,
        *,
        prompt: str,
        max_tokens: int,
        sampler: object,
        verbose: bool,
    ) -> str:
        del model, tokenizer_arg, max_tokens, sampler, verbose
        assert prompt == "fallback prompt"
        return '{"decision":"DENY","rule_id":"x","margin":-1}'

    provider = MlxLmProvider(
        model=object(),
        tokenizer=tokenizer,
        generate_function=generate,
        sampler="greedy",
    )

    completion = provider.complete(
        system_block="unchanged rules",
        messages=(Message(role="user", content="case"),),
        model_id="local/model@revision",
        decoding={"temperature": 0, "max_tokens": 64},
    )

    assert completion.provider_prompt == "fallback prompt"
    assert tokenizer.last_messages == [
        {"role": "user", "content": "unchanged rules\n\ncase"}
    ]
