#Get the data from sql database

from src.preparation.get_sql_data import get_articles
from src.preparation.get_json_data import jsons_to_dfs

from src.preprocessing.vectorize_tf_idf import vectorize_texts_tf_idf
import pandas as pd
from src.modelling.hierarchical import cluster

if __name__=="__main__":
    sources = ["HindustanTimes", "toi", "ie", "hindu"]
    in_data_dir = "data/input/"
    out_data_dir = "data/cluster_out/"
    json_files = [in_data_dir+f"{source}.json" for source in sources]
    for s in sources:
        get_articles(s, in_data_dir)
    
    article_df = jsons_to_dfs(json_files)

    vec = vectorize_texts_tf_idf(article_df.text,(1,3))

    h_cno = cluster(vec,len(vec)//4)

    article_df["cluster"] = h_cno

    article_df.sort_values(by=['cluster'], inplace=True)

    df_out = pd.DataFrame()

    df_out = article_df[["title","cluster"]].copy()

    df_out.to_csv(out_data_dir+"cluster_file.csv")




    
