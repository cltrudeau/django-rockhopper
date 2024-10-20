#!/bin/bash

echo "============================================================"
echo "== pyflakes =="
pyflakes rockhopper | grep -v migration
