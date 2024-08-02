#!/bin/bash

USERNAME="${ICL_USERNAME}"
PASSWORD="${ICL_PASSWORD}"

api_port=5000

# Read command-line options
while getopts ":p:s:" opt; do
  case ${opt} in
    p) jp_port=$OPTARG;;
    s) api_port=$OPTARG;;

    \?) echo "Usage: run-server [-p jupter server port] (-s api port)"
      exit 1
    ;;
  esac
done

if [ -z "${jp_port}" ] ; then
    echo "Port must be specified."
    echo "Usage: run-server [-p jupter server port] (-s api port)"
    exit 1
fi

echo "Starting ${env} on Jupyter Lab on port ${jp_port}..."
echo "Server listening on port ${api_port}..."
sshpass -p "$PASSWORD" ssh -tt \
-L "${jp_port}:localhost:${jp_port}" \
-L "${api_port}:localhost:${api_port}" \
$USERNAME@shell2.doc.ic.ac.uk "~/start-api.sh -p ${jp_port} -s ${api_port}"