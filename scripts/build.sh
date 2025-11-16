#!/bin/sh

# example usage: ./scripts/build.sh seminar_1/seminar-1-report.tex

# Ensure an argument was given
if [ $# -eq 0 ]; then
  echo "Usage: $0 path/to/filename.tex"
  exit 1
fi

# Full path to the .tex file (relative or absolute)
TEXFILE="$1"

# Directory containing the .tex file
TEXDIR=$(dirname "$TEXFILE")

# Base filename without extension
BASENAME=$(basename "$TEXFILE" .tex)

# Output directory inside that folder
OUTDIR="$TEXDIR/out"

# Create the output directory if it doesn't exist
mkdir -p "$OUTDIR"

# Run pdflatex twice for references/TOC
pdflatex -interaction=nonstopmode -output-directory="$OUTDIR" "$TEXFILE"
pdflatex -interaction=nonstopmode -output-directory="$OUTDIR" "$TEXFILE"

echo "Built PDF: $OUTDIR/$BASENAME.pdf"
