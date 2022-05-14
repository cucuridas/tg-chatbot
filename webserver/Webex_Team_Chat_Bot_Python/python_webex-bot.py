from http.server import HTTPServer, BaseHTTPRequestHandler
from tkinter.font import BOLD
import urllib.request as urllib2
import json
import ssl
import re
import requests
from operator import itemgetter
from config import *
from crayons import cyan,red,green,yellow

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# USED FOR OFF-LINE DEBUG
debug_flag = True

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        print(cyan('Webhook triggered',bold=True))
        webhook = json.loads(body)
        print(green('    Retreive message',bold=True))
        result = send_webex_get('https://webexapis.com/v1/messages/{0}'.format(webhook['data']['id']))
        result = json.loads(result)
    
        if webhook['data']['personEmail'] != bot_email:
            in_message = result.get('text', '').lower()
            in_message = in_message.replace(bot_name.lower(), '')
            print(yellow("Message :",bold=True))
            print(cyan(in_message,bold=True))
            
            #help를 통한 지원
            if in_message.startswith('help'):
                print(yellow("help received let s reply",bold=True))
                msg = '''**How To Use:**\n- **help**, bring this help; \n- **:command-1**, trigger some python function 
                \n- **:command-2**, trigger some python function 2\n
                '''
                send_webex_post("https://webexapis.com/v1/messages",
                                {"roomId": webhook['data']['roomId'], "markdown": msg})
            #webEx 연동을 확인하기 위한 구문
            elif in_message.startswith('ping'):
                print(yellow("let s reply PONG to this ping",bold=True))
                send_webex_post("https://webexapis.com/v1/messages",
                               {"roomId": webhook['data']['roomId'], "markdown": "*PONG !*"}  ) 
            #엘라스틱 호출 구문 구문 부분            
            else:
                print(yellow('test',bold=True))
                elUrl = "http://localhost:9200" 
                elastcicRequest = urllib2.Request(elUrl)
                test = urllib2.urlopen(elastcicRequest,context=ctx).read()

                send_webex_post("https://webexapis.com/v1/messages",
                               {"roomId": webhook['data']['roomId'], "markdown": str(test)}  )  
        else:
            print(cyan('This is a message is a reply sent by BOT. Don t handle it',bold=True))
        return "true"


        
def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts=False):
    if type(data) == 'str':
        return data.encode('utf-8')
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.items()
        }
    return data
    
def send_webex_get(url):
    request = urllib2.Request(url,
                              headers={"Accept": "application/json",
                                       "Content-Type": "application/json"})
    request.add_header("Authorization", "Bearer " + bearer)
    contents = urllib2.urlopen(request, context=ctx).read()
    return contents

def send_webex_post(url, data):
    request = urllib2.Request(url, json.dumps(data).encode('utf-8'),
                              headers={"Accept": "application/json",
                                       "Content-Type": "application/json"})
    request.add_header("Authorization", "Bearer " + bearer)
    contents = urllib2.urlopen(request, context=ctx).read()
    return contents
    

def webex_print(header, message):
    global investigation_report
    if debug_flag:
        print(header + message.replace('\n', ''))
    investigation_report.append(header + message)
    return

def delete_webhook(webhook_id):

    url = "https://webexapis.com/v1/webhooks/" + webhook_id

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer " + bearer
    }

    requests.request("DELETE", url, headers=headers, data=payload)


def add_webhook():

    url = "https://webexapis.com/v1/webhooks"
    payload = "{\"name\": \"" + webhook_name + "\",\"targetUrl\": \"" + webhook_url + "\",\"resource\": \"messages\",\"event\": \"created\"}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + bearer
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)


def update_webhook():

    url = "https://webexapis.com/v1/webhooks"
    payload = "{\"name\": \"" + webhook_name + "\",\"targetUrl\": \"" + webhook_url + "\",\"status\": \"active\"}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + bearer
    }

    requests.request("PUT", url, headers=headers, data=payload)


def get_bot_status():
    url = "https://webexapis.com/v1/rooms"
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer " + bearer
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json_loads_byteified(response.text)
    print(yellow("Bot is currently member of Webex Rooms:",bold=True))
    if 'items' in data:
        for room in data['items']:
            print(green("     ID: {}".format(room['id']),bold=True))

    url = "https://webexapis.com/v1/webhooks"
    response = requests.request("GET", url, headers=headers, data=payload)
    data = json_loads_byteified(response.text)
    print(green("Bot is currently configured with webhooks:",bold=True))
    if 'items' in data:
        for webhook in data['items']:
            print(" => ID: {}".format(webhook['id']))
            print("     Name: {}".format(webhook['name'].encode('utf8')))
            print("     Url: {}".format(webhook['targetUrl']))
            print(green("     Status: {}".format(webhook['status']),bold=True))
            if webhook['name'] != webhook_name:
                print("    === REMOVING WEBHOOK ===")
                delete_webhook(webhook['id'])
                print("    === REMOVED ===")
            if webhook['status'] != 'active':
                print("    === UPDATING WEBHOOK STATUS ===")
                update_webhook()
                print("    === STATUS UPDATED ===")
            if (webhook['targetUrl'] != webhook_url):
                print("    === NEED TO UPDATE WEBHOOK ===")
                delete_webhook(webhook['id'])
                print("    === OLD WEBHOOK REMOVED ===")
                print("    === ADDING NEW WEBHOOK ===")
                add_webhook()
                print("    === NEW WEBHOOK ADDED ===")
        if len(data['items']) == 0:
            print("    === NO WEBHOOKS DETECTED ===")
            add_webhook()
            print("    === NEW WEBHOOK ADDED  ===")        
def main():
    print(yellow("Don't forget to start NGROK with : ngrok http 3000",bold=True))
    print()
    print(yellow("Let's check the Webex Team Bot Status",bold=True))
    get_bot_status()
    print(yellow("Bot Ready, Let's start the Web Server and listen on Port 3000",bold=True))
    httpd = HTTPServer(('localhost', 3000), SimpleHTTPRequestHandler)
    httpd.serve_forever()


if __name__== "__main__":
    main()
