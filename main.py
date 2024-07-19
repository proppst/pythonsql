import psycopg2
from psycopg2.sql import SQL, Identifier

def create_db(conn):
    with conn.cursor() as cur:
         cur.execute("""
            CREATE TABLE IF NOT EXISTS clients (
	        id SERIAL PRIMARY KEY,
	        firstname VARCHAR(40) NOT NULL,
	        secondname VARCHAR(40) NOT NULL,
	        email VARCHAR(40) NOT NULL);
            """)
         cur.execute("""
             CREATE TABLE IF NOT EXISTS phones(
             id SERIAL PRIMARY KEY,
             client_id INTEGER REFERENCES clients(id),
             phone VARCHAR(12));
             """)
         conn.commit()
def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO clients (firstname, secondname, email)
            VALUES (%s,%s,%s)
            RETURNING id, firstname, secondname, email;
            """, (first_name, last_name, email))
        return cur.fetchone()
def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO phones(client_id, phone)
            VALUES(%s, %s)
            RETURNING client_id, phone;
            """, (client_id, phone))
        return cur.fetchone()

def change_client(conn, client_id, firstname=None, secondname=None, email=None, phones=None):
    with conn.cursor() as cur:
        arg_list = {'firstname': firstname, 'secondname': secondname, 'email': email}
        for key, arg in arg_list.items():
            if arg:
                cur.execute(SQL('UPDATE clients SET {}=%s WHERE id = %s').format(Identifier(key)),
                            (arg, client_id))
        cur.execute("""
                    SELECT * FROM clients
                    WHERE id = %s;
                    """, client_id)
        return cur.fetchall()
def delete_phone(conn, client_id, phone):
    pass

def delete_client(conn, client_id):
    pass

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    pass


with psycopg2.connect(database="netdb", user="postgres", password="271080") as conn:
    pass  # вызывайте функции здесь
create_db(conn)
#print(add_client(conn, 'Sit', 'Van', 'sit@mail.ru'))
#conn.commit()
with conn.cursor() as cur:
    cur.execute("""
            SELECT * FROM clients
            """)
    print(cur.fetchall())
#print(add_phone(conn, '8', '89589248162'))
#print(change_client(conn, '1', 'Har', 'Mamu'))
conn.close()

