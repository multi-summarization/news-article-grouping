import json
import requests
import os


def update_articles(title,content):
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTkzMTA0MDUsImlhdCI6MTYxOTIyNDAwNSwic3ViIjoxfQ.aigrpmZDzADk48FbxYgdpToxDJLugRiZukMHZDJNymc"

    URL =  "https://multi-news-summary.herokuapp.com/api/v1/"

    data = {
        "title": title,
        "contents": content
    }

    headers = {"api-token":token}
    
    URL_ARTICLE = URL + "articles/"
    URL_CLUSTER = URL + "clusters/"

    #os.environ['NO_PROXY'] = '127.0.0.1'
    r = requests.post(URL_ARTICLE, json=data, headers=headers)

    return r

def update_clusters(cluster_no,article_id, source_title, source_url ):
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTkzMTA0MDUsImlhdCI6MTYxOTIyNDAwNSwic3ViIjoxfQ.aigrpmZDzADk48FbxYgdpToxDJLugRiZukMHZDJNymc"

    URL =  "https://multi-news-summary.herokuapp.com/api/v1/"

    data = {
        "cluster_no": cluster_no,
        "article_id": article_id,
        "source_title" : source_title,
        "source_url": source_url
    }

    headers = {"api-token":token}
    
    URL_ARTICLE = URL + "articles/"
    URL_CLUSTER = URL + "clusters/"

    #os.environ['NO_PROXY'] = '127.0.0.1'
    r = requests.post(URL_CLUSTER, json=data, headers=headers)

    return r


def update_full(title , content, source_url , source_title):
    #title = "this is the seconda article"
    #content = "second article thesth tsst. this is actually the third article"
    res = update_articles(title,content)
    data = res.json()
    art_id = data.get("id")
    #source_url = ["https://www.hindustantimes.com/world-news/us-defends-curbs-on-vaccine-raw-material-exports-angela-merkel-targets-indian-pharma-101619206077962.html"]
    #source_title = ["US defends curbs on vaccine raw material exports, Angela Merkel targets Indian pharma"]
    for i in range(len(source_title)):
        update_clusters(art_id,art_id,source_title[i], source_url[i])
    print(art_id)

"""
if __name__ == "__main__":
    title = "this is the seconda article"
    content = "second article thesth tsst. this is actually the third article"
    res = update_articles(title,content)
    data = res.json()
    art_id = data.get("id")
    source_url = ["https://www.hindustantimes.com/world-news/us-defends-curbs-on-vaccine-raw-material-exports-angela-merkel-targets-indian-pharma-101619206077962.html"]
    source_title = ["US defends curbs on vaccine raw material exports, Angela Merkel targets Indian pharma"]
    for i in range(len(source_title)):
        update_clusters(art_id,art_id,source_title[i], source_url[i])
    print(art_id)
"""

    


