# Telestream SPG9000 Exporter for Prometheus

## Running
The SPG9000 data exporter is a python application. It is provided here in the context of a Docker container running Python Slim, but the script can be adapted to run as a Linux service. 

By default Flask runs on port 5000, but this can be mapped to any port on the computer running Docker.

Visit http://<docker ip>:<port>/metrics?api_key=<api_key>&target=0.0.0.0 where <docker ip> is the IP address of the docker installation, <port> is the external port that is mapped to container port 5000, <api_key> is the configured API key on the Telestream SPG9000, and 0.0.0.0 is the IP of the Telestream SPG9000 to get metrics from.
