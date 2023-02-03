# This script uses an input function to prompt for VPC ID
# "VPC ID" is then used to filter security groups associated with EC2 instances in the selected VPC
# Outputs saves security_groups.csv
# Requires Python3, pip, and boto3
# @nickopop

import boto3
import csv

vpc_id = input("Enter the VPC ID: ")

ec2 = boto3.client('ec2')

security_groups = ec2.describe_security_groups(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])['SecurityGroups']

with open('security_groups.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Security Group ID', 'Description', 'Inbound Rules', 'EC2 Instances'])
    for security_group in security_groups:
        group_id = security_group['GroupId']
        description = security_group.get('Description', '')
        inbound_rules = []
        for rule in security_group.get('IpPermissions', []):
            inbound_rules.append(f"{rule['IpProtocol']} ({rule.get('FromPort', 'N/A')}-{rule.get('ToPort', 'N/A')})")
        instances = []
        instances_desc = ec2.describe_instances(
            Filters=[
                {
                    'Name': 'instance.group-id',
                    'Values': [group_id]
                },
                {
                    'Name': 'vpc-id',
                    'Values': [vpc_id]
                }
            ]
        )
        for reservation in instances_desc['Reservations']:
            for instance in reservation['Instances']:
                instances.append(instance['InstanceId'])
        writer.writerow([group_id, description, ', '.join(inbound_rules), ', '.join(instances)])