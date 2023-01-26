from flask import Flask, render_template
from database import Database

app = Flask(__name__)

db = Database("sqlite:///test.db")

@app.route('/')
def index():
    users = db.get_all_users()
    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run()
