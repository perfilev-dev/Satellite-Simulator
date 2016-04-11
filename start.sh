#!/bin/bash
source venv/bin/activate
mongod -dbpath db/ &
python main.py