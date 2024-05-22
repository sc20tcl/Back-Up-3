import time
import azure.functions as func
import logging
import uuid
from azure.functions.decorators.core import DataType
from random import randint
import concurrent.futures
import json
import threading
from tabulate import tabulate

def simSensor(sensorId):
    sensor_data = []

    # simulate a sensor recording
    data = {
        "Id": str(uuid.uuid4()),
        "sensorId": sensorId,
        "temperature": randint(8, 15),
        "wind": randint(15, 25),
        "humidity": randint(40, 70),
        "co2": randint(500, 1500)
    }
    sensor_data.append(data)    
    return sensor_data

app = func.FunctionApp()

@app.function_name(name="recordSensors")
@app.route(route="sensoreCapture", auth_level=func.AuthLevel.ANONYMOUS)
@app.generic_output_binding(arg_name="sensorReading", type="sql", CommandText="dbo.DisSensor", ConnectionStringSetting="SqlConnectionString",
    data_type=DataType.STRING)

def recordSensors(req: func.HttpRequest, sensorReading: func.Out[func.SqlRow]) -> func.HttpResponse:
    rows = []

    # record data for 20 sensors
    for x in range(20):
        generated_data = simSensor(x+1)

        for y in generated_data:
             # add each of the datatpoints to one array to be pushed
            rows.append(func.SqlRow.from_dict(y))
    

    # push data to database
    sensorReading.set(rows)

    return func.HttpResponse(
        body=req.get_body(),
        status_code=201,
        mimetype="application/json")



@app.route(route="dataAnalysis", auth_level=func.AuthLevel.ANONYMOUS)
@app.generic_input_binding(arg_name="sensorStats", type="sql",
                        CommandText="""SELECT sensorId,
                                MIN(temperature) AS min_temperature,
                                MAX(temperature) AS max_temperature,
                                AVG(temperature) AS avg_temperature,
                                MIN(wind) AS min_wind,
                                MAX(wind) AS max_wind,
                                AVG(wind) AS avg_wind,
                                MIN(humidity) AS min_humidity,
                                MAX(humidity) AS max_humidity,
                                AVG(humidity) AS avg_humidity,
                                MIN(co2) AS min_co2,
                                MAX(co2) AS max_co2,
                                AVG(co2) AS avg_co2
                            FROM
                                dbo.DisSensor
                            GROUP BY
                                sensorId""",
                        CommandType="Text",
                        ConnectionStringSetting="SqlConnectionString")
def getSensorData(req: func.HttpRequest, sensorStats: func.SqlRowList) -> func.HttpResponse:
    rows = list(map(lambda r: json.loads(r.to_json()), sensorStats))

    # Format the rows as a table
    table = tabulate(rows, headers="keys", tablefmt="grid")

    # Print the table to the console
    logging.info(table)

    return func.HttpResponse(
        "Table logged in the function's console",
        status_code=200,
        mimetype="text/plain"
    )

@app.function_name(name="SensorTrigger")
@app.generic_trigger(arg_name="trigger", type="sqlTrigger",
                        TableName="dbo.DisSensor",
                        ConnectionStringSetting="SqlConnectionString",
                        data_type=DataType.STRING)
@app.generic_input_binding(arg_name="sensorStats", type="sql",
                        CommandText="""SELECT sensorId,
                                MIN(temperature) AS min_temperature,
                                MAX(temperature) AS max_temperature,
                                AVG(temperature) AS avg_temperature,
                                MIN(wind) AS min_wind,
                                MAX(wind) AS max_wind,
                                AVG(wind) AS avg_wind,
                                MIN(humidity) AS min_humidity,
                                MAX(humidity) AS max_humidity,
                                AVG(humidity) AS avg_humidity,
                                MIN(co2) AS min_co2,
                                MAX(co2) AS max_co2,
                                AVG(co2) AS avg_co2
                            FROM
                                dbo.DisSensor
                            GROUP BY
                                sensorId""",
                        CommandType="Text",
                        ConnectionStringSetting="SqlConnectionString")
def sql_trigger(trigger, sensorStats):
    rows = list(map(lambda r: json.loads(r.to_json()), sensorStats))

    # Format the rows as a table
    table = tabulate(rows, headers="keys", tablefmt="grid")

    # Print the table to the console
    logging.info(table)
