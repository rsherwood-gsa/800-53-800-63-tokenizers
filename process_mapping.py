import re

with open("mapping.txt") as mapping_file:
    map_lines = mapping_file.readlines()

current_control = ""

matched_sections = []
control_mapping = []

for line in map_lines:
    # Identify NIST Control IDs
    control_match = re.search('([^\d-]{2}-\d)', line)
    if control_match is not None:
        current_control = line.strip()
        continue

    if line.strip()[0] == "*":
        # Strip out the reference to the document, to simplify regex matching
        document = line.split("-")[1]
        section_match = re.findall('([\d\.]+)', line)
        matched_sections = section_match

        if len(matched_sections) > 0:
            for section in matched_sections[3:]:
                control_mapping.append(f"{current_control}:{document}-{section}")

with open("mapped_controls.txt", "w") as mapped_controls:
    for mapping in control_mapping:
        mapped_controls.write(f"{mapping}\n")
