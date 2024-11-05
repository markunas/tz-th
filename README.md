# Zelus/Teamworks Take Home
```
Phil Markunas
phil.markunas@gmail.com
```

## Setup
1. Add cricket data from Google Drive [link](https://drive.google.com/drive/folders/13INimKGJfEcXooZhKMoM4U_cZV2k6TTU?usp=sharing) to /data folder in root of repo (it will be ignored via .gitignore)
2. Start Docker on your machine (download via https://www.docker.com/products/docker-desktop/ if needed)
3. Install Docker image: `docker build -t cricket .`
4. Run desired CLI commands on Docker container: `docker-compose run --rm app sh -c "python <CLI command>"`

## Data
* Data from Google Drive [link](https://drive.google.com/drive/folders/13INimKGJfEcXooZhKMoM4U_cZV2k6TTU?usp=sharing) (the same data provided by the take-home assignment) is by default accessed in a /data folder in the root of the repo
* The following files must be included:
    * innings_results.json
    * match_results.json
* The pipeline will save intermediate data in a CSV file named `selected_matches_final_data.csv` in the same /data folder
* The model is trained on the entirety of this `selected_matches_final_data.csv` data file

## Model
* The model is a simple sklearn RandomForestClassifier

## Supported CLI Commands
This code comde with a top-level run_cricket_pipeline.py with the following arguments (accessible via --help):
```
usage: run_cricket_pipeline.py [-h] [-dfp DATA_FOLDER_PATH] [-id] [-it] [-o OVERS] [-tn TEAM_NAMES] [-po] [-pa] [-pmp] [-ppa]

1) Ingests cricket data from a local folder, 2) Saves intermediate cricket data in a CSV file, 3) Trains a model from that intermediate data.

options:
  -h, --help            show this help message and exit
  -dfp DATA_FOLDER_PATH, --data-folder-path DATA_FOLDER_PATH
                        Path to the data folder
  -id, --ingest-data    Ingest cricket data from the data folder
  -it, --ireland-test   Run the pipeline for Ireland test matches
  -o OVERS, --overs OVERS
                        Use only this number of overs in match data for prediction using the trained model. Example: --overs 5
  -tn TEAM_NAMES, --team-names TEAM_NAMES
                        Use only these team names (separated by a space) match data for prediction using trained model. Example: --team-names "India Australia"
  -po, --print-overs    Print the overs of the prediction data
  -pa, --print-accuracy-score
                        Print the accuracy score of the predictions
  -pmp, --print-model-predictions
                        Print the predictions of the trained model
  -ppa, --print-predicted-model-accuracy
                        Print the accuracy score of the predictive model using train/test split
```

The model is always trained on all provided data, but you can predict on a subset of the existing data, or provide an entirely new dataset for prediction by setting a different data folder path.

### Testing
* Run requested "Ireland 5 overs" test from the take-home instructions: `docker-compose run --rm app sh -c "python run_cricket_pipeline.py --ireland-test"`
* Run all Python unit tests: `docker-compose run --rm app sh -c "python -m unittest test_pipeline.TestPipelineMethods"`
* Run specific unit tests: `docker-compose run --rm app sh -c “python -m unittest test_pipeline.TestPipelineMethods.<name of test function>”`

### Data Ingestion
* Ingests data with a new data folder path: `docker-compose run --rm app sh -c "python run_cricket_pipeline.py --ingest-data --data-folder-path './new_data_folder/'"`
* If you exclude the `--ingest-data` flag (after having already run it once), this will allow you to run other commands (like predictions) without ingesting the data again (which is a time-consuming step)

### Train Model
* Run pipeline and train model using the entire dataset: `docker-compose run --rm app sh -c "python run_cricket_pipeline.py`

### Predict on a Subset of Data
* Using the trained model, predicts on a subset of overs (integer) and teams (separate teams with a space): `docker-compose run --rm app sh -c "python run_cricket_pipeline.py --overs 20 --teams 'India Australia'"`
* You can test on an entirely different dataset if you create a new `selected_matches_final_data.csv` and set a different `--data-folder-path` than the default without using the `--ingest-data` flag (so you'll predict without data ingestion)

### Print Results
* Using the same patterns outlined above, you can:
    * `--print-overs`: Prints out the dataframe for overs, including actual runs_scored so you can directly compare actual to predicted
    * `--print-model-predictions`: Prints out the model's runs_scored per delivery predictions
    * `--print-accuracy-score`: Compares predicted runs_scored versus actual runs_scored
    * `--print-predicted-model-accuracy`: Does a 75%/25% train/test split and gives predicted model accuracy using cross-validation
