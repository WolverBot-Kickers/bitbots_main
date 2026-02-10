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
    
    # State
    # 0 = Normal (Keep)
    # 1 = Inside Multi-line Lua Block (Skip until }%)
    # 2 = Inside ELSE block of a Wrapper (Skip until %{end}%)
    state = 0
    
    for i, line in enumerate(lines):
        original_line = line
        stripped = line.strip()
        
        # 1. Header
        if "# template language: lua" in line:
            continue
            
        # 2. Lua Replacements (Values)
        if "%{=" in line:
            # Replace with default texture logic or string
            # textureUrl [ %{='"Wolfgang_textures/number_' .. number .. '.png"'}% ]
            if "Wolfgang_textures" in line:
                 line = re.sub(r'%\{=.*\}%', '"Wolfgang_textures/number_1.png"', line)
                 new_lines.append(line)
                 continue
                 
        # 3. Control Flow
        
        # Check for start of Multi-line block
        # Heuristic: Starts with %{ but does NOT end with }% on same line.
        if "%{" in line and "}%" not in line:
            state = 1
            print(f"Line {i+1}: Start multi-line Lua block. Skipping.")
            continue
            
        # Check for END of Multi-line block
        if "}%" in line and state == 1:
            state = 0
            print(f"Line {i+1}: End multi-line Lua block. Resuming.")
            continue
            
        # Inside Multi-line block?
        if state == 1:
            # Skip content
            continue
        
        # Single-line Wrapper Logic
        # It has %{ and }% on same line.
        if "%{" in line and "}%" in line:
            # Analyze type
            
            # %{else}%
            if "%{else}%" in stripped:
                state = 2
                print(f"Line {i+1}: Found %{{else}}%. Skipping ELSE branch.")
                continue
                
            # %{end}%
            if "%{end}%" in stripped:
                # If we were skipping an ELSE branch, stop skipping.
                if state == 2:
                    state = 0
                    print(f"Line {i+1}: Found %{{end}}%. End ELSE branch. Resuming.")
                # If we were in Normal mode (just ending a Keep block), just remove the line.
                continue

            # %{ if ... }% (Opening a block we want to KEEP)
            if "if fields." in stripped or 'if color ==' in stripped:
                # We want to keep the VRML following this line, so we effectively "strip" the wrapper line.
                # Just continue.
                continue
            
            # Catch-all for other single-line Lua?
            # e.g. %{ local x = 1 }% ?
            # Not expected in this file, but if found, check if it's purely Lua.
            # If so, safe to skip.
            print(f"Line {i+1}: Dropping unhandled single-line Lua: {stripped}")
            continue

        # Inside ELSE block?
        if state == 2:
            # We are in the 'else' branch of a conditional. Skip lines (VRML or whatever).
            # We must watch out for nested %{end}%? 
            # Assuming no nesting in ELSE blocks for now.
            # The %{end}% check above handles the termination.
            continue
            
        # 4. Standard VRML
        if state == 0:
            new_lines.append(line)
            
    print(f"Writing {len(new_lines)} lines...")
    with open(FILE_PATH, 'w') as f:
        f.writelines(new_lines)
    print("Done.")

if __name__ == "__main__":
    migrate()
