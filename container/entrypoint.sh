#!/bin/sh
service supervisor start &&
cd /usr/src/app &&
python server.py
