from ingollmbencheval.report import ReportGenerator

MODEL = "gpt-4o"


def main():
    report_gen = ReportGenerator(model=MODEL)
    report_gen.analyze_tasks()


if __name__ == "__main__":
    main()
