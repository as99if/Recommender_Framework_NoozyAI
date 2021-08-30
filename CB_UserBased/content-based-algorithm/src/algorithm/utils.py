"""
Created on 10 may 2021

getResults : format the result list
merge_data : merge xapi statements and video metadata
create_view_matrix: creates matrix against xapi statements and video metadata


@author:     Asif Ahmed
"""
import logging
import pprint

import isodate
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

"""

"""


## pre-process

def xapi_data_clean(data_stats) -> pd.DataFrame:
    """
    :param data_stats:
    :return:
    """
    logging.debug("xapi data clean")
    df_stats = pd.json_normalize(data_stats)
    df_stats = df_stats.drop(columns=['id', 'stored', 'version', 'authority.objectType',
                                      'authority.account.homePage', 'authority.account.name', 'actor.objectType',
                                      'object.objectType'])
    df_stats = df_stats.rename(columns={'actor.mbox': 'actor_mbox', "verb.id": "verbIRI",
                                        "verb.display.en-US": "display", "object.id": "videoIRI",
                                        'context.extensions.https://smartvideo.fr/xapi/extensions/position': 'position'})

    #df_stats['userID'] = df_stats['actor_mbox'].str.findall('(\d+)').apply(''.join)
    #df_stats['dc:identifier'] = df_stats['videoIRI'].str.replace("https://smartvideo.fr/xapi/objects/video#", "")
    df_stats['dc:identifier'] = df_stats['videoIRI'].str.split('#').str[1]
    df_stats['userID'] = df_stats['actor_mbox'].str.split('#').str[1]
    df_stats['userID'] = df_stats['userID'].str.split('@').str[0]

    df_stats = df_stats.drop_duplicates(subset=['userID', 'dc:identifier'], keep='first')

    df_stats['position'] = df_stats.apply(conv_position, axis=1)
    df_stats = df_stats.dropna(axis=1)
    logging.info("xapi data cleaned")
    logging.debug(df_stats)
    return df_stats


def metadata_clean(metadata, metadata_parameters) -> pd.DataFrame:
    """
    pre-process metadata (DataFrame) according to algorithm id's mapped parameter
    :param metadata_parameters:
    :param metadata:
    :return: dataframe
    """

    logging.debug("metadata clean")
    for index, row in metadata.iterrows():
        metadata.loc[index, 'dc:genreID'] = row['dc:type'][0]['identifier']
        metadata.loc[index, 'dc:genre'] = row['dc:type'][0]['title']

    cols = ['dc:title', 'dc:source.title', 'dc:genre']

    for col in cols:
        metadata[col] = metadata[col].str.encode('latin-1').str.decode('utf-8')

    metadata = metadata.drop(columns=['dc:type'])
    logging.debug(metadata)
    return metadata


def merge_data(df_stats, df_videos) -> pd.DataFrame:

    logging.debug("gerge")
    merge = pd.merge(df_videos, df_stats, how='left', left_on='dc:identifier', right_on='dc:identifier',
                     suffixes=('_df_stats', '_df_videos'))  # error
    merge['bin_position'] = 0
    merge.loc[merge['position'] > 0.1, 'bin_position'] = 1
    # print("merged")
    logging.debug(merge)
    # pprint.pprint(merge[['dc:identifier', 'userID', 'bin_position']])
    # sys.exit()
    return merge


def create_view_matrix(merged_dataset) -> pd.DataFrame:
    logging.debug("generating view matrix")
    view_matrix = pd.pivot_table(
        merged_dataset, index="userID", columns='dc:identifier', values="bin_position", fill_value=0)
    # print(view_matrix)
    logging.debug(view_matrix)
    return view_matrix


##post-process


def post_process(result, df_videos, user_id=None, merged_dataset=None, view_matrix=None) -> pd.DataFrame:
    """
    :param result:
    :param df_videos:
    :param user_id:
    :param merged_dataset:
    :param view_matrix:
    :return:
    """
    topN = []

    # print(f"for {user_id}")
    # print(result)
    if user_id is not "None":
        topN = filter_videos_per_user(result['dc:identifier'], user_id, view_matrix)
    else:
        topN = result

    logging.debug("post-process")
    rst = pd.DataFrame(topN, columns=['dc:identifier'])
    # for score
    rst = pd.merge(rst, result, how='left', left_on='dc:identifier', right_on='dc:identifier')
    result = pd.merge(rst, df_videos, how='left', left_on='dc:identifier', right_on='dc:identifier')
    result = result[['dc:identifier', 'score', 'dc:available', 'dc:title', 'dc:source.title', 'dc:genre']]

    # print("after post process")
    logging.debug(result)
    return result


