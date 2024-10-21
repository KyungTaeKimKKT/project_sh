#!/bin/sh
echo "Run Background Job"

python 기상청.py & python 생산모니터링.py & python asyncPing.py