from flask import Flask, request

# 載入 json 標準函式庫，處理回傳的資料格式
import json
import shutil

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

@app.route("/api/LineSaveBot", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        access_token = '4ZB/3l4oMmhE1N7wptjVM93w7KJESmMG8Y6cuVnixjNyqU9bxVpplslgFVOT/dumv8D48POyq2cvfszxvAyxBYuY2E0tEu7B2ZN5czYx6PcUfk5LDK0/U7UdJ0s5aSdI29qxO1YvtCEU3jbT6WwdNQdB04t89/1O/w1cDnyilFU='                                    # 你的 Access Token
        secret = '85ee09f1b9be6639b5471a2afbe22134'                                          # 你的 Channel Secret
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        type = json_data['events'][0]['message']['type']     # 取得 LINE 收到的訊息類型
        # 判斷如果是文字
        if type=='text':
            '''
            msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息
            reply = msg
            '''
            reply = ''
        # 判斷如果是圖片
        elif type == 'image':
            msgID = json_data['events'][0]['message']['id']  # 取得訊息 id
            message_content = line_bot_api.get_message_content(msgID)  # 根據訊息 ID 取得訊息內容
            # 在同樣的資料夾中建立以訊息 ID 為檔名的 .jpg 檔案
            with open(f'{msgID}.jpg', 'wb') as fd:
                fd.write(message_content.content)             # 以二進位的方式寫入檔案
            
            dest1 = f'{msgID}.jpg'
            dest2 = r'C:\Users\Dennis Chou\Downloads\存檔'
            shutil.move(dest1,dest2)


            reply = '圖片儲存完成！'                             # 設定要回傳的訊息
        # 判斷如果是影片
        elif type=='video':
            msgID = json_data['events'][0]['message']['id']
            message_content = line_bot_api.get_message_content(msgID)
            with open(f'{msgID}.mp4', 'wb') as fd:
                fd.write(message_content.content)

            dest1 = f'{msgID}.mp4'
            dest2 = r'C:\Users\Dennis Chou\Downloads\存檔'
            shutil.move(dest1,dest2)


            reply = '影片儲存完成！'
        else:
            reply = '你傳的不是文字影片或圖片呦～'
        print(reply)
        line_bot_api.reply_message(tk,TextSendMessage(reply))  # 回傳訊息
    except:
        print(body)                                            # 如果發生錯誤，印出收到的內容
    return 'OK'                                                # 驗證 Webhook 使用，不能省略

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=443)
    '''
    (host='0.0.0.0', port=443)
    '''
