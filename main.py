#!/usr/bin/env python3
"""
Main script for demonstrating AWS cloud automation simulation.
"""

import argparse
import logging
import json
import sys
from pathlib import Path

from cloud_automation import AWSAutomation


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def provision_example_infrastructure(automation: AWSAutomation):
    """Provision example infrastructure."""
    print("\n" + "="*60)
    print("Provisioning Example Infrastructure")
    print("="*60 + "\n")
    
    infrastructure_config = {
        "ec2": [
            {
                "instance_type": "t2.micro",
                "ami_id": "ami-0c55b159cbfafe1f0",
                "tags": {"Name": "web-server-1", "Environment": "production"}
            },
            {
                "instance_type": "t2.small",
                "ami_id": "ami-0c55b159cbfafe1f0",
                "tags": {"Name": "app-server-1", "Environment": "production"}
            }
        ],
        "s3": [
            {
                "bucket_name": "my-app-data-bucket",
                "region": "us-east-1",
                "versioning": True,
                "tags": {"Project": "MyApp", "Environment": "production"}
            },
            {
                "bucket_name": "my-app-logs-bucket",
                "region": "us-east-1",
                "tags": {"Project": "MyApp", "Type": "Logs"}
            }
        ],
        "rds": [
            {
                "db_instance_identifier": "myapp-db",
                "engine": "mysql",
                "instance_class": "db.t3.micro",
                "allocated_storage": 20,
                "multi_az": True,
                "tags": {"Name": "MyApp Database", "Environment": "production"}
            }
        ],
        "lambda": [
            {
                "function_name": "data-processor",
                "runtime": "python3.9",
                "handler": "index.handler",
                "memory_size": 256,
                "timeout": 30,
                "tags": {"Project": "MyApp", "Function": "DataProcessor"}
            }
        ]
    }
    
    results = automation.provision_infrastructure(infrastructure_config)
    
    print("\n✅ Infrastructure Provisioned Successfully!\n")
    print("Resource Summary:")
    print(f"  EC2 Instances: {len(results['ec2_instances'])}")
    for instance_id in results['ec2_instances']:
        print(f"    - {instance_id}")
    
    print(f"\n  S3 Buckets: {len(results['s3_buckets'])}")
    for bucket in results['s3_buckets']:
        print(f"    - {bucket}")
    
    print(f"\n  RDS Instances: {len(results['rds_instances'])}")
    for db_instance in results['rds_instances']:
        print(f"    - {db_instance}")
    
    print(f"\n  Lambda Functions: {len(results['lambda_functions'])}")
    for function in results['lambda_functions']:
        print(f"    - {function}")
    
    return results


def show_infrastructure_status(automation: AWSAutomation):
    """Display current infrastructure status."""
    print("\n" + "="*60)
    print("Current Infrastructure Status")
    print("="*60 + "\n")
    
    status = automation.get_infrastructure_status()
    
    print("EC2 Instances:")
    if status['ec2_instances']:
        for instance in status['ec2_instances']:
            print(f"  {instance['instance_id']}: {instance['state']} ({instance['instance_type']})")
            print(f"    Public IP: {instance['public_ip']}")
    else:
        print("  No instances found")
    
    print("\nS3 Buckets:")
    if status['s3_buckets']:
        for bucket in status['s3_buckets']:
            print(f"  {bucket['bucket_name']}: {bucket['region']}")
            print(f"    Objects: {len(bucket['objects'])}, Size: {bucket['size_bytes']} bytes")
    else:
        print("  No buckets found")
    
    print("\nRDS Instances:")
    if status['rds_instances']:
        for db in status['rds_instances']:
            print(f"  {db['db_instance_identifier']}: {db['status']} ({db['engine']})")
            print(f"    Endpoint: {db['endpoint']}")
    else:
        print("  No RDS instances found")
    
    print("\nLambda Functions:")
    if status['lambda_functions']:
        for func in status['lambda_functions']:
            print(f"  {func['function_name']}: {func['state']} ({func['runtime']})")
            print(f"    Memory: {func['memory_size']}MB, Invocations: {func['invocations']}")
    else:
        print("  No Lambda functions found")


def demonstrate_operations(automation: AWSAutomation):
    """Demonstrate various operations."""
    print("\n" + "="*60)
    print("Demonstrating Additional Operations")
    print("="*60 + "\n")
    
    # EC2 operations
    print("Creating additional EC2 instance...")
    instance_id = automation.ec2.create_instance(
        instance_type="t3.medium",
        tags={"Name": "demo-instance"}
    )
    print(f"  Created: {instance_id}")
    
    print(f"\nStopping instance {instance_id}...")
    automation.ec2.stop_instance(instance_id)
    print("  Instance stopped")
    
    # S3 operations
    print("\nCreating S3 bucket and uploading objects...")
    bucket_name = "demo-bucket-12345"
    automation.s3.create_bucket(bucket_name=bucket_name)
    automation.s3.put_object(bucket_name, "file1.txt", "Hello World!")
    automation.s3.put_object(bucket_name, "data/file2.json", '{"key": "value"}')
    print(f"  Bucket: {bucket_name}")
    print(f"  Objects: {len(automation.s3.list_objects(bucket_name))}")
    
    # Lambda operations
    print("\nInvoking Lambda function...")
    result = automation.lambda_mgr.invoke_function(
        "data-processor",
        payload={"data": "test"}
    )
    print(f"  Status: {result.get('status_code')}")
    print(f"  Result: {result.get('payload', {}).get('message')}")


def cleanup_infrastructure(automation: AWSAutomation, resource_ids):
    """Clean up all provisioned resources."""
    print("\n" + "="*60)
    print("Cleaning Up Infrastructure")
    print("="*60 + "\n")
    
    results = automation.destroy_infrastructure(resource_ids)
    
    print("Cleanup Summary:")
    print(f"  EC2 instances terminated: {results['ec2_terminated']}")
    print(f"  S3 buckets deleted: {results['s3_deleted']}")
    print(f"  RDS instances deleted: {results['rds_deleted']}")
    print(f"  Lambda functions deleted: {results['lambda_deleted']}")
    
    print("\n✅ Cleanup completed!\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="AWS Cloud Automation Simulation Script"
    )
    parser.add_argument(
        "--config",
        help="Path to configuration YAML file",
        type=str
    )
    parser.add_argument(
        "-v", "--verbose",
        help="Enable verbose logging",
        action="store_true"
    )
    parser.add_argument(
        "--skip-cleanup",
        help="Skip cleanup of resources at the end",
        action="store_true"
    )
    parser.add_argument(
        "--demo",
        help="Run full demonstration",
        action="store_true",
        default=True
    )
    
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    
    print("\n" + "="*60)
    print("AWS Cloud Automation Simulation")
    print("="*60)
    print("\nThis script simulates AWS resource automation.")
    print("No actual AWS resources will be created.\n")
    
    # Initialize automation
    automation = AWSAutomation(
        config_file=args.config,
        simulation_mode=True
    )
    
    if args.demo:
        # Provision infrastructure
        resource_ids = provision_example_infrastructure(automation)
        
        # Show status
        show_infrastructure_status(automation)
        
        # Demonstrate operations
        demonstrate_operations(automation)
        
        # Show final status
        show_infrastructure_status(automation)
        
        # Cleanup
        if not args.skip_cleanup:
            cleanup_infrastructure(automation, resource_ids)
        else:
            print("\n⚠️  Cleanup skipped. Resources remain in simulated state.\n")
    
    print("="*60)
    print("Simulation Complete")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
