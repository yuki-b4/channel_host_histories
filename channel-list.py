from tokenize import generate_tokens
import requests
import pdb
import re
import csv

SLACK_CHANNEL_ID = 'C057JGRUJDB'
SLACK_URL = "https://slack.com/api/conversations.history"
TOKEN = "xoxp-3614707066023-3622707033654-5449811432391-3751a01182f9bbfb64d35616859a1937"

def get_https_strings(text):
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    https_strings = re.findall(pattern, text)
    return https_strings

def get_urls():
    payload = {
        "channel": SLACK_CHANNEL_ID,
        "oldest": "1622761200"
    }
    headersAuth = {
    'Authorization': 'Bearer '+ str(TOKEN),
    }  
    response = requests.get(SLACK_URL, headers=headersAuth, params=payload)
    json_data = response.json()
    msgs = json_data['messages']
    urls = []
    index = 1
    for msg in msgs:
      # slackチャンネルのURLは含めない
      if not ("https://saito-mentee" in msg["text"]) and (len(get_https_strings(msg["text"])) > 0):
        # 同じスレッドに複数のURLがあることを考慮
        for text in get_https_strings(msg["text"]):
          urls.append([index, text])
          index = index + 1

    print(urls)
    return urls

def generate_csv():
  postred_urls = get_urls()

  # CSVファイルのパス
  csv_file_path = 'posted_urls.csv'

  # CSVファイルを書き込みモードで開く
  with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["番号", "URL"])

    # 配列の各行をCSVファイルに書き込む
    for row in postred_urls:
        writer.writerow(row)

  print(f'CSVファイル "{csv_file_path}" が生成されました。')

generate_csv()
