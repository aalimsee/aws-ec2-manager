from utils import initialize_ec2_client, load_tracker_file, save_tracker_file

def terminate_instance(instance_id):
    """
    Terminates an EC2 instance and removes it from the tracker file.
    """
    ec2_client = initialize_ec2_client()
    try:
        ec2_client.terminate_instances(InstanceIds=[instance_id])
        print(f"Instance '{instance_id}' terminated successfully.")

        # Remove from tracker
        tracker_data = load_tracker_file()
        if instance_id in tracker_data:
            del tracker_data[instance_id]
            save_tracker_file(tracker_data)
            print(f"Instance '{instance_id}' removed from tracker file.")
        else:
            print(f"Instance '{instance_id}' was not found in the tracker file.")
    except Exception as e:
        print(f"Error terminating instance '{instance_id}': {e}")

if __name__ == "__main__":
    instance_id = input("Enter the instance ID to terminate: ")
    confirm = input(f"Are you sure you want to terminate instance '{instance_id}'? (yes/no): ").lower()
    if confirm == "yes":
        terminate_instance(instance_id)
    else:
        print("Operation canceled.")

