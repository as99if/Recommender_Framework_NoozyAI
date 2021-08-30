#!/usr/bin/env python
# coding: utf-8


import configparser
import json
import os
import sys

import requests
from requests.auth import HTTPBasicAuth

# TODO python module for xapi - terminated and connected statement

filepath = os.path.join(os.path.dirname(sys.modules['__main__'].__file__), "config/noozy.ini")


def get_all_statements(since_date=None, until_date=None):
    headers = {
        "X-Experience-API-Version": "1.0.3",
        "Content-Type": "application/json",
    }

    config = configparser.ConfigParser()
    config.read(filepath)
    coords = config["STATEMENTS"]

    url = "http://" + coords["Host"]
    user = coords["User"]
    password = coords["Password"]

    params = {}

    if since_date is not None and until_date is None:
        params = {"since": since_date}

    if since_date is not None and until_date is not None:
        params = {"since": since_date, "until": until_date}

    discover_api = requests.get(
        url, headers=headers, params=params, auth=HTTPBasicAuth(user, password)
    ).json()
    data_stats = discover_api["statements"]

    while discover_api.get("more"):
        discover_api = requests.get(
            discover_api["more"],
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(user, password),
        ).json()
        data_stats.extend(discover_api["statements"])

    return data_stats


def get_connected_statements(since_date=None, until_date=None):
    headers = {  # headers dict to send in request
        "X-Experience-API-Version": "1.0.3",
        "Content-Type": "application/json",
    }

    config = configparser.ConfigParser()
    config.read(filepath)
    coords = config["STATEMENTS"]

    url = "http://" + coords["Host"]
    user = coords["User"]
    password = coords["Password"]

    verb = "https://smartvideo.fr/xapi/verbs/connected"

    if since_date is None and until_date is None:
        params = {"verb": verb}

    if since_date is not None and until_date is None:
        params = {"verb": verb, "since": since_date}

    if since_date is not None and until_date is not None:
        params = {"verb": verb, "since": since_date, "until": until_date}

    discover_api = requests.get(
        url, headers=headers, params=params, auth=HTTPBasicAuth(user, password)
    ).json()
    data_stats = discover_api["statements"]

    while discover_api.get("more"):
        discover_api = requests.get(
            discover_api["more"],
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(user, password),
        ).json()
        data_stats.extend(discover_api["statements"])

    return data_stats


def get_searched_statements(since_date=None, until_date=None):
    headers = {  # headers dict to send in request
        "X-Experience-API-Version": "1.0.3",
        "Content-Type": "application/json",
    }

    config = configparser.ConfigParser()
    config.read(filepath)
    coords = config["STATEMENTS"]

    url = "http://" + coords["Host"]
    user = coords["User"]
    password = coords["Password"]

    verb = "https://smartvideo.fr/xapi/verbs/searched"

    if since_date is None and until_date is None:
        params = {"verb": verb}

    if since_date is not None and until_date is None:
        params = {"verb": verb, "since": since_date}

    if since_date is not None and until_date is not None:
        params = {"verb": verb, "since": since_date, "until": until_date}

    discover_api = requests.get(
        url, headers=headers, params=params, auth=HTTPBasicAuth(user, password)
    ).json()
    data_stats = discover_api["statements"]

    while discover_api.get("more"):
        discover_api = requests.get(
            discover_api["more"],
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(user, password),
        ).json()
        data_stats.extend(discover_api["statements"])

    return data_stats


def get_selected_statements(since_date=None, until_date=None):
    headers = {  # headers dict to send in request
        "X-Experience-API-Version": "1.0.3",
        "Content-Type": "application/json",
    }

    config = configparser.ConfigParser()
    config.read(filepath)
    coords = config["STATEMENTS"]

    url = "http://" + coords["Host"]
    user = coords["User"]
    password = coords["Password"]

    verb = "https://smartvideo.fr/xapi/verbs/selected"

    if since_date is None and until_date is None:
        params = {"verb": verb}

    if since_date is not None and until_date is None:
        params = {"verb": verb, "since": since_date}

    if since_date is not None and until_date is not None:
        params = {"verb": verb, "since": since_date, "until": until_date}

    discover_api = requests.get(
        url, headers=headers, params=params, auth=HTTPBasicAuth(user, password)
    ).json()
    data_stats = discover_api["statements"]

    while discover_api.get("more"):
        discover_api = requests.get(
            discover_api["more"],
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(user, password),
        ).json()
        data_stats.extend(discover_api["statements"])

    return data_stats


