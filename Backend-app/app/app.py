from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from app.routes.api_routes import api_routes 
from app.routes.task_routes import task_routes
from flask_cors import CORS
import threading
from app.handlers.chatra_handler import chatra_handler
from app.handlers.gmail_handler import gmail_handler
from app.handlers.shopify_hander import shopify_handler


#shopify_thread = threading.Thread(target=shopify_handler)
#shopify_thread.start()

app = Flask(__name__)
CORS(app)
app.register_blueprint(task_routes, url_prefix='/tasks')
app.register_blueprint(api_routes, url_prefix='/api')
CORS(app)
@app.route('/')
def home():
    return "Welcome to the Flask App!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)


