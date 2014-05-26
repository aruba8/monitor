#!/bin/bash
#

mkdir -p logs_app/old

CURRPATH=$(pwd)
export PYTHONPATH=${CURRPATH}:${CURRPATH}/db:${CURRPATH}/workers:${CURRPATH}/utils

PROGRAM="app.py"
CURDATE=$(date +"%Y_%m_%d_%H%M%S")
LOGFILE=monitor.log
JA_PID=monitor.pid
PROG_BIN="python $PROGRAM"
PID=`ps -aef | grep "$PROGRAM" | grep -v grep | awk '{print $2}'`

#move logs modified more than 24h ago to logs/old folder
#find logs_app/ -maxdepth 1 -type f -mtime +1 -name "*.log*" -exec mv {} logs_app/old >/dev/null 2>&1 \;


case "$1" in
  start)

    if [ ! -z ${PID} ]
    then
        echo -n " "
        echo -n "Server monitor is running"
        echo " "
    else
        echo -n "Starting server monitor: "
        echo ""
        ${PROG_BIN} > ${LOGFILE} 2>&1 &
        echo $! > ${JA_PID}
        echo "Server monitor started. PID:$!"
        echo "Logfile is : $LOGFILE"
        echo ""
    fi
    ;;
  stop)
    echo -n "Shutting down monitor server: "
    echo ""
    for i in ${PID}; do
        kill -9 ${i}
        rm -f ${JA_PID}
    done
    echo -n "Server monitor is down."
    echo ""
    ;;
  restart)
    $0 stop
    $0 start

    ;;
  status)
    STATUS=`ps -aef | grep "$PROGRAM" | grep -v grep | awk '{print $2}' | head -1`
    if [ ! -z ${STATUS} ]
    then
        echo -n "Server monitor is running"
        echo ""
        for i in ${PID}; do
            echo PID:${i}
        done
        echo ""
    else
        echo -n "Server monitor is down."
        echo ""
    fi
    ;;
  *)
    echo "Usage: monitor.sh {start|stop|restart|status}"
    exit 1

esac

exit 0