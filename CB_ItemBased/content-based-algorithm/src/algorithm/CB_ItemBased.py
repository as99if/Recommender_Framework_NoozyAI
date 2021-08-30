import logging

import pandas as pd


## TODO create variation - evaluate from noozy


def recommend(df_videos, video_id, sim_matrix, on="description"):
    """
    Gives a DataFrame of recommended video, similar to the given reference 'video_id',
    using TF-IDF vectores and cosine similarity matrix.
    Args:
        df_videos: (Dataframe) Metadata
        video_id: (String) Video Identifier
        sim_matrix: (Numpy Array)
        on: (String) Data field for similarity

    Returns:

    """
    indices = pd.Series(
        df_videos.index, index=df_videos['dc:identifier'])  # or 'videoID' # .drop_duplicates()
    # Get the index of the video that matches the hash key / video ID
    idx = indices[video_id]
    # Get the pair-wise similarity scores of all videos with that video
    sim_scores = list(enumerate(sim_matrix[idx]))
    # print(f"similarity score on {on}")

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    video_indices = [i[0] for i in sim_scores]
    score = [i[1] for i in sim_scores]
    # df_sim_score = pd.DataFrame.from_records(sim_scores, columns=['index', 'score'])
    # sim_scores = pd.DataFrame(sim_scores, columns=['sim_score'])
    # all the videos sorted by cosine similarity
    rst = df_videos['dc:identifier'].iloc[video_indices]

    result = pd.DataFrame({'dc:identifier': rst, 'score': score})

    result = result.iloc[1:]


    return result


def get_recommendation(args):
    """
    Args:
        args: (dict) all the necessary informations

    Returns: (DataFrame) Recommendation

    """

    result = None
    if args['algorithm_type'] == 'Basic':
        logging.debug("Description Based")
        result = recommend(args['df_videos'], args['video_id'],
                           sim_matrix=args['description_sim_matrix'], on="description")
        # main parameter for sorting is similarity of description
        # print(result)

    if args['algorithm_type'] == 'ThematicBased':
        logging.debug("Keyword Based")
        result = recommend(args['df_videos'], args['video_id'],
                           sim_matrix=args['thematic_sim_matrix'], on="thematic")
        # print(result)

    if args['algorithm_type'] == 'Hybrid':
        logging.debug("Hybrid")
        hybrid_sim_matrix = args['description_sim_matrix'].dot(args['thematic_sim_matrix'])
        result = recommend(args['df_videos'], args['video_id'],
                           sim_matrix=hybrid_sim_matrix, on="hybrid")
        # print(result)

    # print(result)
    return result
