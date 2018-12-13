from app import application
from app.configs import current_config

app = application.initialize_app(current_config)

if __name__ == '__main__':
    app.run(port=80, host="0.0.0.0")
