import jieba
import jieba.analyse
import csv
import numpy as np

# 寻找那些有问题的符号
def check_corpus(new_idf_path):
    path = new_idf_path
    content = open(new_idf_path, 'rb').read().decode('utf-8')
    idf_freq = {}
    for line in content.splitlines():
        print(line)
        word, freq = line.strip().split(' ')

# check_corpus('new_corpus.txt')

time = []
seq = []
# 提取出与美国和欧洲有关的新闻
with open("DXYNews.csv", 'r', encoding='utf-8') as f:
    data = csv.reader(f)
    for row in data:
        if "美国" in row[4] or "欧洲" in row[4]:
            time.append(row[2].split()[0])
            seq.append(row[4])
str = '\n'.join(seq)

# 载入字典
key_num = 5
# jieba.load_userdict('user_dict.txt')
jieba.analyse.set_idf_path('new_corpus.txt')
jieba.analyse.set_stop_words('stop_words.txt')
tags = jieba.analyse.extract_tags(str, topK=100, withWeight=False, allowPOS=('n', 'nz', 'nt'))
print(tags)

tags = tags[:key_num]
data = {}
for t, s in zip(time, seq):
    update = data.get(t, {})
    for tag in tags:
        if tag in s:
            num = update.get(tag, 0)
            update[tag] = s.count(tag)
        else:
            update[tag] = 0
    data[t] = update

data = sorted(data.items(), key=lambda i: i[0])
headers = ['Date'] + tags
rows = []
for k in data:
    if k[0] != 'pubDate':
        tmp = k[1]
        tmp['Date'] = k[0]
        rows.append(tmp)
print(rows)
# 导出数据
with open('data.csv', 'w', encoding='utf-8') as f:
    f_csv = csv.DictWriter(f, headers, lineterminator = '\n')
    f_csv.writeheader()
    for r in rows:
        f_csv.writerow(r)

