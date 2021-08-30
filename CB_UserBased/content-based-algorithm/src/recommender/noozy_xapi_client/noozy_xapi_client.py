import pandas as pd

import recommender.noozy_xapi_client.noozy_xapi_request as xapi_request


class XapiClient:

    def get_terminated_statements(self, since_date=None, until_date=None) -> pd.DataFrame:
        x = xapi_request.get_terminated_statements(since_date, until_date)
        # pprint.pprint(x)
        return xapi_request.get_terminated_statements(since_date, until_date)

    def get_completed_statements(self, since_date=None, until_date=None) -> pd.DataFrame:
        return xapi_request.get_completed_statements(since_date, until_date)
