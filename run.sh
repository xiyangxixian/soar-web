#!/bin/bash
dir=`dirname $0`
chmod -R a+x $dir/soar
chmod -R a+w $dir/tmp
python $dir/soar-web.py