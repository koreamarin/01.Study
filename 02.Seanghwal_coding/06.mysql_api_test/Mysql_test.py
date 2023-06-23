import pymysql

conn = pymysql.connect(user='root', password='fbwldnjs1127', host = 'localhost', port = '', db='mysql_api_test', charset='utf8',autocommit=True)
cur = conn.cursor()


# DATABASE 관련 명령어
def show_databases() :                          # database 리스트 출력.
    cur.execute('SHOW DATABASES;')
    print(cur.fetchall())

def delete_database(delete_database_name) :     # database 삭제.
    cur.execute(f'DROP DATABASE {delete_database_name};')
    show_databases()

def create_database(create_database_name) :     # database 생성. 변수는 database name
    cur.execute(f'CREATE DATABASE {create_database_name};')
    show_databases()

def use_database(use_database_name) :           # database 선택.
    cur.execute(f'USE {use_database_name};')



# TABLE 관련 명령어
def show_table() :
    cur.execute(f'SHOW TABLES;')
    print(cur.fetchall())


def DESC_table() :
    cur.execute(f'DESC topic;')
    for i in cur.fetchall() :
        print(i)


def create_table() :
    cur.execute("""
                    CREATE TABLE topic(
                    id INT(11) NOT NULL AUTO_INCREMENT,
                    title VARCHAR(100) NOT NULL,
                    description TEXT NULL,
                    created DATETIME NOT NULL,
                    author_id INT(5) NULL,
                    PRIMARY KEY(id));
    """)
    show_table()



# RECORD 관련 명령어
def insert_record(table,title,description,author_id) :
    cur.execute(f"INSERT INTO {table} (title, description, created, author_id) VALUES ('{title}','{description}',NOW(),'{author_id}');")
    read_table(table)

def read_table(table) :      # 읽은 
    cur.execute(f'SELECT * FROM {table};')
    for i in cur.fetchall() :
        for j in i :
            print(j)
        print()

def delete_record(table,id) :
    cur.execute(f'DELETE FROM {table} WHERE id={id}')
    read_table(table)





############ main #################

table = 'topic'
title = ['MySQL','ORACLE','SQL Server','PostgreSQL','MongoDB']
description = ['MySQL is ...','Oracle is ...','SQL Server is ...','PostgreSQL is ...','MongoDB is ...']
author_id = ['1','1','2','3','1']

# for i in range(5) :
#     insert_record(table,title[i],description[i],author_id[i])
insert_record(table,title[0],description[0],author_id[0])


conn.close()