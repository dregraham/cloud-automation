"""
Tests for S3Manager
"""

from cloud_automation.s3_manager import S3Manager


class TestS3Manager:
    """Test cases for S3Manager."""

    def setup_method(self):
        """Set up test fixtures."""
        self.s3 = S3Manager(simulation_mode=True)

    def test_create_bucket(self):
        """Test creating an S3 bucket."""
        bucket_name = self.s3.create_bucket(
            bucket_name="test-bucket",
            region="us-east-1",
            tags={"Project": "test"}
        )
        
        assert bucket_name == "test-bucket"
        assert "test-bucket" in self.s3.buckets
        
        bucket = self.s3.buckets[bucket_name]
        assert bucket["region"] == "us-east-1"
        assert bucket["tags"]["Project"] == "test"
        assert bucket["versioning"] is False

    def test_create_existing_bucket(self):
        """Test creating a bucket that already exists."""
        self.s3.create_bucket(bucket_name="test-bucket")
        result = self.s3.create_bucket(bucket_name="test-bucket")
        
        assert result == "test-bucket"

    def test_delete_bucket(self):
        """Test deleting an empty bucket."""
        self.s3.create_bucket(bucket_name="test-bucket")
        
        result = self.s3.delete_bucket("test-bucket")
        assert result is True
        assert "test-bucket" not in self.s3.buckets

    def test_delete_nonempty_bucket_without_force(self):
        """Test deleting a non-empty bucket without force flag."""
        self.s3.create_bucket(bucket_name="test-bucket")
        self.s3.put_object("test-bucket", "file.txt", "content")
        
        result = self.s3.delete_bucket("test-bucket", force=False)
        assert result is False
        assert "test-bucket" in self.s3.buckets

    def test_delete_nonempty_bucket_with_force(self):
        """Test deleting a non-empty bucket with force flag."""
        self.s3.create_bucket(bucket_name="test-bucket")
        self.s3.put_object("test-bucket", "file.txt", "content")
        
        result = self.s3.delete_bucket("test-bucket", force=True)
        assert result is True
        assert "test-bucket" not in self.s3.buckets

    def test_put_object(self):
        """Test putting an object into a bucket."""
        self.s3.create_bucket(bucket_name="test-bucket")
        
        result = self.s3.put_object("test-bucket", "file.txt", "Hello World")
        assert result is True
        
        bucket = self.s3.buckets["test-bucket"]
        assert len(bucket["objects"]) == 1
        assert bucket["objects"][0]["key"] == "file.txt"
        assert bucket["objects"][0]["size"] == len("Hello World")

    def test_put_object_overwrites_existing(self):
        """Test that putting an object overwrites existing one."""
        self.s3.create_bucket(bucket_name="test-bucket")
        self.s3.put_object("test-bucket", "file.txt", "Hello")
        self.s3.put_object("test-bucket", "file.txt", "Hello World")
        
        bucket = self.s3.buckets["test-bucket"]
        assert len(bucket["objects"]) == 1
        assert bucket["objects"][0]["size"] == len("Hello World")

    def test_delete_object(self):
        """Test deleting an object from a bucket."""
        self.s3.create_bucket(bucket_name="test-bucket")
        self.s3.put_object("test-bucket", "file.txt", "content")
        
        result = self.s3.delete_object("test-bucket", "file.txt")
        assert result is True
        
        bucket = self.s3.buckets["test-bucket"]
        assert len(bucket["objects"]) == 0

    def test_list_buckets(self):
        """Test listing all buckets."""
        self.s3.create_bucket(bucket_name="bucket1")
        self.s3.create_bucket(bucket_name="bucket2")
        
        buckets = self.s3.list_buckets()
        assert len(buckets) == 2
        
        bucket_names = [b["bucket_name"] for b in buckets]
        assert "bucket1" in bucket_names
        assert "bucket2" in bucket_names

    def test_list_objects(self):
        """Test listing objects in a bucket."""
        self.s3.create_bucket(bucket_name="test-bucket")
        self.s3.put_object("test-bucket", "file1.txt", "content1")
        self.s3.put_object("test-bucket", "file2.txt", "content2")
        
        objects = self.s3.list_objects("test-bucket")
        assert len(objects) == 2

    def test_list_objects_with_prefix(self):
        """Test listing objects with a prefix filter."""
        self.s3.create_bucket(bucket_name="test-bucket")
        self.s3.put_object("test-bucket", "data/file1.txt", "content1")
        self.s3.put_object("test-bucket", "data/file2.txt", "content2")
        self.s3.put_object("test-bucket", "logs/file3.txt", "content3")
        
        objects = self.s3.list_objects("test-bucket", prefix="data/")
        assert len(objects) == 2
        
        for obj in objects:
            assert obj["key"].startswith("data/")

    def test_get_bucket_info(self):
        """Test getting bucket information."""
        self.s3.create_bucket(
            bucket_name="test-bucket",
            region="us-west-2",
            versioning=True
        )
        
        info = self.s3.get_bucket_info("test-bucket")
        assert info is not None
        assert info["bucket_name"] == "test-bucket"
        assert info["region"] == "us-west-2"
        assert info["versioning"] is True

    def test_enable_versioning(self):
        """Test enabling versioning on a bucket."""
        self.s3.create_bucket(bucket_name="test-bucket", versioning=False)
        
        result = self.s3.enable_versioning("test-bucket")
        assert result is True
        
        bucket = self.s3.buckets["test-bucket"]
        assert bucket["versioning"] is True
