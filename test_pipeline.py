import unittest
import pandas as pd
from pandas.testing import assert_series_equal

from cricket_pipeline import global_pipeline_methods
from cricket_pipeline.ingest_cricket_data import *
from cricket_pipeline.predictor import *


class TestPipelineMethods(unittest.TestCase):
    def setUp(self):
        self.predictor = Predictor()
        self.data_folder_path = './data/'
        self.cricket_data = IngestCricketData(data_folder_path=self.data_folder_path)

    ## global_pipeline_methods.py
    def test_return_astype_df(self):
        sample_df = pd.DataFrame({
            'team': ['Australia'],
            'innings': [1],
            'remaining_overs': [46.1],
            'remaining_wickets': [10],
            'runs_scored': [int(1)] # Should be 'category'
        })
        sample_df = global_pipeline_methods.return_astype_df(sample_df)
        self.assertIsNotNone(sample_df)
        self.assertIsInstance(sample_df, pd.DataFrame)
        self.assertEqual(sample_df.dtypes['runs_scored'], 'category')

    ## ingest_cricket_data.py
    def test_data_ingestion(self):
        self.assertIsNotNone(self.cricket_data)
        self.assertIsInstance(self.cricket_data, IngestCricketData)
        self.assertIsNotNone(self.cricket_data.innings_results_df, 'Innings results data not loaded.')
        self.assertIsNotNone(self.cricket_data.match_results_df, 'Match results data not loaded.')

    def test_return_remaining_overs(self):
        remaining_overs = self.cricket_data.return_remaining_overs(10.4)
        self.assertEqual(remaining_overs, '39.2')
    
    def test_calculate_remaining_wickets(self):
        inning_wickets_df = pd.Series([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
        remaining_wickets = self.cricket_data.calculate_remaining_wickets(inning_wickets_df)
        self.assertIsNotNone(remaining_wickets)
        self.assertIsInstance(remaining_wickets, pd.Series)
        assert_series_equal(remaining_wickets, pd.Series([10, 9, 9, 8, 8, 7, 7, 6, 6, 5]))

    ## predictor.py
    def test_predictor_initialization(self):
        self.assertIsNotNone(self.predictor)
        self.assertIsInstance(self.predictor, Predictor)

    def test_filter_selected_matches_final_data(self):
        self.cricket_data.save_intermediate_data_to_csv()
        self.predictor.filter_selected_matches_final_data(team_names='Australia', number_of_overs=5)
        self.assertEqual(['Australia'], self.predictor.selected_matches_final_data_df['team'].unique())
        self.assertEqual(30, len(self.predictor.selected_matches_final_data_df))
    
    def test_predict_runs_scored(self):
        self.cricket_data.save_intermediate_data_to_csv()
        self.predictor.filter_selected_matches_final_data(team_names='Australia', number_of_overs=5)
        self.predictor.train_model()
        self.predictor.predict_runs_scored()
        self.assertIsNotNone(self.predictor.y_pred)
        self.assertEqual(30, len(self.predictor.y_pred))

    if __name__ == '__main__':
        unittest.main()