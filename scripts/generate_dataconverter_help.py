import subprocess
from pathlib import Path

# Run the command and capture the output
result = subprocess.run(
    ["dataconverter", "--help"], capture_output=True, text=True, check=False
)

print(result.stdout)

# Write the output to a new Markdown file
output_file = Path(__file__).parent.parent.joinpath(
    "docs", "how-tos", "dataconverter_help_output.md"
)
with open(output_file, "w") as f:
    f.write("```shell\n")
    f.write(result.stdout)
    f.write("```\n")
