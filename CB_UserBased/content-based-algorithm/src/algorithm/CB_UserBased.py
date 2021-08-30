import algorithm.utils as util
import pandas as pd
import logging


## TODO

def recommend(df_videos, video_id, sim_matrix, on="description", date_range=None):
    """
        :param sim_matrix:
        :param on:
        :param df_videos: ["hash_key"]
        :param video_id: ["hash_key"]
        :param description_sim_matrix: tf-idf similarity matrix, dataframe
        :return:
        """
    '''
    if date_range['before'] is not None and date_range['after'] is not None:
        df_videos = util.filter_by_date_range(df_videos=df_videos,
                                              video_id=video_id,
                                              before=date_range['before'],
                                              after=date_range['after'])
    '''
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

    # result = result.reset_index()
    # result = result[['dc:identifier', 'score']]
    # print(f"content based recommendation on {on}")
    # print(result)
    # result = result[:20]
    return result


def get_recommendation(args):
    ref_videos = util.get_last_seen_n_videos(user_id=args['user_id'], n=3, merged_data=args['merged_data'],
                                             df_videos=args['df_videos'])
    logging.debug("reference videos: " + str(ref_videos))

    mixed_result = pd.DataFrame()
    for video_id in ref_videos:
        if args['algorithm_type'] == 'Basic':
            logging.debug("description based")
            result = recommend(args['df_videos'], video_id=video_id, sim_matrix=args['description_sim_matrix'],
                               on="description")
            # main parameter for sorting is similarity of description
            mixed_result = mixed_result.append(result)  # result_list.append(result)

        if args['algorithm_type'] == 'ThematicBased':
            logging.debug("Keyword based")
            result = recommend(args['df_videos'], video_id=video_id, sim_matrix=args['thematic_sim_matrix'],
                               on="thematic")
            # print(result)
            # print(f"result for {args['algorithm_type']} {video_id}")
            mixed_result = mixed_result.append(result)

        if args['algorithm_type'] == 'Hybrid':
            logging.debug("Hybrid")
            hybrid_sim_matrix = args['description_sim_matrix'].dot(args['thematic_sim_matrix'])
            result = recommend(args['df_videos'], video_id,
                               sim_matrix=hybrid_sim_matrix, on="hybrid")
            # print(result)
            # print(f"result for {args['algorithm_type']} {video_id}")
            mixed_result = mixed_result.append(result)

    mixed_result = mixed_result.drop_duplicates()
    mixed_result = mixed_result.sort_values('score', ascending=False)
    logging.debug(f"recommendation generated for user-id: {args['user_id']}")
    return mixed_result
