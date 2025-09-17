
from flask import Flask, request, jsonify, g
import sqlite3, time, hmac, hashlib, base64

app = Flask(__name__)
DATABASE = 'library.db'
SECRET = b'supersecretkey'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with open('schema.sql', 'r') as f:
            db.executescript(f.read())
        db.commit()

def generate_token(username):
    ts = str(int(time.time()))
    msg = username + ':' + ts
    sig = hmac.new(SECRET, msg.encode(), hashlib.sha256).digest()
    return base64.urlsafe_b64encode((msg+':'+base64.urlsafe_b64encode(sig).decode()).encode()).decode()

def verify_token(token):
    try:
        raw = base64.urlsafe_b64decode(token.encode()).decode()
        username, ts, sigb64 = raw.split(':')
        msg = username+':'+ts
        sig = base64.urlsafe_b64decode(sigb64.encode())
        expected = hmac.new(SECRET, msg.encode(), hashlib.sha256).digest()
        if hmac.compare_digest(sig, expected):
            return username
    except Exception:
        return None
    return None

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    u, p = data.get('username'), data.get('password')
    cur = get_db().execute('SELECT * FROM users WHERE username=? AND password=?',(u,p))
    row = cur.fetchone()
    if row:
        token = generate_token(u)
        return jsonify({'token': token})
    return jsonify({'error':'Invalid credentials'}), 401

def protected(f):
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization','')
        if auth.startswith('Bearer '):
            token = auth.split()[1]
            user = verify_token(token)
            if user:
                g.current_user = user
                return f(*args, **kwargs)
        return jsonify({'error':'Unauthorized'}), 401
    wrapper.__name__=f.__name__
    return wrapper

@app.route('/api/students', methods=['GET','POST'])
@protected
def students():
    db = get_db()
    if request.method=='POST':
        d=request.get_json()
        db.execute('INSERT INTO students(name,roll_no,course,email,phone) VALUES(?,?,?,?,?)',
                   (d['name'], d['roll_no'], d['course'], d['email'], d['phone']))
        db.commit()
        return jsonify({'status':'ok'})
    cur=db.execute('SELECT * FROM students')
    return jsonify([dict(x) for x in cur.fetchall()])

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000)