def get_shared_statements(since_date=None, until_date=None):
    headers = {  # headers dict to send in request
        "X-Experience-API-Version": "1.0.3",
        "Content-Type": "application/json",
    }

    config = configparser.ConfigParser()
    config.read(filepath)
    coords = config["STATEMENTS"]

    url = "http://" + coords["Host"]
    user = coords["User"]
    password = coords["Password"]

    verb = "https://smartvideo.fr/xapi/verbs/shared"

    if since_date is None and until_date is None:
        params = {"verb": verb}

    if since_date is not None and until_date is None:
        params = {"verb": verb, "since": since_date}

    if since_date is not None and until_date is not None:
        params = {"verb": verb, "since": since_date, "until": until_date}

    discover_api = requests.get(
        url, headers=headers, params=params, auth=HTTPBasicAuth(user, password)
    ).json()
    data_stats = discover_api["statements"]

    while discover_api.get("more"):
        discover_api = requests.get(
            discover_api["more"],
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(user, password),
        ).json()
        data_stats.extend(discover_api["statements"])

    return data_stats


def get_liked_statements(since_date=None, until_date=None):
    headers = {  # headers dict to send in request
        "X-Experience-API-Version": "1.0.3",
        "Content-Type": "application/json",
    }

    config = configparser.ConfigParser()
    config.read(filepath)
    coords = config["STATEMENTS"]

    url = "http://" + coords["Host"]
    user = coords["User"]
    password = coords["Password"]

    verb = "https://smartvideo.fr/xapi/verbs/liked"

    if since_date is None and until_date is None:
        params = {"verb": verb}

    if since_date is not None and until_date is None:
        params = {"verb": verb, "since": since_date}

    if since_date is not None and until_date is not None:
        params = {"verb": verb, "since": since_date, "until": until_date}

    discover_api = requests.get(
        url, headers=headers, params=params, auth=HTTPBasicAuth(user, password)
    ).json()
    data_stats = discover_api["statements"]

    while discover_api.get("more"):
        discover_api = requests.get(
            discover_api["more"],
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(user, password),
        ).json()
        data_stats.extend(discover_api["statements"])

    return data_stats


def get_rated_statements(since_date=None, until_date=None):
    headers = {  # headers dict to send in request
        "X-Experience-API-Version": "1.0.3",
        "Content-Type": "application/json",
    }

    config = configparser.ConfigParser()
    config.read(filepath)
    coords = config["STATEMENTS"]

    url = "http://" + coords["Host"]
    user = coords["User"]
    password = coords["Password"]

    verb = "https://smartvideo.fr/xapi/verbs/rated"

    if since_date is None and until_date is None:
        params = {"verb": verb}

    if since_date is not None and until_date is None:
        params = {"verb": verb, "since": since_date}

    if since_date is not None and until_date is not None:
        params = {"verb": verb, "since": since_date, "until": until_date}

    discover_api = requests.get(
        url, headers=headers, params=params, auth=HTTPBasicAuth(user, password)
    ).json()
    data_stats = discover_api["statements"]

    while discover_api.get("more"):
        discover_api = requests.get(
            discover_api["more"],
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(user, password),
        ).json()
        data_stats.extend(discover_api["statements"])

    return data_stats


def get_annotated_statements(since_date=None, until_date=None):
    headers = {  # headers dict to send in request
        "X-Experience-API-Version": "1.0.3",
        "Content-Type": "application/json",
    }

    config = configparser.ConfigParser()
    config.read(filepath)
    coords = config["STATEMENTS"]

    url = "http://" + coords["Host"]
    user = coords["User"]
    password = coords["Password"]

    verb = "https://smartvideo.fr/xapi/verbs/annotated"

    if since_date is None and until_date is None:
        params = {"verb": verb}

    if since_date is not None and until_date is None:
        params = {"verb": verb, "since": since_date}

    if since_date is not None and until_date is not None:
        params = {"verb": verb, "since": since_date, "until": until_date}

    discover_api = requests.get(
        url, headers=headers, params=params, auth=HTTPBasicAuth(user, password)
    ).json()
    data_stats = discover_api["statements"]

    while discover_api.get("more"):
        discover_api = requests.get(
            discover_api["more"],
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(user, password),
        ).json()
        data_stats.extend(discover_api["statements"])

    return data_stats


