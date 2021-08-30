import json
import logging
import os
import sys

import pandas as pd

from .noozy_request import NoozyRequest


class MetadataClient:

    def __init__(self, parameters=None, date=None) -> None:
        """
        :param parameters:
        :param date:
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
        logging.info("fetched all video metadata from redis")

        filename = f'recommender/noozy_metadata_client/all_metadata_latest.json'
        path = os.path.dirname(sys.modules['__main__'].__file__)
        store_filename = os.path.join(path, filename)
        with open(store_filename, 'w') as outfile:
            json.dump(self._metadata.to_dict(orient="records"), outfile)


    def get_all_video_id(self) -> pd.DataFrame:
        """
        :param date:
        :return: dataframe
        """
        # print("getting video identifiers")

        return self.metadata["dc:identifier"]

    def get_all_video_metadata(self, parameters=None):
        """
        :param parameters:
        :param date:
        :return: dataframe
        """
        return self.metadata[parameters]

    def get_video_metadata_by_id(self, video_id) -> pd.DataFrame:
        return self.metadata.loc["dc:identifier"] == video_id



