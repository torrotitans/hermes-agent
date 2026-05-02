# Experiment Logging

## TSV Format

Tab-separated values file (`results.tsv`) with header row:

```
commit	val_bpb	memory_gb	status	description
```

### Fields

| Field | Format | Notes |
|-------|--------|-------|
| `commit` | 7-char short hash | e.g., `a1b2c3d` |
| `val_bpb` | float, 6 decimals | `0.000000` for crashes |
| `memory_gb` | float, 1 decimal | `peak_vram_mb / 1024`, `0.0` for crashes |
| `status` | enum | `keep`, `discard`, or `crash` |
| `description` | string | Short text of what was tried |

### Example

```
commit	val_bpb	memory_gb	status	description
a1b2c3d	0.997900	44.0	keep	baseline
b2c3d4e	0.993200	44.2	keep	increase LR to 0.04
c3d4e5f	1.005000	44.0	discard	switch to GeLU activation
d4e5f6g	0.000000	0.0	crash	double model width (OOM)
```

## Extraction Commands

```bash
# Get val_bpb and peak VRAM from run.log
grep "^val_bpb:\|^peak_vram_mb:" run.log

# Extract just val_bpb
grep "^val_bpb:" run.log
```

## Important Notes

- Use **tabs**, not commas (commas break in descriptions)
- Do NOT commit `results.tsv` — leave it untracked by git
- Log crashes with `0.000000` for val_bpb and `0.0` for memory
