from unittest import TestCase

from src.noozy_recommender_engine import RecommenderEngine


class TestRecommenderEngine(TestCase):
    def test_get_recommendation(self):
        algorithm_id = 'content_based'
        n = 10
        video_id = 'rLRW4BTrYx'
        user_id = '12325334'
        recommender_engine = RecommenderEngine()
        result = recommender_engine.get_recommendation(algorithm_id, n, video_id, user_id=user_id)
        print(result)
        #self.assertTrue(recommender_engine.get_recommendation(algorithm_id, n, video_id, user_id=user_id))

