#!/bin/bash

# Source ROS 2 environment
source install/setup.sh

# Export Webots Environment Variables
export WEBOTS_HOME=/home/bitbots/bitbots_main/.pixi/envs/default/share/webots
export WEBOTS_HOST=host.docker.internal

echo "Starting Simulation Backend (Bridge to Webots) on port 1234..."
ros2 launch bitbots_webots_sim simulation_docker.launch multi_robot:=true sim_port:=1234 &
PID_BACKEND=$!
sleep 5 # Wait for backend to initialize

echo "Launching Single Robot (Amy) for Performance..."
ros2 launch src/bitbots_misc/bitbots_bringup/launch/namespaced_teamplayer.launch robot_name:=amy sim:=true &
# ros2 launch src/bitbots_misc/bitbots_bringup/launch/namespaced_teamplayer.launch robot_name:=jack sim:=true &

# Commented out to save resources
# ros2 launch src/bitbots_misc/bitbots_bringup/launch/namespaced_teamplayer.launch robot_name:=rory sim:=true &
# ros2 launch src/bitbots_misc/bitbots_bringup/launch/namespaced_teamplayer.launch robot_name:=donna sim:=true &

echo "Simulation running!"
echo "Backend PID: $PID_BACKEND"
wait
