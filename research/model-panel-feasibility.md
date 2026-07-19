# Preliminary model-panel feasibility

**Checked:** 2026-07-17
**Purpose:** Establish a no-spend smoke-test path before any confirmatory model panel is frozen. This is not yet a protocol decision.

## Local runtime

[MLX LM](https://github.com/ml-explore/mlx-lm) is the most natural local runner on this M1 Pro. Its official repository supports Apple-silicon inference, Hugging Face models, quantization, batch generation, and an OpenAI-compatible server. Current release notes explicitly include Qwen 3.5 support. The local machine has 16 GB unified memory and about 34 GiB free disk, so models must be loaded and cached sequentially; a collection of full-precision checkpoints is not practical.

**Architecture caveat discovered during setup:** the shell and kernel run arm64, but the installed Homebrew `uv` and Python 3.12 report x86_64. That environment is suitable for the deterministic research package but not for MLX acceleration. The smoke protocol therefore has an explicit runtime gate: install or locate a separately pinned native-arm64 Python/MLX environment, or use a native-arm64 llama.cpp runner. Do not silently run the local-model tier through Rosetta and report it as native MLX.

The smoke tier should use pinned four-bit MLX conversions or self-convert pinned official checkpoints. Community quantizations are convenient but should not be the only provenance path: record the upstream repository and revision, converter and revision, quantization recipe, tokenizer files, chat template, runtime version, and generated file hashes.

## Candidate local families

| Family | Official checkpoint evidence | Local role | Main caveat |
| --- | --- | --- | --- |
| Qwen | [Qwen3.5-4B official configuration](https://huggingface.co/Qwen/Qwen3.5-4B/blob/c7429d5a8ed57f4a9cfdaf1af76a8943eba0ae97/config.json); [Transformers Qwen3.5 docs](https://huggingface.co/docs/transformers/model_doc/qwen3_5) | Current small model for smoke and task calibration | Pin an exact revision; thinking/non-thinking behavior and chat-template defaults must be controlled. |
| Gemma | [google/gemma-3-4b-it](https://huggingface.co/google/gemma-3-4b-it) | Independent model family at 4B scale | Gated terms may require local Hugging Face acceptance; multimodal packaging is unnecessary overhead for text-only tasks. |
| Llama | [meta-llama/Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) | Older but widely recognized third family and implementation cross-check | Gated access and model age; license/attribution requirements must be followed. |
| Mistral | [mistralai/Mistral-7B-Instruct-v0.3](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3) | Apache-licensed 7B comparison if memory and speed permit | Older snapshot and larger local footprint; not a substitute for a current stronger reference model. |

These small checkpoints are suitable for generator/parser debugging, ceiling/floor calibration, and deterministic pipeline checks. They are not automatically an adequate scientific panel. A final panel must represent at least three genuinely different model families and avoid drawing frontier-model conclusions from small quantized models.

## Required runtime checks before model selection

1. Run the exact same frozen prompt through two independent runtime paths for a small response set, such as MLX LM and Transformers or llama.cpp, and compare parsed decisions. Token-level identity is not required across backends, but material conclusion changes must be reported.
2. Measure baseline accuracy and invalid-output rate without any history manipulation. Reject task configurations above 95% or below 50% for most planned models unless the protocol supplies a principled recalibration rule.
3. Check the longest intended history on the 16 GB machine before freezing horizons. Record peak memory, wall time, prompt tokens, completion tokens, and any cache quantization.
4. Run fixed-seed repeatability checks. Greedy decoding should be the main reproducible path where supported; any stochastic arm needs explicit seeds and repeated-sampling logic.
5. Preserve the rendered chat transcript after the tokenizer template, not only abstract role/content JSON. This is essential when comparing assistant-history deletion and literal fresh-context conditions.
6. Verify that a hard reset actually begins a new model context and replays a byte-identical system/rule/target block. An in-context instruction to ignore history is a separate treatment.

## Confirmatory tier

A credible confirmatory panel may need one or more stronger hosted or larger open models after the free smoke tier establishes task validity and a bottom-up call count. The panel, exact provider/model identifiers, prices, and maximum authorized spend must be frozen only after explicit user approval. No paid inference has been run.

Hosted APIs are especially valuable as a cross-check against quantization-specific local effects, but they create reproducibility limits: model aliases can move, providers can retire snapshots, and deterministic seeds may be unavailable. Preserve request and response bodies, provider request IDs where exposed, dates, parameters, token counts, and contemporaneous model documentation.

## Pinned no-cost family canaries after the Qwen pilot

Two public, ungated MLX artifacts were selected for pre-confirmatory family canaries, not yet for the frozen confirmatory panel:

- **Phi:** `mlx-community/Phi-4-mini-instruct-4bit` revision `ac1c269cb4222a4e136a3d09edad301056c1f36a`; local weight SHA-256 `9dcfcdc0a579494283f2d2317ad686123782ce461d1111690ede7c904ff3f87b`; approximately 2.16 GB. The upstream [Microsoft Phi-4-mini-instruct model card](https://huggingface.co/microsoft/Phi-4-mini-instruct) identifies a 3.8B dense decoder model under the MIT license.
- **Mistral:** `mlx-community/Mistral-7B-Instruct-v0.3-4bit` revision `a4b8f870474b0eb527f466a03fbc187830d271f5`; local weight SHA-256 `d7182d886f93a9efa73d6d556ee33ffe839a4e09e15965eeef46f295ab5b503d`; approximately 4.08 GB. The upstream [Mistral-7B-Instruct-v0.3 model card](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3) identifies the instruct-tuned 7B family and Apache-2.0 license.

Both community conversions remain secondary artifacts. Every local file, actual chat-templated prompt, runtime version, and response will be hashed. Each family must first pass a four-target fresh baseline and tokenizer preflight; failure to produce strict JSON or maintain an adequate task range is a rejection, not a prompt-tuning invitation after history outcomes are viewed.

## Tokenizer-first replacement screen

The Phi/Mistral screen showed that model-family feasibility cannot be inferred from fresh-context accuracy alone. Phi passed exact matching only under the separately frozen `outcome_code` representation but then copied that record format, producing just 1/16 strict-valid history responses. Mistral produced no admissible positive/negative pair in either representation or world. Neither family is retained for effect estimation.

To avoid further multi-gigabyte trial downloads, three additional public tokenizers were pinned and screened before weights or responses:

- `mlx-community/SmolLM3-3B-4bit` revision `d3a7e0594d6642dbcfb7d149bed8b0bdf49f95ce`: 32/32 literal and coded pairs accepted in both worlds. The downloaded weight SHA-256 is `d501e6193d7eb84e10d3c377007d1fc4b4b2fa08799dd10fa4f6a75033334a70`; the [upstream SmolLM3 card](https://huggingface.co/HuggingFaceTB/SmolLM3-3B) identifies a 3B model under Apache-2.0.
- `mlx-community/Llama-3.2-3B-Instruct-4bit` revision `7f0dc925e0d0afb0322d96f9255cfddf2ba5636e`: 32/32 literal and coded pairs accepted in both worlds. The downloaded weight SHA-256 is `d75e1ee0ea653cc5b76191ec934c7c0d568e94d4e47846619f1f4bc715b7b265`; the [upstream Llama 3.2 card](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) uses the Llama 3.2 community license.
- `mlx-community/IBM-granite-3.2-2b-instruct-4bit` revision `5b85640a7a63ec2b3acd3203066a6045dfababe6`: literal pairs failed in both worlds; coded pairs passed. Weights were not downloaded and the candidate was deprioritized.

SmolLM3 and Llama 3.2 remain canary candidates only. They must pass the same label-balanced fresh baseline before any history call; a tokenizer pass is not evidence of task validity.

## Bounded replacement result

The local replacement search stopped after two small passing-tokenizer candidates and two final 8B candidates:

- SmolLM3 3B failed the fresh gate at 5/8 strict-valid and 4/8 decision-correct.
- Llama 3.2 3B was 8/8 strict-valid but only 5/8 correct and approved every permit target.
- Granite 3.3 8B revision `0751a30ba2420ecd5c2f142707dd4fcfacc4486e`, weight SHA-256 `f85549d4fa19542939bdcd2a3f5c81f24575baafb3d71f6d50e39033d93a5247`, was 4/4 valid and 3/4 correct on benefit but only 1/4 valid/correct on permit. The [official IBM card](https://huggingface.co/ibm-granite/granite-3.3-8b-instruct) identifies an 8B model under Apache-2.0.
- Llama 3.1 8B revision `241a666dad6cb93c8ff213d39a7f34a36bf26db4`, weight SHA-256 `08eff50fa4eb1fe499ead69eaeb4c5177ae82f218da0b55e0e31d7a989debb92`, passed at 8/8 valid and 7/8 correct. The [official Meta card](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) describes the instruct model and Llama 3.1 community license.

Only Llama 3.1 advanced to literal-history canaries. Its benefit and permit estimates had opposite signs (`+0.25` and `−1.0` on four targets each), so it does not rescue a stable pooled effect. The no-cost local search is closed. A three-family confirmatory claim now requires a separately justified stronger family or hosted snapshot, explicit license/provider review, a priced call manifest, and user approval before any paid inference.