def get_added_to_statements(since_date=None, until_date=None):
    headers = {  # headers dict to send in request
        "X-Experience-API-Version": "1.0.3",
        "Content-Type": "application/json",
    }

    config = configparser.ConfigParser()
    config.read(filepath)
    coords = config["STATEMENTS"]

    url = "http://" + coords["Host"]
    user = coords["User"]
    password = coords["Password"]

    verb = "https://smartvideo.fr/xapi/verbs/added-to-playlist"

    if since_date is None and until_date is None:
        params = {"verb": verb}

    if since_date is not None and until_date is None:
        params = {"verb": verb, "since": since_date}

    if since_date is not None and until_date is not None:
        params = {"verb": verb, "since": since_date, "until": until_date}

    discover_api = requests.get(
        url, headers=headers, params=params, auth=HTTPBasicAuth(user, password)
    ).json()
    data_stats = discover_api["statements"]

    while discover_api.get("more"):
        discover_api = requests.get(
            discover_api["more"],
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(user, password),
        ).json()
        data_stats.extend(discover_api["statements"])

    return data_stats


def get_deleted_from_statements(since_date=None, until_date=None):
    headers = {  # headers dict to send in request
        "X-Experience-API-Version": "1.0.3",
        "Content-Type": "application/json",
    }

    config = configparser.ConfigParser()
    config.read(filepath)
    coords = config["STATEMENTS"]

    url = "http://" + coords["Host"]
    user = coords["User"]
    password = coords["Password"]

    verb = "https://smartvideo.fr/xapi/verbs/deleted-from-playlist"

    if since_date is None and until_date is None:
        params = {"verb": verb}

    if since_date is not None and until_date is None:
        params = {"verb": verb, "since": since_date}

    if since_date is not None and until_date is not None:
        params = {"verb": verb, "since": since_date, "until": until_date}

    discover_api = requests.get(
        url, headers=headers, params=params, auth=HTTPBasicAuth(user, password)
    ).json()
    data_stats = discover_api["statements"]

    while discover_api.get("more"):
        discover_api = requests.get(
            discover_api["more"],
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(user, password),
        ).json()
        data_stats.extend(discover_api["statements"])

    return data_stats


def get_played_statements(since_date=None, until_date=None):
    headers = {  # headers dict to send in request
        "X-Experience-API-Version": "1.0.3",
        "Content-Type": "application/json",
    }

    config = configparser.ConfigParser()
    config.read(filepath)
    coords = config["STATEMENTS"]

    url = "http://" + coords["Host"]
    user = coords["User"]
    password = coords["Password"]

    verb = "https://smartvideo.fr/xapi/verbs/played"

    if since_date is None and until_date is None:
        params = {"verb": verb}

    if since_date is not None and until_date is None:
        params = {"verb": verb, "since": since_date}

    if since_date is not None and until_date is not None:
        params = {"verb": verb, "since": since_date, "until": until_date}

    discover_api = requests.get(
        url, headers=headers, params=params, auth=HTTPBasicAuth(user, password)
    ).json()
    data_stats = discover_api["statements"]

    while discover_api.get("more"):
        discover_api = requests.get(
            discover_api["more"],
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(user, password),
        ).json()
        data_stats.extend(discover_api["statements"])

    return data_stats


def get_paused_statements(since_date=None, until_date=None):
    headers = {  # headers dict to send in request
        "X-Experience-API-Version": "1.0.3",
        "Content-Type": "application/json",
    }

    config = configparser.ConfigParser()
    config.read(filepath)
    coords = config["STATEMENTS"]

    url = "http://" + coords["Host"]
    user = coords["User"]
    password = coords["Password"]

    verb = "https://smartvideo.fr/xapi/verbs/paused"

    if since_date is None and until_date is None:
        params = {"verb": verb}

    if since_date is not None and until_date is None:
        params = {"verb": verb, "since": since_date}

    if since_date is not None and until_date is not None:
        params = {"verb": verb, "since": since_date, "until": until_date}

    discover_api = requests.get(
        url, headers=headers, params=params, auth=HTTPBasicAuth(user, password)
    ).json()
    data_stats = discover_api["statements"]

    while discover_api.get("more"):
        discover_api = requests.get(
            discover_api["more"],
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(user, password),
        ).json()
        data_stats.extend(discover_api["statements"])

    return data_stats


