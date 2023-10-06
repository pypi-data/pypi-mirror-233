#!/bin/sh -e

# Set path to virtual environment.
export PREFIX=""
if [ -d 'venv' ] ; then
    export PREFIX="venv/bin/"
fi

set -x

# Run scrapper (output file should end in: website/cache.json).
${PREFIX}python ./scripts/scraper.py

# Copy to data file of rand_useragent python project.
cp ./website/cache.jsonl ./rand_useragent/data/browsers.jsonl
