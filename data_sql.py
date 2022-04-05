from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgres://postgres:toor@localhost/Baras')
db = scoped_session(sessionmaker(bind=engine))

users = db.execute("SELECT * FROM login_credentials WHERE email_id='nayanjmehta.nm@gmail.com';").fetchall()
print(users[0][3])

