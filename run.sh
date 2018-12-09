#!/bin/bash
dir=`dirname $0`
chmod -R a+x $dir/soar
chmod -R a+w $dir/tmp
chmod -R a+w $dir/data
chmod -R a+w $dir/static/data
python $dir/soar-web.py