from flask import Flask

# Application initializations
app = Flask(__name__)

# settings
app.secret_key = "mysecretkey"
