#!/bin/bash
#

mkdir -p logs_worker/old


PROGRAM="worker.py"
CURDATE=$(date +"%Y_%m_%d_%H%M%S")
LOGFILE=logs_worker/worker${CURDATE}.log
JA_PID=worker.pid
PROG_BIN="python $PROGRAM"
PID=`ps -aef | grep "$PROGRAM" | grep -v grep | awk '{print $2}'`

#move logs modified more than 24h ago to logs/old folder
find logs_worker/ -maxdepth 1 -type f -mtime +1 -name "*.log*" -exec mv {} logs_worker/old >/dev/null 2>&1 \;


case "$1" in
  start)

    if [ ! -z ${PID} ]
    then
        echo -n " "
        echo -n "Worker is running"
        echo " "
    else
        echo -n "Starting worker: "
        echo ""
        ${PROG_BIN} > ${LOGFILE} 2>&1 &
        echo $! > ${JA_PID}
        echo "Worker started. PID:$!"
        echo "Logfile is : $LOGFILE"
        echo ""
    fi
    ;;
  stop)
    echo -n "Shutting down worker: "
    echo ""
    for i in ${PID}; do
        kill -9 ${i}
        rm -f ${JA_PID}
    done
    echo -n "Worker is down."
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
        echo -n "Worker is running"
        echo ""
        for i in ${PID}; do
            echo PID:${i}
        done
        echo ""
    else
        echo -n "Worker is down."
        echo ""
    fi
    ;;
  *)
    echo "Usage: worker.sh {start|stop|restart|status}"
    exit 1

esac

exit 0
