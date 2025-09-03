#!/usr/bin/env bash
set -euo pipefail
python3 src/main.py            # builds into docs/ with base "/"
cd docs && python3 -m http.server 8888
  