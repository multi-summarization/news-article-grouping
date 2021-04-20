import json
import collections
import mysql.connector import connect, Error

def store_cluster_id(host, dbname, user, pwd, table, cluster):

    conn_string = f"host={host} dbname={dbname} user={user} password={pwd}"
    conn = connect(conn_string)
    cursor = conn.cursor()

    #cluster is list of cluster_id , article_id

    for c_id , art_id in cluster:
        sql = f"UPDATE {table}  SET cluster = %s WHERE id = %s"
        val = (c_id, art_id)
        cursor.execute(sql, val)

    conn.commit()

    conn.close ()


