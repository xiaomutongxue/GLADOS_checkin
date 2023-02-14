import requests, os, json



# 填写微信PUSH_PLUS_TOKEN,不开启则不用填
PUSH_PLUS_TOKEN1 = "xxxxxxxx"
# 填入glados账号对应cookie
GLADOS_COOKIE1 = "xxxxxxxx"

def start(GLADOS_COOKIE,PUSH_PLUS_TOKEN):
    url = "https://glados.rocks/api/user/checkin"
    url2 = "https://glados.rocks/api/user/status"
    origin = "https://glados.rocks"
    referer = "https://glados.rocks/console/checkin"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    payload = {
        'token': 'glados.network'
    }
    checkin = requests.post(url,
                            headers={'cookie': GLADOS_COOKIE, 'referer': referer, 'origin': origin, 'user-agent': useragent,
                                     'content-type': 'application/json;charset=UTF-8'}, data=json.dumps(payload))
    state = requests.get(url2,
                         headers={'cookie': GLADOS_COOKIE, 'referer': referer, 'origin': origin, 'user-agent': useragent})
    # print(res)

    if 'message' in checkin.text:
        mess = checkin.json()['message']
        if mess == '\u6ca1\u6709\u6743\u9650':
            if(PUSH_PLUS_TOKEN != 'xxxxxxxx'):
                notice("cookie过期,请重新获取COOKIE",PUSH_PLUS_TOKEN)
            else:
                print("未设置PUSH_PLUS_TOKEN，不开启通知。")
        else:
            time = state.json()['data']['leftDays']
            time = time.split('.')[0]
            # print(time)
            mess2 = "*************GlaDOS签到小助手*************"
            mess2 = "GlaDOS签到:" + mess + '，你还有 ' + time + ' 天!'
            notice( mess2,PUSH_PLUS_TOKEN)


def notice( mess,PUSH_PLUS_TOKEN):
    url = "http://www.pushplus.plus/send"

    data = {
            "token": PUSH_PLUS_TOKEN1,
            "title": "GlaDOS签到小助手",
            "content": mess,
            "topic": '',
        }
    body = json.dumps(data).encode(encoding="utf-8")
    headers = {"Content-Type": "application/json"}
    response = requests.post(url=url, data=body, headers=headers).json()
    print(response)
    if response["code"] == 200:
        print("PUSHPLUS 推送成功！")

if __name__ == '__main__':
    if "PUSH_PLUS_TOKEN" in os.environ:
        PUSH_PLUS_TOKEN = os.environ["PUSH_PLUS_TOKEN"]
    else:
        PUSH_PLUS_TOKEN = PUSH_PLUS_TOKEN1
    if "GLADOS_COOKIE" in os.environ or GLADOS_COOKIE1 !="xxxxxxxx":
        if "GLADOS_COOKIE" in os.environ:
            GLADOS_COOKIE = os.environ["GLADOS_COOKIE"]
        if(GLADOS_COOKIE1 !="xxxxxxxx"):
            start(GLADOS_COOKIE1,PUSH_PLUS_TOKEN)
        else:
            start(GLADOS_COOKIE,PUSH_PLUS_TOKEN)

