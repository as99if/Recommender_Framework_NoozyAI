"""
Created on 10 may 2021

Plug in algorithm module and map required parameters here.

gets recommendation with given algorithms
and
saves/store the results in a formatted manner

@author:     Asif Ahmed
"""
import datetime
import importlib
import os
import sys

import pandas as pd
import yaml


class AlgorithmConfig:
    def __init__(self) -> None:
        # get input
        path = os.path.dirname(sys.modules['__main__'].__file__)
        input_filename = os.path.join(path, "recommender_algorithm_input.yml")
        with open(input_filename) as input_file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            algo_config = yaml.load(input_file, Loader=yaml.FullLoader)
            # print(algo_config)

        input_data = algo_config['input']
        self.algorithm_id = input_data['algorithm_id']
        self.algorithm_type = input_data['algorithm_type']
        self.dependant_data_parameters = input_data['dependant_data_parameters']
        self.date_range_dependency = input_data['date_range_dependency']
        self.date_range_before = input_data['date_range_before']
        self.date_range_after = input_data['date_range_after']
        self.start_from = input_data['start_from']
        self.n = input_data['n']
        self.video_id_requirement = input_data['video_id_requirement']
        self.user_id_requirement = input_data['user_id_requirement']

        self.algorithm_package = "algorithm." + self.algorithm_id
        

    def run_algorithm(self, args) -> pd.DataFrame:
        """
        :param df_videos:
        :param video_id:
        :param user_id:
        :param merged_data:
        :param view_matrix:
        :return: recommendations
        """
        # TODO
        # from self.algorithm_package import self.algorithm_class_name as algorithm_module
        algorithm_module = importlib.import_module(self.algorithm_package, package=self.algorithm_id)
        algorithm_module_get_recommendation = getattr(algorithm_module, "get_recommendation")
        return algorithm_module_get_recommendation(args)

    def get_dependant_data_parameters_from_input(self) -> list:
        return self.dependant_data_parameters

    def get_algorithm_id_from_input(self) -> str:
        return self.algorithm_id

    def get_date_from_input(self) -> datetime.datetime:
        return datetime.datetime(year=self.start_from['year'], month=self.start_from['month'],
                                 day=self.start_from['day'])

    def get_video_id_requirement(self):
        return self.video_id_requirement

    def get_n_from_input(self) -> int:
        return self.n

    def get_algorithm_type_from_input(self) -> int:
        return self.algorithm_type

    def get_date_range(self):
        return {
            "before": self.date_range_before,
            "after": self.date_range_after
        }
