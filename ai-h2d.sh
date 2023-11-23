#! /usr/bin/bash

container_name="ai-h2d"

volume_to_map="/home/$USER/Desktop/ai-h2d-workshop"

if [ ! -d $volume_to_map ]; then
	mkdir $volume_to_map
fi

sudo docker stop $container_name

sudo docker rm $container_name

sudo docker run -it -p 5000:5000 -v $volume_to_map:/app --name $container_name ai-h2d
