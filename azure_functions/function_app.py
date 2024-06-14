import azure.functions as func
import logging
import json
import mysql.connector
import os
import traceback

app = func.FunctionApp()

# Database connection setup
db_config = {
    'user': os.environ["MYSQL_USER"],
    'password': os.environ["MYSQL_PASSWORD"],
    'host': os.environ["MYSQL_HOST"],
    'database': os.environ["MYSQL_DATABASE"]
}


def process_event(data):
    # Insert into MySQL
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sensor_data (sensor_id, timestamp, value, lat, lng, unit, type, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            int(data['sensor_id']), data['timestamp'], data['value'],
            data['metadata']['location']['lat'], data['metadata']['location']['lng'],
            data['metadata']['unit'], data['metadata']['type'], data['metadata']['description']
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"Error inserting into MySQL: {e}")
        logging.error(traceback.format_exc())

    

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name=os.environ["EVENTHUB_NAME"], connection= os.environ["CONNECTION_STRING"])
def event_hub_message_trigger(azeventhub: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s', azeventhub.get_body().decode('utf-8'))
    event_data = azeventhub.get_body().decode('utf-8')
    try:
        data = json.loads(event_data)
        process_event(data)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
        logging.error(traceback.format_exc())
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        logging.error(traceback.format_exc())

