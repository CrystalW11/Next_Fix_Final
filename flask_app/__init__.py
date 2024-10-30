from flask import Flask
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.secret_key = "this is supposed to be at least 16 characters long I hope it makes the cut!"
bcrypt = Bcrypt(app)



