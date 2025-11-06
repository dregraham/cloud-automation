"""
Tests for EC2Manager
"""

import pytest
from cloud_automation.ec2_manager import EC2Manager


class TestEC2Manager:
    """Test cases for EC2Manager."""

    def setup_method(self):
        """Set up test fixtures."""
        self.ec2 = EC2Manager(simulation_mode=True)

    def test_create_instance(self):
        """Test creating an EC2 instance."""
        instance_id = self.ec2.create_instance(
            instance_type="t2.micro",
            ami_id="ami-12345",
            tags={"Name": "test-instance"}
        )
        
        assert instance_id is not None
        assert instance_id.startswith("i-")
        
        # Verify instance was added to instances dict
        assert instance_id in self.ec2.instances
        
        # Verify instance details
        instance = self.ec2.instances[instance_id]
        assert instance["instance_type"] == "t2.micro"
        assert instance["ami_id"] == "ami-12345"
        assert instance["state"] == "running"
        assert instance["tags"]["Name"] == "test-instance"

    def test_terminate_instance(self):
        """Test terminating an EC2 instance."""
        instance_id = self.ec2.create_instance()
        
        result = self.ec2.terminate_instance(instance_id)
        assert result is True
        
        # Verify instance state changed
        instance = self.ec2.instances[instance_id]
        assert instance["state"] == "terminated"

    def test_terminate_nonexistent_instance(self):
        """Test terminating a non-existent instance."""
        result = self.ec2.terminate_instance("i-nonexistent")
        assert result is False

    def test_stop_instance(self):
        """Test stopping an EC2 instance."""
        instance_id = self.ec2.create_instance()
        
        result = self.ec2.stop_instance(instance_id)
        assert result is True
        
        instance = self.ec2.instances[instance_id]
        assert instance["state"] == "stopped"

    def test_start_instance(self):
        """Test starting a stopped EC2 instance."""
        instance_id = self.ec2.create_instance()
        self.ec2.stop_instance(instance_id)
        
        result = self.ec2.start_instance(instance_id)
        assert result is True
        
        instance = self.ec2.instances[instance_id]
        assert instance["state"] == "running"

    def test_get_instance_info(self):
        """Test getting instance information."""
        instance_id = self.ec2.create_instance(
            instance_type="t3.medium",
            tags={"Name": "test"}
        )
        
        info = self.ec2.get_instance_info(instance_id)
        assert info is not None
        assert info["instance_id"] == instance_id
        assert info["instance_type"] == "t3.medium"

    def test_get_nonexistent_instance_info(self):
        """Test getting info for non-existent instance."""
        info = self.ec2.get_instance_info("i-nonexistent")
        assert info is None

    def test_list_instances(self):
        """Test listing all instances."""
        id1 = self.ec2.create_instance()
        id2 = self.ec2.create_instance()
        
        instances = self.ec2.list_instances()
        assert len(instances) == 2
        
        instance_ids = [inst["instance_id"] for inst in instances]
        assert id1 in instance_ids
        assert id2 in instance_ids

    def test_list_instances_by_state(self):
        """Test listing instances filtered by state."""
        id1 = self.ec2.create_instance()
        id2 = self.ec2.create_instance()
        self.ec2.stop_instance(id2)
        
        running = self.ec2.list_instances(state="running")
        assert len(running) == 1
        assert running[0]["instance_id"] == id1
        
        stopped = self.ec2.list_instances(state="stopped")
        assert len(stopped) == 1
        assert stopped[0]["instance_id"] == id2

    def test_tag_instance(self):
        """Test tagging an instance."""
        instance_id = self.ec2.create_instance(tags={"Name": "original"})
        
        result = self.ec2.tag_instance(instance_id, {"Environment": "test", "Owner": "admin"})
        assert result is True
        
        instance = self.ec2.instances[instance_id]
        assert instance["tags"]["Name"] == "original"
        assert instance["tags"]["Environment"] == "test"
        assert instance["tags"]["Owner"] == "admin"

    def test_instance_has_ip_addresses(self):
        """Test that created instances have IP addresses."""
        instance_id = self.ec2.create_instance()
        instance = self.ec2.instances[instance_id]
        
        assert "public_ip" in instance
        assert "private_ip" in instance
        assert instance["public_ip"].startswith("54.")
        assert instance["private_ip"].startswith("10.0.")
