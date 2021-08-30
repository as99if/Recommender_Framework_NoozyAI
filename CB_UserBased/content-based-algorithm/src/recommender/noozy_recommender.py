"""
Created on 10 may 2021
gets recommendation with give algorithms
and
saves/store the results in a formatted manner

@author:     Asif Ahmed
"""
import logging
import pprint

import pytz
from algorithm import utils as util
from config.algorithm_config import AlgorithmConfig
from recommender.noozy_metadata_client.noozy_harvested_metadata_client import MetadataClient
from recommender.noozy_xapi_client.noozy_xapi_client import XapiClient

"""
Recommender Process
"""


class NoozyRecommender:

    def __init__(self) -> None:
        logging.debug("initializing recommender")
        self.algorithm = AlgorithmConfig()
        self.xapi_client = XapiClient()
        metadata_parameters = self.algorithm.get_dependant_data_parameters_from_input()

        algorithm_id = self.algorithm.get_algorithm_id_from_input()
        algorithm_type = self.algorithm.get_algorithm_type_from_input()

        date_range = self.algorithm.get_date_range()
        date = pytz.utc.localize(self.algorithm.get_date_from_input())
        self.metadata_client = MetadataClient(date=date)
        df_videos = self.metadata_client.get_all_video_metadata(parameters=metadata_parameters)

        # preprocess
        date_range = self.algorithm.get_date_range()
        df_videos = util.metadata_clean(df_videos, metadata_parameters)

        df_stats = self.xapi_client.get_terminated_statements()
        df_stats = util.xapi_data_clean(df_stats)
        merge = util.merge_data(df_stats, df_videos)
        view_matrix = util.create_view_matrix(merge)


        # for content based

        description_sim_matrix = util.create_tf_idf_cosine_matrix(df_videos, on="description")
        thematic_sim_matrix = util.create_tf_idf_cosine_matrix(df_videos, on="subject")

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
        """get_cb_videos_by_adv
                Returns a list of Hash keys # noqa: E501
                :param n: Number of returned videos
                :type n: int
                :param user_id: ID of the current user
                :required user_id: false
                :type user_id: str
                :param video_id: hash key of a video
                :required video_id: true
                :type video_id: str
                :rtype: Result : dict (NOT DATAFRAME)
                """

        # try:

        self.args.update({"video_id": video_id, "user_id": user_id})
        logging.debug(self.args)

        result = self.algorithm.run_algorithm(self.args)

        result = util.post_process(result, self.args["df_videos"], user_id=self.args["user_id"],
                                   merged_dataset=self.args["merged_data"],
                                   view_matrix=self.args["view_matrix"])

        result = util.process_diversity(result, n)
        result = util.get_result(result, n, algo_id=f'{self.args["algorithm_id"]}', user_id=self.args["user_id"])

        result = result.to_dict(orient="records")

        return result

    def get_all_user_id(self) -> list:
        logging.debug("getting all user ids from view matrix")
        list_users = self.args['view_matrix'].index.values.tolist()
        logging.debug(list_users)
        return list_users

    def get_all_video_id(self) -> list:
        logging.debug("getting all video ids from metadata")
        video_ids = self.metadata_client.get_all_video_id().values.tolist()
        logging.debug(video_ids)
        return video_ids

# user_id, merge, data, df_videos, view_matrix, n
