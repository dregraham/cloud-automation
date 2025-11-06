#!/usr/bin/env python3
"""
Example script demonstrating infrastructure provisioning from configuration.
"""

from cloud_automation import AWSAutomation
import sys


def main():
    """Provision infrastructure from example config."""
    print("=" * 60)
    print("AWS Cloud Automation - Configuration Example")
    print("=" * 60)
    
    # Load config and provision
    automation = AWSAutomation(
        config_file="config/example_config.yaml",
        simulation_mode=True
    )
    
    if not automation.config:
        print("Error: Could not load configuration file")
        sys.exit(1)
    
    print("\nProvisioning infrastructure from config/example_config.yaml...")
    results = automation.provision_infrastructure(automation.config)
    
    print("\n✅ Provisioning Complete!")
    print("\nResources Created:")
    print(f"  EC2 Instances: {len(results['ec2_instances'])}")
    print(f"  S3 Buckets: {len(results['s3_buckets'])}")
    print(f"  RDS Instances: {len(results['rds_instances'])}")
    print(f"  Lambda Functions: {len(results['lambda_functions'])}")
    
    print("\nInfrastructure Details:")
    print("-" * 60)
    
    # Show EC2 details
    for instance in automation.ec2.list_instances():
        print(f"\nEC2 Instance: {instance['instance_id']}")
        print(f"  Type: {instance['instance_type']}")
        print(f"  State: {instance['state']}")
        print(f"  Public IP: {instance['public_ip']}")
        if instance['tags']:
            print(f"  Tags: {instance['tags']}")
    
    # Show S3 details
    for bucket in automation.s3.list_buckets():
        print(f"\nS3 Bucket: {bucket['bucket_name']}")
        print(f"  Region: {bucket['region']}")
        print(f"  Versioning: {bucket['versioning']}")
        if bucket['tags']:
            print(f"  Tags: {bucket['tags']}")
    
    # Show RDS details
    for db in automation.rds.list_instances():
        print(f"\nRDS Instance: {db['db_instance_identifier']}")
        print(f"  Engine: {db['engine']} {db['engine_version']}")
        print(f"  Class: {db['instance_class']}")
        print(f"  Status: {db['status']}")
        print(f"  Endpoint: {db['endpoint']}")
    
    # Show Lambda details
    for func in automation.lambda_mgr.list_functions():
        print(f"\nLambda Function: {func['function_name']}")
        print(f"  Runtime: {func['runtime']}")
        print(f"  Memory: {func['memory_size']}MB")
        print(f"  Timeout: {func['timeout']}s")
    
    print("\n" + "=" * 60)
    print("Note: All resources are simulated. No actual AWS resources created.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
