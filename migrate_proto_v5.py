import re
import sys
import os

FILE_PATH = '/Users/jacobmazelin/Main-Desktop/All_Code/UM/Wolverbot_Kickers/bitbots_main_fork/src/bitbots_simulation/bitbots_webots_sim/protos/robots/Wolfgang/Wolfgang.proto'

def migrate():
    print(f"Reading {FILE_PATH}...")
    with open(FILE_PATH, 'r') as f:
        lines = f.readlines()
        
    print(f"Read {len(lines)} lines.")
    new_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # Remove Lua comments
        if "--" in line:
            # Check if it's not inside a string?
            # But in this file, -- only appears as Lua comments.
            # VRML comments are #.
            continue
            
        new_lines.append(line)
            
    print(f"Writing {len(new_lines)} lines...")
    with open(FILE_PATH, 'w') as f:
        f.writelines(new_lines)
    print("Done.")

if __name__ == "__main__":
    migrate()
