import requests
from dotenv import load_dotenv
import os
import json
import time



class Bot:

    tmp_ts = None

    def __init__(self):
        load_dotenv()

        self.token = os.getenv("ACCESS_TOKEN")
        self.user_id = os.getenv("USER_ID")

        self.api_uri = "https://api.vk.com/method/"


    def GetByConversationMessageId(self, peer_id):
        req_uri = self.api_uri + f"messages.getByConversationMessageId?peer_id={peer_id}&conversation_message_ids=1&extended=0&access_token={self.token}&v=5.131"
        r = requests.post(req_uri)
        print(r.text)

    def GetLongPollCredentials(self, need_pts=1, lp_version=3):
        req_uri = self.api_uri + f"messages.getLongPollServer?needpts={need_pts}&lp_version={lp_version}&access_token={self.token}&v=5.131"
        r = requests.post(req_uri)
        
        self.creds = json.loads(r.text)['response']
        print(self.creds)
    
    def __ConnectLongPoll(self):
        ts = None
        if self.tmp_ts is None:
            ts = self.creds['ts']
        else:
            ts = self.tmp_ts
        
        req_uri = f"https://{self.creds['server']}?act=a_check&key={self.creds['key']}&ts={ts}&wait=25&mode=2&version=3"
        r = requests.post(req_uri)
        events_json = json.loads(r.text)
        self.tmp_ts = events_json['ts']
        print(r.text)

    def ListenLongPoll(self):
        while True:
            self.__ConnectLongPoll()
            time.sleep(5)