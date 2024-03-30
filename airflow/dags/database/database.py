import pymysql
import pymysql.cursors

user_name = 'root'
password = '비밀번호 기입'
host_ip = '175.45.200.149'
db_name = 'stock_db'

connection = pymysql.connect(host=host_ip,
                             user=user_name,
                             password=password,
                             database=db_name,
                             cursorclass=pymysql.cursors.DictCursor)
