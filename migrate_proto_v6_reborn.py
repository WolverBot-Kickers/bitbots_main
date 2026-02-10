import re
import sys

# Paths
ORIG_FILE = 'Wolfgang_orig.proto'
TARGET_FILE = 'Wolfgang.proto'

def main():
    print(f"Reading {ORIG_FILE}...")
    with open(ORIG_FILE, 'r') as f:
        lines = f.readlines()

    new_lines = []
    
    # States
    # 0: KEEP (Normal)
    # 1: SKIP (Inside a block we want to remove, e.g. blue/else/name_parsing)
    state = 0
    
    # We need to handle nesting if any? 
    # Glancing at file, nesting seems minimal or non-existent for the blocks we skip.
    # But "enablePhysics" might contain "red/blue"? No, usually other way around.
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # 1. Header (Replace R2022b with R2025a)
        if "#VRML_SIM R2022b utf8" in line:
            new_lines.append("#VRML_SIM R2025a utf8\n")
            continue
            
        # 2. Lua Value Injection %{=...}%
        # textureUrl [ %{='"Wolfgang_textures/number_' .. number .. '.png"'}% ]
        if "%{=" in line:
            # Replace strictly with default texture
            if "textureUrl" in line:
                # Keep indentation
                indent = line[:line.find("textureUrl")]
                new_lines.append(f'{indent}textureUrl [ "Wolfgang_textures/number_1.png" ]\n')
            else:
                 # Fallback?
                 print(f"Propagating unhandled value injection at line {i+1}: {stripped}")
                 new_lines.append(line)
            continue
            
        # 3. Control Logic
        
        # A. Name Parsing Block (Always Skip)
        if "if fields.name.value" in line and "%{" in line:
            state = 1 # Start skipping
            continue
            
        # B. Enable Flags (Always Keep Content, Drop Wrapper)
        if "if fields.enable" in line and "%{" in line:
            # We want the content, so we just drop this line.
            # State remains 0 (Keep).
            continue
            
        # C. Color Logic (Red/Blue/Else)
        if 'if color == "red"' in line and "%{" in line:
            # Keep content (red is default). Drop line.
            continue
            
        if 'elseif color == "blue"' in line and "%{" in line:
            # Skip blue content.
            state = 1
            continue
            
        if "%{else}%" in line or "%{ else }%" in line:
            # If we were in KEEP mode (red), now we hit ELSE (black/default?), we should SKIP?
            # Original: red -> 1,0,0. blue -> 0,0,1. else -> 0,0,0.
            # We want RED (1,0,0). So we SKIP else.
            # If we were ALREADY in SKIP mode (blue), we KEEP SKIPPING.
            state = 1
            continue
        
        if "%{elseif" in line:
             # Catch-all for other elseifs?
             state = 1
             continue

        # D. End
        if "%{ end }%" in line or "%{end}%" in line:
            # If we were skipping, we perform a "Resume".
            # If we were keeping (red/enable), line is dropped, continue keeping.
            
            # Problem: How do we know if this 'end' closes a SKIP block or a KEEP block?
            # We can use a depth counter?
            # Or just reset to 0?
            
            # Since nesting is low:
            # The 'enable' blocks wrap BIG chunks.
            # The 'color' blocks are small.
            
            # If we set state=0 here, we might accidentally un-skip a parent block?
            # But we are blindly treating 'enable' as "remove line, keep content".
            # So 'enable' does NOT trigger state change.
            
            # Only 'name parsing', 'blue', 'else' trigger state=1.
            # When we hit 'end', we should go back to state=0.
            state = 0
            continue
            
        # 4. Content
        if state == 0:
            new_lines.append(line)
            
    # Post-processing: Add 'name IS name' if missing
    # Check if 'name IS name' exists in Robot block
    has_name_mapping = any("name IS name" in l for l in new_lines)
    if not has_name_mapping:
        # Find 'Robot {'
        for idx, l in enumerate(new_lines):
            if "Robot {" in l:
                # Insert at idx+1
                new_lines.insert(idx+1, "    name IS name\n")
                break
                
    print(f"Writing {len(new_lines)} lines to {TARGET_FILE}...")
    with open(TARGET_FILE, 'w') as f:
        f.writelines(new_lines)
    print("Done.")

if __name__ == "__main__":
    main()
