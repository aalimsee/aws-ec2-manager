import boto3

# Initialize Boto3 clients
ec2 = boto3.client('ec2')

# Step 1: Create VPC
response = ec2.create_vpc(CidrBlock='10.0.0.0/16')
vpc_id = response['Vpc']['VpcId']
ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={'Value': True})
ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})

# Tag the VPC with the name
ec2.create_tags(Resources=[vpc_id], Tags=[{'Key': 'Name', 'Value': 'aalimsee-vpc'}])
print(f"VPC created: {vpc_id} with name 'aalimsee-vpc'")

# Step 2: Create Subnets
# Public Subnet
response = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.1.0/24', AvailabilityZone='us-east-1a')
public_subnet_id = response['Subnet']['SubnetId']
ec2.modify_subnet_attribute(SubnetId=public_subnet_id, MapPublicIpOnLaunch={'Value': True})

# Tag the Public Subnet with the name
ec2.create_tags(Resources=[public_subnet_id], Tags=[{'Key': 'Name', 'Value': 'aalimsee-public-subnet'}])
print(f"Public Subnet created: {public_subnet_id} with name 'aalimsee-public-subnet'")

# Private Subnet
response = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.2.0/24', AvailabilityZone='us-east-1a')
private_subnet_id = response['Subnet']['SubnetId']

# Tag the Private Subnet with the name
ec2.create_tags(Resources=[private_subnet_id], Tags=[{'Key': 'Name', 'Value': 'aalimsee-private-subnet'}])
print(f"Private Subnet created: {private_subnet_id}")

# Step 3: Create and Attach Internet Gateway
response = ec2.create_internet_gateway()
igw_id = response['InternetGateway']['InternetGatewayId']
ec2.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)

# Tag the Internet Gateway with the name
ec2.create_tags(Resources=[igw_id], Tags=[{'Key': 'Name', 'Value': 'aalimsee-igw'}])
print(f"Internet Gateway created and attached: {igw_id}")

# Step 4: Create Route Tables
# Public Route Table
response = ec2.create_route_table(VpcId=vpc_id)
public_route_table_id = response['RouteTable']['RouteTableId']
ec2.associate_route_table(RouteTableId=public_route_table_id, SubnetId=public_subnet_id)
ec2.create_route(RouteTableId=public_route_table_id, DestinationCidrBlock='0.0.0.0/0', GatewayId=igw_id)

# Tag the Public Route Table with the name
ec2.create_tags(Resources=[public_route_table_id], Tags=[{'Key': 'Name', 'Value': 'aalimsee-public-route-table'}])
print(f"Public Route Table created and associated: {public_route_table_id}")

# Private Route Table (no NAT or IGW access)
response = ec2.create_route_table(VpcId=vpc_id)
private_route_table_id = response['RouteTable']['RouteTableId']
ec2.associate_route_table(RouteTableId=private_route_table_id, SubnetId=private_subnet_id)

# Tag the Private Route Table with the name
ec2.create_tags(Resources=[private_route_table_id], Tags=[{'Key': 'Name', 'Value': 'aalimsee-private-route-table'}])
print(f"Private Route Table created and associated: {private_route_table_id}")

# Step 5: Create Security Groups
# Public Security Group
response = ec2.create_security_group(GroupName='aalimsee_PublicSG', Description='Public Security Group', VpcId=vpc_id)
public_sg_id = response['GroupId']
ec2.authorize_security_group_ingress(
    GroupId=public_sg_id,
    IpPermissions=[
        {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
        {'IpProtocol': 'tcp', 'FromPort': 443, 'ToPort': 443, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
        {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},  # SSH from your IP
        {'IpProtocol': 'tcp', 'FromPort': 23, 'ToPort': 23, 'IpRanges': [{'CidrIp': '10.0.0.0/16'}]},  # Telnet to private EC2
    ]
)
print(f"Public Security Group created: {public_sg_id}")

# Private Security Group
response = ec2.create_security_group(GroupName='aalimsee_PrivateSG', Description='Private Security Group', VpcId=vpc_id)
private_sg_id = response['GroupId']
ec2.authorize_security_group_ingress(
    GroupId=private_sg_id,
    IpPermissions=[
        # Allow Telnet (port 23) from Public Security Group
        {'IpProtocol': 'tcp', 'FromPort': 23, 'ToPort': 23, 'UserIdGroupPairs': [{'GroupId': public_sg_id}]},
        # Allow SSH (port 22) from Public Security Group
        {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'UserIdGroupPairs': [{'GroupId': public_sg_id}]},
    ]
)
print(f"Private Security Group created and updated for SSH and Telnet: {private_sg_id}")

# Step 6: Launch EC2 Instances
# Public EC2 Instance (aalimsee-public-01)
response = ec2.run_instances(
    ImageId="ami-01816d07b1128cd2d",  # Replace with your AMI ID
    InstanceType='t2.micro',
    MaxCount=1,
    MinCount=1,
    KeyName='aalimsee-keypair',  # Updated key pair name
    NetworkInterfaces=[{
        'SubnetId': public_subnet_id,
        'DeviceIndex': 0,
        'AssociatePublicIpAddress': True,
        'Groups': [public_sg_id]
    }]
)
public_instance_id = response['Instances'][0]['InstanceId']

# Tag the public EC2 instance with the name 'aalimsee-public-01'
ec2.create_tags(Resources=[public_instance_id], Tags=[{'Key': 'Name', 'Value': 'aalimsee-public-01'}])
print(f"Public EC2 Instance launched: {public_instance_id} with name 'aalimsee-public-01'")

# Private EC2 Instance (aalimsee-private-01)
response = ec2.run_instances(
    ImageId="ami-01816d07b1128cd2d",  # Replace with your AMI ID
    InstanceType='t2.micro',
    MaxCount=1,
    MinCount=1,
    KeyName='aalimsee-keypair',  # Updated key pair name
    NetworkInterfaces=[{
        'SubnetId': private_subnet_id,
        'DeviceIndex': 0,
        'Groups': [private_sg_id]
    }]
)
private_instance_id = response['Instances'][0]['InstanceId']

# Tag the private EC2 instance with the name 'aalimsee-private-01'
ec2.create_tags(Resources=[private_instance_id], Tags=[{'Key': 'Name', 'Value': 'aalimsee-private-01'}])
print(f"Private EC2 Instance launched: {private_instance_id} with name 'aalimsee-private-01'")
