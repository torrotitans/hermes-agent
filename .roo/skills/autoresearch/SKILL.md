---
name: autoresearch
description: >-
  Run autonomous AI research experiments using karpathy's autoresearch framework.
  Gives an AI agent a small LLM training setup (train.py) and lets it experiment
  overnight — modifying architecture, hyperparameters, optimizer, and training loop,
  then evaluating val_bpb improvement over fixed 5-minute time budgets.
  Keywords: autonomous research, AI research agent, LLM training, model optimization,
  GPT training, val_bpb, Muon optimizer, training loop, experiment automation,
  karpathy, nanochat, self-modifying code, overnight experiment
---

# autoresearch

Autonomous AI research agent framework. Give an AI agent a training script and let it
improve the model overnight by modifying code, training for 5 minutes, and keeping
improvements that lower `val_bpb`.

## When to use

- You want an AI agent to autonomously improve a small LLM training setup
- You have a single NVIDIA GPU (H100 preferred, smaller GPUs supported with tuning)
- You want to run overnight experiments with fixed 5-minute time budgets
- You want to iterate on model architecture, optimizer, or hyperparameters without manual effort

## When NOT to use

- You need distributed/multi-GPU training (use the parent [nanochat](https://github.com/karpathy/nanochat) repo)
- You want to train on CPU or MPS without using a fork (see forks section below)
- You need long training runs (this is designed for 5-minute experiments)
- You want to modify data preparation or evaluation code (those are read-only)

## Prerequisites

1. NVIDIA GPU (tested on H100)
2. Python 3.10+
3. [uv](https://docs.astral.sh/uv/) project manager
4. Git repository initialized

## Setup

1. Clone the autoresearch repo:
   ```bash
   git clone https://github.com/karpathy/autoresearch.git
   cd autoresearch
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Prepare data (one-time, ~2 min):
   ```bash
   uv run prepare.py
   ```

4. Verify baseline training works:
   ```bash
   uv run train.py
   ```

## Core Files

| File | Role | Agent Can Modify? |
|------|------|-------------------|
| [`train.py`](https://github.com/karpathy/autoresearch/blob/main/train.py) | Model, optimizer, training loop | **YES** — only file agent edits |
| [`prepare.py`](https://github.com/karpathy/autoresearch/blob/main/prepare.py) | Data prep, tokenizer, dataloader, eval | **NO** — read-only |
| [`program.md`](https://github.com/karpathy/autoresearch/blob/main/program.md) | Agent instructions | **NO** — human edits this |

## Experiment Loop

1. Create branch: `git checkout -b autoresearch/<tag>` (e.g., `mar5`)
2. Initialize `results.tsv` with header: `commit\tval_bpb\tmemory_gb\tstatus\tdescription`
3. **LOOP FOREVER:**
   a. Tune `train.py` with an experimental idea
   b. `git commit -m "description of change"`
   c. `uv run train.py > run.log 2>&1`
   d. Extract results: `grep "^val_bpb:\|^peak_vram_mb:" run.log`
   e. Log to `results.tsv`
   f. If val_bpb improved → keep commit; if worse → `git reset --hard HEAD~1`
   g. Timeout: kill runs exceeding 10 minutes

## Key Metric

- **val_bpb** (validation bits per byte) — lower is better
- Fixed 5-minute training time budget per experiment
- ~12 experiments/hour, ~100 experiments overnight

## Output Format

```
---
val_bpb:          0.997900
training_seconds: 300.1
total_seconds:    325.9
peak_vram_mb:     45060.2
mfu_percent:      39.80
total_tokens_M:   499.6
num_steps:        953
num_params_M:     50.3
depth:            8
```

## Platform Forks

| Fork | Platform |
|------|----------|
| [miolini/autoresearch-macos](https://github.com/miolini/autoresearch-macos) | macOS |
| [trevin-creator/autoresearch-mlx](https://github.com/trevin-creator/autoresearch-mlx) | macOS (MLX) |
| [jsegov/autoresearch-win-rtx](https://github.com/jsegov/autoresearch-win-rtx) | Windows |
| [andyluo7/autoresearch](https://github.com/andyluo7/autoresearch) | AMD |

## Small GPU Tuning

For MacBooks or smaller GPUs:
1. Use [TinyStories dataset](https://huggingface.co/datasets/karpathy/tinystories-gpt4-clean)
2. Lower `vocab_size` (4096, 2048, 1024, or 256 for byte-level)
3. Lower `MAX_SEQ_LEN` in `prepare.py` (down to 256)
4. Lower `DEPTH` in `train.py` (from 8 to 4)
5. Use `WINDOW_PATTERN` of just `"L"` instead of `"SSSL"`
6. Lower `TOTAL_BATCH_SIZE` to powers of 2 (e.g., `2**14`)

## References

- [`references/experiment-logging.md`](references/experiment-logging.md) — detailed TSV logging format and examples
