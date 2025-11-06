"""
Lambda Function Manager
Simulates AWS Lambda function management operations.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import random
import string


logger = logging.getLogger(__name__)


class LambdaManager:
    """Manages Lambda function operations (simulation)."""

    def __init__(self, simulation_mode: bool = True):
        """
        Initialize Lambda Manager.

        Args:
            simulation_mode: If True, simulates operations without real AWS calls
        """
        self.simulation_mode = simulation_mode
        self.functions: Dict[str, Dict[str, Any]] = {}
        logger.info("LambdaManager initialized")

    def create_function(
        self,
        function_name: str,
        runtime: str = "python3.9",
        handler: str = "index.handler",
        role: str = "arn:aws:iam::123456789012:role/lambda-role",
        code: Optional[str] = None,
        description: str = "",
        timeout: int = 3,
        memory_size: int = 128,
        environment: Optional[Dict[str, str]] = None,
        tags: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> str:
        """
        Create (simulate) a Lambda function.

        Args:
            function_name: Name of the function
            runtime: Runtime environment (python3.9, nodejs18.x, etc.)
            handler: Function handler
            role: IAM role ARN
            code: Function code (simulated)
            description: Function description
            timeout: Timeout in seconds
            memory_size: Memory allocated in MB
            environment: Environment variables
            tags: Dictionary of tags
            **kwargs: Additional parameters

        Returns:
            Function name
        """
        if function_name in self.functions:
            logger.warning(f"Lambda function {function_name} already exists")
            return function_name

        function_arn = (
            f"arn:aws:lambda:us-east-1:123456789012:function:{function_name}"
        )
        
        function_info = {
            "function_name": function_name,
            "function_arn": function_arn,
            "runtime": runtime,
            "handler": handler,
            "role": role,
            "description": description,
            "timeout": timeout,
            "memory_size": memory_size,
            "environment": environment or {},
            "tags": tags or {},
            "code_size": len(code) if code else 1024,
            "code_sha256": f"sha256-{''.join(random.choices(string.hexdigits, k=64))}",
            "last_modified": datetime.now(timezone.utc).isoformat(),
            "version": "$LATEST",
            "state": "Active",
            "invocations": 0
        }
        
        self.functions[function_name] = function_info
        logger.info(
            f"Created Lambda function {function_name} "
            f"(runtime: {runtime}, memory: {memory_size}MB)"
        )
        
        return function_name

    def delete_function(self, function_name: str) -> bool:
        """
        Delete (simulate) a Lambda function.

        Args:
            function_name: Name of the function to delete

        Returns:
            True if successful, False otherwise
        """
        if function_name not in self.functions:
            logger.warning(f"Lambda function {function_name} not found")
            return False

        del self.functions[function_name]
        logger.info(f"Deleted Lambda function {function_name}")
        return True

    def invoke_function(
        self,
        function_name: str,
        payload: Optional[Dict[str, Any]] = None,
        invocation_type: str = "RequestResponse"
    ) -> Dict[str, Any]:
        """
        Invoke (simulate) a Lambda function.

        Args:
            function_name: Name of the function to invoke
            payload: Event data to pass to the function
            invocation_type: Type of invocation (RequestResponse, Event, DryRun)

        Returns:
            Dictionary with invocation results
        """
        if function_name not in self.functions:
            logger.warning(f"Lambda function {function_name} not found")
            return {"error": "Function not found"}

        function = self.functions[function_name]
        function["invocations"] += 1
        
        result = {
            "status_code": 200,
            "executed_version": "$LATEST",
            "payload": {
                "message": "Function executed successfully (simulated)",
                "input": payload or {}
            }
        }
        
        logger.info(f"Invoked Lambda function {function_name}")
        return result

    def update_function_code(
        self,
        function_name: str,
        code: Optional[str] = None,
        **kwargs
    ) -> bool:
        """
        Update (simulate) Lambda function code.

        Args:
            function_name: Name of the function
            code: New function code
            **kwargs: Additional parameters

        Returns:
            True if successful, False otherwise
        """
        if function_name not in self.functions:
            logger.warning(f"Lambda function {function_name} not found")
            return False

        function = self.functions[function_name]
        function["code_size"] = len(code) if code else function["code_size"]
        function["code_sha256"] = f"sha256-{''.join(random.choices(string.hexdigits, k=64))}"
        function["last_modified"] = datetime.now(timezone.utc).isoformat()
        
        logger.info(f"Updated code for Lambda function {function_name}")
        return True

    def update_function_configuration(
        self,
        function_name: str,
        timeout: Optional[int] = None,
        memory_size: Optional[int] = None,
        environment: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> bool:
        """
        Update (simulate) Lambda function configuration.

        Args:
            function_name: Name of the function
            timeout: New timeout in seconds
            memory_size: New memory size in MB
            environment: New environment variables
            **kwargs: Additional parameters

        Returns:
            True if successful, False otherwise
        """
        if function_name not in self.functions:
            logger.warning(f"Lambda function {function_name} not found")
            return False

        function = self.functions[function_name]
        
        if timeout is not None:
            function["timeout"] = timeout
        if memory_size is not None:
            function["memory_size"] = memory_size
        if environment is not None:
            function["environment"] = environment
        
        function["last_modified"] = datetime.now(timezone.utc).isoformat()
        
        logger.info(f"Updated configuration for Lambda function {function_name}")
        return True

    def get_function_info(self, function_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a Lambda function.

        Args:
            function_name: Name of the function

        Returns:
            Dictionary with function information or None
        """
        return self.functions.get(function_name)

    def list_functions(self) -> List[Dict[str, Any]]:
        """
        List all Lambda functions.

        Returns:
            List of function information dictionaries
        """
        return list(self.functions.values())

    def add_permission(
        self,
        function_name: str,
        statement_id: str,
        action: str,
        principal: str,
        **kwargs
    ) -> bool:
        """
        Add (simulate) a permission to a Lambda function.

        Args:
            function_name: Name of the function
            statement_id: Unique statement identifier
            action: Action to allow (e.g., lambda:InvokeFunction)
            principal: Principal to grant permission
            **kwargs: Additional parameters

        Returns:
            True if successful, False otherwise
        """
        if function_name not in self.functions:
            logger.warning(f"Lambda function {function_name} not found")
            return False

        logger.info(
            f"Added permission to Lambda function {function_name}: "
            f"{action} for {principal}"
        )
        return True
