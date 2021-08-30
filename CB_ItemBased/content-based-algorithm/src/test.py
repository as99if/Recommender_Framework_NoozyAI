import datetime

from recommender_algorithm_run import Run
import sys
import logging

logging.basicConfig(level=logging.DEBUG)
logging.info("application started")
user_id = 'None'
logging.info("Test starting for user " + user_id)
a = datetime.datetime.now()
# for test before unit test
test = Run()
test.test(user_id)
logging.info('application ended')
b = datetime.datetime.now()
delta = b - a
logging.info("propagation delay")
logging.info(str(int(delta.total_seconds() * 1000)) + " ms")

