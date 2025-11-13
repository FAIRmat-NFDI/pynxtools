#!/bin/bash
set -euo pipefail

project_dir=$(dirname "$(dirname "$(realpath "$0")")")
cd "$project_dir"

dict_file=".cspell/custom-dictionary.txt"
tmp_file="$(mktemp)"
merged_file="$(mktemp)"

echo "Regenerating custom dictionary for cspell..."

# Run cspell (ignore its exit code — nonzero just means unknown words found)
cspell_output=$(mktemp)
if ! cspell --config cspell.json \
  --no-progress --no-summary --words-only \
  "README.md" "CITATION.cff" \
  "docs/**/*" \
  "src/pynxtools/**/*.py" \
  "tests/**/*.py" \
  > "$cspell_output"; then
  :
fi

# Sort unique new findings
sort -u "$cspell_output" > "$tmp_file"

# Compute newly discovered words
if [[ -f "$dict_file" ]]; then
  new_words=$(comm -23 <(sort -u "$tmp_file") <(sort -u "$dict_file") || true)
else
  new_words=$(cat "$tmp_file")
fi

# Merge existing + new, ensuring nothing is lost
(cat "$dict_file" "$tmp_file" 2>/dev/null | sort -u) > "$merged_file"
mv "$merged_file" "$dict_file"

# Report
if [[ -n "$new_words" ]]; then
  echo "🆕 New words added to $dict_file:"
  echo "$new_words" | sed 's/^/  - /'
else
  echo "✅ No new words added."
fi

# Cleanup
rm -f "$tmp_file" "$cspell_output" "$merged_file"

echo "Done!"