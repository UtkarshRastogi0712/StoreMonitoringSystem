# Store Management System

## Description
TLDR - The project in essence looks over a large network of store around the world in various timezones and calculates the duration of the store being up and running from relevant data in a relevant format.

The API reads data from 3 dynamically updated CSV files:
* Timezone : Containing the timezone of each store
* Store status : The status (active/inactive) of a store collected at a particular time in UTC
* Business hours : The stipulated business hours of a store in the local timezone

This data is read from the CSV files and fed to a MySQL database with the same structure. The data is then read from the database using pydantic models and sqlalchemy ORM to be processed. The status of a store is extracted daily, where we calculate the interval for which the store was online every day in the time range. This is then converted to the local timezone using data from the Timezone table. Finally we calculate the overlap between the processed local uptime and the stipulated business hours to get the output report. The output report is stored in a redis cache for an hour until the CSV data is updated or rendered obsolete.

## Endpoints
* /trigger_report : This endpoint triggers report generation from the current relevant updated data and returns a report_id for reference.
* /get_report : This endpoint takes an input report_id which fetches a report from the redis cache if one exists. Otherwise returns the status that the report is being processed and generated.

## Tech Stack
* FastAPI
* MySQL
* Redis

## Libraries
* sqlalchemy
* pymysql
* pydantic
* pandas
* pytz
* datetime
