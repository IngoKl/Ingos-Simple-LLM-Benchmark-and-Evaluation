import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ingollmbencheval.database import Result
from ingollmbencheval.utils import sanitize_model_name


class ReportGenerator:
    def __init__(
        self, model, benchmark_id=None, db_path="sqlite:///benchmark_results.db"
    ):
        self.db_path = db_path
        self.model = model
        self.benchmark_id = benchmark_id
        self.engine = create_engine(self.db_path)
        self.Session = sessionmaker(bind=self.engine)
        self.model_report = self._get_model_report()

    def _get_model_report(self):
        with self.Session() as session:
            query = session.query(
                Result.benchmark_id,
                Result.task_id,
                Result.task_version,
                Result.timestamp,
                Result.response,
                Result.completion_tokens,
                Result.success,
            )
            query = query.filter(Result.model == self.model)

            if self.benchmark_id:
                query = query.filter(Result.benchmark_id == self.benchmark_id)

            return query.all()

    def analyze_tasks(self):
        task_analysis = {}

        for row in self.model_report:
            (
                benchmark_id,
                task_id,
                task_version,
                timestamp,
                response,
                completion_tokens,
                success,
            ) = row
            task_key = f"{task_id} (v{task_version})"
            if task_key not in task_analysis:
                task_analysis[task_key] = {
                    "model": self.model,
                    "benchmark_id": self.benchmark_id,
                    "total_runs": 0,
                    "successful_runs": 0,
                }

            task_analysis[task_key]["total_runs"] += 1
            task_analysis[task_key]["successful_runs"] += success
            task_analysis[task_key]["success_rate"] = (
                task_analysis[task_key]["successful_runs"]
                / task_analysis[task_key]["total_runs"]
            ) * 100

        # Convert task_analysis to a pandas DataFrame
        df = pd.DataFrame.from_dict(task_analysis, orient="index")
        df.reset_index(inplace=True)
        df.rename(columns={"index": "task"}, inplace=True)

        # Export to CSV
        csv_filename = f"reports/{sanitize_model_name(self.model)}_{self.benchmark_id}_task_analysis.csv"
        df.to_csv(csv_filename, index=False)
        print(f"Task analysis exported to {csv_filename}")

        return task_analysis
