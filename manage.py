"""API entry module"""

import os
from app import create_app


# get the environment name and creat the application context
env = os.getenv('FLASK_ENV', 'production')
app = create_app(env)


if __name__ == '__main__':
    app.run()
