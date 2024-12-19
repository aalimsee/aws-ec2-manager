from utils import initialize_ec2_client

def list_instances():
    """
    Lists all EC2 instances.
    """
    ec2_client = initialize_ec2_client()
    try:
        response = ec2_client.describe_instances()
        instances = []
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                instances.append({
                    "InstanceId": instance["InstanceId"],
                    "State": instance["State"]["Name"],
                    "AMI": instance["ImageId"],
                    "InstanceType": instance["InstanceType"],
                    "LaunchTime": instance["LaunchTime"],
                })
        return instances
    except Exception as e:
        print(f"Error listing instances: {e}")
        return []

if __name__ == "__main__":
    instances = list_instances()
    print("Instances:")
    for instance in instances:
        print(f"- {instance['InstanceId']} (State: {instance['State']}, Type: {instance['InstanceType']}, AMI: {instance['AMI']}, LaunchTime: {instance['LaunchTime']})")

