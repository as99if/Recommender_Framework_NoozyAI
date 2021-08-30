"""
Initiates recommender and does all the work from here.
Created on 10 may 2021
gets recommendation with give algorithms
and
saves/store the results in a formatted manner

@author:     Asif Ahmed
"""
import logging
import sys

import pytz
import pprint
from config.algorithm_config import AlgorithmConfig
from algorithm import utils as util
from recommender.noozy_metadata_client.noozy_harvested_metadata_client import MetadataClient
from recommender.noozy_xapi_client.noozy_xapi_client import XapiClient

"""
Recommender Process
"""


class NoozyRecommender:

    def __init__(self) -> None:
        """
        Initiates the recommender, picks upalgorithm configuration from yaml file, fetches metadata and xapi statements
        as per desire. Makes the data and informations ready for algorithm the generate predictions.
        """
        self.algorithm = AlgorithmConfig()
        self.xapi_client = XapiClient()
        metadata_parameters = self.algorithm.get_dependant_data_parameters_from_input()
        algorithm_id = self.algorithm.get_algorithm_id_from_input()
        algorithm_type = self.algorithm.get_algorithm_type_from_input()
        date_range = self.algorithm.get_date_range()
        date = pytz.utc.localize(self.algorithm.get_date_from_input())
        self.metadata_client = MetadataClient(date=date)

        ## data and knowledge collection
        df_videos = self.metadata_client.get_all_video_metadata(parameters=metadata_parameters)
        df_stats = self.xapi_client.get_terminated_statements()

        ## preprocess
        df_videos = util.metadata_clean(df_videos, metadata_parameters)
        df_stats = util.xapi_data_clean(df_stats)

        ## merge metadata and xapi staements to get a view matrix
        merge = util.merge_data(df_stats, df_videos)
        view_matrix = util.create_view_matrix(merge)

        ## desired similarity matrices
        description_sim_matrix = util.create_tf_idf_cosine_matrix(df_videos, on="description")
        thematic_sim_matrix = util.create_tf_idf_cosine_matrix(df_videos, on="subject")

        ## args is sent to the algorithm
        self.args = {
            "algorithm_id": algorithm_id,
            "algorithm_type": algorithm_type,
            "metadata_parameter": metadata_parameters,
            "date_range": date_range,
            "start_date": date,
            "df_videos": df_videos,
            "df_stats": df_stats,
            "merged_data": merge,
            "view_matrix": view_matrix,
            "description_sim_matrix": description_sim_matrix,
            "thematic_sim_matrix": thematic_sim_matrix,
        }
        # super(RecommenderEngine, self).__init__()

    def get_recommendation(self, n, video_id=None, user_id=None) -> dict:
        """
        video_id == None means, the algorithm is not itembased OR, recommendations are not saved with video_ids.
        'None' is not a video id.
        user_id == None means, unauthorised user. 'None' is an user_id.
        Args:
            n: (int) top max
            video_id: (String)
            user_id: (String)

        Returns:

        """
        ## all the information to send in the algorithm
        self.args.update({"video_id": video_id, "user_id": user_id})
        logging.debug(self.args)
        ## start the algorithm
        result = self.algorithm.run_algorithm(self.args)
        ## post-process recommendation results and filter per user
        result = util.post_process(result, self.args["df_videos"], user_id=user_id,
                                   merged_dataset=self.args["merged_data"],
                                   view_matrix=self.args["view_matrix"])
        ## diversity algorithm
        result = util.process_diversity(result, n)
        ## format result for serving
        result = util.get_result(result, n, algo_id=f'{self.args["algorithm_id"]}', user_id=user_id)
        result = result.to_dict(orient="records")

        return result

    def get_all_user_id(self) -> list:
        """
        Returns: (List) of all users from view matrix
        """
        logging.debug("getting all user ids from view matrix")
        list_users = self.args['view_matrix'].index.values.tolist()
        logging.debug(list_users)
        return list_users

    def get_all_video_id(self) -> list:
        """
        Returns: (List) of all video ids from metadata
        """
        logging.debug("getting all video ids from metadata")
        video_ids = self.metadata_client.get_all_video_id().values.tolist()
        logging.debug(video_ids)
        return video_ids

# user_id, merge, data, df_videos, view_matrix, n
