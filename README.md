# HAIB_SoftwareDevelopment_Informatics

Web application scripts are found in the hw_web_app folder as they are loaded within the database server at hardy-weinberg.haib.org

When editing the helloworld.py file:
1. MUST COPY saved file from server into /root/hw 
[bheater@hardy-weinberg hw]$ sudo cp helloworld.py /root/hw/helloworld.py

2. IF NO --rm in bash script, Remove the docker container
[bheater@hardy-weinberg hw]$ sudo docker rm hello-world

3. DO NOT need to recreate the image: run the bash script
bheater@hardy-weinberg hw]$ sudo ./runOrRestartHelloWorld.sh

Instructions to Start the Web Application 
docker run --rm --network hw_network -p 5000:5000 --name hello-world testapp

View the Started Web App: http://hardy-weinberg.haib.org:5000/
