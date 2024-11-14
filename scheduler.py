# scheduler.py
import boto3
from datetime import datetime, timedelta
import logging
import config  # Import the config module

# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_lambda_arn(env, func_type, resource):
    return f"{config.LAMBDA_BASE_ARN}-{env.lower()}-{resource}-{func_type}"


def create_schedule(env, func_type, schedule_time, schedule_name, service):
    client = boto3.client("scheduler", region_name="us-east-1")
    resource_schedule_name = f"{schedule_name}-{service.upper()}"

    # Create schedule only for the specified service
    client.create_schedule(
        Name=resource_schedule_name,
        ScheduleExpression=f"at({schedule_time})",
        ScheduleExpressionTimezone=config.TIMEZONE,
        Target={
            "Arn": get_lambda_arn(env, func_type, service),
            "RoleArn": config.SCHEDULE_CLI_ARN,
        },
        FlexibleTimeWindow={"Mode": "OFF"},
        ActionAfterCompletion="DELETE",
    )
    logger.info("%s Schedule Created: %s", service.upper(), resource_schedule_name)


def schedule_service(env, func_type, service, start_date, end_date, schedule_time):
    try:
        start_dt = datetime.strptime(
            f"{start_date}T{schedule_time}", "%Y-%m-%dT%H:%M:%S"
        )
        end_dt = datetime.strptime(f"{end_date}T{schedule_time}", "%Y-%m-%dT%H:%M:%S")
        if start_dt > end_dt:
            return "Start date cannot be later than end date."
    except ValueError:
        return "Invalid date/time format."

    # Create schedules for each day within the range
    for day in range((end_dt - start_dt).days + 1):
        schedule_date = start_dt + timedelta(days=day)
        schedule_name = (
            f"{env}-{func_type}-schedule-{schedule_date.strftime('%d%b%Y-%H%M')}"
        )
        create_schedule(
            env, func_type, schedule_date.isoformat(), schedule_name, service
        )

    return f"{func_type.capitalize()} schedule created for {service.upper()} in {env} environment."

    # Log success message
    logging.info("Schedule created successfully.")
    return "Schedule created successfully."
