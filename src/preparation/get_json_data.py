import pandas as pd

def jsons_to_dfs(file_name_list):
    df = pd.DataFrame()
    for file_name in file_name_list:
        df_temp = pd.read_json (file_name)
        df = pd.concat([df, df_temp], ignore_index=True)

    df = df.rename(columns={'headline': 'title', 'content': 'text'})

    return df