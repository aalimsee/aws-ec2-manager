import boto3

# Initialize Boto3 clients
ec2 = boto3.client('ec2')

# Function to terminate EC2 instances
def terminate_instance(instance_id):
    ec2.terminate_instances(InstanceIds=[instance_id])
    print(f"Terminated EC2 instance: {instance_id}")

# Function to delete security groups
def delete_security_group(security_group_id):
    ec2.delete_security_group(GroupId=security_group_id)
    print(f"Deleted Security Group: {security_group_id}")

# Function to delete subnets
def delete_subnet(subnet_id):
    ec2.delete_subnet(SubnetId=subnet_id)
    print(f"Deleted Subnet: {subnet_id}")

# Function to detach and delete internet gateway
def delete_internet_gateway(igw_id, vpc_id):
    ec2.detach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
    ec2.delete_internet_gateway(InternetGatewayId=igw_id)
    print(f"Deleted Internet Gateway: {igw_id}")

# Function to delete route tables
def delete_route_table(route_table_id):
    ec2.delete_route_table(RouteTableId=route_table_id)
    print(f"Deleted Route Table: {route_table_id}")

# Function to delete VPC
def delete_vpc(vpc_id):
    ec2.delete_vpc(VpcId=vpc_id)
    print(f"Deleted VPC: {vpc_id}")

# Cleanup process

# Step 1: List and terminate EC2 instances
public_instance_id = 'i-0739f453b1f4316dd'  # Replace with actual Public EC2 Instance ID
private_instance_id = 'i-00f220004e98cdeb0'  # Replace with actual Private EC2 Instance ID

terminate_instance(public_instance_id)
terminate_instance(private_instance_id)

# Step 2: Delete Security Groups
public_sg_id = 'sg-0d1d2934d64254280'  # Replace with actual Public Security Group ID
private_sg_id = 'sg-005835670e58bdd90'  # Replace with actual Private Security Group ID

delete_security_group(public_sg_id)
delete_security_group(private_sg_id)

# Step 3: Delete Subnets
public_subnet_id = 'subnet-098d17b2492e16171'  # Replace with actual Public Subnet ID
private_subnet_id = '022e307f624f0797a'  # Replace with actual Private Subnet ID

delete_subnet(public_subnet_id)
delete_subnet(private_subnet_id)

# Step 4: Delete Internet Gateway
igw_id = 'igw-0ae5e4620df107482'  # Replace with actual Internet Gateway ID
vpc_id = 'vpc-0bf8346db7ac93569'  # Replace with actual VPC ID

delete_internet_gateway(igw_id, vpc_id)

# Step 5: Delete Route Tables
public_route_table_id = 'rtb-0ce3ac1d4f12b83d5'  # Replace with actual Public Route Table ID
private_route_table_id = 'rtb-00eca27066b709eed'  # Replace with actual Private Route Table ID

delete_route_table(public_route_table_id)
delete_route_table(private_route_table_id)

# Step 6: Delete VPC
delete_vpc(vpc_id)

print("Cleanup process complete.")

