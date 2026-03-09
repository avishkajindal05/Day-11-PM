import os
import csv
import json
import time
import traceback

INPUT_DIR = "csv_files"
REPORT_FILE = "processing_report.json"

MAX_RETRIES = 3
RETRY_DELAY = 1


def process_csv_file(file_path):
    """
    Reads a CSV file and computes simple aggregates.
    Assumes numeric columns where possible.
    """

    aggregates = {}

    with open(file_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        rows = list(reader)

        if not rows:
            raise ValueError("CSV file is empty")

        # Identify numeric columns
        numeric_columns = {}

        for col in reader.fieldnames:
            numeric_columns[col] = []

        for row in rows:
            for col, val in row.items():
                try:
                    numeric_columns[col].append(float(val))
                except (ValueError, TypeError):
                    pass

        for col, values in numeric_columns.items():
            if values:
                aggregates[col] = {
                    "count": len(values),
                    "sum": sum(values),
                    "avg": sum(values) / len(values)
                }

    return aggregates


def process_with_retry(file_path):
    """
    Retry logic only for PermissionError.
    """

    attempts = 0

    while attempts < MAX_RETRIES:
        try:
            return process_csv_file(file_path)

        except PermissionError:
            attempts += 1
            if attempts >= MAX_RETRIES:
                raise
            time.sleep(RETRY_DELAY)

        except Exception:
            raise


def main():

    report = {
        "files_processed": [],
        "files_failed": [],
        "error_details": {}
    }

    if not os.path.exists(INPUT_DIR):
        print("Input directory does not exist")
        return

    for file_name in os.listdir(INPUT_DIR):

        if not file_name.endswith(".csv"):
            continue

        file_path = os.path.join(INPUT_DIR, file_name)

        try:
            aggregates = process_with_retry(file_path)

            report["files_processed"].append({
                "file": file_name,
                "aggregates": aggregates
            })

        except Exception:

            error_trace = traceback.format_exc()

            report["files_failed"].append(file_name)

            report["error_details"][file_name] = error_trace

            print(f"Failed processing {file_name}")

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    print("Processing completed")
    print(f"Report saved to {REPORT_FILE}")


if __name__ == "__main__":
    main()