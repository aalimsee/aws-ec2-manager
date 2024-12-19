from utils import load_tracker_file, save_tracker_file

def track_instance(instance_data):
    """
    Adds a new instance to the tracker file.
    If the instance is already tracked, it skips adding.
    """
    tracker_data = load_tracker_file()
    instance_id = instance_data["instance_id"]

    if instance_id not in tracker_data:
        tracker_data[instance_id] = instance_data
        save_tracker_file(tracker_data)
        print(f"Instance '{instance_id}' added to tracker file.")
    else:
        print(f"Instance '{instance_id}' is already tracked.")

def remove_tracked_instance(instance_id):
    """
    Removes an instance from the tracker file.
    """
    tracker_data = load_tracker_file()
    if instance_id in tracker_data:
        del tracker_data[instance_id]
        save_tracker_file(tracker_data)
        print(f"Instance '{instance_id}' removed from tracker file.")
    else:
        print(f"Instance '{instance_id}' is not in the tracker file.")

def display_tracked_instances():
    """
    Displays all instances in the tracker file.
    """
    tracker_data = load_tracker_file()
    if tracker_data:
        print("Tracked EC2 Instances:")
        for instance_id, details in tracker_data.items():
            print(f"- {instance_id}: {details}")
    else:
        print("No EC2 instances are being tracked.")

if __name__ == "__main__":
    print("Options:")
    print("1. Track a new instance")
    print("2. Remove an instance from the tracker")
    print("3. Display tracked instances")
    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        instance_id = input("Enter instance ID: ")
        ami_id = input("Enter AMI ID: ")
        instance_type = input("Enter instance type (e.g., t2.micro): ")
        key_name = input("Enter key pair name: ")
        security_group = input("Enter security group name: ")
        created_on = input("Enter creation timestamp (e.g., 2024-12-17T10:00:00Z): ")

        instance_data = {
            "instance_id": instance_id,
            "ami_id": ami_id,
            "instance_type": instance_type,
            "key_name": key_name,
            "security_group": security_group,
            "created_on": created_on,
        }
        track_instance(instance_data)

    elif choice == "2":
        instance_id = input("Enter instance ID to remove: ")
        remove_tracked_instance(instance_id)

    elif choice == "3":
        display_tracked_instances()

    else:
        print("Invalid choice. Exiting.")

