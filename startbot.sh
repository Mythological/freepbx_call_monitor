#!/bin/bash

screen -dmS freepbx_monitor
screen -S freepbx_monitor -p 0 -X stuff "cd ~/freepbx_call_monitor$(printf \\r)"
screen -S freepbx_monitor -p 0 -X stuff "python3 missedcall.py$(printf \\r)"