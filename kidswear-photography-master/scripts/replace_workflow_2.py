import sys

with open('SKILL.md', 'r') as f:
    lines = f.readlines()

start_line = -1
end_line = -1

for i, line in enumerate(lines):
    if line.strip() == '### Execution Workflow':
        start_line = i
    if line.strip() == '#### Scene Recommendation Mapping Table':
        end_line = i
        break

if start_line != -1 and end_line != -1:
    new_lines = lines[:start_line] + [
        '### Execution Workflow\n',
        '\n',
        '> 🛑 **System-Level Failsafe Directives**:\n',
        '> - During the parameter collection and user questioning phase, **STRICTLY PROHIBITED** from reading any other Markdown files.\n',
        '> - Upon receiving the complete user selection and preparing to construct prompts, you **MUST ONLY** read `SCENE_FRAMING_RULES.md` to obtain the 5 camera angles for the current scene.\n',
        '\n',
        '0. **Intelligent Garment Analysis (Background Execution)**\n',
        '   - Automatically identify: category, style, brand tier, color, material, season\n',
        '   - Determine brand tone: luxury / fashion / mass-market / sports\n',
        '   - **Identify garment type (garment_type)**:\n',
        '     - `upper_body`: Top (T-shirt/hoodie/jacket/shirt/polo, etc.)\n',
        '     - `lower_body`: Bottom (pants/skirt/shorts, etc.)\n',
        '     - `full_outfit`: Complete outfit (matching top and bottom)\n',
        '     - `dress`: Dress/romper/jumper\n',
        '\n',
        '1. **Consolidated Parameter Confirmation (Ask Once)**\n',
        '   - After analyzing the white-background image, consult the "Scene Recommendation Mapping Table" below to select the 6 most suitable scenes.\n',
        '   - Then, **use a single message** to confirm all required parameters from the user:\n',
        '\n',
        '   > Your clothing style is identified as [Insert Identified Style]. I recommend the following 6 most matching photography scenes for you:\n',
        '   > - **A. [Scene Name in English]** — [1-sentence description, under 10 words]\n',
        '   > - **B. [Scene Name in English]** — [1-sentence description]\n',
        '   > ... (list all 6)\n',
        '   >\n',
        '   > To generate the perfect model images, please also let me know:\n',
        '   > 1. Model Gender (Boy / Girl)\n',
        '   > 2. Model Type (Asian / European)\n',
        '   > 3. Age Group (3-6 years / 6-10 years / 10-14 years)\n',
        '   > \n',
        '   > You can reply directly, for example: "Choose scene B, girl, Asian, 6-10 years."\n',
        '\n',
        '   Wait for the user\'s combined reply, record `scene_type`, gender, model type, and age group, then proceed directly to the image generation workflow.\n',
        '\n',
        '   > **Tip**: If the user already provided some or all of this information when uploading the image, use the provided info and only ask for the missing parts.\n',
        '\n',
        '   ' # to match the indentation of the next line
    ] + lines[end_line:]
    
    with open('SKILL.md', 'w') as f:
        f.writelines(new_lines)
    print("Replaced lines", start_line, "to", end_line)
else:
    print("Could not find lines. Start:", start_line, "End:", end_line)
