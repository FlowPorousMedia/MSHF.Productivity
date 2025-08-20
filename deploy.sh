#!/bin/bash
cd /home/erythrocyte/progs/FlowPM.SimpleProdMSHF
git pull origin main
source /home/erythrocyte/.virtualenvs/simpleprod-env/bin/activate
pip install -r requirements.txt