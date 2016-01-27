# -*- coding: utf-8 -*-

import tweepy
import datetime  # datetimeモジュールのインポート
import time
import sys

argvs = sys.argv
argc = len(argvs)

if argc != 2:
    print('ファイルを指定してください')
    exit()

filename = argvs[1]


def getapi():
    with open('keys.txt', 'r') as f:
        keys = f.readlines()
    CONSUMER_KEY = keys[0].strip()
    CONSUMER_SECRET = keys[1].strip()
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    redirect_url = auth.get_authorization_url()
    print('次のURLブラウザにコピーして開いて認証して' + redirect_url)
    verifier = input('ここにPINコードを入力：').strip()
    auth.get_access_token(verifier)
    ACCESS_TOKEN = auth.access_token
    ACCESS_SECRET = auth.access_token_secret
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    return tweepy.API(auth)


def getmojisuu(files):
    with open(files, 'r') as f:
        mojisuu = len(f.read())
    return mojisuu


def tweet(api, status, before=0):
    if before == 0:
        try:
            now = api.update_status(status)
            print(status)
            return now
        except:
            print('ツイート失敗したよ')
            return 0
    else:
        try:
            now = api.update_status(status, in_reply_to_status_id=before.id)
            print(status)
            print('in_reply_to', before.id)
            return now
        except:
            print('ツイート失敗したよ')
            return 0

api = getapi()

mojisuu = getmojisuu(filename)
beforemojisuu = mojisuu
status = 'いまのsotsuron.texの文字数は' + str(mojisuu) + 'です．'
before = tweet(api, status)

d = datetime.datetime.today()
print(str(59 - d.minute) + '分スリープします')
time.sleep((59 - d.minute) * 60)

while True:
    d = datetime.datetime.today()
    if(d.minute == 0):
        mojisuu = getmojisuu(filename)
        if mojisuu > beforemojisuu:
            status = 'いまのsotsuron.texの文字数は' + \
                str(mojisuu) + 'です．（' + str(mojisuu - beforemojisuu) + '文字増加）'
        elif mojisuu == beforemojisuu:
            status = 'いまのsotsuron.texの文字数は' + \
                str(mojisuu) + 'です．（変化なし）'
        else:
            status = 'いまのsotsuron.texの文字数は' + \
                str(mojisuu) + 'です．（' + str(beforemojisuu - mojisuu) + '文字減少）'
        beforemojisuu = mojisuu
        before = tweet(api, status, before)
        time.sleep(59 * 60)
        print('59分スリープします')
