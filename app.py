# app.py
import scheduler  # Import the scheduler module
import config  # Import the config module
import logging
from datetime import datetime
import pytz
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Route to render the HTML form
@app.route("/")
def index():
    # Retrieve existing schedules
    schedules = scheduler.get_existing_schedules()
    # Print the schedules to the console for debugging
    print("Schedules fetched:", schedules)
    return render_template("index.html", schedules=schedules)


# Route to handle schedule deletion
@app.route('/delete_schedule', methods=['POST'])
def delete_schedule():
    schedule_name = request.form['schedule_name']
    # Logic to delete the schedule
    try:
        delete_schedule_from_db(schedule_name)
        return render_template('index.html', result=f"Schedule {schedule_name} deleted successfully!", schedules=get_schedules())
    except Exception as e:
        return render_template('index.html', result="Error deleting schedule.", schedules=get_schedules())



@app.route("/schedule", methods=["POST"])
def create_schedule():
    logging.info("Received request to create schedule.")

    # Get data from the form submission
    env = request.form.get("env")
    func_type = request.form.get("func_type")
    service = request.form.get("service")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    schedule_time = request.form.get("schedule_time")

    logging.info(
        f"Received data - env: {env}, func_type: {func_type}, service: {service}, "
        f"start_date: {start_date}, end_date: {end_date}, schedule_time: {schedule_time}"
    )

    # Ensure schedule_time has seconds
    if len(schedule_time.split(":")) == 2:  # Only HH:MM provided
        schedule_time += ":00"

    # Convert the time to 24-hour format with seconds in IST
    try:
        schedule_time_dt = datetime.strptime(
            schedule_time,
            (
                "%I:%M %p"
                if "AM" in schedule_time or "PM" in schedule_time
                else "%H:%M:%S"
            ),
        )

        ist_timezone = pytz.timezone(config.TIMEZONE)
        schedule_time_ist = ist_timezone.localize(schedule_time_dt)
        schedule_time_24hr_ist = schedule_time_ist.strftime("%H:%M:%S")

    except ValueError:
        logging.error("Invalid time format")
        return render_template(
            "index.html", result="Invalid time format. Use HH:MM AM/PM or HH:MM:SS."
        )

    try:
        start_dt = f"{start_date}T{schedule_time_24hr_ist}"
        end_dt = f"{end_date}T{schedule_time_24hr_ist}"

        result = scheduler.schedule_service(
            env, func_type, service, start_date, end_date, schedule_time_24hr_ist
        )
        logging.info(f"Scheduler response: {result}")
        return render_template("index.html", result=result)
    except Exception as e:
        logging.error(f"Failed to create schedule: {e}")
        return render_template("index.html", result=f"Failed to create schedule: {e}")


if __name__ == "__main__":
    app.run(debug=True)
