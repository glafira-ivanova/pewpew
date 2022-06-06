#!/usr/bin/env python3.8

import os
import sys
import subprocess
import requests
import base64
import json
import psycopg2

def get_dump(token_string):
    r = requests.get(f'https://hackattic.com/challenges/backup_restore/problem?access_token={token_string}')
    r.raise_for_status()
    dump = r.json()['dump']
    dump_decoded = base64.b64decode(dump)
    dump_filename = None
    with open('database.backup', 'w', encoding='utf-8') as f:
        f.write(dump_decoded.decode('utf-8'))
    dump_filename = f.name
    return dump_filename

def restore_backup(database, user, passwd, host, dump):
    subprocess.check_call(f'pg_restore -h {host} -U {user} -d {database} {dump}', shell=True, env=dict(os.environ, PGPASSWORD=passwd))


def get_data(database, user, passwd, host):
    conn = psycopg2.connect(dbname=database, user=user, password=passwd, host=host)
    cursor = conn.cursor()
    cursor.execute('SELECT ssn FROM table WHERE alive = true')
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return [i[0] for i in records]

def submit_solution(token_string, alive_list):
    r = requests.post(f'https://hackattic.com/challenges/backup_restore/solve?access_token={token_string}', data = json.dumps({'alive_ssns': alive_list}))
    response.raise_for_status()
    print(r.status_code)

if __name__ == '__main__':
    token, db_name, db_user, db_pass, db_host = sys.argv[1:]
    dump_filename = get_dump(token)
    restore_backup(db_name, db_user, db_pass, db_host, dump_filename)
    records = get_data(db_name, db_user, db_pass, db_host)
    submit_solution(token, records)
