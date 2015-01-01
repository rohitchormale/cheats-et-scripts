#!/bin/bash
lockfile=/var/tmp/lock
if ( set -o noclobber; echo "$$" > "$lockfile") 2> /dev/null; then
    trap 'rm -f "$lockfile"; exit $?' INT TERM EXIT
        # run job
        # ...
else
    echo "Lock Exists: $lockfile owned by $(cat $lockfile)"    
fi

#source
#http://unix.stackexchange.com/questions/22044/correct-locking-in-shell-scripts

