#!/usr/bin/python3.6

import boto3
import botocore
import paramiko
import string
import secrets
import subprocess

def add_user(company, password):
    key = paramiko.RSAKey.from_private_key_file("sftpdServer.pem")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # alphabet = string.ascii_letters + string.digits
    # password = ''.join(secrets.choice(alphabet) for i in range(8))
#    company = lambda_context.company
    # Connect/ssh to an instance
    try:
        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
        client.connect(hostname="ec2-34-192-3-121.compute-1.amazonaws.com", username="ubuntu", pkey=key)
        # Execute a command(cmd) after connecting/ssh to an instance
        stdin, stdout, stderr = client.exec_command(f"add_user {company} {password}")
#        print (password)

        # close the client connection once the job is done
        client.close()
    except:
        print ("Something wrong")

def lambda_handler(event, lambda_context):
    company = event['company']
    password = event['password']
    add_user(company, password)
