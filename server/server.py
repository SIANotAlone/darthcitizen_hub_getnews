from flask import Flask

import logger
import yaml
from routes import mainBP
from flask_cors import CORS

class Server:
    IP = '0.0.0.0'
    PORT = 0
    Logger = logger.Logger()

    def __init__(self):
        with open('server/config.yaml', 'r') as file:
            config = yaml.safe_load(file)
            self.IP = config['server']['ip']
            self.PORT = config['server']['port']

        self.Logger.logInfo(f'server starting on port {config["server"]["port"]} with ip {config["server"]["ip"]}')

    def RunServer(self):
        app = Flask(__name__)
        CORS(app, resources={
            r"/update_news": {
                "origins": ["http://localhost:8080", "http://example.com"],
                "methods": ["GET", "POST"],
                "allow_headers": ["Content-Type"]
            }
        })
        app.register_blueprint(mainBP)
        app.run(host= self.IP, port=self.PORT)


s = Server()
s.RunServer()