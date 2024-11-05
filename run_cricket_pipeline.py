import numpy as np
import sys, argparse

from cricket_pipeline.ingest_cricket_data import IngestCricketData
from cricket_pipeline.predictor import Predictor

# Prints the entire numpy array
np.set_printoptions(threshold=sys.maxsize)

def main(data_folder_path='../data/', ingest_data=False, ireland_test=False, overs=None, team_names=None, print_overs=False, print_accuracy_score=False, print_model_predictions=False, print_predicted_model_accuracy=False):
    ## 1. Ingest Cricket Data & Train Model on All Cricket Data
    if ingest_data:
        cricket_data = IngestCricketData(data_folder_path=data_folder_path)
        cricket_data.save_intermediate_data_to_csv()

    predictor = Predictor(data_folder_path=data_folder_path)
    predictor.train_model()
    if print_predicted_model_accuracy:
        predictor.print_predicted_model_accuracy()

    ## 2. Predict Runs Scored (optionally with subset of cricket data)
    if ireland_test:
        predictor.filter_selected_matches_final_data(team_names='Ireland', number_of_overs=5)
        print_overs = True
        print_model_predictions = True
    
    if (overs is not None) or (team_names is not None):
        predictor.filter_selected_matches_final_data(team_names=team_names, number_of_overs=overs)

    predictor.predict_runs_scored()

    if print_overs:
        predictor.print_overs()

    if print_model_predictions:
        predictor.print_model_predictions()

    if print_accuracy_score:
        predictor.print_actual_model_accuracy_score()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='1) Ingests cricket data from a local folder, 2) Saves intermediate cricket data in a CSV file, 3) Trains a model from that intermediate data.')
    parser.add_argument('-dfp', '--data-folder-path', type=str, default='./data/', help='Path to the data folder')
    parser.add_argument('-id', '--ingest-data', action='store_true', default=False, help='Ingest cricket data from the data folder')
    parser.add_argument('-it', '--ireland-test', action='store_true', default=False, help='Run the pipeline for Ireland test matches')
    parser.add_argument('-o', '--overs', type=int, default=None, help='Use only this number of overs in match data for prediction using the trained model. Example: --overs 5')
    parser.add_argument('-tn', '--team-names', type=str, default=None, help='Use only these team names (separated by a space) match data for prediction using trained model. Example: --team-names "India Australia"')
    parser.add_argument('-po', '--print-overs', action='store_true', default=False, help='Print the overs of the prediction data')
    parser.add_argument('-pa', '--print-accuracy-score', action='store_true', default=False, help='Print the accuracy score of the predictions')
    parser.add_argument('-pmp', '--print-model-predictions', action='store_true', default=False, help='Print the predictions of the trained model')
    parser.add_argument('-ppa', '--print-predicted-model-accuracy', action='store_true', default=False, help='Print the accuracy score of the predictive model using train/test split')
    args = parser.parse_args()
    main(data_folder_path=args.data_folder_path, ireland_test=args.ireland_test, overs=args.overs, team_names=args.team_names, print_overs=args.print_overs, print_accuracy_score=args.print_accuracy_score, print_model_predictions=args.print_model_predictions, print_predicted_model_accuracy=args.print_predicted_model_accuracy)