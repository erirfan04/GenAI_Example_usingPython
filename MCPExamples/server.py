
from mcp.server.fastmcp import FastMCP
import requests
import json
import pandas as pd
from datetime import datetime
import os
import logging

# ---------------------------------------------------
# Base Directory
# ---------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------
# Folder Paths
# ---------------------------------------------------

LOG_DIR = os.path.join(BASE_DIR, "logs")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
EMPLOYEE_FILE = os.path.join(BASE_DIR, "employees.json")

# ---------------------------------------------------
# Create folders if not exists
# ---------------------------------------------------

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# ---------------------------------------------------
# Logging Configuration
# ---------------------------------------------------

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "app.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------------------------------------------
# Create MCP Server
# ---------------------------------------------------

mcp = FastMCP("Business Assistant Server")

# ---------------------------------------------------
# Tool 1 - Employee Search
# ---------------------------------------------------

@mcp.tool()
def search_employee(emp_id: int):
    """
    Search employee details by employee ID
    """

    try:

        with open(EMPLOYEE_FILE, "r") as file:
            employees = json.load(file)

        for emp in employees:

            if emp["id"] == emp_id:

                logging.info(f"Employee found: {emp_id}")

                return emp

        return {
            "message": "Employee not found"
        }

    except Exception as e:

        logging.error(str(e))

        return {
            "error": str(e)
        }

# ---------------------------------------------------
# Tool 2 - Weather API
# ---------------------------------------------------

@mcp.tool()
def get_weather(city: str):
    """
    Get weather details for a city
    """

    try:

        url = f"https://wttr.in/{city}?format=j1"

        response = requests.get(url, timeout=10)

        data = response.json()

        current = data["current_condition"][0]

        result = {
            "city": city,
            "temperature": current["temp_C"],
            "humidity": current["humidity"],
            "weather": current["weatherDesc"][0]["value"]
        }

        logging.info(f"Weather checked for {city}")

        return result

    except Exception as e:

        logging.error(str(e))

        return {
            "error": str(e)
        }

# ---------------------------------------------------
# Tool 3 - Salary Statistics
# ---------------------------------------------------

@mcp.tool()
def salary_statistics():
    """
    Calculate employee salary statistics
    """

    try:

        with open(EMPLOYEE_FILE, "r") as file:
            employees = json.load(file)

        df = pd.DataFrame(employees)

        result = {
            "total_employees": int(len(df)),
            "average_salary": float(df["salary"].mean()),
            "maximum_salary": float(df["salary"].max()),
            "minimum_salary": float(df["salary"].min())
        }

        logging.info("Salary statistics generated")

        return result

    except Exception as e:

        logging.error(str(e))

        return {
            "error": str(e)
        }

# ---------------------------------------------------
# Tool 4 - Generate Report
# ---------------------------------------------------

@mcp.tool()
def generate_report():
    """
    Generate employee report
    """

    try:

        with open(EMPLOYEE_FILE, "r") as file:
            employees = json.load(file)

        report_file = os.path.join(
            REPORT_DIR,
            f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        with open(report_file, "w") as report:

            report.write("EMPLOYEE REPORT\n")
            report.write("=" * 50 + "\n\n")

            for emp in employees:

                report.write(
                    f"ID: {emp['id']}\n"
                    f"Name: {emp['name']}\n"
                    f"Department: {emp['department']}\n"
                    f"Salary: {emp['salary']}\n"
                    f"{'-'*40}\n"
                )

        logging.info("Report generated")

        return {
            "message": "Report generated successfully",
            "report_file": report_file
        }

    except Exception as e:

        logging.error(str(e))

        return {
            "error": str(e)
        }

# ---------------------------------------------------
# Tool 5 - System Health
# ---------------------------------------------------

@mcp.tool()
def system_health():
    """
    Check server health
    """

    return {
        "server": "Running",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Healthy"
    }

# ---------------------------------------------------
# Run MCP Server
# ---------------------------------------------------

if __name__ == "__main__":

    logging.info("MCP Server Started")

    mcp.run(transport="stdio")

