# Ingo's (Simple) LLM Benchmark and Evaluation

This project provides a very simple benchmarking and evaluation tool for testing LLMs via OpenAI-compatible APIs. It is highly idiosyncratic and contains some tasks I find interesting. 

Hence, it is not meant to be comprehensive or all-encompassing at all, but rather a set of personal benchmarks and evaluations for LLMs. It exists because I do believe that, despite the broad availability of standardized benchmarks and evaluations (e.g., the [EleutherAI LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness)), there is still a lot of value in developing and testing your own tasks.

## Features

- Supports OpenAI-compatible endpoints
- Simple JSON-based task format
- Customizable benchmark parameters
- Storing benchmark results in SQLite database for easy analysis and reporting

## Task Format

The tasks are defined in JSON format and are stored in the `tasks` directory. The are grouped into different files, for example `math.json`.

```
{
    "id": "math-1a",
    "task_version": "1.0.0",
    "description": "A simple addition task.",
    "prompt": "What is 10 + 13?",
    "solution": "23",
    "match_type": "exact-match"
}
```

Each task has an `id`, a `task_version`, a `description`, a `prompt`, a `solution`, and a `match_type`.

### Match Types

The benchmark tool supports various match types for evaluating responses:

1. exact-match (This is case-sensitive)
2. exact-match-ci (This is case-insensitive)
2. partial-match (This is case-insensitive)
3. regex match

Tasks are evaluated as "success" or "failure" based on the match type and result.

### A/B/X Variants of Tasks

If there are multiple versions of the same tasks (e.g., with slightly different prompts), A/B/X variants of a task are defined.

## Usage

### Installation

1. Install the project using Poetry:
   ```
   poetry install
   ```

2. (Re)Create the database:
   ```
   poetry run create-database
   poetry run recreate-database
   ```

### Benchmarking / Evaluation

You can test a single model or all models available at the endpoint. You can also test a single set of tasks or all tasks.

1. Configure the benchmark parameters in `run_benchmark.py`:

2. Run the benchmark:
   ```
   poetry run python run_benchmark.py
   ```

### Generating Reports

Generate a report for a specific model

1. Configure the report parameters in `generate_model_report.py`:

2. Generate the report:
    ```
    poetry run python generate_model_report.py
    ```

If you want to analyze a specific benchmark, you can do so by passing the benchmark name to the `ReportGenerator` class.

## Results

Benchmark results are stored in an SQLite database (`benchmark_results.db` by default). The `ReportGenerator` class can be used to analyze the results and generate CSV reports.