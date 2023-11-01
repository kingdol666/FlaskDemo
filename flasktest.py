# 导入相关模块
import json
import os

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send, emit
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from flask_cors import CORS

from FlaskDemo.model.MyShiCi import ShiCiGet
from FlaskDemo.model.test import myQuestion
from FlaskDemo.utils.ImageToText import predict_step

# 创建Flask应用对象
app = Flask(__name__, template_folder='templates')
# 创建SocketIO对象
CORS(app, cors_allowed_origins="*")
socketio = SocketIO(app, cors_allowed_origins="*")
shici = ShiCiGet()


# 定义路由，返回聊天室页面
@app.route('/')
def index():
    return render_template('chat.html')


# 定义事件处理函数，当客户端连接时打印一条消息
@socketio.on('connect')
def handle_connect():
    print('Client connected')


# 定义事件处理函数，当客户端断开时打印一条消息
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


# 定义事件处理函数，当客户端发送message事件时，将消息广播给所有客户端
@socketio.on('message')
def handle_message(message):
    print('Received message: ' + message)
    send(message, broadcast=True)


# 定义事件处理函数，当客户端发送json事件时，将数据广播给所有客户端
@socketio.on('json')
def handle_json(json):
    print('Received json: ' + str(json))
    emit('json', json, broadcast=True)


########################################################################
user_socket_dict = {}


# 建立websocket连接时,前端将名字发送过来了
@app.route("/my_socket/<username>")
def my_socket(username):
    # 获取当前客户端与服务器的Socket连接
    user_socket = request.environ.get("wsgi.websocket")  # type:WebSocket

    if user_socket:
        # 以名字为key,连接对象为value添加到字典中
        user_socket_dict[username] = user_socket
    while 1:
        # 等待前端将消息发送过来,此时是json数据
        msg = user_socket.receive()
        print(msg)  # {"from_user":"wuchao","chat":"123","to_user":"xiaohei"}
        # 反序列化
        msg_dict = json.loads(msg)
        # 查找字典中前端要发送信息给那个人的名字
        to_username = msg_dict.get("to_user")
        # 获取目标人物的连接地址
        to_user_socket = user_socket_dict.get(to_username)
        # 将信息发送给目标人物
        to_user_socket.send(msg)


########################################################################

@app.route("/siliao")
def gc():
    return render_template("siliao.html")


@socketio.on('signal')
def handle_message(message):
    print('Received message: ' + message)
    # send(message, broadcast=True)
    emit("signal", message)


@socketio.on('boardSignal')
def handle_message(message):
    print('Received message: ' + message)
    # send(message, broadcast=True)
    emit("boardSignal", message, broadcast=True)


@app.route("/get_xinghuo", methods=['POST'])
def get_xinghuo():
    if request.method == 'POST':  # 判断是否是 POST 请求
        import random
        userId = random.randint(1000, 10000)
        print(userId)
        userId_str = str(userId)
        # 获取表单数据
        text = request.form.get('text')  # 传入表单对应输入字段的 name 值
        res = myQuestion(text, {
            "UserId": userId_str,
            "Content": "",
            "Authorization": "Bearer your_token",
            "Content-Type": "application/json"
        })
        print(res)
        return jsonify({'text': res})
    return None


@app.route("/get_shici", methods=['POST'])
def get_shici():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        text = request.form.get('text')  # 传入表单对应输入字段的 name 值
        res = shici.execute(text)
        return jsonify({'text': res})
    return None


@app.route("/imageToText", methods=['GET'])
def imageToText():
    text = predict_step(["./images/2.png"])
    print(text[0])
    myText = text[0]
    res = myQuestion(f"请根据{myText}帮我写一首诗", {
        "UserId": "666",
        "Content": "",
        "Authorization": "Bearer your_token",
        "Content-Type": "application/json"
    })
    print(res)
    return jsonify({'text': res})


@app.route("/upload", methods=['POST'])
def get_frame():
    # file = request.files['file']
    # print(file.name)  # 传入表单对应输入字段的 name 值
    # return jsonify(file.name)
    # 接收图片
    text = []
    file_paths = ""
    upload_file = request.files['file']
    # 获取图片名
    file_name = upload_file.filename
    # 文件保存目录（桌面）
    file_path = r'./images/'
    if upload_file:
        # 地址拼接
        file_paths = os.path.join(file_path, file_name)
        # 保存接收的图片到桌面
        upload_file.save(file_paths)
        # 随便打开一张其他图片作为结果返回，
        text = predict_step([file_paths])
    thisText = text[0]
    res = myQuestion(f"请根据{thisText}帮我写一首诗,中文回答,并且尽量文字优美,直接给我返回诗歌本身,不需要多余回答", {
        "UserId": "666",
        "Content": "",
        "Authorization": "Bearer your_token",
        "Content-Type": "application/json"
    })
    print(res)
    os.remove(file_paths)
    message = res
    socketio.emit("boardSignal", message)
    return jsonify({'text': res})


# 启动应用和socketio服务
if __name__ == '__main__':
    http_serv = WSGIServer(("0.0.0.0", 5000), app, handler_class=WebSocketHandler)
    print("Starting")
    http_serv.serve_forever()
