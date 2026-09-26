from connection import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
    DELETE FROM cameras WHERE id == 3
""")

conn.commit()
conn.close()
