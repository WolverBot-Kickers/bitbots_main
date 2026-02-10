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
    
    skip_depth = 0
    
    for i, line in enumerate(lines):
        # 1. Remove template language header
        if "# template language: lua" in line:
            # Skip this line
            continue
            
        # 2. Lua Output Injection
        if "%{=" in line:
            # Replace with default texture
            line = re.sub(r'%\{=.*\}%', '"Wolfgang_textures/number_1.png"', line)
            new_lines.append(line)
            continue

        # 3. Lua Control Blocks
        if "%{" in line:
            # Check content
            
            # Name Parsing
            if "if fields.name.value" in line:
                skip_depth += 1
                continue
                
            # Enable Flags
            if "if fields.enable" in line:
                # Keep body, discard line
                continue
                
            # Color Logic
            if 'if color == "red"' in line:
                continue
            if 'elseif color == "blue"' in line:
                skip_depth += 1
                continue
                
            # ELSE
            if "%{else}%" in line:
                # If we are strictly in an enable/if block (depth 0), start skipping else.
                if skip_depth == 0:
                    skip_depth += 1
                continue
                
            # END
            if "%{end}%" in line:
                if skip_depth > 0:
                    skip_depth -= 1
                continue
                
            # Catch-all
            if skip_depth > 0:
                continue
            
            # If line is Lua but not handled above:
            # e.g. "local x = ..."
            # We should probably discard it to be safe if it contains %{
            if "%{" in line and "}%" in line and skip_depth == 0:
                print(f"Dropping unhandled Lua line {i+1}: {line.strip()}")
                continue
                
            # If skip_depth > 0, we already continued.
        
        # 4. Standard Lines
        if skip_depth == 0:
            new_lines.append(line)
            
    print(f"Writing {len(new_lines)} lines...")
    with open(FILE_PATH, 'w') as f:
        f.writelines(new_lines)
    print("Done.")

if __name__ == "__main__":
    migrate()
