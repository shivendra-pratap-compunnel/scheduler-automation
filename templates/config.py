# config.py

# AWS Lambda and IAM ARNs
LAMBDA_BASE_ARN = "arn:aws:lambda:us-east-1:746669213641:function:nrt"
SCHEDULE_CLI_ARN = "arn:aws:iam::746669213641:role/nrt-scheduler-cli-role"

# Timezone and other constants
TIMEZONE = "Asia/Kolkata"

# Supported environments and services (if needed)
SUPPORTED_ENVIRONMENTS = ["DEV1", "DEV2", "QA1", "QA2", "UAT1", "UAT2"]
SUPPORTED_SERVICES = ["ec2", "rds"]
