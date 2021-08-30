"""
Created on 10 may 2021

mapping and storing result

@author:     Asif Ahmed
"""

import json
import logging
import os
import sys
import time

from recommender.noozy_result_client.noozy_result_redis_client import NoozyResultStoreClient


class Store:

    def __init__(self, algorithm_id=None) -> None:
        self.start_timestamp = time.time()
        self.recomendations = []
        self.user_specific_recommendation_result = []
        self.algorithm_id = algorithm_id
        self.client = NoozyResultStoreClient()

        self.iterator = 0

    def append_result(self, result, n, user_id=None, video_id=None, genre=None, keyword=None) -> None:
        """
        return dict
        :param result: dataframe
        :param N:
        :param video_id:
        :param user_id:
        """
        recommendation = {
            "header": {
                # "algorithm_id": self.algorithm_id,
                "N": n,
                "user_id": user_id,
                "video_id": video_id,
                "timestamp": time.time()
            },
            "result": result
        }
        '''
        ### Extra - for evaluation

        _r = {
            "ref" : video_id,
            "result": result
        }
        if user_id is None or user_id is 'None':
            filename = f'results/forEvaluation-KeywordBased/recommendation_{video_id}_{self.algorithm_id}.json'
            path = os.path.dirname(sys.modules['__main__'].__file__)
            store_filename = os.path.join(path, filename)
            with open(store_filename, 'w') as json_file:
                json.dumps(_r, json_file)
        '''
        # pprint.pprint(recommendation)
        self.user_specific_recommendation_result.append(recommendation)

        # print(f"appending - {self.algorithm_id} - to - user : {user_id}")

    def put_item(self, user_id=None) -> bool:
        rec = {
            "user_id": user_id,
            self.algorithm_id: self.user_specific_recommendation_result
        }
        # for redis
        self.client.put_item(user_id=user_id, algorithm_id=self.algorithm_id,
                             item=self.user_specific_recommendation_result)

        # for json log file
        if len(self.recomendations) > 0:
            for item in self.recomendations:
                if item["user_id"] == user_id:
                    item[self.algorithm_id] = self.user_specific_recommendation_result
                    self.user_specific_recommendation_result = []
                    return True
            self.recomendations.append(rec)
            self.user_specific_recommendation_result = []
            return True
        else:
            self.recomendations.append(rec)
            self.user_specific_recommendation_result = []
            return True

    def log_store(self) -> bool:
        """
        :param keyword:
        :param genre:
        :param result: dataframe
        :param algorithm_id: recommendation algorithm ID
        :param n: number of result
        :param video_id: id of the video on which the result is based on
        :param user_id: id of the user on whom the result is based on
        :return: stores recommendation results into json for now
            for each user,
            "user_id" : {
                "header" : {},
                "results" : []
                }
        """
        try:
            finish_timestamp = time.time()
            recommendation_result = {
                "recommendation_results": self.recomendations,
                "process_start_timestamp": self.start_timestamp,
                "process_finish_timestamp": finish_timestamp
            }
            # recommendation = recommendation.to_json(orient="records")
            # pprint.pprint(recommendation_result)

            filename = f'results/recommendation_{self.algorithm_id}.json'
            path = os.path.dirname(sys.modules['__main__'].__file__)
            store_filename = os.path.join(path, filename)
            with open(store_filename, 'w') as json_file:
                json.dump(recommendation_result, json_file)

            logging.info("saved result " + store_filename)
            return True
        except KeyError:
            return False
