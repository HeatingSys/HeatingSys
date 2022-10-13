from database import get_db, close_db


db = get_db()
user = db.execute("""SELECT * FROM users);""").fetchone()
db.commit()

print(user)
