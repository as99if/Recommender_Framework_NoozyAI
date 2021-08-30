
import datetime
import logging

from recommender_algorithm_run import Run

logging.basicConfig(level=logging.DEBUG)
user_id = '14121898'
# user_id = 'None'
logging.info("Test starting for user: " + user_id)
a = datetime.datetime.now()
# for test before unit test
test = Run()
test.test(user_id)
logging.info('application ended')
b = datetime.datetime.now()
delta = b - a
logging.info("Propagation delay")
logging.info(str(int(delta.total_seconds() * 1000)) + " ms")
