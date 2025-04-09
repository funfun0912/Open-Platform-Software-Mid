import requests
from bs4 import BeautifulSoup
import csv

# PTT 熱門看板頁面
url = 'https://www.ptt.cc/bbs/hotboards.html'

# 取得網頁內容
response = requests.get(url)
response.encoding = 'utf-8'  # 避免亂碼

# 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(response.text, 'html.parser')

# 找到所有看板資訊
boards = soup.select('div.b-ent')

# 寫入 CSV 檔案
with open('static.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['看板名稱', '網址'])

    for board in boards:
        name = board.select_one('div.board-name').text
        link = 'https://www.ptt.cc' + board.a['href']
        writer.writerow([name, link])

print("✅ 完成！已將熱門看板寫入 static.csv")
