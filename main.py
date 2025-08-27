from flask import Flask, render_template, redirect, url_for, request, session
from database_models import User, Invite
from database_connect import SessionLocal, Base, engine
import uuid
import config
import hashlib

app = Flask(__name__)
app.secret_key = config.flask_secret_key

Base.metadata.create_all(engine)

def get_hash(text: str):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def create_user(username, password, telegram):
    db_session = SessionLocal()
    try:
        new_user = User(uuid=str(uuid.uuid4()), username=username, password=password, telegram=telegram)
        db_session.add(new_user)
        db_session.commit()
        return new_user.uuid
    except Exception as e:
        print(e)
        return None
    finally:
        db_session.close()

def create_invite(username, telegram):
    db_session = SessionLocal()
    try:
        new_invite = Invite(username=username, telegram=telegram, uuid=uuid.uuid4())
        db_session.add(new_invite)
        db_session.commit()
        return new_invite.uuid
    except Exception as e:
        print(e)
        return None
    finally:
        db_session.close()

def get_user_by_uuid(uuid):
    db_session = SessionLocal()
    try:
        user = db_session.query(User).filter(User.uuid == uuid).first()
        return user
    except Exception as e:
        print(e)
        return None
    finally:
        db_session.close()

def get_user_by_username(username):
    db_session = SessionLocal()
    try:
        user = db_session.query(User).filter(User.username == username).first()
        return user
    except Exception as e:
        print(e)
        return None
    finally:
        db_session.close()

def get_invite(uuid):
    db_session = SessionLocal()
    try:
        invite = db_session.query(Invite).filter(Invite.uuid == uuid).first()
        return invite
    except Exception as e:
        print(e)
        return None
    finally:
        db_session.close()

def update_invite(uuid, status):
    db_session = SessionLocal()
    try:
        invite = db_session.query(Invite).filter(Invite.uuid == uuid).first()
        invite.status = status
        db_session.commit()
    except Exception as e:
        print(e)
        return None
    finally:
        db_session.close()

def update_user_telegram(username, telegram):
    db_session = SessionLocal()
    try:
        user = db_session.query(User).filter(User.username == username).first()
        user.telegram = telegram
        db_session.commit()
    except Exception as e:
        print(e)
        return None
    finally:
        db_session.close()

@app.route("/")
def index():
    return """<p>Логин</p>
    <form action="/login" method="post">
            <p>Логин: <input type="text" name="username"></p>
            <p>Пароль: <input type="password" name="password"></p>
            <p>
                <input type="submit" name="action" value="Войти">
            </p>
        </form>
        <p>Регистрация</p>
        <form action="/register" method="post">
            <p>Логин: <input type="text" name="invite"></p>
            <p>Пароль: <input type="password" name="password"></p>
            <p>
                <input type="submit" name="action" value="Зарегистрироваться" formaction="/register">
            </p>
        </form>"""

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')

        if hash(password) == get_user_by_username(username).password:
            session["uuid"] = get_user_by_username(username).uuid
            return redirect('/')
        
        return "<p>Неправильный логин или пароль!</p><p><a href='/'>На главную</a></p>"
    except:
        session.clear()
        return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    try:
        invite = request.form.get('invite')
        password = request.form.get('password')

        inv = get_invite(invite)
        if inv.status == "not_used":
            update_invite(invite, "used")
            uuid = create_user(inv.username, password, inv.telegram)
            session["uuid"] = uuid
            return redirect('/')
        else:
            return "<p>Инвайт уже был использован.</p><p><a href='/'>На главную</a></p>"
    except Exception as e:
        print(e)
        session.clear()
        return redirect('/')
    

if __name__ == "__main__":
    # print(get_hash("12345"))
    # print(create_user("abobus", "12345", "@abobusik"))
    # create_invite("agusev", "@agusev2311")
    # create_invite("hjdadfgsd", "@123456uio")
    app.run(debug=True)