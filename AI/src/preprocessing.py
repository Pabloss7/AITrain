import pandas as pd

def preprocess_player_match(player_df, reference_columns):
    player_df_encoded = player_df.reindex(columns=reference_columns, fill_value=0)
    print("Player dataset encoded: \n", player_df_encoded)
    return player_df_encoded
    