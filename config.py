# config.py

# AWS account id
AWS_ACCOUNT_ID = "746669213641"

LAMBDA_BASE_ARN = f"arn:aws:lambda:us-east-1:{AWS_ACCOUNT_ID}:function:nrt"
SCHEDULE_CLI_ARN = f"arn:aws:iam::{AWS_ACCOUNT_ID}:role/nrt-scheduler-cli-role"


# Timezone and other constants
TIMEZONE = "Asia/Kolkata"

# Supported environments and services (if needed)
SUPPORTED_ENVIRONMENTS = ["DEV1", "DEV2", "QA1", "QA2", "UAT1", "UAT2"]
SUPPORTED_SERVICES = ["ec2", "rds"]
