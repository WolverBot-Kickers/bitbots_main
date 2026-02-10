
import os
import sys
import time

# Set up environment to find the controller
sys.path.append("/home/bitbots/bitbots_main/.pixi/envs/default/lib/python3.12/site-packages")
os.environ["WEBOTS_HOME"] = "/home/bitbots/bitbots_main/.pixi/envs/default/share/webots"

from controller import Robot

def try_connect(name):
    print(f"--- Trying to connect as '{name}' ---")
    if name:
        os.environ["WEBOTS_CONTROLLER_URL"] = f"tcp://host.docker.internal:1234/{name}"
    else:
         os.environ["WEBOTS_CONTROLLER_URL"] = "tcp://host.docker.internal:1234"
    
    try:
        r = Robot()
        print(f"SUCCESS: Connected as '{name}'!")
        print(f"Robot name: {r.getName()}")
        # r.step(32) 
        del r
        return True
    except Exception as e:
        print(f"FAILED to connect as '{name}': {e}")
        return False

# Try 'amy'
try_connect("amy")
print("")

# Try 'Amy'
try_connect("Amy")
print("")

# Try 'Wolfgang'
try_connect("Wolfgang")
print("")

# Try 'wolfgang'
try_connect("wolfgang")
print("")

# Try 'supervisor_robot' (should work if not already taken, but it is taken by the running launch)
# try_connect("supervisor_robot") 
