import re
import os

FILE_PATH = '/Users/jacobmazelin/Main-Desktop/All_Code/UM/Wolverbot_Kickers/bitbots_main_fork/src/bitbots_simulation/bitbots_webots_sim/protos/robots/Wolfgang/Wolfgang.proto'

def migrate():
    with open(FILE_PATH, 'r') as f:
        lines = f.readlines()
        
    new_lines = []
    
    # State tracking
    # nesting_level of skips
    skip_depth = 0
    
    for line in lines:
        stripped = line.strip()
        
        # 1. Header Update
        if line.startswith("#VRML_SIM"):
            new_lines.append("#VRML_SIM R2025a utf8\n")
            continue
            
        # 2. Lua Value Injection %{= ... }%
        # Example: textureUrl [ %{='"Wolfgang_textures/number_' .. number .. '.png"'}% ]
        if "%{=" in line:
            # Replace with hardcoded number 1 texture
            line = re.sub(r'%\{=.*\}%', '"Wolfgang_textures/number_1.png"', line)
            new_lines.append(line)
            continue
            
        # 3. Lua Control Blocks %{ ... }%
        if "%{" in line:
            # Analyze the control statement
            
            # Start of Name Parsing Block (Top of file)
            # if fields.name.value ~= '' then
            if "if fields.name.value" in line:
                skip_depth += 1
                continue
                
            # Enable Flags: if fields.enableXXX.value then
            # We want to KEEP the body (so don't increment skip), but we discard the line.
            if "if fields.enable" in line:
                continue
                
            # Color Logic: if color == "red" then
            # We KEEP red (default).
            if 'if color == "red"' in line:
                continue
                
            # Color Logic: elseif color == "blue" then
            # We SKIP blue.
            if 'elseif color == "blue"' in line:
                skip_depth += 1
                continue
                
            # Generic ELSE
            # If we were in a "keep" block (like enable or red), else means switch to skip.
            # If we were in a "skip" block (like name parsing), else is irrelevant, we stay skipping.
            if "%{else}%" in line:
                # If skip_depth is 0, it means we are in a 'kept' block's else branch.
                # So we must start skipping.
                if skip_depth == 0:
                    skip_depth += 1
                # If skip_depth > 0, we are already skipping, so we ignore.
                continue
                
            # END
            if "%{end}%" in line:
                # If we were skipping, we might finish skipping.
                if skip_depth > 0:
                    skip_depth -= 1
                continue
                
            # Catch-all for other Lua lines inside blocks (e.g. "local x = 1")
            # If we are skipping, we skip.
            if skip_depth > 0:
                continue
                
            # If we are NOT skipping, but it's a Lua line (e.g. inside kept block but pure logic?)
            # Example: "local color = ..." (wait, that was in top block which is skipped)
            # If there are other logic lines in kept blocks, we should probably skip them too as they are not VRML.
            # So if line has %{ and }% but isn't handled above, skip it.
            continue
            
        # 4. Standard VRML Lines
        if skip_depth == 0:
             # Look for Robot node to inject name mapping if missing?
             # Actually, we will do name mapping via regex/replace later or manual edit.
             new_lines.append(line)
             
    with open(FILE_PATH, 'w') as f:
        f.writelines(new_lines)
        
if __name__ == "__main__":
    migrate()
