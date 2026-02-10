import re

# Source and Target
SOURCE = 'Wolfgang.proto' # We effectively restored this from orig
TARGET = 'Wolfgang.proto'

def migrate():
    print(f"Reading {SOURCE}...")
    with open(SOURCE, 'r') as f:
        lines = f.readlines()
        
    new_lines = []
    
    # Flags to track state
    # We will use simple line context detection because we know the file structure.
    
    skip_mode = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # 1. Update Header
        if "VRML_SIM R2022b" in line:
            new_lines.append("#VRML_SIM R2025a utf8\n")
            continue
            
        # 2. Inject `name IS name`
        # We look for `controller IS controller` and insert before or after it.
        if "controller IS controller" in line:
            # Check if we already inserted it (in case we run this multiple times on same file, though we shouldn't)
            new_lines.append("    name IS name\n")
            new_lines.append(line)
            continue
            
        # 3. Drop Method: Name Parsing Block
        # Starts with %{ and contains "fields.name.value"
        if "%{" in line and "fields.name.value" in line:
            skip_mode = True
            continue
        
        if skip_mode and stripped == "}%":
            skip_mode = False
            continue
            
        if skip_mode:
            continue
            
        # 4. Handle "Texture URL" lines
        # textureUrl [ %{='"Wolfgang_textures/number_' .. number .. '.png"'}% ]
        if "textureUrl" in line and "%{=" in line:
            # Preserve indentation
            indent = line.split("textureUrl")[0]
            new_lines.append(f'{indent}textureUrl [ "Wolfgang_textures/number_1.png" ]\n')
            continue
            
        # 5. Handle "Color" blocks
        # We want to keep RED, skip BLUE/ELSE.
        # Pattern: %{ if color == "red" then }%
        if 'if color == "red"' in line:
            # Drop the wrapper line, keep lines following it.
            continue
            
        # Pattern: %{ elseif color == "blue" then }%
        # We want to SKIP the following lines until the next logic marker.
        # Actually, simpler: The file structure is:
        # %{ if red }%
        #   baseColor 1 0 0
        # %{ elseif blue }%
        #   baseColor 0 0 1
        # %{ else }%
        #   baseColor 0 0 0
        # %{ end }%
        
        # So:
        # If line contains "elseif color" -> Skip next line(s)? 
        # But we are processing line by line.
        # Let's just drop the lines we know we don't want.
        
        if 'if color == "blue"' in line: # elseif or if
            # This and the next line (baseColor 0 0 1) should be skipped?
            # actually, if I just "continue" on this line, the NEXT line (baseColor...) will be included.
            # I need to skip the content too.
            # Since I know the content is 1 line, I can just consume it?
            # Or use a mini-state.
            pass
            
        # Let's use a robust approach for these inner blocks.
        # We will filter out lines based on content if they are part of the "blue" or "else" blocks.
        
        if 'baseColor' in line:
            # Check context.
            # If we just saw "blue", we skip.
            # But we are stateless in this loop block.
            pass
            
    # RESTART STRATEGY: 
    # Let's iterate and build a cleaner list.
    
    final_lines = []
    iterator = iter(lines)
    
    try:
        while True:
            line = next(iterator)
            
            # Header
            if "VRML_SIM R2022b" in line:
                final_lines.append("#VRML_SIM R2025a utf8\n")
                continue
                
            # Name Mapping
            if "controller IS controller" in line:
                 final_lines.append("    name IS name\n")
                 final_lines.append(line)
                 continue
                 
            # Name Parsing Block (Multi-line)
            # %{
            #   if fields.name.value ...
            #   ...
            # }%
            if "%{" in line and "fields.name.value" in line:
                # Consume lines until }%
                while "}%" not in line:
                    line = next(iterator)
                continue # Skip the }% line too
                
            # Enable Flags (Single line wrapper around block)
            # %{if fields.enableBoundingObject.value then}%
            if "%{if fields.enable" in line:
                continue # Drop this line, process body next iteration
                
            # End of Enable Flags
            # %{ end }%
            # Note: This is ambiguous with End of Color Block.
            # But VRML structure usually isolates them.
            # If we see `%{ end }%` or `%{end}%`, we just drop it.
            if "%{ end }%" in line.strip() or "%{end}%" in line.strip():
                continue
                
            # Texture URL (Single line replacement)
            if "textureUrl" in line and "%{=" in line:
                 indent = line.split("textureUrl")[0]
                 final_lines.append(f'{indent}textureUrl [ "Wolfgang_textures/number_1.png" ]\n')
                 continue
                 
            # Color Logic - RED (Keep body, drop wrapper)
            if 'if color == "red"' in line:
                continue
                
            # Color Logic - BLUE (Drop wrapper AND body)
            if 'color == "blue"' in line:
                # Consume next line (the color definition)
                # Assuming it is 1 line.
                # In original file:
                #   baseColor 0.0, 0.0, 1.0
                next(iterator) 
                continue
                
            # Color Logic - ELSE (Drop wrapper AND body)
            if "%{else}%" in line or "%{ else }%" in line:
                # Consume next line (baseColor 0 0 0)
                next(iterator)
                continue
                
            # Catch-all for other Lua markers?
            if "%{" in line or "}%" in line:
                # Log it but maybe keep it if it's not matched above?
                # No, we want to kill all Lua.
                print(f"Dropping residual Lua: {line.strip()}")
                continue
                
            # If we got here, it's valid VRML (we hope)
            final_lines.append(line)
            
    except StopIteration:
        pass
        
    print(f"Writing {len(final_lines)} lines...")
    with open(TARGET, 'w') as f:
        f.writelines(final_lines)

if __name__ == "__main__":
    migrate()
