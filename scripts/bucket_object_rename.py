import subprocess


def run_command(cmd):
    return subprocess.check_output(cmd, shell=True).decode("utf8").split()


files = run_command("gsutil ls gs://inflation-project-parser-output")

for file_name in files:
    # "gs://inflation-project-parser-output/2022-03-28.parse.jsonl.gz"
    if file_name.endswith(".gz"):
        new_file_name, _ = file_name.rsplit(".", maxsplit=1)
        print(f"command running `gsutil mv {file_name} {new_file_name}`")
        run_command(f"gsutil mv {file_name} {new_file_name}")
