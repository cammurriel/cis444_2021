import psycopg2


def get_db():
    return psycopg2.connect(host="localhost", dbname="books" , user="cammurriel", password="123")

def get_db_instance():  
    db  = get_db()
    cur  = db.cursor( )

    return db, cur 



if __name__ == "__main__":
    db, cur = get_db_instance()

    cur.execute("select * from users")
    for r in cur.fetchall():
        print(r)

    cur.execute('create table books ( book_title varchar(255), price SMALLINT);')
    db.commit()