def get_seeked_statements(since_date=None, until_date=None):
    headers = {  # headers dict to send in request
        "X-Experience-API-Version": "1.0.3",
        "Content-Type": "application/json",
    }

    config = configparser.ConfigParser()
    config.read(filepath)
    coords = config["STATEMENTS"]

    url = "http://" + coords["Host"]
    user = coords["User"]
    password = coords["Password"]

    verb = "https://smartvideo.fr/xapi/verbs/seeked"

    if since_date is None and until_date is None:
        params = {"verb": verb}

    if since_date is not None and until_date is None:
        params = {"verb": verb, "since": since_date}

    if since_date is not None and until_date is not None:
        params = {"verb": verb, "since": since_date, "until": until_date}

    discover_api = requests.get(
        url, headers=headers, params=params, auth=HTTPBasicAuth(user, password)
    ).json()
    data_stats = discover_api["statements"]

    while discover_api.get("more"):
        discover_api = requests.get(
            discover_api["more"],
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(user, password),
        ).json()
        data_stats.extend(discover_api["statements"])

    return data_stats


def get_terminated_statements(since_date=None, until_date=None):
    headers = {  # headers dict to send in request
        "X-Experience-API-Version": "1.0.3",
        "Content-Type": "application/json",
    }

    config = configparser.ConfigParser()
    '''TODO : fix this filepath issue'''

    config.read(filepath)

    coords = config["STATEMENTS"]

    url = "http://" + coords["Host"]
    user = coords["User"]
    password = coords["Password"]

    verb = "https://smartvideo.fr/xapi/verbs/terminated"

    if since_date is None and until_date is None:
        params = {"verb": verb}

    if since_date is not None and until_date is None:
        params = {"verb": verb, "since": since_date}

    if since_date is not None and until_date is not None:
        params = {"verb": verb, "since": since_date, "until": until_date}

    discover_api = requests.get(
        url, headers=headers, params=params, auth=HTTPBasicAuth(user, password)
    ).json()
    data_stats = discover_api["statements"]

    while discover_api.get("more"):
        discover_api = requests.get(
            discover_api["more"],
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(user, password),
        ).json()
        data_stats.extend(discover_api["statements"])

    return data_stats


def get_completed_statements(since_date=None, until_date=None):
    headers = {  # headers dict to send in request
        "X-Experience-API-Version": "1.0.3",
        "Content-Type": "application/json",
    }

    config = configparser.ConfigParser()
    config.read(filepath)
    coords = config["STATEMENTS"]

    url = "http://" + coords["Host"]
    user = coords["User"]
    password = coords["Password"]

    verb = "https://smartvideo.fr/xapi/verbs/completed"

    if since_date is None and until_date is None:
        params = {"verb": verb}

    if since_date is not None and until_date is None:
        params = {"verb": verb, "since": since_date}

    if since_date is not None and until_date is not None:
        params = {"verb": verb, "since": since_date, "until": until_date}

    discover_api = requests.get(
        url, headers=headers, params=params, auth=HTTPBasicAuth(user, password)
    ).json()
    data_stats = discover_api["statements"]

    while discover_api.get("more"):
        discover_api = requests.get(
            discover_api["more"],
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(user, password),
        ).json()
        data_stats.extend(discover_api["statements"])

    return data_stats


def get_statements_by_video(videoID, since_date=None, until_date=None):
    headers = {  # headers dict to send in request
        "X-Experience-API-Version": "1.0.3",
        "Content-Type": "application/json",
    }

    config = configparser.ConfigParser()
    config.read(filepath)
    coords = config["STATEMENTS"]

    url = "http://" + coords["Host"]
    user = coords["User"]
    password = coords["Password"]

    activity = "https://smartvideo.fr/xapi/objects/video#" + videoID

    if since_date is None and until_date is None:
        params = {"activity": activity}

    if since_date is not None and until_date is None:
        params = {"activity": activity, "since": since_date}

    if since_date is not None and until_date is not None:
        params = {
            "activity": activity,
            "since": since_date,
            "until": until_date,
        }

    discover_api = requests.get(
        url, headers=headers, params=params, auth=HTTPBasicAuth(user, password)
    ).json()
    data_stats = discover_api["statements"]

    while discover_api.get("more"):
        discover_api = requests.get(
            discover_api["more"],
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(user, password),
        ).json()
        data_stats.extend(discover_api["statements"])

    return data_stats


