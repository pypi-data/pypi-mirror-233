import click
from databricks import sql
import json
import hashlib
import hmac
import base64
import requests
from datetime import datetime
import pytz
from typing import List, Tuple
import os
from airflow.hooks.base_hook import BaseHook
import logging
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

@click.command()
@click.option('--env', default='databricks')
@click.option('--dwhcid', default='databricks_connection')
@click.option('--azmonitorcid', default='azure_monitor')
def dbtlog(env,dwhcid,azmonitorcid):
   
   az_conn = BaseHook.get_connection(str(azmonitorcid))
   azure_monitor_extras_dict = json.loads(az_conn.get_extra())

   
   workspace_id = str(azure_monitor_extras_dict['workspace_id'])
   primary_key = str(azure_monitor_extras_dict['primary_key'])
   execution_start_date = os.getenv("AIRFLOW_CTX_EXECUTION_DATE")

   if(env == "databricks"):
        conn = BaseHook.get_connection(str(dwhcid))
        databricks_extras_dict = json.loads(conn.get_extra())
        connection_string = str(conn.host)
        logging.info(str(conn.password))
        token = str(conn.password)
        http_path = str(databricks_extras_dict["http_path"])

        connection = sql.connect(
                           server_hostname = connection_string,
                           http_path = http_path,
                           access_token = token)
        cursor = connection.cursor()


   if(env == "snowflake"):
        snowflake_conn = BaseHook.get_connection(str(dwhcid))
        engine = create_engine(URL(
            account = str(snowflake_conn.account),
            user = str(snowflake_conn.login),
            password = str(snowflake_conn.password),
            database = str(snowflake_conn.database),
            schema = str(snowflake_conn.schema),
            warehouse = str(snowflake_conn.warehouse),
            role= str(snowflake_conn.role),
        ))
        print(engine)
        cursor = engine.connect()

   
   results = []

   print(f"select * from `model_executions` WHERE node_id NOT LIKE 'model.dbt_artifacts%' and run_started_at > '{execution_start_date}'") 
   cursor.execute(f"select * from `model_executions` WHERE node_id NOT LIKE 'model.dbt_artifacts%' and run_started_at > '{execution_start_date}'")
   results.append(list_to_dict(cursor.fetchall(),cursor.description))

   cursor.execute(f"select * from `seed_executions` WHERE node_id NOT LIKE 'model.dbt_artifacts%' and run_started_at > '{execution_start_date}'")
   results.append(list_to_dict(cursor.fetchall(),cursor.description))

   cursor.execute(f"select * from `test_executions` WHERE node_id NOT LIKE 'model.dbt_artifacts%' and run_started_at > '{execution_start_date}'")
   results.append(list_to_dict(cursor.fetchall(),cursor.description))

   cursor.execute(f"select * from `snapshot_executions` WHERE node_id NOT LIKE 'model.dbt_artifacts%' and run_started_at > '{execution_start_date}'")
   results.append(list_to_dict(cursor.fetchall(),cursor.description))

   flattened_list = [item for sublist in results for item in sublist]

   results_json = json.dumps(flattened_list, indent=2)
   print(results_json)

   invocation_result = []
   cursor.execute(f"select * from `invocations` WHERE run_started_at > '{execution_start_date}'")
   invocation_result.append(list_to_dict(cursor.fetchall(),cursor.description))
   invocation_results_json = json.dumps(flattened_list, indent=2)
   cursor.close()
   connection.close()

   send_custom_data("dbtlogs",results_json,workspace_id,primary_key)
   send_custom_data("invocationlogs",invocation_results_json,workspace_id,primary_key)

def list_to_dict(list, description: List[Tuple]):
    result = []
    for row in list:
      result_dict = {}
      for i, column in enumerate(description):
         result_dict[column[0]] = str(row[i])
      result.append(result_dict)
    return result

def get_last_logged_time(workspace_id,primary_key):
    server_time_string = get_server_time()
    signature = get_request_signature(server_time_string,workspace_id,primary_key)
    print(signature)
    url = f"https://{workspace_id}.ods.opinsights.azure.com/api/logs?api-version=2016-04-01"

def send_custom_data(log_name, data,workspace_id,primary_key):
    json_request_data = data
    server_time_string = get_server_time()
    signature = get_request_signature(server_time_string, json_request_data,workspace_id,primary_key)
    print(signature)
    url = f"https://{workspace_id}.ods.opinsights.azure.com/api/logs?api-version=2016-04-01"
    headers = {
        "Authorization": signature,
        "Content-Type": "application/json",
        "Log-Type": log_name,
        "x-ms-date": get_x_ms_date(),
        "time-generated-field": "LogGeneratedTime",
    }
    try:
        response = requests.post(url, headers=headers, data=json_request_data)
        status_code = response.status_code
        if status_code != 200:
            raise RuntimeError("Unable to send custom log data to Azure Monitor")
    except Exception as e:
        raise e
    

def get_request_signature(server_time_string, request_data,workspace_id,primary_key):
    http_method = "POST"
    content_type = "application/json"
    xms_date = f"x-ms-date:{server_time_string}"
    resource = "/api/logs"
    string_to_hash = "\n".join([http_method, str(len(request_data.encode("utf-8"))), content_type, xms_date, resource])
    hashed_string = get_hmac256(string_to_hash, primary_key)
    return f"SharedKey {workspace_id}:{hashed_string}"


def get_server_time():
    now = datetime.utcnow()
    return now.strftime("%a, %d %b %Y %H:%M:%S GMT")

def get_hmac256(input_string, key):
    sha256_hmac = hmac.new(base64.b64decode(key.encode("utf-8")), input_string.encode("utf-8"), hashlib.sha256)
    return base64.b64encode(sha256_hmac.digest()).decode("utf-8")


def get_x_ms_date():
    utc_now = datetime.now(pytz.timezone('UTC'))
    formatted_date = utc_now.strftime('%a, %d %b %Y %H:%M:%S GMT')
    return formatted_date

if __name__ == '__main__':
   dbtlog()