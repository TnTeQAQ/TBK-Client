#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import etcd3
import tzcp.tbk.tbk_pb2 as tbkpb
from tbkpy import _core as tbkpy

import utils.Utils as uitls
from config.SystemConfig import config
from utils.ClientLogManager import client_logger


class TBKManager:
    def __init__(self):
        self.param_tree = None
        self._param_data = None
        self._message_data = None
        tbkpy.init(config.TBK_NODE_NAME)
        self.MESSAGE_PREFIX = "/tbk/ps"
        self.PARAM_PREFIX = "/tbk/params"
        self.etcd = self._client()

        self.callback_dict = {}
        self.subscriber_dict = {}

    @staticmethod
    def _client():
        pki_path = os.path.join(os.path.expanduser("~"), ".tbk/etcdadm/pki")
        return etcd3.client(
            host="127.0.0.1",
            port=2379,
            ca_cert=os.path.join(pki_path, "ca.crt"),
            cert_key=os.path.join(pki_path, "etcdctl-etcd-client.key"),
            cert_cert=os.path.join(pki_path, "etcdctl-etcd-client.crt"),
        )

    # 获取原始的param信息
    def get_original_param(self, _prefix=None):
        prefix = self.PARAM_PREFIX + (_prefix if _prefix else "")
        raw_data = self.etcd.get_prefix(prefix)
        data = dict(
            [
                (r[1].key.decode('utf-8', errors='ignore')[12:], r[0].decode('utf-8', errors='ignore'))
                for r in raw_data
            ]
        )
        return data

    # 获取处理后的param
    def get_param(self, _prefix=None):
        data = self.get_original_param(_prefix)
        result = {}
        # 遍历原始字典并分类存储
        for key, value in data.items():
            base_key = key.rsplit("/", 1)[0]
            suffix = key.rsplit("/", 1)[1]
            if base_key not in result:
                result[base_key] = {"info": None, "type": None, "value": None}
            if suffix == "__i__":
                result[base_key]["info"] = value
            elif suffix == "__t__":
                result[base_key]["type"] = value
            elif suffix == "__v__":
                result[base_key]["value"] = value
        self.param_tree = uitls.build_param_tree(result)
        return result

    @property
    def param_data(self):
        # self._old_param_data = self._param_data
        self._param_data = self.get_param()
        return self._param_data

    # 获取 message 信息
    def get_message(self):
        processes = {}
        publishers = {}
        subscribers = {}
        res = self.etcd.get_prefix(self.MESSAGE_PREFIX)
        for r in res:
            key, value = r[1].key.decode(), r[0]
            keys = key[len(self.MESSAGE_PREFIX):].split("/")[1:]
            info = None
            if len(keys) == 1:
                info = tbkpb.State()
                info.ParseFromString(value)
                processes[info.uuid] = info
            elif len(keys) == 3:
                if keys[1] == "pubs":
                    info = tbkpb.Publisher()
                    info.ParseFromString(value)
                    publishers[info.uuid] = info
                elif keys[1] == "subs":
                    info = tbkpb.Subscriber()
                    info.ParseFromString(value)
                    subscribers[info.uuid] = info
            else:
                client_logger.log("ERROR", f"TBKApi: Error: key error:{key}")
        res = {"ps": processes, "pubs": publishers, "subs": subscribers}
        return res

    @property
    def message_data(self):
        # self._old_message_data = self._message_data
        self._message_data = self.get_message()
        return self._message_data

    @property
    def message_tree(self):
        message_tree = {}
        for node_type in self.message_data:
            tree = {}
            if node_type == "ps":
                continue
            elif node_type == "subs":
                continue
            elif node_type == "pubs":
                data = self.message_data[node_type]
                for uuid in data:
                    node_name = data[uuid].ep_info.node_name
                    if node_name == config.TBK_NODE_NAME:
                        puuid = node_name
                    else:
                        puuid = f"{node_name}_{data[uuid].puuid}"
                    if puuid not in tree:
                        tree[puuid] = {}
                    tree[puuid][uuid] = data[uuid]
            else:
                client_logger.log("ERROR", f"{self.__class__} build message_tree type error!")
            message_tree[node_type] = tree
        return message_tree

    def unsubscribe(self, info: dict, is_del_msg=False):
        puuid = info["puuid"]
        name = info["name"]
        msg_name = info["msg_name"]
        tag = info["tag"]
        if tag in self.callback_dict.get(puuid, {}).get(msg_name, {}).get(name, {}):
            del self.callback_dict[puuid][msg_name][name][tag]
        if len(self.callback_dict[puuid][msg_name][name]) < 1 or is_del_msg:
            del self.subscriber_dict[puuid][msg_name][name]
            del self.callback_dict[puuid][msg_name][name]

    def is_subscribed(self, info: dict) -> bool:
        return info["name"] in self.subscriber_dict.get(info["puuid"], {}).get(info["msg_name"], {})

    def callback_manager(self, msg, info):
        puuid = info["puuid"]
        name = info["name"]
        msg_name = info["msg_name"]
        for tag in self.callback_dict.get(puuid, {}).get(msg_name, {}).get(name, {}):
            callback = (
                self.callback_dict.get(puuid, {})
                .get(msg_name, {})
                .get(name, {})
                .get(tag)
            )
            if callback:
                callback(msg)

    def subscriber(self, info: dict, callback):
        puuid = info["puuid"]
        name = info["name"]
        msg_name = info["msg_name"]
        tag = info["tag"]
        # if "user_data" in info:
        #     user_data = info["user_data"]
        self.callback_dict.setdefault(puuid, {}).setdefault(msg_name, {}).setdefault(
            name, {}
        )[tag] = callback

        if self.subscriber_dict.get(puuid, {}).get(msg_name, {}).get(name) is not None:
            # 如果self.subscriber_dict[puuid][msg_name][name] 如果已经订阅则退出
            return
        client_logger.log("INFO", f"Add new subscriber({puuid}, {msg_name}, {name})")
        self.subscriber_dict.setdefault(puuid, {}).setdefault(msg_name, {})[name] = (
            tbkpy.Subscriber(
                # puuid, #这个属性tbk内还没开出接口
                name,
                msg_name,
                lambda msg: self.callback_manager(msg, info),
            )
        )
