
import os
import time
from controller import Supervisor

def reload_world():
    print("Attempting to connect to Supervisor...")
    # Ensure WEBOTS_CONTROLLER_URL is set
    if "WEBOTS_CONTROLLER_URL" not in os.environ:
        os.environ["WEBOTS_CONTROLLER_URL"] = "tcp://host.docker.internal:1234/supervisor_robot"
    
    try:
        s = Supervisor()
        print("Connected to Supervisor.")
        
        # Check if worldReload exists (it should in R2025a)
        if hasattr(s, 'worldReload'):
            print("Triggering world reload...")
            s.worldReload()
            print("World reload command sent.")
            return True
        else:
            print("Error: worldReload() method not found on Supervisor object.")
            return False
            
    except Exception as e:
        print(f"Failed to connect or reload: {e}")
        return False

# Retry loop in case socket is still busy
for i in range(5):
    if reload_world():
        break
    print("Retrying in 2 seconds...")
    time.sleep(2)
