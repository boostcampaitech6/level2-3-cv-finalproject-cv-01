import pymysql
import pymysql.cursors

user_name = 'admin'
pass_my = '비밀번호 기입'
host_my = '공인 IP'
db_name = 'airflow_test_db'

connection = pymysql.connect(host=host_my,
                             user=user_name,
                             password=pass_my,
                             database=db_name,
                             cursorclass=pymysql.cursors.DictCursor)
