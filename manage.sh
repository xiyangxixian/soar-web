#!/bin/bash
dir=`dirname $0`
pybin='python'

function start(){
  if [[ "$(checkPid)" ]]; then
    echo 'soar web is running'
  else
    chmod -R a+x $dir/soar
    chmod -R a+w $dir/tmp
    chmod -R a+w $dir/data
    chmod -R a+w $dir/static/data
    nohup $pybin $dir/soar-web.py > /dev/null 2>&1 &
    echo 'soar web start ....... ok'
  fi
}

function stop(){
  pid=$(checkPid)
  if [[ "$pid" ]]; then
    kill -9 $pid
  fi
  echo 'soar web stop ....... ok'
}

function restart() {
    stop
    start
}

function checkPid(){
  ps ax | grep soar-web.py | grep -v grep  | awk '{print $1}'
}

if [[ "$1" ]]; then
  $1
fi
