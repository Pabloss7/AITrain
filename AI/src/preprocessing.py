import pandas as pd

def preprocess_player_match(player_df, reference_columns):
    player_df_encoded = pd.get_dummies(player_df, columns=categorical_columns)
    player_df_encoded = player_df_encoded.reindex(columns=reference_columns, fill_value=0)
    return player_df_encoded
    