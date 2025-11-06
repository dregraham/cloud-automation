class MockAWS:
    def create_ec2(self, res):
        print(f"🖥️  Launching EC2 instance '{res['Name']}' "
              f"in region {res['Region']} with AMI {res['AMI']}")

    def create_s3(self, res):
        print(f"🪣 Creating S3 bucket '{res['Name']}' "
              f"in region {res['Region']} with encryption={res['Encryption']}")

    def create_iam(self, res):
        print(f"🔐 Creating IAM role '{res['Name']}' with policy {res['Policy']}")
