import stanza
import glob
import pathlib
import re

nlp = stanza.Pipeline('en', download_method=stanza.DownloadMethod.REUSE_RESOURCES, processors='tokenize')

def get_sentences(input: str) -> list[str]:
    sentences: list[str] = []
    processed_text: stanza.Document = nlp(input)
    for sentence in processed_text.sentences:
        sentences.append(sentence.text)
    return sentences


for text_file in glob.glob("63-4-TXT/*.txt"):
    # Calculate the target filename from the source filename
    target_doc = pathlib.Path.joinpath(pathlib.Path.cwd(), pathlib.Path("63-4-processed"), pathlib.Path(text_file).name)

    # open and tokenize the source file
    with open(text_file) as raw_doc:
        policy_lines = raw_doc.readlines()

    line_count = len(policy_lines)

    # Initialize section number to empty string
    sec_num = ""

    # Precompile the regex for a leading section number ()
    sec_num_re = re.compile(r"^(?P<section_number>[0-9.]+)\s")

    processed_lines: list[str] = []
    for index, line in enumerate(policy_lines):
        print(f"Processing line {index} of {line_count} from {text_file}.")

        # Check for section numbers
        sec_num_matches = sec_num_re.match(line)
        if sec_num_matches is not None:
            #print(sec_num_matches.groupdict()["section_number"])
            sec_num = sec_num_matches.groupdict()["section_number"]
            continue

        # Get rid of empty lines
        elif line[0] == "\n":
            continue

        # If we get here, we're probably dealing with a regular line of text 
        else:
            for sentence in  get_sentences(input=line):
                if "SHALL" in sentence:
                    processed_lines.append(f"{sec_num}: {sentence}")


    # Write out the tokenized file, terminating each string with a newline
    target_doc.write_text("\n".join(processed_lines), encoding="utf-8")