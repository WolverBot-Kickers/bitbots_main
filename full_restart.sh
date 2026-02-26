#!/bin/bash

echo "=== RESTARTING SIMULATION ==="

# 1. Kill Webots on Host
echo "Closing Webots..."
pkill -f webots-bin || pkill -f webots || echo "Webots already closed."

# 2. Restart Docker Processes (NOT Container)
echo "Stopping Simulation Processes..."
docker exec bitbots_sim pkill -f python
docker exec bitbots_sim pkill -f ros2
docker exec bitbots_sim pkill -f launching

# 3. Launch Webots (Host)
echo "Launching Webots..."
open -a /Applications/Webots.app src/bitbots_simulation/bitbots_webots_sim/worlds/match.wbt &

# 4. Launch Simulation Stack (Docker)
echo "Waiting for Webots (5s)..."
sleep 5
echo "Launching Simulation Stack (Amy Only)..."
# Use pixi run to ensure environment is active
docker exec -d bitbots_sim zsh -c "/home/bitbots/.pixi/bin/pixi run ./launch_game.sh"

echo "=== DONE ==="
echo "1. Webots should open."
echo "2. Press PLAY (Cmd+2)."
echo "3. Amy should move."
