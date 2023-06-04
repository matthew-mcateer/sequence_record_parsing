import subprocess
from flytekit import task, workflow

@task
def split_sequences(file_path: str) -> str:
    SPLIT = 'gcsplit' if System.properties['os.name'] == 'Mac OS X' else 'csplit'
    # file_path = "~/sample.fa" would normally be an input argument
    output_prefix = 'seq_'
    # run the csplit command, storing the outputs in files with names prefixed by 'seq_'
    subprocess.check_output(f"{SPLIT} {file_path} '%^>%' '/^>/' '{{*}}' -f {output_prefix}", shell=True)
    return output_prefix

@task
def reverse(input_prefix: str) -> str:
    # use a shell command to get a list of all files that match the prefix
    files = subprocess.check_output(f"ls {input_prefix}*", shell=True).decode().split('\n')
    reversed_sequences = []
    # iterate through each file
    for f in files:
        if f:  # skip empty names
            # reverse the content of each file and store the result
            reversed_sequences.append(subprocess.check_output(f"cat {f} | rev", shell=True).decode())
    return "\n".join(reversed_sequences)

@workflow
def reverse_workflow(file_path: str) -> str:
    prefix = split_sequences(file_path=file_path)
    return reverse(input_prefix=prefix)
