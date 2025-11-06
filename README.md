# Cloud Automation - AWS Resource Simulation

A Python-based repository that simulates automating cloud resources in AWS. This tool provides a safe environment to learn and experiment with AWS infrastructure automation without incurring actual AWS costs or creating real resources.

## Features

- 🚀 **Simulate AWS Resource Management** - EC2, S3, RDS, and Lambda
- 🎯 **No AWS Costs** - All operations are simulated locally
- 📝 **YAML Configuration Support** - Define infrastructure as code
- 🧪 **Comprehensive Testing** - Full test suite included
- 📊 **Detailed Logging** - Track all operations and state changes
- 🔧 **Easy to Use** - Simple API and CLI interface

## Supported AWS Services

### EC2 (Elastic Compute Cloud)
- Create, terminate, stop, and start instances
- Tag management
- Instance information retrieval
- State tracking (running, stopped, terminated)

### S3 (Simple Storage Service)
- Create and delete buckets
- Upload and delete objects
- Versioning support
- Encryption settings
- Prefix-based object listing

### RDS (Relational Database Service)
- Create and delete database instances
- Support for MySQL, PostgreSQL, MariaDB
- Multi-AZ configuration
- Snapshot management
- Instance modification

### Lambda
- Create and delete functions
- Function invocation simulation
- Code and configuration updates
- Environment variable management
- Permission management

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/dregraham/cloud-automation.git
cd cloud-automation
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install development dependencies (for testing):
```bash
pip install -r requirements-dev.txt
```

## Quick Start

### Running the Demo

Run the main demonstration script to see the automation in action:

```bash
python main.py --demo
```

This will:
1. Provision a complete infrastructure (EC2, S3, RDS, Lambda)
2. Display the status of all resources
3. Demonstrate various operations
4. Clean up all resources

### Using as a Library

```python
from cloud_automation import AWSAutomation

# Initialize the automation system
automation = AWSAutomation(simulation_mode=True)

# Create an EC2 instance
instance_id = automation.ec2.create_instance(
    instance_type="t2.micro",
    tags={"Name": "my-server", "Environment": "dev"}
)

# Create an S3 bucket
bucket_name = automation.s3.create_bucket(
    bucket_name="my-app-data",
    region="us-east-1",
    versioning=True
)

# Upload an object
automation.s3.put_object(bucket_name, "data.json", '{"key": "value"}')

# Create a Lambda function
function_name = automation.lambda_mgr.create_function(
    function_name="data-processor",
    runtime="python3.9",
    handler="index.handler",
    memory_size=256
)

# Get infrastructure status
status = automation.get_infrastructure_status()
print(status)
```

### Using Configuration Files

Create a YAML configuration file (see `config/example_config.yaml`):

```yaml
ec2:
  - instance_type: t2.micro
    ami_id: ami-0c55b159cbfafe1f0
    tags:
      Name: web-server
      Environment: production

s3:
  - bucket_name: my-application-data
    region: us-east-1
    versioning: true
    tags:
      Project: MyApp
```

Then load and provision:

```python
automation = AWSAutomation(config_file="config/my_config.yaml")
results = automation.provision_infrastructure(automation.config)
```

## Project Structure

```
cloud-automation/
├── cloud_automation/          # Main package
│   ├── __init__.py           # Package initialization
│   ├── aws_automation.py     # Main orchestrator
│   ├── ec2_manager.py        # EC2 operations
│   ├── s3_manager.py         # S3 operations
│   ├── rds_manager.py        # RDS operations
│   └── lambda_manager.py     # Lambda operations
├── tests/                    # Test suite
│   ├── test_ec2_manager.py
│   ├── test_s3_manager.py
│   └── test_aws_automation.py
├── config/                   # Configuration examples
│   └── example_config.yaml
├── main.py                   # CLI demo script
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
└── README.md                 # This file
```

## Running Tests

