"""
AWS Automation Module
Main orchestrator for AWS resource automation simulation.
"""

import logging
from typing import Dict, List, Optional, Any
import yaml

from .ec2_manager import EC2Manager
from .s3_manager import S3Manager
from .rds_manager import RDSManager
from .lambda_manager import LambdaManager


logger = logging.getLogger(__name__)


class AWSAutomation:
    """
    Main class for orchestrating AWS resource automation.
    Simulates various AWS operations without actually making API calls to AWS.
    """

    def __init__(self, config_file: Optional[str] = None, simulation_mode: bool = True):
        """
        Initialize AWS Automation.

        Args:
            config_file: Path to YAML configuration file
            simulation_mode: If True, simulates operations without real AWS calls
        """
        self.simulation_mode = simulation_mode
        self.config = self._load_config(config_file) if config_file else {}
        
        # Initialize resource managers
        self.ec2 = EC2Manager(simulation_mode=simulation_mode)
        self.s3 = S3Manager(simulation_mode=simulation_mode)
        self.rds = RDSManager(simulation_mode=simulation_mode)
        self.lambda_mgr = LambdaManager(simulation_mode=simulation_mode)
        
        logger.info(f"AWS Automation initialized (simulation_mode={simulation_mode})")

    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Loaded configuration from {config_file}")
            return config
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
            return {}

    def provision_infrastructure(self, infrastructure_config: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Provision complete infrastructure based on configuration.

        Args:
            infrastructure_config: Dictionary containing infrastructure specifications

        Returns:
            Dictionary with resource IDs for each service
        """
        results = {
            "ec2_instances": [],
            "s3_buckets": [],
            "rds_instances": [],
            "lambda_functions": []
        }

        # Provision EC2 instances
        if "ec2" in infrastructure_config:
            for ec2_config in infrastructure_config["ec2"]:
                instance_id = self.ec2.create_instance(**ec2_config)
                results["ec2_instances"].append(instance_id)
                logger.info(f"Created EC2 instance: {instance_id}")

        # Provision S3 buckets
        if "s3" in infrastructure_config:
            for s3_config in infrastructure_config["s3"]:
                bucket_name = self.s3.create_bucket(**s3_config)
                results["s3_buckets"].append(bucket_name)
                logger.info(f"Created S3 bucket: {bucket_name}")

        # Provision RDS instances
        if "rds" in infrastructure_config:
            for rds_config in infrastructure_config["rds"]:
                db_instance_id = self.rds.create_instance(**rds_config)
                results["rds_instances"].append(db_instance_id)
                logger.info(f"Created RDS instance: {db_instance_id}")

        # Provision Lambda functions
        if "lambda" in infrastructure_config:
            for lambda_config in infrastructure_config["lambda"]:
                function_name = self.lambda_mgr.create_function(**lambda_config)
                results["lambda_functions"].append(function_name)
                logger.info(f"Created Lambda function: {function_name}")

        return results

    def destroy_infrastructure(self, resource_ids: Dict[str, List[str]]) -> Dict[str, int]:
        """
        Destroy infrastructure resources.

        Args:
            resource_ids: Dictionary with resource IDs to destroy

        Returns:
            Dictionary with count of destroyed resources per service
        """
        results = {
            "ec2_terminated": 0,
            "s3_deleted": 0,
            "rds_deleted": 0,
            "lambda_deleted": 0
        }

        # Terminate EC2 instances
        for instance_id in resource_ids.get("ec2_instances", []):
            if self.ec2.terminate_instance(instance_id):
                results["ec2_terminated"] += 1

        # Delete S3 buckets
        for bucket_name in resource_ids.get("s3_buckets", []):
            if self.s3.delete_bucket(bucket_name):
                results["s3_deleted"] += 1

        # Delete RDS instances
        for db_instance_id in resource_ids.get("rds_instances", []):
            if self.rds.delete_instance(db_instance_id):
                results["rds_deleted"] += 1

        # Delete Lambda functions
        for function_name in resource_ids.get("lambda_functions", []):
            if self.lambda_mgr.delete_function(function_name):
                results["lambda_deleted"] += 1

        return results

    def get_infrastructure_status(self) -> Dict[str, Any]:
        """
        Get status of all managed resources.

        Returns:
            Dictionary with status of all resources
        """
        return {
            "ec2_instances": self.ec2.list_instances(),
            "s3_buckets": self.s3.list_buckets(),
            "rds_instances": self.rds.list_instances(),
            "lambda_functions": self.lambda_mgr.list_functions()
        }
