import psycopg2
conn = psycopg2.connect(dbname='postgres', user='postgres', password='satyam', host='localhost')
conn.autocommit = True
cur = conn.cursor()
cur.execute("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='test_finance_tracker' AND pid <> pg_backend_pid()")
cur.execute('DROP DATABASE IF EXISTS test_finance_tracker')
print('Dropped test_finance_tracker')
conn.close()
