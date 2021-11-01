pid=$(ps -ef | grep "mitm" | grep -v grep | awk '{print $2}')
kill -9 $pid