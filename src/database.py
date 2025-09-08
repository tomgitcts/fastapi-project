
import sqlite3


DB_NAME = 'employees_db.db'
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory  = sqlite3.Row
    print(conn)
    return conn

# if os.path.exists(DB_NAME):
#     print("Exists")
#     print(DB_NAME)
#     try:
#         conn = sqlite3.connect("employees_db.db")
#         cursor = conn.cursor()
#         cursor.execute("Select * from employees")
#         tables = cursor.fetchall()
#         cursor.execute("Select 1;")
#         conn.close()
#         print(tables)
#     except Exception as e:
#         print("Error connecting DB",e)
# else:
#     print("No path found")


# ls = get_connection()
# print(ls)