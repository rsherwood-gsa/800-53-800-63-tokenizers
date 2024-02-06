import json

with open("oscal-content/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json") as oscal_file:
    oscal_json = oscal_file.read()

oscal_data = json.loads(oscal_json)

controls = []

def statement_part_to_text(part):
    # convert a "part" statement object to plain text
    statement_text = ""

    # Grab the prose element from the statement
    if "prose" in part.keys():
        statement_text = statement_text + " " + part["prose"]
    
    # Process subparts recursively if they exist
    if "parts" in part.keys():
        for sub_part in part["parts"]:
            statement_text = statement_text + statement_part_to_text(part=sub_part)
    
    # return the result
    return statement_text


statement_dict = {}

for group in oscal_data['catalog']['groups']:
    for control in group['controls']:
        control_id = control["id"]
        if "parts" in control.keys():
            for part in control['parts']: 
                if part['name'] == 'statement':
                    statement_dict[control_id] = statement_part_to_text(part)

with open("800-53-statements.txt", "w") as statement_file:
    for statement_id in statement_dict:
        statement_file.write(f"{statement_id}: {statement_dict[statement_id]}\n")

