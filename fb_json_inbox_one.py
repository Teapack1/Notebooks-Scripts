import json
import csv
from datetime import datetime


def fix_encoding(text):
    """
    Try to fix the encoding by assuming the text is double-encoded.
    """

    return text.encode("latin-1").decode("utf-8")


def process_messages(json_filepath, csv_filepath):
    """
    Read messages from a JSON file and write them to a CSV file.
    """
    with open(json_filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    with open(csv_filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date and Time", "Name", "Content"])  # Header row

        for message in data["messages"]:
            date_time = datetime.fromtimestamp(message["timestamp_ms"] / 1000).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            sender_name = fix_encoding(message["sender_name"])
            content = message.get("content", "No content available")
            content = fix_encoding(content) if content else "No content available"

            writer.writerow([date_time, sender_name, content])

    print(f"CSV file has been created at {csv_filepath} with the message data.")


# Example Usage
json_input_path = "message_1.json"
csv_output_path = "output_messages.csv"

process_messages(json_input_path, csv_output_path)
