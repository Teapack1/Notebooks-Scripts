import os
import json
import csv
from datetime import datetime

unknown_counter = 0  # Global counter for "Unknown" conversation names


def fix_encoding(text):
    """
    Attempt to correct the encoding by trying multiple encodings.
    """

    return text.encode("latin-1").decode("utf-8")


def process_messages(json_filepath, csv_writer, conversation_name):
    """
    Read messages from a JSON file and write them to the provided CSV writer along with the conversation name, skipping messages with no content.
    """
    with open(json_filepath, "r", encoding="utf-8") as file:
        data = json.load(file)
        for message in data.get("messages", []):
            content = message.get("content")
            if content:  # Check if content exists and is not None
                date_time = datetime.fromtimestamp(
                    message["timestamp_ms"] / 1000
                ).strftime("%Y-%m-%d %H:%M:%S")
                sender_name = message.get("sender_name", "").strip()
                sender_name = (
                    "Unknown" if not sender_name else fix_encoding(sender_name)
                )
                content = fix_encoding(content)
                csv_writer.writerow(
                    [date_time, sender_name, content, conversation_name]
                )
            # Skip the row entirely if there's no content


def process_directory(directory_path, unknown_counter):
    """
    Process all messages in JSON files within a directory, outputting to a CSV file in the same directory.
    Includes a unique identifier for unnamed conversations.
    """
    # Extracts conversation name and checks if it's purely numeric
    conversation_name = directory_path.split(os.sep)[-1].split("_")[0]
    if (
        conversation_name.isdigit()
    ):  # Checks if the conversation name consists only of digits
        unknown_counter += 1
        conversation_name = f"Unknown{unknown_counter}"

    csv_filepath = os.path.join(directory_path, "combined_messages.csv")
    for ex_csv_file in os.listdir(directory_path):
        if ex_csv_file.endswith(".csv"):
            ex_csv_filepath = os.path.join(directory_path, ex_csv_file)
            os.remove(ex_csv_filepath)

    with open(csv_filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["Date and Time", "Name", "Content", "Conversation"]
        )  # Header row with new column

        for filename in os.listdir(directory_path):
            if filename.endswith(".json"):
                json_filepath = os.path.join(directory_path, filename)
                process_messages(json_filepath, writer, conversation_name)

    print(f"CSV file has been created at {csv_filepath}")
    return unknown_counter  # Return the updated counter


def process_all_folders(base_directory_path):
    """
    Process all subfolders within the base directory, each containing JSON files for messages.
    """
    unknown_counter = 0  # Initialize the counter for unknown conversation names
    for folder_name in os.listdir(base_directory_path):
        folder_path = os.path.join(base_directory_path, folder_name)
        if os.path.isdir(folder_path):
            unknown_counter = process_directory(
                folder_path, unknown_counter
            )  # Update the counter


# This function produces csv dataset file out of all the "combined_messages.csv" files in the subfolders of the base directory.
# It combines all the messages from all the conversations into one dataset. The first column date and time, the second column is who wrote the message, if there is nothing, write "unknown", the second column is the content of the message.


def produce_csv_dataset(base_directory_path):
    """
    Combine all the "combined_messages.csv" files in the subfolders of the base directory into one dataset.
    """
    csv_dataset_filepath = os.path.join(base_directory_path, "all_messages_dataset.csv")
    with open(csv_dataset_filepath, "w", newline="", encoding="utf-8") as dataset_file:
        writer = csv.writer(dataset_file)
        writer.writerow(
            ["Date and Time", "Name", "Content", "Conversation"]
        )  # Updated header row

        for folder_name in os.listdir(base_directory_path):
            folder_path = os.path.join(base_directory_path, folder_name)
            if os.path.isdir(folder_path):
                csv_filepath = os.path.join(folder_path, "combined_messages.csv")
                if os.path.exists(csv_filepath):
                    with open(csv_filepath, "r", encoding="utf-8") as file:
                        reader = csv.reader(file)
                        next(reader)  # Skip header row
                        for row in reader:
                            if not row[1].strip():
                                row[1] = "Unknown"
                            writer.writerow(row)
    print(f"CSV dataset file has been created at {csv_dataset_filepath}")


# Example Usage
base_directory_path = "C:\\Users\\majoron\\Desktop\\facebook-ondramajor-19_04_2024-Ub746IDG\\your_facebook_activity\\messages\\inbox"  # Modify this path as needed

process_all_folders(base_directory_path)
produce_csv_dataset(base_directory_path)
