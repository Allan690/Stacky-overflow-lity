import overflow_lite.user_authentication
import overflow_lite.views
from flask import Flask
app = Flask(__name__)

app.register_blueprint(overflow_lite.user_authentication.auth, url_prefix='/api/v1/auth')
app.register_blueprint(overflow_lite.views.quiz, url_prefix='/api/v1')
