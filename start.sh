#!/bin/bash

SCRIPT_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
#python3 -m venv imageenv
#source imageenv/bin/activate
#pip install -r $SCRIPT_PATH/requirements.txt > /dev/null

PORT=9999
lsof -i:$PORT | grep -v "PID" | awk '{print $2}' | xargs -r kill -9
sleep 1

cd $SCRIPT_PATH
nohup uvicorn main:app --reload --workers=4 --host 0.0.0.0 --port $PORT > $SCRIPT_PATH/uvicorn.log 2>&1 &
