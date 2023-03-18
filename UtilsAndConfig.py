import re
import os
import io
import json
import requests
from flask.json import JSONEncoder
from urllib.request import urlopen
from PIL import Image, ImageTk
import configparser
from urllib.parse import quote


class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, str):
            return str(obj, encoding='utf-8')
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        if isinstance(obj, object):
            return obj.get_json()
        return json.JSONEncoder.default(self, obj)


# HTTP和SOCKET 地址配置
class ServerConfig:
    def __init__(self):
        cfg = configparser.ConfigParser()
        #
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'server.conf')
        cfg.read(file_path)
        self.SERVER_IP = str(cfg.get("server", "SERVER_IP"))
        self.HTTP_PORT = int(cfg.get("server", "HTTP_PORT"))
        self.SOCKET_PORT = int(cfg.get("server", "SOCKET_PORT"))
        self.HTTP_SERVER_ADDRESS = 'http://' + self.SERVER_IP + ':' + str(self.HTTP_PORT)
        self.SOCKET_SERVER_ADDRESS = 'http://' + self.SERVER_IP + ':' + str(self.SOCKET_PORT)
        self.SQLALCHEMY_DATABASE_URI = str(cfg.get("server", "SQLALCHEMY_DATABASE_URI"))


serverConfig = ServerConfig()
# Socket通信常量 枚举
# 登录
USER_LOGIN = 'USER_LOGIN'
# 登录成功
USER_LOGIN_SUCCESS = 'USER_LOGIN_SUCCESS'
# 登录失败
USER_LOGIN_FAILED = 'USER_LOGIN_FAILED'
# 发送聊天消息
CHAT_SEND_MSG = 'FRIENDS_SEND_MSG'
# 发送聊天消息成功：对方在线
CHAT_SEND_MSG_SUCCESS = 'FRIENDS_SEND_MSG_SUCCESS'
# 发送聊天消息失败：对方离线
CHAT_SEND_MSG_ERR = 'FRIENDS_SEND_MSG_ERR'
# 新聊天消息
CHAT_HAS_NEW_MSG = 'FRIENDS_NEW_MSG'
# 好友状态改变
FRIENDS_ONLINE_CHANGED = 'FRIENDS_ONLINE_CHANGED'
# 好友/群数量改变
FRIENDS_GROUPS_COUNT_CHANGED = 'FRIENDS_GROUPS_COUNT_CHANGED'
# 发送消息验证
MESSAGE_SEND_MSG = 'MESSAGE_SEND_MSG'
# 新消息验证
MESSAGE_NEW_MSG = 'MESSAGE_NEW_MSG'
# 发送聊天文件
CHAT_SEND_FILE = 'CHAT_SEND_FILE'
# 发送聊天文件成功：对方在线
CHAT_SEND_FILE_SUCCESS = 'CHAT_SEND_FILE_SUCCESS'
# 发送聊天文件失败：对方离线
CHAT_SEND_FILE_ERR = 'CHAT_SEND_FILE_ERR'
# 新聊天文件
CHAT_HAS_NEW_FILE = 'CHAT_HAS_NEW_FILE'
# 强制退出
SYSTEM_LOGOUT = 'SYSTEM_LOGOUT'


# 登录名 字母开头 字母+数字组合 5-15位
def check_login_name(name):
    if name is None or len(name) < 5 or len(name) > 15:
        return False
    if not name.encode('utf-8').isalnum():
        return False
    if not re.match(r'[a-zA-Z][0-9a-zA-Z]', name):
        return False
    return True


# 编码聊天信息   \n替换为/n
def encode_msg(msg):
    return str(msg).replace('\n', '/n')


# 解码 /n替换为\n
def decode_msg(msg):
    return msg.replace('/n', '\n')


# 本地聊天记录缓存路径
def get_local_cache_path(uid, is_friend, from_id, to_id, is_send):
    # 好友：/static/LocalCache/{uid}/friend/{toid}.crcd
    # 群：  /static/LocalCache/{uid}/group/{gid}.crcd

    path = '\\static\\LocalCache\\{uid}\\{type}\\{toid}.crcd'
    # 发送方
    if is_friend == 1:
        if is_send:
            path = path.replace('{uid}', str(from_id))
            path = path.replace('{toid}', str(to_id))
        else:
            path = path.replace('{uid}', str(to_id))
            path = path.replace('{toid}', str(from_id))
        path = path.replace('{type}', 'friends')
    else:
        path = path.replace('{uid}', str(uid))
        path = path.replace('{toid}', str(to_id))
        path = path.replace('{type}', 'groups')
    return os.path.abspath(os.path.dirname(__file__)) + path


def get_one_chat_record(is_friend, uid, to_id):
    path = get_local_cache_path(uid, is_friend, uid, to_id, True)
    check_path(path)
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        last_line = lines[-1]
    return decode_msg(last_line)


def add_one_chat_record(uid, is_friend, from_id, to_id, msg, is_send):
    record_path = get_local_cache_path(uid, is_friend, from_id, to_id, is_send)

    check_path(record_path)
    with open(record_path, 'a', encoding='utf-8') as f:
        f.write('\n' + encode_msg(msg))


def check_path(path):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    if not os.path.exists(path):
        f = open(path, 'w', encoding='utf-8')
        f.write('[[start]]')


def get_username_by_uid(uid):
    url = serverConfig.HTTP_SERVER_ADDRESS + '/getUsernameByUid?uid=' + str(uid)
    result_json = json.loads(requests.get(url).text)
    if result_json['code'] == 200:
        return result_json['data']
    return ''


def get_group_name_by_gid(gid):
    url = serverConfig.HTTP_SERVER_ADDRESS + '/getGnameByGid?gid=' + str(gid)
    result_json = json.loads(requests.get(url).text)
    if result_json['code'] == 200:
        return result_json['data']
    return ''


# 按比例处理照片大小
def resize_image(is_http_img, path, max_w, max_h):
    if is_http_img:
        url = serverConfig.HTTP_SERVER_ADDRESS + path
        file_name = url.split('/')[-1]
        quote_name = quote(file_name)
        url = url.replace(file_name, quote_name)
        image_bytes = urlopen(url).read()
        data_stream = io.BytesIO(image_bytes)
        img_open = Image.open(data_stream)
    else:
        img_open = Image.open(path)
    w, h = img_open.size
    if w <= max_w and h <= max_h:
        return ImageTk.PhotoImage(img_open)
    if (1.0*w/max_w) > (1.0*h/max_h):
        scale = 1.0 * w / max_w
    else:
        scale = 1.0 * h / max_h
    img_open = img_open.resize((int(w/scale), int(h/scale)), Image.ANTIALIAS)
    return ImageTk.PhotoImage(img_open)