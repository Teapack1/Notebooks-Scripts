import os
import json
import csv
from datetime import datetime


def fix_encoding(text):
    """
    Attempt to correct the encoding by trying multiple encodings.
    """
    try:
        return text.encode("latin-1").decode("utf-8")
    except UnicodeEncodeError:
        try:
            return text.encode("cp1252").decode("utf-8")
        except UnicodeEncodeError:
            return text  # If still fails, return the original text


def process_messages(json_filepath, csv_writer):
    """
    Read messages from a JSON file and write them to the provided CSV writer.
    """
    with open(json_filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

        for message in data.get("messages", []):
            date_time = datetime.fromtimestamp(message["timestamp_ms"] / 1000).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            sender_name = fix_encoding(message.get("sender_name", "Unknown"))
            content = message.get("content", "No content available")
            content = fix_encoding(content)

            csv_writer.writerow([date_time, sender_name, content])


def process_directory(directory_path):
    """
    Process all messages in JSON files within a directory, outputting to a CSV file in the same directory.
    """
    csv_filepath = os.path.join(directory_path, "combined_messages.csv")

    with open(csv_filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date and Time", "Name", "Content"])  # Header row

        for filename in os.listdir(directory_path):
            if filename.endswith(".json"):
                json_filepath = os.path.join(directory_path, filename)
                process_messages(json_filepath, writer)

    print(f"CSV file has been created at {csv_filepath}")


def process_all_folders(base_directory_path):
    """
    Process all subfolders within the base directory, each containing JSON files for messages.
    """
    for folder_name in os.listdir(base_directory_path):
        folder_path = os.path.join(base_directory_path, folder_name)
        if os.path.isdir(folder_path):
            process_directory(folder_path)


# Example Usage
base_directory_path = "C:\\Users\\majoron\\Desktop\\facebook-ondramajor-19_04_2024-Ub746IDG\\your_facebook_activity\\messages\\inbox"  # Modify this path as needed
process_all_folders(base_directory_path)
