"""
AWS Provisioning Demo (Mock)
Author: Dre Graham
Purpose: Demonstrate how to provision AWS resources with Python and boto3-style logic
"""

import json
from datetime import datetime
from mock_aws import MockAWS

def main():
    print("Starting AWS Provisioning Simulation...\n")

    # Load resource definitions
    with open("resources.json", "r") as f:
        resources = json.load(f)

    aws = MockAWS()

    for res in resources["Resources"]:
        if res["Type"] == "EC2":
            aws.create_ec2(res)
        elif res["Type"] == "S3":
            aws.create_s3(res)
        elif res["Type"] == "IAM":
            aws.create_iam(res)
        else:
            print(f"⚠️ Unknown resource type: {res['Type']}")

    print("\n✅ Provisioning complete!")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
