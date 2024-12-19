from utils import load_tracker_file

def display_tracked_instances():
    """
    Displays all tracked EC2 instances.
    """
    tracker_data = load_tracker_file()
    if tracker_data:
        print("Tracked EC2 Instances:")
        for instance_id, details in tracker_data.items():
            print(f"- {instance_id}: {details}")
    else:
        print("No EC2 instances are being tracked.")

if __name__ == "__main__":
    display_tracked_instances()

