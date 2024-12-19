import boto3
import json
import os

# Tracker file path
TRACKER_FILE = "ec2_tracker.json"

# Load tracker file
def load_tracker_file():
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r") as file:
            return json.load(file)
    return {}

# Save tracker file
def save_tracker_file(data):
    with open(TRACKER_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Initialize EC2 client
def initialize_ec2_client():
    return boto3.client("ec2")

