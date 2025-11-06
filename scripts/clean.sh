#!/bin/sh

# Move to the project root (one level above scripts/)
cd "$(dirname "$0")/.."

# Find all 'out' directories anywhere in the project
# and delete everything inside them except PDFs
find . -type d -name out -exec find {} -type f ! -name '*.pdf' -delete \;

echo "Cleaned all 'out' folders (kept PDFs)."
