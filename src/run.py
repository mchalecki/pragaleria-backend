import os

from app import application

config_name = os.environ['config']
config_name = "development"
app = application.create_app(config_name)

if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0")
