import csv
import pdb
import re
from tokenize import generate_tokens

from bs4 import BeautifulSoup
import requests

SLACK_CHANNEL_ID = 'C057JGRUJDB'
SLACK_URL = "https://slack.com/api/conversations.history"
# 共有されたTOKENを代入
TOKEN = "hoge"

def get_https_strings(text):
    pattern = "(https?://.+?)>"
    https_strings = re.findall(pattern, text)
    https_strings = list(map(lambda x: re.sub('\|.+', '', x), https_strings))
    return https_strings

def get_title(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    # Twitterの投稿などでtitle要素が存在しないときは'タイトル'を返す
    try:
        return soup.title.text
    except:
        return 'タイトル'

def get_contents():
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
    contents = []
    index = 1
    for msg in msgs:
      # slackチャンネルとNotionページのURLは含めない
      if not ("https://saito-mentee" in msg["text"] or "https://www.notion.so" in msg["text"]) and (len(get_https_strings(msg["text"])) > 0):
        for url in get_https_strings(msg["text"]):
          title = get_title(url)
          contents.append([title, index, url])
          index = index + 1
    print(contents)
    return contents

def generate_csv():
  posted_contents = get_contents()

  # CSVファイルのパス
  csv_file_path = 'posted_contents.csv'

  # CSVファイルを書き込みモードで開く
  with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["名前", "番号", "URL"])

    # 配列の各行をCSVファイルに書き込む
    for row in posted_contents:
        writer.writerow(row)

  print(f'CSVファイル "{csv_file_path}" が生成されました。')

generate_csv()