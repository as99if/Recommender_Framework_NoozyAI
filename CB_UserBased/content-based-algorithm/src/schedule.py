'''
Created on 6 mars 2021
schedule module

It consists on applying recommendation by executing the algorithm modules
and storing the recommendation results into a REDIS repository.

The recommendation process is scheduled

Usage:
    $ pyhon schedule.py [(-f or --from) (scratch or former)] [(-i or --ini) <config filename>]
Example :
    $ python schedule.py --from scratch --ini noozy.ini

@author:     Azim Roussanaly
@copyright:  2021 LORIA/Université de Lorraine. All rights reserved.
@license:    GNU General Public License, Version 3
@contact:    azim.roussanaly@loria.fr
@deffield    updated: Mar, 05, 2021


@author:     Azim Roussanaly
@copyright:  2021 LORIA/Université de Lorraine. All rights reserved.
@license:    GNU General Public License, Version 3
@contact:    azim.roussanaly@loria.fr


@deffield    updated: Aug, 2021
@by: Olfa Messaoud
'''

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import sys
import os
import logging
import datetime
from recommender_algorithm_run import Run


LOG_FILE = './src/noozy.log'


# ===============================================================================
# recommendation
# ===============================================================================
def process():
    try:
        logging.info('Recommendation starting')
        a = datetime.datetime.now()
        Run.run()
        logging.info('Recommendation ended')
        b = datetime.datetime.now()
        delta = b - a
        logging.info(str(int(delta.total_seconds() * 1000)) + " ms")

        with open(LOG_FILE, "a") as fin:
            fin.write("Schedule Terminated Successfully for " +
                      datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + "\n")

    except Exception as e:
        logging.error("Error : Recommendation failed !")
        logging.error(e.args)
    # update the last recommendation date



# ===============================================================================
# main function
# ===============================================================================
def main():
    '''
    standalone recommendation process
    :param datetime start : the starting date for harvesting
    :param str filename : the file where the timestamp of the last harvesting is stored
    '''
    logging.info("Starting a new Recommendation...")
    # here the main process can start
    process()
    logging.info("Done !")
    return 0


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    scheduler = BlockingScheduler(timezone='Europe/Paris')
    scheduler.add_job(main, trigger='cron', day='*', hour='4', minute='00')


    try:
        scheduler.start()
        logging.info("Recommendation scheduled...")
    except (KeyboardInterrupt, SystemExit):
        logging.warning("Schedule interrupted")