def get_terminated_statements_by_video(videoID,
                                       since_date=None,
                                       until_date=None):
    headers = {  # headers dict to send in request
        "X-Experience-API-Version": "1.0.3",
        "Content-Type": "application/json",
    }

    config = configparser.ConfigParser()
    config.read(filepath)
    coords = config["STATEMENTS"]

    url = "http://" + coords["Host"]
    user = coords["User"]
    password = coords["Password"]

    verb = "https://smartvideo.fr/xapi/verbs/terminated"
    activity = "https://smartvideo.fr/xapi/objects/video#" + videoID

    if since_date is None and until_date is None:
        params = {"verb": verb, "activity": activity}

    if since_date is not None and until_date is None:
        params = {"verb": verb, "activity": activity, "since": since_date}

    if since_date is not None and until_date is not None:
        params = {
            "verb": verb,
            "activity": activity,
            "since": since_date,
            "until": until_date,
        }

    discover_api = requests.get(
        url, headers=headers, params=params, auth=HTTPBasicAuth(user, password)
    ).json()
    data_stats = discover_api["statements"]

    while discover_api.get("more"):
        discover_api = requests.get(
            discover_api["more"],
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(user, password),
        ).json()
        data_stats.extend(discover_api["statements"])

    return data_stats


def get_statements_by_user(userID, since_date=None, until_date=None):
    headers = {  # headers dict to send in request
        "X-Experience-API-Version": "1.0.3",
        "Content-Type": "application/json",
    }

    config = configparser.ConfigParser()
    config.read(filepath)
    coords = config["STATEMENTS"]

    url = "http://" + coords["Host"]
    user = coords["User"]
    password = coords["Password"]

    actor = {"mbox": "mailto:user#" + userID + "@smartvideo.fr"}

    # convert into JSON:
    agent = json.dumps(actor)

    if since_date is None and until_date is None:
        params = {"agent": agent}

    if since_date is not None and until_date is None:
        params = {"agent": agent, "since": since_date}

    if since_date is not None and until_date is not None:
        params = {
            "agent": agent,
            "since": since_date,
            "until": until_date,
        }

    discover_api = requests.get(
        url, headers=headers, params=params, auth=HTTPBasicAuth(user, password)
    ).json()
    data_stats = discover_api["statements"]

    while discover_api.get("more"):
        discover_api = requests.get(
            discover_api["more"],
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(user, password),
        ).json()
        data_stats.extend(discover_api["statements"])

    return data_stats


def get_terminated_statements_by_user(userID,
                                      since_date=None,
                                      until_date=None):
    headers = {  # headers dict to send in request
        "X-Experience-API-Version": "1.0.3",
        "Content-Type": "application/json",
    }

    config = configparser.ConfigParser()
    config.read(filepath)
    coords = config["STATEMENTS"]

    url = "http://" + coords["Host"]
    user = coords["User"]
    password = coords["Password"]

    verb = "https://smartvideo.fr/xapi/verbs/terminated"
    actor = {"mbox": "mailto:user#" + userID + "@smartvideo.fr"}

    # convert into JSON:
    agent = json.dumps(actor)

    if since_date is None and until_date is None:
        params = {"agent": agent, "verb": verb}

    if since_date is not None and until_date is None:
        params = {"agent": agent, "verb": verb, "since": since_date}

    if since_date is not None and until_date is not None:
        params = {
            "agent": agent,
            "verb": verb,
            "since": since_date,
            "until": until_date,
        }

    discover_api = requests.get(
        url, headers=headers, params=params, auth=HTTPBasicAuth(user, password)
    ).json()
    data_stats = discover_api["statements"]

    while discover_api.get("more"):
        discover_api = requests.get(
            discover_api["more"],
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(user, password),
        ).json()
        data_stats.extend(discover_api["statements"])

    return data_stats
