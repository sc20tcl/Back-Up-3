import requests
import logging
from kubernetes import client, config
import math
import redis
import sys

from datetime import datetime, timedelta

redis_host = 'my-redis-master' 
redis_port = 6379
redis_password = 'MUzG8RpNtw'  

# Initialize Redis client
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

def get_last_scale_time():
    last_time = r.get('last_scale_time')
    return datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S') if last_time else None

def update_last_scale_time():
    r.set('last_scale_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def can_scale_down():
    last_time = get_last_scale_time()
    if not last_time or datetime.now() - last_time > timedelta(minutes=5):  # Cooldown period
        return True
    return False

def get_current_replicas(deployment_name, namespace):
    config.load_incluster_config()
    k8s_client = client.AppsV1Api()
    deployment = k8s_client.read_namespaced_deployment(deployment_name, namespace)
    return deployment.spec.replicas

def scale_decision(deployment_name, namespace, recommended_pods):
    last_scale_time = get_last_scale_time()
    logging.info("last scale time: %s", last_scale_time)
    current_pods = get_current_replicas(deployment_name, namespace)
    if recommended_pods == current_pods:
        logging.info("No scaling action needed.")
        return

    if recommended_pods > current_pods:
        logging.info("Scaling up as per recommendation.")
        scale_deployment(deployment_name, namespace, recommended_pods)
    else:
        if can_scale_down():
            logging.info(f"Scaling down to {recommended_pods} replicas.")
            update_last_scale_time()
            scale_deployment(deployment_name, namespace, recommended_pods)
        else:
            logging.info(f"Cool down period is still active no scale down permitted")
    

def get_traffic(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        traffic = data.get('traffic', 0)  
        logging.info(f"Successfully called {url}: {response.text}")
        sys.stdout.flush()
        return traffic
    except requests.exceptions.RequestException as e:
        logging.error(f"Error calling {url}: {str(e)}")
        return None
    
def predict_traffic(url, requests_per_minute):
    url = 'http://20.33.62.78:5000/predict'
    
    headers = {'Content-Type': 'application/json'}
    
    data = {
        'current_traffic': requests_per_minute
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        forecast_value = float(json_response['forecast'][0])
        logging.info(f"Successfully called {url}: {response.text}")
        sys.stdout.flush()
        return forecast_value
    else:
        logging.error(f"Failed to get prediction, status code: {response.status_code}")
        return None
    
def optimum_pods(qpm):
    url = "http://20.33.62.78:5002/optimum_pods?qps=" + str(float(qpm)/60)
    response = requests.get(url)
    
    if response.status_code == 200:
        json_response = response.json()
        optimum_pods = int(json_response['optimum_pods'])
        logging.info(f"Successfully called {url}: {response.text}")
        sys.stdout.flush()
        return optimum_pods
    else:
        logging.error(f"Failed to get optimum pods, Received status code {response.status_code}")
        return None

def scale_deployment(deployment_name, namespace, num_pods):
    logging.info(f"Attempting to scale Deployment: {deployment_name} to {num_pods} pods...")
    try:
        config.load_incluster_config()
        k8s_client = client.AppsV1Api()
        
        k8s_client.patch_namespaced_deployment_scale(
            name=deployment_name,
            namespace=namespace,
            body={'spec': {'replicas': num_pods}}
        )
        logging.info(f"Deployment {deployment_name} scaled to {num_pods} pods.")
    except Exception as e:
        logging.error(f"Failed to scale deployment: {str(e)}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    traffic_url = 'http://20.33.62.78:5001/traffic'
    traffic_model_url = 'http://20.33.62.78:5000/predict'
    deployment_name = 'teastore-webui'
    namespace = 'default'

    traffic = get_traffic(traffic_url)
    logging.info(f"Traffic: {traffic}")
    if traffic is not None:
        predicted_traffic = predict_traffic(traffic_model_url, traffic)
        logging.info(f"Predicted Traffic: {predicted_traffic}")
        if predicted_traffic is not None:
            num_pods = optimum_pods(predicted_traffic)
            logging.info(f"Optimum Pods: {num_pods}")
            scale_decision(deployment_name, namespace, num_pods)
           
