"""
Content based recommendation on all videos, for None user and for all user
Created on 10 may 2021
@author:     Asif Ahmed
"""
import datetime
import logging

from config.algorithm_config import AlgorithmConfig
from recommender.noozy_recommender import NoozyRecommender
from recommender.noozy_result_client.noozy_recommendation_store import Store


class Run:

    def test(self, user_id: None) -> None:
        """
            create AlgorithmConfig, NoozyRecommender and Store object
            which get input and configuration from yaml file, all metadata and xapi statements,
            cleans data, pre-process, generates view_matrix and similarity matrices
            for the whole session
            """
        algo = AlgorithmConfig()
        recommender = NoozyRecommender()
        store = Store(algorithm_id=algo.get_algorithm_id_from_input())

        n = algo.get_n_from_input()

        video_ids = ['None']
        if algo.get_video_id_requirement() == "required":
            video_ids = recommender.get_all_video_id()
        if algo.get_video_id_requirement() == "optional":
            video_ids.extend(recommender.get_all_video_id())

        logging.debug("user if: " + user_id)
        for video_id in video_ids:
            logging.debug("video id" + video_id)
            result = recommender.get_recommendation(n, user_id=user_id,
                                                    video_id=video_id if video_id != 'None' else None)

            # append with result of user_id  (KEY = user_id)
            store.append_result(result, n=n, user_id=user_id,
                                video_id=video_id if video_id != 'None' else None)
            # store all the result for user_id in repo
        store.put_item(user_id=user_id)

        # create and store result log
        store.log_store()


    def run(self) -> None:

        """
        create AlgorithmConfig, NoozyRecommender and Store object
        which get input and configuration from yaml file, all metadata and xapi statements,
        cleans data, pre-process, generates view_matrix and similarity matrices
        for the whole session
        """
        algo = AlgorithmConfig()
        recommender = NoozyRecommender()
        store = Store(algorithm_id=algo.get_algorithm_id_from_input())

        n = algo.get_n_from_input()

        video_ids = ['None']
        if algo.get_video_id_requirement() == "required":
            video_ids = recommender.get_all_video_id()
        if algo.get_video_id_requirement() == "optional":
            video_ids.extend(recommender.get_all_video_id())

        # unauthorised users (None) and authorised user
        user_ids = ["None"]
        user_ids.extend(recommender.get_all_user_id())

        # get recommendation list
        for user_id in user_ids:
            for video_id in video_ids:
                result=recommender.get_recommendation(n, user_id=user_id, video_id=video_id)
                # append with result of user_id  (KEY = user_id)
                store.append_result(result, n=n, user_id=user_id, video_id=video_id)
            # store all the result for user_id in repo
            store.put_item(user_id=user_id)

        # create and store result log
        store.log_store()
        # add all the print into log TODO


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('application starting')
    a = datetime.datetime.now()
    # for test before unit test
    run = Run()
    run.run()
    logging.info('application ended')
    b = datetime.datetime.now()
    delta = b - a
    logging.info("Propagation delay")
    logging.info(str(int(delta.total_seconds() * 1000)) + " ms")
