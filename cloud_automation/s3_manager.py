"""
S3 Bucket Manager
Simulates S3 bucket management operations.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import random


logger = logging.getLogger(__name__)


class S3Manager:
    """Manages S3 bucket operations (simulation)."""

    def __init__(self, simulation_mode: bool = True):
        """
        Initialize S3 Manager.

        Args:
            simulation_mode: If True, simulates operations without real AWS calls
        """
        self.simulation_mode = simulation_mode
        self.buckets: Dict[str, Dict[str, Any]] = {}
        logger.info("S3Manager initialized")

    def create_bucket(
        self,
        bucket_name: str,
        region: str = "us-east-1",
        acl: str = "private",
        versioning: bool = False,
        encryption: bool = True,
        tags: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> str:
        """
        Create (simulate) an S3 bucket.

        Args:
            bucket_name: Name of the bucket to create
            region: AWS region for the bucket
            acl: Access control list (private, public-read, etc.)
            versioning: Enable versioning
            encryption: Enable encryption
            tags: Dictionary of tags to apply to the bucket
            **kwargs: Additional parameters

        Returns:
            Bucket name
        """
        if bucket_name in self.buckets:
            logger.warning(f"Bucket {bucket_name} already exists")
            return bucket_name

        bucket_info = {
            "bucket_name": bucket_name,
            "region": region,
            "acl": acl,
            "versioning": versioning,
            "encryption": encryption,
            "tags": tags or {},
            "creation_date": datetime.now(timezone.utc).isoformat(),
            "objects": [],
            "size_bytes": 0
        }
        
        self.buckets[bucket_name] = bucket_info
        logger.info(f"Created S3 bucket {bucket_name} in region {region}")
        
        return bucket_name

    def delete_bucket(self, bucket_name: str, force: bool = False) -> bool:
        """
        Delete (simulate) an S3 bucket.

        Args:
            bucket_name: Name of the bucket to delete
            force: If True, delete even if bucket contains objects

        Returns:
            True if successful, False otherwise
        """
        if bucket_name not in self.buckets:
            logger.warning(f"Bucket {bucket_name} not found")
            return False

        bucket = self.buckets[bucket_name]
        if bucket["objects"] and not force:
            logger.warning(f"Bucket {bucket_name} is not empty. Use force=True to delete.")
            return False

        del self.buckets[bucket_name]
        logger.info(f"Deleted S3 bucket {bucket_name}")
        return True

    def put_object(
        self,
        bucket_name: str,
        key: str,
        body: str = "",
        metadata: Optional[Dict[str, str]] = None
    ) -> bool:
        """
        Put (simulate) an object into an S3 bucket.

        Args:
            bucket_name: Name of the bucket
            key: Object key (path/filename)
            body: Object content
            metadata: Object metadata

        Returns:
            True if successful, False otherwise
        """
        if bucket_name not in self.buckets:
            logger.warning(f"Bucket {bucket_name} not found")
            return False

        object_info = {
            "key": key,
            "size": len(body),
            "metadata": metadata or {},
            "last_modified": datetime.now(timezone.utc).isoformat(),
            "etag": f"etag-{random.randint(100000, 999999)}"
        }
        
        bucket = self.buckets[bucket_name]
        
        # Remove existing object with same key
        bucket["objects"] = [obj for obj in bucket["objects"] if obj["key"] != key]
        
        # Add new object
        bucket["objects"].append(object_info)
        bucket["size_bytes"] += object_info["size"]
        
        logger.info(f"Put object {key} to bucket {bucket_name}")
        return True

    def delete_object(self, bucket_name: str, key: str) -> bool:
        """
        Delete (simulate) an object from an S3 bucket.

        Args:
            bucket_name: Name of the bucket
            key: Object key to delete

        Returns:
            True if successful, False otherwise
        """
        if bucket_name not in self.buckets:
            logger.warning(f"Bucket {bucket_name} not found")
            return False

        bucket = self.buckets[bucket_name]
        
        # Find and remove the object
        for obj in bucket["objects"]:
            if obj["key"] == key:
                bucket["size_bytes"] -= obj["size"]
                bucket["objects"].remove(obj)
                logger.info(f"Deleted object {key} from bucket {bucket_name}")
                return True

        logger.warning(f"Object {key} not found in bucket {bucket_name}")
        return False

    def list_buckets(self) -> List[Dict[str, Any]]:
        """
        List all buckets.

        Returns:
            List of bucket information dictionaries
        """
        return list(self.buckets.values())

    def list_objects(self, bucket_name: str, prefix: str = "") -> List[Dict[str, Any]]:
        """
        List objects in a bucket, optionally filtered by prefix.

        Args:
            bucket_name: Name of the bucket
            prefix: Filter objects by prefix

        Returns:
            List of object information dictionaries
        """
        if bucket_name not in self.buckets:
            logger.warning(f"Bucket {bucket_name} not found")
            return []

        objects = self.buckets[bucket_name]["objects"]
        
        if prefix:
            return [obj for obj in objects if obj["key"].startswith(prefix)]
        
        return objects

    def get_bucket_info(self, bucket_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a bucket.

        Args:
            bucket_name: Name of the bucket

        Returns:
            Dictionary with bucket information or None
        """
        return self.buckets.get(bucket_name)

    def enable_versioning(self, bucket_name: str) -> bool:
        """
        Enable versioning for a bucket.

        Args:
            bucket_name: Name of the bucket

        Returns:
            True if successful, False otherwise
        """
        if bucket_name in self.buckets:
            self.buckets[bucket_name]["versioning"] = True
            logger.info(f"Enabled versioning for bucket {bucket_name}")
            return True
        return False
