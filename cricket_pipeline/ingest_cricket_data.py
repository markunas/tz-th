import warnings
import pandas as pd

from .global_pipeline_methods import return_astype_df

class IngestCricketData:
    default_data_folder_path = './data/'
    warnings.filterwarnings('ignore')

    def __init__(self, data_folder_path=default_data_folder_path):
        self.innings_results_df = pd.read_json(data_folder_path+'innings_results.json')
        self.match_results_df = pd.read_json(data_folder_path+'match_results.json')
        self.save_to_file = data_folder_path+'selected_matches_final_data.csv'

    def ingest_cricket_data_from_file(self):
        self.innings_results_df = pd.read_json('./data/innings_results.json')
        self.match_results_df = pd.read_json('./data/match_results.json')

    def calculate_remaining_wickets(self, inning_wickets_df):
        old_remaining_wickets_df = inning_wickets_df
        new_remaining_wickets_df = pd.Series(0, index=inning_wickets_df.index)
        new_remaining_wickets_df.iloc[0] = 10 - old_remaining_wickets_df.iloc[0]
        for i in range(1, len(new_remaining_wickets_df)):
            new_remaining_wickets_df.iloc[i] = new_remaining_wickets_df.iloc[i-1] - old_remaining_wickets_df.iloc[i]
        return new_remaining_wickets_df

    def return_test_inning(self, selected_matches_df):
        return selected_matches_df[(selected_matches_df['innings'] == 1) & (selected_matches_df.index == 997995)]

    def return_two_innings_per_match(self, selected_matches_df, match_id):
        inning_one_df = selected_matches_df[(selected_matches_df['innings'] == 1) & (selected_matches_df.index == match_id)]
        inning_two_df = selected_matches_df[(selected_matches_df['innings'] == 2) & (selected_matches_df.index == match_id)]
        return inning_one_df, inning_two_df

    def return_remaining_overs(self, over):
        remaining_overs = 50 - (over + 0.4)
        if remaining_overs % 1 > 0.5:
            remaining_overs = int(remaining_overs) + 1
        
        return "%.1f" % remaining_overs

    def save_intermediate_data_to_csv(self):
        male_match_ids_with_winner = self.match_results_df[(self.match_results_df['gender'] == 'male') & (self.match_results_df['outcome.winner'].notna())]['matchid']
        selected_matches_df = self.innings_results_df[self.innings_results_df['matchid'].isin(male_match_ids_with_winner)].set_index('matchid')
        selected_matches_df.index = selected_matches_df.index.astype(int)
        selected_matches_final_data_df = selected_matches_df[['team', 'innings', 'over', 'wicket.kind', 'runs.total']]
        selected_matches_final_data_df.rename(columns={
                'over': 'remaining_overs',
                'wicket.kind': 'remaining_wickets',
                'runs.total': 'runs_scored'
            }, inplace=True)
        
        try:
            selected_matches_final_data_df['remaining_overs'] = selected_matches_final_data_df['remaining_overs'].apply(lambda x: self.return_remaining_overs(x))
        except:
            print(selected_matches_final_data_df['remaining_overs'])
            print('Error in calculating remaining overs.')

        selected_matches_final_data_df['remaining_wickets'].fillna(0, inplace=True)
        selected_matches_final_data_df['remaining_wickets'][selected_matches_final_data_df['remaining_wickets'] != 0] = 1

        for match_id in selected_matches_final_data_df.index.unique():
            inning_one_df, inning_two_df = self.return_two_innings_per_match(selected_matches_final_data_df, match_id)
            new_inning_one_remaining_wickets = self.calculate_remaining_wickets(inning_one_df['remaining_wickets'])
            new_inning_two_remaining_wickets = self.calculate_remaining_wickets(inning_two_df['remaining_wickets'])
            match_wickets = pd.concat([new_inning_one_remaining_wickets, new_inning_two_remaining_wickets])
            selected_matches_final_data_df.loc[match_id, 'remaining_wickets'] = match_wickets

        selected_matches_final_data_astype_df = return_astype_df(selected_matches_final_data_df)

        selected_matches_final_data_astype_df.to_csv(self.save_to_file)
        print(f'Cricket match data saved to {self.save_to_file}')