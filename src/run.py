import os

from app import application

config_name = os.environ['config']
app = application.initialize_app(config_name)

if __name__ == '__main__':
    app.run(port=80, host="0.0.0.0")
