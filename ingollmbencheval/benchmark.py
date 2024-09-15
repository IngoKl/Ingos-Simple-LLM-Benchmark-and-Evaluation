import glob
import json
import re
import time
from datetime import datetime

import openai
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ingollmbencheval.database import Result


def is_correct_response(response, solution, match_type):
    if match_type == "exact-match":
        return response.strip() == solution.strip()
    elif match_type == "exact-match-ci":
        return response.strip().lower() == solution.strip().lower()
    elif match_type == "partial-match":
        return solution.strip().lower() in response.lower()
    elif match_type == "regex-match":
        try:
            pattern = re.compile(solution)
            return bool(pattern.fullmatch(response.strip()))
        except re.error as e:
            print(f"Invalid regex pattern '{solution}': {e}")
            return False
    else:
        print(f"Unknown match type '{match_type}'")
        return False


class Benchmark:
    def __init__(
        self,
        api_key,
        base_url,
        model,
        num_runs,
        temperature,
        benchmark_id,
        db_path="sqlite:///benchmark_results.db",
        task_file=None,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.num_runs = num_runs
        self.temperature = temperature
        self.benchmark_id = benchmark_id
        self.db_path = db_path
        self.task_file = task_file

        # Initialize the OpenAI client
        self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)

        # Set up SQLAlchemy
        self.engine = create_engine(self.db_path)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def test_model(self):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello, world!"}],
                temperature=self.temperature,
            )
            return response
        except Exception as e:
            print(f"Error testing model {self.model}: {e}")
            return False

    def run(self):
        # Get task files based on the task_file parameter
        if self.task_file:
            task_files = [self.task_file]
        else:
            task_files = glob.glob("tasks/*.json")

        # Iterate over each task file
        for task_file in task_files:
            with open(task_file, "r") as f:
                tasks_data = json.load(f)
                tasks = tasks_data["tasks"]

            # Iterate over each task in the file
            for task in tasks:
                for _ in range(self.num_runs):
                    # Prepare the prompt as a conversation
                    prompt = task["prompt"]
                    messages = [{"role": "user", "content": prompt}]

                    # Extract solution and match_type
                    solution = task.get("solution", "")
                    match_type = task.get("match_type", "exact-match")

                    try:
                        response = self.client.chat.completions.create(
                            model=self.model,
                            messages=messages,
                            temperature=self.temperature,
                        )
                    except openai.NotFoundError:
                        print(f"Model {self.model} not found or wrong model type")
                        break
                    except openai.PermissionDeniedError:
                        print(f"Permission denied for model {self.model}")
                        break
                    except Exception as e:
                        print(f"Error processing task '{task['id']}': {e}")
                        # Optional: Wait before retrying
                        time.sleep(5)

                    try:
                        # Extract the response text
                        completion_tokens = response.usage.completion_tokens
                        response_text = response.choices[0].message.content

                        # Check if the response is correct
                        success = is_correct_response(
                            response_text, solution, match_type
                        )

                        # Get the current timestamp
                        timestamp = datetime.now().isoformat()

                        # Create a new Result object and add it to the session
                        result = Result(
                            benchmark_id=self.benchmark_id,
                            task_id=task["id"],
                            task_version=task["task_version"],
                            model=self.model,
                            temperature=self.temperature,
                            timestamp=timestamp,
                            response=response_text,
                            completion_tokens=completion_tokens,
                            success=success,
                        )
                        self.session.add(result)

                        # Commit the transaction
                        self.session.commit()

                        # Optional: Print progress
                        status = "SUCCESS" if success else "FAILURE"
                        print(
                            f"[{timestamp}] Task '{task['id']}' using model '{self.model}' completed with status: {status}. Response: {response_text.replace('\n', ' ')[0:50]}"
                        )
                    except Exception as e:
                        print(f"Error processing task '{task['id']}': {e}")

        # Close the session
        self.session.close()
