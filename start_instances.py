from utils import initialize_ec2_client

def start_instances(instance_ids):
    """
    Starts the specified EC2 instances.
    """
    ec2_client = initialize_ec2_client()
    try:
        response = ec2_client.start_instances(InstanceIds=instance_ids)
        for instance in response["StartingInstances"]:
            print(f"Instance {instance['InstanceId']} is starting. Current state: {instance['CurrentState']['Name']}")
    except Exception as e:
        print(f"Error starting instances: {e}")

if __name__ == "__main__":
    instance_ids = input("Enter the instance IDs to start (comma-separated): ").strip().split(',')
    instance_ids = [id.strip() for id in instance_ids]
    if instance_ids:
        start_instances(instance_ids)
    else:
        print("No instance IDs provided.")

