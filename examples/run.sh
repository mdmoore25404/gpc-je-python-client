#!/bin/bash

echo "purging any jobs leftover"
python3 jobpurge.py 
echo "loading example jobs"
python3 jobload.py
echo "starting workers"
python3 jobwork.py
