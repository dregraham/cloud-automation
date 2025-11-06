"""
EC2 Instance Manager
Simulates EC2 instance management operations.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import random
import string


logger = logging.getLogger(__name__)


class EC2Manager:
    """Manages EC2 instance operations (simulation)."""

    def __init__(self, simulation_mode: bool = True):
        """
        Initialize EC2 Manager.

        Args:
            simulation_mode: If True, simulates operations without real AWS calls
        """
        self.simulation_mode = simulation_mode
        self.instances: Dict[str, Dict[str, Any]] = {}
        logger.info("EC2Manager initialized")

    def _generate_instance_id(self) -> str:
        """Generate a simulated EC2 instance ID."""
        random_part = ''.join(random.choices(string.hexdigits.lower(), k=17))
        return f"i-{random_part}"

    def create_instance(
        self,
        instance_type: str = "t2.micro",
        ami_id: str = "ami-default",
        key_name: Optional[str] = None,
        security_groups: Optional[List[str]] = None,
        tags: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> str:
        """
        Create (simulate) an EC2 instance.

        Args:
            instance_type: EC2 instance type (e.g., t2.micro, t3.medium)
            ami_id: Amazon Machine Image ID
            key_name: SSH key pair name
            security_groups: List of security group names/IDs
            tags: Dictionary of tags to apply to the instance
            **kwargs: Additional parameters

        Returns:
            Instance ID of the created instance
        """
        instance_id = self._generate_instance_id()
        
        instance_info = {
            "instance_id": instance_id,
            "instance_type": instance_type,
            "ami_id": ami_id,
            "key_name": key_name,
            "security_groups": security_groups or [],
            "tags": tags or {},
            "state": "running",
            "launch_time": datetime.now(timezone.utc).isoformat(),
            "public_ip": f"54.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
            "private_ip": f"10.0.{random.randint(0,255)}.{random.randint(0,255)}"
        }
        
        self.instances[instance_id] = instance_info
        logger.info(f"Created EC2 instance {instance_id} (type: {instance_type})")
        
        return instance_id

    def terminate_instance(self, instance_id: str) -> bool:
        """
        Terminate (simulate) an EC2 instance.

        Args:
            instance_id: ID of the instance to terminate

        Returns:
            True if successful, False otherwise
        """
        if instance_id in self.instances:
            self.instances[instance_id]["state"] = "terminated"
            logger.info(f"Terminated EC2 instance {instance_id}")
            return True
        else:
            logger.warning(f"Instance {instance_id} not found")
            return False

    def stop_instance(self, instance_id: str) -> bool:
        """
        Stop (simulate) an EC2 instance.

        Args:
            instance_id: ID of the instance to stop

        Returns:
            True if successful, False otherwise
        """
        if instance_id in self.instances:
            if self.instances[instance_id]["state"] == "running":
                self.instances[instance_id]["state"] = "stopped"
                logger.info(f"Stopped EC2 instance {instance_id}")
                return True
        logger.warning(f"Cannot stop instance {instance_id}")
        return False

    def start_instance(self, instance_id: str) -> bool:
        """
        Start (simulate) an EC2 instance.

        Args:
            instance_id: ID of the instance to start

        Returns:
            True if successful, False otherwise
        """
        if instance_id in self.instances:
            if self.instances[instance_id]["state"] == "stopped":
                self.instances[instance_id]["state"] = "running"
                logger.info(f"Started EC2 instance {instance_id}")
                return True
        logger.warning(f"Cannot start instance {instance_id}")
        return False

    def get_instance_info(self, instance_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about an instance.

        Args:
            instance_id: ID of the instance

        Returns:
            Dictionary with instance information or None
        """
        return self.instances.get(instance_id)

    def list_instances(self, state: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all instances, optionally filtered by state.

        Args:
            state: Filter by instance state (running, stopped, terminated)

        Returns:
            List of instance information dictionaries
        """
        if state:
            return [info for info in self.instances.values() if info["state"] == state]
        return list(self.instances.values())

    def tag_instance(self, instance_id: str, tags: Dict[str, str]) -> bool:
        """
        Add tags to an instance.

        Args:
            instance_id: ID of the instance
            tags: Dictionary of tags to add

        Returns:
            True if successful, False otherwise
        """
        if instance_id in self.instances:
            self.instances[instance_id]["tags"].update(tags)
            logger.info(f"Tagged instance {instance_id} with {tags}")
            return True
        return False
