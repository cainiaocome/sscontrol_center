#!/usr/bin/env bash
# control alipaywatch and sscontrol_center

function process_name_to_pid
{
    if [ $# -ne 1 ];then
        echo "error, process_name_to_status need one and only one parameter"
        exit 1
    fi
    alipaywatch_process=`ps aux | grep -v grep | grep alipaywatch`
    if [ -z "$alipaywatch_process" ];then
        return 0
    else
        return -1
    fi
}
function start_job 
{
    echo "start"
}
function stop_job
{
    echo "stop"
}
function job_status
{
    echo "status"
}
#nohup ./alipaywatch.py >/dev/null 2>&1 &
#nohup ./sscontrol_center.py >/dev/null 2>&1 &
while getopts "a:" arg
do
    case "$arg" in
    "a")
        case "$OPTARG" in
        "start")
            start_job
            ;;
        "stop")
            stop_job
            ;;
        "status")
            job_status
            ;;
        esac
        ;;
    esac
done
