# this test must setup a mysql server, and modify DBCONF
import json
import sqlalchemy
from unittest.mock import patch
from .. import engine

DBCONF={
    'db_id': 'testdb',
    'db_type': engine.DB_MYSQL,
    'db_host': '192.168.1.100',
    'db_port': '3306',
    'db_user': 'root',
    'db_pass': '12345'
}

def teardown_function():
    db = DBCONF
    db_name = db['db_name'] if 'db_name' in db else ''
    db_host = db['db_host'] if 'db_host' in db else ''
    db_port = db['db_port'] if 'db_port' in db else 3306
    db_user = db['db_user']
    db_pass = db['db_pass']
    sqlstr= f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    eng=sqlalchemy.create_engine(sqlstr)
    eng.execute("drop database if exists jp_sql_unit_test")


@patch("jupyterlab_sql_explorer.handlers.engine._getDbInfo")
async def test_mysql_dbtable(mock_dbinfo, jp_fetch):
    mock_dbinfo.return_value=DBCONF

    response = await jp_fetch("jupyterlab-sql-explorer", "dbtables", params={'dbid': 'testdb'})
    assert response.code == 200

    # create database jp_sql_unit_test
    response = await jp_fetch("jupyterlab-sql-explorer", "query",
                              method='POST',
                              body=json.dumps({'dbid': 'testdb', 'sql': 'create database jp_sql_unit_test'}))
    assert response.code == 200
    payload = json.loads(response.body)
    assert payload['error'] == 'RETRY'

    response = await jp_fetch("jupyterlab-sql-explorer", "query", params={'taskid': payload['data']})
    assert response.code == 200
    payload = json.loads(response.body)
    assert payload == {'data': {}}

    response = await jp_fetch("jupyterlab-sql-explorer", "dbtables", params={'dbid': 'testdb'})
    assert response.code == 200
    payload = json.loads(response.body)
    dbs=set()
    for d in payload['data']:
        dbs.add(d['name'])
    assert 'jp_sql_unit_test' in dbs

    # create table in jp_sql_unit_test
    response = await jp_fetch("jupyterlab-sql-explorer", "query",
                              method='POST',
                              body=json.dumps({
                                  'dbid': 'testdb',
                                  'sql': "create table jp_sql_unit_test.tab1 ( a int , b int) comment 'TEST COMMENT'"}))
    assert response.code == 200
    payload = json.loads(response.body)
    assert payload['error'] == 'RETRY'

    response = await jp_fetch("jupyterlab-sql-explorer", "query", params={'taskid': payload['data']})
    assert response.code == 200
    payload = json.loads(response.body)
    assert payload == {'data': {}}

    # check result table
    response = await jp_fetch("jupyterlab-sql-explorer", "dbtables", params={'dbid': 'testdb', 'db': 'jp_sql_unit_test'})
    assert response.code == 200
    payload = json.loads(response.body)
    assert payload == {"data": [{'name': 'tab1', 'desc': 'TEST COMMENT', 'type': 'table', 'subtype': 'T'}]}

    # get clomns
    response = await jp_fetch("jupyterlab-sql-explorer", "columns", params={'dbid': 'testdb', 'db': 'jp_sql_unit_test', 'tbl': 'tab1'})
    assert response.code == 200
    payload = json.loads(response.body)
    assert payload == {'data': [{'name': 'a', 'desc': '', 'type': 'col'}, {'name': 'b', 'desc': '', 'type': 'col'}]}

    # drop database jp_sql_unit_test
    response = await jp_fetch("jupyterlab-sql-explorer", "query",
                              method='POST',
                              body=json.dumps({'dbid': 'testdb', 'sql': 'drop database jp_sql_unit_test'}))
    assert response.code == 200
    payload = json.loads(response.body)
    assert payload['error'] == 'RETRY'

    response = await jp_fetch("jupyterlab-sql-explorer", "query", params={'taskid': payload['data']})
    assert response.code == 200
    payload = json.loads(response.body)
    assert payload == {'data': {}}
