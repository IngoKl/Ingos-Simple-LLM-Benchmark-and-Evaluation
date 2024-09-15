import os
import uuid

import openai

from ingollmbencheval.benchmark import Benchmark
from ingollmbencheval.report import ReportGenerator

API_KEY = os.environ.get("OPENAI_API_KEY", "local-llm")
BASE_URL = "http://localhost:1234/v1"  # Set to "https://api.openai.com/v1" for OpenAI

MODEL = "gpt-4o"  # Set to False to test all models
TEMPERATURE = 0.2

BENCHMARK_ID = False  # Set to False to generate a benchmark id
TASK_FILE = "tasks/misc.json"  # Set to False to run all tasks
NUM_RUNS = 1


def main():
    if MODEL:
        benchmark = Benchmark(
            api_key=API_KEY,
            base_url=BASE_URL,
            model=MODEL,
            num_runs=NUM_RUNS,
            temperature=TEMPERATURE,
            benchmark_id=BENCHMARK_ID,
            task_file=TASK_FILE,
            db_path="sqlite:///benchmark_results.db",
        )

        if not benchmark.test_model():
            print(f"Skipping model {MODEL} because it failed the test")
            return

        benchmark.run()

        report_gen = ReportGenerator(model=MODEL, benchmark_id=BENCHMARK_ID)
        report_gen.analyze_tasks()
    else:
        # Initialize the OpenAI client
        client = openai.OpenAI(api_key=API_KEY, base_url=BASE_URL)

        # Get all models
        models = client.models.list()
        for model in models:

            benchmark = Benchmark(
                api_key=API_KEY,
                base_url=BASE_URL,
                model=model.id,
                num_runs=NUM_RUNS,
                temperature=TEMPERATURE,
                benchmark_id=BENCHMARK_ID,
                task_file=TASK_FILE,
                db_path="sqlite:///benchmark_results.db",
            )

            if not benchmark.test_model():
                print(f"Skipping model {model.id} because it failed the test")
                continue

            try:
                benchmark.run()

                report_gen = ReportGenerator(model=model.id, benchmark_id=BENCHMARK_ID)
                report_gen.analyze_tasks()
            except Exception as e:
                print(f"Error running benchmark for model {model.id}: {e}")
                continue


if __name__ == "__main__":
    if not BENCHMARK_ID:
        BENCHMARK_ID = str(uuid.uuid4())[:8]

    main()
