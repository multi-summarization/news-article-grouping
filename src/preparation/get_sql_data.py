import json
import collections
import mysql.connector import connect, Error


def get_data(host, dbname, user, pwd, table, output_file):

    conn_string = f"host={host} dbname={dbname} user={user} password={pwd}"
    conn = connect(conn_string)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()

    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['id'] = row[0]
        d['source'] = row[1]
        d['headline'] = row[2]
        d['link'] = row[3]
        d['cat'] = row[4]
        d['content'] = row[5]
        objects_list.append(d)
    j = json.dumps(objects_list)
    with open('output_file', 'w') as f:
        f.write(j)

    conn.close ()