def filter_videos_per_user(sorted_keys, user_id, view_matrix) -> list:
    topN = []
    logging.debug("filter per user")
    # print(sorted_keys)
    for key in sorted_keys:
        try:
            if view_matrix.loc[user_id][key] == 0:
                topN.append(key)
        except KeyError:
            logging.debug("Invalid key " + key)
            # print("Invalid key " + key)
    # print("topN:")
    # print(topN)
    return topN


def process_diversity(result, N):
    logging.debug('adding diversity layer')
    result = result.drop_duplicates(subset=['dc:source.title'], keep='first')
    result = result.head(N)
    logging.debug(result)
    result = result[['dc:identifier', 'score']]

    return result


def get_result(result, N, algo_id, user_id: None) -> dict:
    """
    :param result: dataframe
    :param N:
    :param algo_id:
    :param user_id:
    :return: dict
    """
    result = result.rename(columns={'dc:identifier': 'video_id'})
    result['algorithmID'] = algo_id
    result['rank'] = [x for x in range(1, N + 1)]
    #result['score'] = [(1 - (x / N)) for x in range(N)]
    logging.debug('prepare results')
    logging.debug(result)
    return result


def conv_position(row):
    return isodate.parse_duration(row['position']).total_seconds()


def create_tf_idf_cosine_matrix(df_videos, on):
    """
    generates cosine similarity matrix against tf-idf scores
    :param on:
    :param df_videos: dataframe
    :return: cosine similarity matrix : dataframe
    """

    # Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
    # https://stackoverflow.com/questions/57359982/remove-stopwords-in-french-and-english-in-tfidfvectorizer
    # install nltk_data
    # https://github.com/gunthercox/ChatterBot/issues/930#issuecomment-322111087

    class LemmaTokenizer:
        ignore_tokens = [',', '.', ';', ':', '"', '``', "''", '`']

        def __init__(self):
            self.wnl = ()

        def __call__(self, doc):
            return [self.wnl.lemmatize(t) for t in word_tokenize(doc) if t not in self.ignore_tokens]

    logging.info("generating cosine sim matrix with tf-idf vectors")
    # nltk
    final_stopwords_list = stopwords.words('french')
    tokenizer = LemmaTokenizer()
    # https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
    tfidf = TfidfVectorizer(stop_words=final_stopwords_list,
                            tokenizer=None, preprocessor=None, analyzer='word')
    # tokenizer=tokenizer, preprocessor=None, analyzer='word')
    # print(df_videos[f'dc:{on}'])
    # Replace NaN with an empty string
    df_videos[f'dc:{on}'] = df_videos[f'dc:{on}'].fillna('')
    # keywords , actors, genre etc too
    df_videos[f'dc:{on}'] = df_videos[f'dc:{on}'].astype('str')
    # Construct the required TF-IDF matrix by fitting and transforming the data
    tfidf_matrix = tfidf.fit_transform(df_videos[f'dc:{on}'])

    cosine_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    # print(on)
    logging.debug("cosine sim matrix")
    logging.debug(cosine_sim_matrix)

    return cosine_sim_matrix


def get_last_seen_n_videos(user_id, n, merged_data, df_videos) -> list:
    logging.debug(f"getting last seen {n} videos - user_id: {user_id}")
    user_df = merged_data.loc[merged_data['userID'] == user_id]
    user_df = user_df[['dc:identifier', 'bin_position', 'dc:available']]
    # user_df = user_df.loc[user_df['bin_position'] > 0]
    user_df = user_df.sort_values(['dc:available'], ascending=False)
    user_df = user_df.sort_values(['bin_position'], ascending=False)
    user_df = user_df['dc:identifier']
    user_df = user_df.values.tolist()
    #print(f"S \n{user_df}\n{type(user_df)}")

    if len(user_df) < n or user_df is None:
        rst = df_videos.sort_values(by='dc:available', ascending=False)
        rst = rst['dc:identifier'].unique()
        #print(f"rst {rst}")
        rst = rst.tolist()
        rst = rst[:n]

        #print(f"voila {rst}\n{type(rst)}")
        if user_df is None:
            user_df = rst
        else:
            user_df = user_df + rst

        #print(f"x \n{user_df}\n{type(user_df)}")
    last_seen_n_videos = user_df[:n]
    return last_seen_n_videos