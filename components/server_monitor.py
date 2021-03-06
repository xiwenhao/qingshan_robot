#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : Xi WenHao
# @Email    : xiwenhao1994@gmail.com
# @Project  : qingshan
# @Time     : 2021/11/10 14:42
# @File     : server_monitor.py

import websocket
from loguru import logger
from db.database import session
from db.subscription import query_group_by_server
from gocqhttp.action.send_msg import send_group_msg
import json

# from settings import cfg

status2desc = {
    1: "开服了❤ 冲~!",
    0: "维护了💔 各位洗洗睡吧"
}

def on_message(ws, msg):
    msg = json.loads(msg)
    if msg["type"] == 2003:
        pass
    elif msg["type"] == 2001:
        logger.info(f"recv: {msg}")
        # send group message
        server = msg["data"]["server"]
        status = msg["data"]["status"]
        group_ids = query_group_by_server(session, server)
        msg = f"""{server}{status2desc[status]}"""
        for id in group_ids:
            send_group_msg(id, msg)


def on_error(ws, error):
    logger.error(error)


def on_close(ws):
    logger.info("### closed ###")


def server_monitor():
    ws = websocket.WebSocketApp(
        # cfg["MONITOR"]["ws_addr"],
        "wss://socket.nicemoe.cn",
        on_message=on_message,
        on_error=on_error, on_close=on_close)
    logger.info("----- server monitor start -----")
    ws.run_forever()
