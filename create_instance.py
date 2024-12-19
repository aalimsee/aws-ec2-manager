from datetime import datetime
from utils import initialize_ec2_client, load_tracker_file, save_tracker_file

def create_instance(ami_id, instance_type, key_name, security_group):
    """
    Creates a new EC2 instance.
    """
    ec2_client = initialize_ec2_client()
    try:
        response = ec2_client.run_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            KeyName=key_name,
            SecurityGroups=[security_group],
            MinCount=1,
            MaxCount=1,
        )
        instance = response["Instances"][0]
        instance_id = instance["InstanceId"]
        print(f"EC2 instance '{instance_id}' created successfully.")

        # Track the instance
        instance_data = {
            "instance_id": instance_id,
            "ami_id": ami_id,
            "instance_type": instance_type,
            "key_name": key_name,
            "security_group": security_group,
            "created_on": str(datetime.now()),
        }
        track_instance(instance_data)
    except Exception as e:
        print(f"Error creating instance: {e}")

def track_instance(instance_data):
    tracker_data = load_tracker_file()
    instance_id = instance_data["instance_id"]
    if instance_id not in tracker_data:
        tracker_data[instance_id] = instance_data
        save_tracker_file(tracker_data)
        print(f"Instance '{instance_id}' added to tracker file.")
    else:
        print(f"Instance '{instance_id}' is already tracked.")

if __name__ == "__main__":
    ami_id = input("Enter AMI ID: ")
    instance_type = input("Enter instance type (e.g., t2.micro): ")
    key_name = input("Enter key pair name: ")
    security_group = input("Enter security group name: ")
    create_instance(ami_id, instance_type, key_name, security_group)

