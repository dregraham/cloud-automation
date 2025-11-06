"""
Cloud Automation Package
A Python library for simulating AWS cloud resource automation.
"""

__version__ = "0.1.0"
__author__ = "Cloud Automation Team"

from .aws_automation import AWSAutomation
from .ec2_manager import EC2Manager
from .s3_manager import S3Manager
from .rds_manager import RDSManager
from .lambda_manager import LambdaManager

__all__ = [
    "AWSAutomation",
    "EC2Manager",
    "S3Manager",
    "RDSManager",
    "LambdaManager",
]
