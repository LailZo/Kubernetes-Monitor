from flask import Flask, render_template
from kubernetes import client, config
import base64

app = Flask(__name__)

def get_all_server_info():
    try:
        # Load Kubernetes configuration from the kube-config file
        kube_config_path = '/app/creds/config'  # Adjust path as needed
        config.load_kube_config(config_file=kube_config_path)

        # Create an instance of the Kubernetes API client
        api_client = client.CoreV1Api()

        server_info = {}
        # Query Kubernetes API for node information
        nodes = api_client.list_node().items
        
        print(nodes)

        for node in nodes:
            node_name = node.metadata.name
            # Collect server information from each node
            node_info = {
                'name': node_name,
                'cpu': node.status.allocatable['cpu'],
                'memory': node.status.allocatable['memory'],
                # Add more server metrics as needed
            }
            server_info[node_name] = node_info
    except Exception as e:
        print(f"Error fetching server info: {e}")
        server_info = {}
    return server_info

@app.route('/')
def index():
    all_server_info = get_all_server_info()
    print(all_server_info)
    return render_template('index.html', all_server_info=all_server_info)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
