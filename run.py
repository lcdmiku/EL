# run.py
import sys
from game import create_app

print(sys.path)  # 打印模块搜索路径

if __name__ == '__main__':
    print(sys.path)


    app = create_app()
    game = create_app()
    game.run(debug=True,host= '10.4.61.238',port=5000)