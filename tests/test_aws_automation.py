"""
Tests for AWSAutomation
"""

from cloud_automation.aws_automation import AWSAutomation


class TestAWSAutomation:
    """Test cases for AWSAutomation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.automation = AWSAutomation(simulation_mode=True)

    def test_initialization(self):
        """Test that AWSAutomation initializes properly."""
        assert self.automation.simulation_mode is True
        assert self.automation.ec2 is not None
        assert self.automation.s3 is not None
        assert self.automation.rds is not None
        assert self.automation.lambda_mgr is not None

    def test_provision_infrastructure(self):
        """Test provisioning complete infrastructure."""
        config = {
            "ec2": [
                {"instance_type": "t2.micro", "tags": {"Name": "test-instance"}}
            ],
            "s3": [
                {"bucket_name": "test-bucket"}
            ],
            "rds": [
                {"db_instance_identifier": "test-db", "engine": "mysql"}
            ],
            "lambda": [
                {"function_name": "test-function", "runtime": "python3.9"}
            ]
        }
        
        results = self.automation.provision_infrastructure(config)
        
        assert len(results["ec2_instances"]) == 1
        assert len(results["s3_buckets"]) == 1
        assert len(results["rds_instances"]) == 1
        assert len(results["lambda_functions"]) == 1
        
        assert results["s3_buckets"][0] == "test-bucket"
        assert results["rds_instances"][0] == "test-db"
        assert results["lambda_functions"][0] == "test-function"

    def test_provision_empty_infrastructure(self):
        """Test provisioning with empty config."""
        results = self.automation.provision_infrastructure({})
        
        assert len(results["ec2_instances"]) == 0
        assert len(results["s3_buckets"]) == 0
        assert len(results["rds_instances"]) == 0
        assert len(results["lambda_functions"]) == 0

    def test_destroy_infrastructure(self):
        """Test destroying infrastructure."""
        # First provision some resources
        config = {
            "ec2": [{"instance_type": "t2.micro"}],
            "s3": [{"bucket_name": "test-bucket"}],
        }
        
        resource_ids = self.automation.provision_infrastructure(config)
        
        # Now destroy them
        results = self.automation.destroy_infrastructure(resource_ids)
        
        assert results["ec2_terminated"] == 1
        assert results["s3_deleted"] == 1

    def test_get_infrastructure_status(self):
        """Test getting infrastructure status."""
        # Provision some resources
        config = {
            "ec2": [{"instance_type": "t2.micro"}],
            "s3": [{"bucket_name": "test-bucket"}],
        }
        
        self.automation.provision_infrastructure(config)
        
        # Get status
        status = self.automation.get_infrastructure_status()
        
        assert "ec2_instances" in status
        assert "s3_buckets" in status
        assert "rds_instances" in status
        assert "lambda_functions" in status
        
        assert len(status["ec2_instances"]) == 1
        assert len(status["s3_buckets"]) == 1

    def test_provision_multiple_resources_same_type(self):
        """Test provisioning multiple resources of the same type."""
        config = {
            "ec2": [
                {"instance_type": "t2.micro"},
                {"instance_type": "t2.small"},
                {"instance_type": "t3.medium"}
            ]
        }
        
        results = self.automation.provision_infrastructure(config)
        
        assert len(results["ec2_instances"]) == 3
        
        # Verify all instances were created
        instances = self.automation.ec2.list_instances()
        assert len(instances) == 3
