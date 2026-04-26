# llms-sql-eval

Public artifacts for reproducing the **automatic** SQL error-type classification (LLM-as-judge) described in the paper _Assessing the Ability of Large Language Models to Detect and Explain Errors in SQL Queries_.

## `automatic/`

| File | Purpose |
|------|---------|
| [`automatic/prompts.yaml`](automatic/prompts.yaml) | System prompt for the judge (`eval_classification_prompt`). |
| [`automatic/request_format.json`](automatic/request_format.json) | How each call packages README + SQL, OpenRouter base URL, label set, and mapping from index label `logical` to the paper’s “Conceptual” column. |
| [`automatic/index.jsonl`](automatic/index.jsonl) | Full exercise index (75 lines). All paths are **relative to `automatic/`** (e.g. `data/codefights-arcade-databases/<exercise>/solution.sql`). |
| `automatic/data/codefights-arcade-databases/` | Mirrored from UTAL: reference solutions, `data.sql`, `README.md`, and four erroneous SQL variants per exercise. |

The runnable evaluation harness (index generation, OpenRouter calls, log aggregation) lives in the authors’ **UTAL** codebase under `sqlagent/` (e.g. `evals.py`, `run_classification_eval.py`, `prompts.yaml`). Keep this repository’s `automatic/prompts.yaml` in sync with `sqlagent/prompts.yaml` when the judge prompt changes.
