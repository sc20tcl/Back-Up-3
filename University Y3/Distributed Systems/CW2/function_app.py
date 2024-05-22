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
    recordings = 1
    sensor_data = []
    for _ in range(recordings):
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

@app.function_name(name="HttpTrigger1")
@app.route(route="hello", auth_level=func.AuthLevel.ANONYMOUS)
@app.generic_output_binding(arg_name="sensorReading", type="sql", CommandText="dbo.Sensors", ConnectionStringSetting="SqlConnectionString",
    data_type=DataType.STRING)

def test_function(req: func.HttpRequest, sensorReading: func.Out[func.SqlRow]) -> func.HttpResponse:
    rows = []
    def thread_function(sensorId):
        generated_data = simSensor(sensorId)

        for x in generated_data:
            rows.append(func.SqlRow.from_dict(x))

    for x in range(20):
        thread_function(x)
    
    sensorReading.set(rows)
    logging.info("data")

    return func.HttpResponse(
        body=req.get_body(),
        status_code=201,
        mimetype="application/json")



    

# The input binding executes the `SELECT * FROM Products WHERE Cost = @Cost` query.
# The Parameters argument passes the `{cost}` specified in the URL that triggers the function,
# `getproducts/{cost}`, as the value of the `@Cost` parameter in the query.
# CommandType is set to `Text`, since the constructor argument of the binding is a raw query.

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
                                dbo.Sensors
                            GROUP BY
                                sensorId""",
                        CommandType="Text",
                        ConnectionStringSetting="SqlConnectionString")
def getSensorData(req: func.HttpRequest, sensorStats: func.SqlRowList) -> func.HttpResponse:
    rows = list(map(lambda r: json.loads(r.to_json()), sensorStats))

    # Format the rows as a table
    table = tabulate(rows, headers="keys", tablefmt="grid")

    # Print the table to the console
    print(table)

    return func.HttpResponse(
        "Table logged in the function's console",
        status_code=200,
        mimetype="text/plain"
    )

    logging.info("changes made")



