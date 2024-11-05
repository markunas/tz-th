import pandas as pd
import warnings

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from .global_pipeline_methods import return_astype_df

class Predictor:
    default_data_folder_path = './data/'
    warnings.filterwarnings('ignore')

    def __init__(self, data_folder_path=default_data_folder_path):
        self.selected_matches_final_data_df = return_astype_df(pd.read_csv(data_folder_path+'selected_matches_final_data.csv'))
        self.trained_model = None

    def filter_selected_matches_final_data(self, team_names:str=None, number_of_overs:int=None):
        if team_names not in [None, [None]]:
            print(f'team_names: {team_names}')
            split_team_names_list = team_names.split()
            self.selected_matches_final_data_df = self.selected_matches_final_data_df[(self.selected_matches_final_data_df['team'].isin(split_team_names_list))]
        
        if number_of_overs is not None:
            print(f'number_of_overs: {number_of_overs}')
            self.selected_matches_final_data_df = self.selected_matches_final_data_df.iloc[:number_of_overs*6]

        self.update_self_X()
        self.update_self_y()

    def print_overs(self):
        print(self.selected_matches_final_data_df)

    def update_self_X(self):
        self.X = self.selected_matches_final_data_df.drop('runs_scored', axis = 1)
        self.X['team'] = self.X['team'].cat.codes
    
    def update_self_y(self):
        self.y = self.selected_matches_final_data_df['runs_scored']

    def train_model(self):
        self.update_self_X()
        self.update_self_y()

        random_forest_model = RandomForestClassifier(random_state=42)
        self.trained_model = random_forest_model.fit(self.X, self.y)
        print('Model trained successfully.')

    def predict_runs_scored(self):
        self.y_pred = self.trained_model.predict(self.X)
        print('Model predictions successful.')

    def print_predicted_model_accuracy(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.25, random_state=0)
        y_pred = self.trained_model.predict(X_test)
        print('\nPredicted model accuracy score: {0:0.5f}'. format(accuracy_score(y_test, y_pred)))

    def print_actual_model_accuracy_score(self):
        print('Actual model accuracy score: {0:0.5f}'. format(accuracy_score(self.y, self.y_pred)))
    
    def print_model_predictions(self):
        print(f'Model Predictions:\n{self.y_pred}')