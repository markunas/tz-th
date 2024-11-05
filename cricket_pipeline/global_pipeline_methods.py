import warnings

def return_astype_df(selected_matches_final_data_df):
    warnings.filterwarnings('ignore')
    selected_matches_final_data_df['team'] = selected_matches_final_data_df['team'].astype('category')
    selected_matches_final_data_df['innings'] = selected_matches_final_data_df['innings'].astype(int)
    selected_matches_final_data_df['remaining_overs'] = selected_matches_final_data_df['remaining_overs'].astype(float)
    selected_matches_final_data_df['remaining_wickets'] = selected_matches_final_data_df['remaining_wickets'].astype(int)
    selected_matches_final_data_df['runs_scored'] = selected_matches_final_data_df['runs_scored'].astype('category')
    return selected_matches_final_data_df