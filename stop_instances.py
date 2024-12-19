from utils import initialize_ec2_client

def stop_instances(instance_ids):
    """
    Stops the specified EC2 instances.
    """
    ec2_client = initialize_ec2_client()
    try:
        response = ec2_client.stop_instances(InstanceIds=instance_ids)
        for instance in response["StoppingInstances"]:
            print(f"Instance {instance['InstanceId']} is stopping. Current state: {instance['CurrentState']['Name']}")
    except Exception as e:
        print(f"Error stopping instances: {e}")

if __name__ == "__main__":
    instance_ids = input("Enter the instance IDs to stop (comma-separated): ").strip().split(',')
    instance_ids = [id.strip() for id in instance_ids]
    if instance_ids:
        stop_instances(instance_ids)
    else:
        print("No instance IDs provided.")

