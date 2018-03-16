#!/bin/bash
echo "Stopping and removing currently running hello-world..."
docker stop hello-world
echo "Starting new hello-world..."
docker run -d --rm --network hw_network -p 5000:5000 --name hello-world -v /root/hw/:/etc/app/ testapp
echo "Server up and running!"
