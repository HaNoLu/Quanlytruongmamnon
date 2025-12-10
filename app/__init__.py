from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary
app = Flask(__name__)
app.secret_key='sjakfhjafjhsejfhjsehfksfhe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Admin%40123@localhost:3306/managedb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
cloudinary.config(
            cloud_name= "diwuthkyv",
            api_key= "563232354487514",
            api_secret= "aZ3jvQ6oQxg_uUM0bNlTb9liy_8",
)
db=SQLAlchemy(app)
login=LoginManager(app)