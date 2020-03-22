#!/usr/bin/python3.6

import paramiko
from slackbot_v2 import config


def add_user(company, password):
    key = paramiko.RSAKey.from_private_key_file(config.EC2_KEY)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
        client.connect(hostname=config.EC2_HOSTNAME, username=config.EC2_USERNAME, pkey=key)
        # Execute a command(cmd) after connecting/ssh to an instance
        stdin, stdout, stderr = client.exec_command(f"add_user {company} {password}")
        client.close()
    except:
        print("Something wrong")


def lambda_handler(event, lambda_context):
    company = event['company']
    password = event['password']
    add_user(company, password)