Run the entire test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=cloud_automation --cov-report=html
```

Run specific test file:

```bash
pytest tests/test_ec2_manager.py
```

Run with verbose output:

```bash
pytest -v
```

## CLI Usage

```bash
# Run full demonstration
python main.py --demo

# Use custom configuration
python main.py --config config/my_config.yaml

# Enable verbose logging
python main.py --demo -v

# Skip cleanup (keep simulated resources)
python main.py --demo --skip-cleanup
```

## Examples

### Example 1: EC2 Fleet Management

```python
from cloud_automation import EC2Manager

ec2 = EC2Manager(simulation_mode=True)

# Create multiple instances
instances = []
for i in range(3):
    instance_id = ec2.create_instance(
        instance_type="t2.micro",
        tags={"Name": f"web-server-{i+1}", "Role": "web"}
    )
    instances.append(instance_id)

# List running instances
running = ec2.list_instances(state="running")
print(f"Running instances: {len(running)}")

# Stop all instances
for instance_id in instances:
    ec2.stop_instance(instance_id)
```

### Example 2: S3 Data Management

```python
from cloud_automation import S3Manager

s3 = S3Manager(simulation_mode=True)

# Create bucket with versioning
bucket_name = "data-lake-bucket"
s3.create_bucket(bucket_name=bucket_name, versioning=True)

# Upload multiple files
files = {
    "data/raw/file1.csv": "col1,col2\n1,2",
    "data/raw/file2.csv": "col1,col2\n3,4",
    "data/processed/output.json": '{"result": "success"}'
}

for key, content in files.items():
    s3.put_object(bucket_name, key, content)

# List objects in a folder
raw_files = s3.list_objects(bucket_name, prefix="data/raw/")
print(f"Raw files: {len(raw_files)}")
```

### Example 3: Complete Infrastructure

```python
from cloud_automation import AWSAutomation

automation = AWSAutomation(simulation_mode=True)

# Define infrastructure
infrastructure = {
    "ec2": [
        {"instance_type": "t2.small", "tags": {"Name": "app-server"}},
        {"instance_type": "t2.micro", "tags": {"Name": "worker-1"}},
    ],
    "s3": [
        {"bucket_name": "app-data", "versioning": True},
        {"bucket_name": "app-backups", "region": "us-west-2"}
    ],
    "rds": [
        {
            "db_instance_identifier": "app-db",
            "engine": "mysql",
            "instance_class": "db.t3.micro",
            "multi_az": True
        }
    ],
    "lambda": [
        {
            "function_name": "nightly-processor",
            "runtime": "python3.9",
            "timeout": 300,
            "memory_size": 1024
        }
    ]
}

# Provision everything
resources = automation.provision_infrastructure(infrastructure)

# Check status
status = automation.get_infrastructure_status()

# Cleanup when done
automation.destroy_infrastructure(resources)
```

## Development

### Code Style

This project uses:
- `black` for code formatting
- `flake8` for linting
- `mypy` for type checking

Format code:
```bash
black cloud_automation/ tests/
```

Lint code:
```bash
flake8 cloud_automation/ tests/
```

### Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Ensure all tests pass
6. Submit a pull request

## Use Cases

This simulation tool is perfect for:

- 🎓 **Learning AWS** - Understand AWS services without AWS account
- 📚 **Training** - Practice infrastructure automation safely
- 🧪 **Testing** - Test automation scripts before deploying to AWS
- 📖 **Documentation** - Create examples and tutorials
- 🔬 **Prototyping** - Design infrastructure before implementation

## Important Notes

⚠️ **This is a simulation tool**
- No actual AWS resources are created
- No AWS credentials required
- No AWS costs incurred
- All operations are local and in-memory

💡 **For production use**
- Replace simulation with actual AWS SDK (boto3) calls
- Implement proper error handling
- Add authentication and authorization
- Follow AWS best practices

## License

This project is open source and available for educational purposes.

## Support

For questions, issues, or contributions, please open an issue on GitHub.

---

**Happy Simulating! 🚀**