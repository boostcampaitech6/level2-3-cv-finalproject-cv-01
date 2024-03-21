import pymysql
import pymysql.cursors

user_name = 'admin'
pass_my = 'mysqlpw1'
host_my = '비밀번호 기입'
db_name = 'airflow_test_db'

connection = pymysql.connect(host=host_my,
                             user=user_name,
                             password=pass_my,
                             database=db_name,
                             cursorclass=pymysql.cursors.DictCursor)