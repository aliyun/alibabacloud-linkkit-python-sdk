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
# !!! Please update config.json and tsl.json by your data !!!!
#

from linkkit import linkkit
import logging
import json

###################################
# define callback functions
###################################


def thing_on_connect(session_flag, rc, user_data):
    print("on_connect, session_flag:%d, rc:%d" % (session_flag, rc))


def thing_on_disconnect(rc, user_data):
    print("on_disconnect, rc:%d" % (rc))


def thing_on_thing_enable(user_data):
    print("on_thing_enable")


def thing_on_thing_prop_post(request_id, code, data, reply_message, user_data):
    print("on_thing_prop_post, request_id:%s, code:%d, data:%s, message:%s" %
          (request_id, code, data, reply_message))


def load_config(filename):
    with open(filename, encoding='utf-8') as f:
        return json.load(f)
    return {}


print('!!! please update config.json and tsl.json by your configuration !!!!\n\n')


###################################
# Client
###################################

# create the client
config_info = load_config('config.json')

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
thing_client.on_thing_prop_post = thing_on_thing_prop_post

# load the tsl template
thing_client.thing_setup("tsl.json")

# connect the cloud
thing_client.connect_async()


########################################
# commands
########################################
# example for property
def cmd_post_property():
    print('post property to cloud')
    property_data = {"abs_speed": 11}
    thing_client.thing_post_property(property_data)


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
  1 - post the properties to cloud\n\
  2 - upload file: test.txt\n\
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
        cmd_post_property()
    elif msg == '2':
        cmd_upload_file()
    if msg.lower() == 'q':
        print('quit...')
        break

