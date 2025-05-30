# run.py
from game import create_app


if __name__ == '__main__':
    app = create_app()
    game = create_app()
    game.run(host= '127.0.0.1',port=5000)