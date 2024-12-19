from utils import initialize_ec2_client

def list_instances_with_names():
    """
    Lists all EC2 instances with their names and details.
    """
    ec2_client = initialize_ec2_client()
    try:
        response = ec2_client.describe_instances()
        instances = []
        
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                # Extract instance details
                instance_id = instance.get("InstanceId", "N/A")
                state = instance["State"]["Name"]
                ami_id = instance.get("ImageId", "N/A")
                instance_type = instance.get("InstanceType", "N/A")
                launch_time = instance.get("LaunchTime", "N/A")
                
                # Get the Name tag (if it exists)
                tags = instance.get("Tags", [])
                name_tag = next((tag["Value"] for tag in tags if tag["Key"] == "Name"), "Unnamed Instance")
                
                # Append instance details
                instances.append({
                    "InstanceId": instance_id,
                    "Name": name_tag,
                    "State": state,
                    "AMI": ami_id,
                    "InstanceType": instance_type,
                    "LaunchTime": str(launch_time),
                })
        
        # Display instances
        if instances:
            print("EC2 Instances:")
            for instance in instances:
                print(
                    f"- {instance['InstanceId']} (Name: {instance['Name']}, State: {instance['State']}, "
                    f"Type: {instance['InstanceType']}, AMI: {instance['AMI']}, LaunchTime: {instance['LaunchTime']})"
                )
        else:
            print("No EC2 instances found.")
    
    except Exception as e:
        print(f"Error listing instances: {e}")

if __name__ == "__main__":
    list_instances_with_names()

