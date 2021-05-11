import json
import collections
import psycopg2


def run(stmt):

    conn =  psycopg2.connect(database='news_app', user='postgres', password='pw1234', host='127.0.0.1')
    cur = conn.cursor()
    cur.execute(stmt)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    objects_list = []

    for row in rows:
        d = collections.OrderedDict()
        d["id"] = row[0]
        d["source"] = row[1]
        d["headline"] = row[2]
        d["link"] = row[3]
        d["category"] = row[4]
        d["content"] = row[5]
        objects_list.append(d)



    return objects_list

def get_articles(source, output_folder):   

    stmt = f"SELECT * FROM articles WHERE source='{source}';"
    try:
        result = run(stmt)
    except psycopg2.Error as e:
        print(e)

    j = json.dumps(result)
    with open(output_folder+f"{source}.json", "w") as f:
        f.write(j)

