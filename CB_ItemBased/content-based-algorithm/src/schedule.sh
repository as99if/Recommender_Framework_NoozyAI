#start schedule
echo ...executing `basename "$0"` 1>&2
python3 ./src/schedule.py
echo `basename "$0"` executed ! 1>&2
