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
        
        # Aggressive Lua Cleanup
        if "%{" in line or "}%" in line:
            continue
            
        if "fields.name.value" in line:
            continue
            
        if "local " in line and "=" in line: # simplistic Lua var detection
            continue
            
        if "table.insert" in line:
            continue
            
        if ":gmatch" in line:
            continue
            
        if 'if color == "red"' in line: # Kept red logic but remove the IF line
             continue
        if 'elseif color == "blue"' in line: # Remove blue logic lines?
             # Wait, if we remove 'elseif', we must also remove the content?
             # But checks above catch variables.
             # If "blue" block has textureUrl...
             continue
             
        # We need to be careful not to delete VRML.
        # But name parsing block is purely Lua.
        
        new_lines.append(line)
            
    print(f"Writing {len(new_lines)} lines...")
    with open(FILE_PATH, 'w') as f:
        f.writelines(new_lines)
    print("Done.")

if __name__ == "__main__":
    migrate()
