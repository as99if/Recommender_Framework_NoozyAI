"""
Collects and process metadata from redis4harvest, with noozy_request.py
"""

import os
import sys

from .noozy_request import NoozyRequest
import datetime
import pytz
import json
import pprint
import pandas as pd


class MetadataClient:

    def __init__(self, parameters=None, date=None) -> None:
        """
        Args:
            parameters:
            date:
        """
        # request from harvested metadata from redis
        # gets all metadata first
        # tic = time.perf_counter()
        print("sending request for all metadata")
        self.metadata = NoozyRequest().get_items(date=date)

        # toc = time.perf_counter()
        # print(f"time : {toc - tic:0.4f} seconds")
        self.metadata = pd.json_normalize(self.metadata)
        # pprint.pprint(self.metadata)
        self._metadata = self.metadata
        print("fetched all video metadata from redis")

        filename = f'recommender/noozy_metadata_client/all_metadata_latest.json'
        path = os.path.dirname(sys.modules['__main__'].__file__)
        store_filename = os.path.join(path, filename)
        with open(store_filename, 'w') as outfile:
            json.dump(self._metadata.to_dict(orient="records"), outfile)


    def get_all_video_id(self) -> pd.DataFrame:
        """
        Returns:
        """
        print("getting identifiers")

        return self.metadata["dc:identifier"]

    def get_all_video_metadata(self, parameters=None):
        """
        Args:
            parameters:

        Returns:

        """
        return self.metadata[parameters]

    def get_all_video_metadata_by_genre(self, genre, parameters=None) -> pd.DataFrame:
        """
        Args:
            genre:
            parameters:
        """
        pass

    def get_all_video_metadata_by_keyword(self, keyword, parameters=None) -> pd.DataFrame:
        """
        Args:
            keyword:
            parameters:

        Returns:

        """
        pass

    def get_video_metadata_by_id(self, video_id) -> pd.DataFrame:
        """
        Args:
            video_id:

        Returns:

        """
        return self.metadata.loc["dc:identifier"] == video_id



