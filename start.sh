#!/usr/bin/env bash

nohup ./alipaywatch.py >/dev/null 2>&1 &
nohup ./sscontrol_center >/dev/null 2>&1 &
