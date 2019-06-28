#
# Copyright (c) 2014-2018 Alibaba Group. All rights reserved.
# License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
#
#  usage:
#  1. create the new topic /{pk}/{dn}/user/echo (sub & pub) for your product
#     in Iot Console(https://iot.console.aliyun.com)
#  2. update config_info with your device information
###############

from linkkit import linkkit
import logging
import json

# please update the following information
# config_info = {
#     "region": "cn-shanghai",
#     "product_key": "{your_product_key}",
#     "device_name": "{your_device_name}",
#     "device_secret": "{device_secret}"
# }
config_info = {
    "region": "cn-shanghai",
    "product_key": "{your_product_key}",
    "device_name": "{your_device_name}",
    "device_secret": "{your_device_secret}"
}


###################################
# define callback functions
###################################


def thing_on_connect(session_flag, rc, user_data):
    print("on_connect, session_flag:%d, rc:%d" % (session_flag, rc))


def thing_on_disconnect(rc, user_data):
    print("on_disconnect, rc:%d" % (rc))


def thing_on_thing_enable(user_data):
    print("on_thing_enable")
    print('subscribe_topic, topic:%s' % echo_topic)
    thing_client.subscribe_topic(echo_topic, 0)


def thing_on_topic_message(topic, payload, qos, user_data):
    print("on_topic_message, receive message, topic:%s, payload:%s, qos:%d" % (topic, payload, qos))


def thing_on_unsubscribe_topic(topic, qos, user_data):
    print("on_unsubscribe_topic, topic:%s, qos:%d" % (topic, qos))


def load_config(filename):
    with open(filename, encoding='utf-8') as f:
        return json.load(f)
    return {}


###################################
# Client
###################################
user_topic = "/%s/%s/user/update" % (config_info["product_key"], config_info["device_name"])
echo_topic = "/%s/%s/user/echo" % (config_info["product_key"], config_info["device_name"])

# create the client
thing_client = linkkit.LinkKit(config_info['region'],
                               config_info['product_key'],
                               config_info['device_name'],
                               config_info['device_secret'])

# enable DEBUG log if needed
thing_client.enable_logger(logging.DEBUG)

# set the callback functions
thing_client.on_connect = thing_on_connect
thing_client.on_disconnect = thing_on_disconnect
thing_client.on_thing_enable = thing_on_thing_enable
thing_client.on_topic_message = thing_on_topic_message
thing_client.on_unsubscribe_topic = thing_on_unsubscribe_topic

thing_client.thing_setup()

# connect the cloud
thing_client.connect_async()


########################################
# commands
########################################
# example for property

g_msg_count = 0


def cmd_pub_to_update():
    global g_msg_count
    g_msg_count += 1
    payload = "test, id: %d" % g_msg_count
    print("pub message, topic:%s, payload:%s, count:%d" % (user_topic, payload, g_msg_count))
    thing_client.publish_topic(user_topic, payload, 0)


g_msg_echo_count = 0


def cmd_pub_to_echo():
    global g_msg_echo_count
    g_msg_echo_count += 1
    print("pub message, topic:%s, count:%d" % (echo_topic, g_msg_echo_count))
    payload = "{id: %d}" % g_msg_echo_count
    thing_client.publish_topic(echo_topic, payload, 0)


def cmd_print_state():
    print('connect_state:', thing_client.check_state())


def cmd_upload_file():
    result = thing_client.upload_file_sync("./test.txt", 'test.txt')
    print('result, code:%s, file_store_id:%s, upload_size:%d' % (result.code,
                       result.file_store_id, result.upload_size))


def dump_help():
    print("\n====================\n\
input the command:\n\
  0 - print the connection state\n\
  1 - pub to /{pk}/{dn}/user/update\n\
  2 - pub to /{pk}/{dn}/user/echo\n\
  q - exit the program\n\
---------------------\n")


while True:
    dump_help()
    msg = input()
    if msg == 'h':
        dump_help()
    if msg == '0':
        cmd_print_state()
    elif msg == '1':
        cmd_pub_to_update()
    elif msg == '2':
        cmd_pub_to_echo()
    if msg.lower() == 'q':
        print('quit...')
        break

