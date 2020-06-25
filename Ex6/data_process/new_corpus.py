import jieba
import csv
import numpy as np
import tqdm
import string

all_key = {}
total = -1
# 载入用户词典
jieba.load_userdict('user_dict.txt')
with open("DXYNews.csv", 'r', encoding='utf-8') as f:
    data = csv.reader(f)
    print("Cutting")
    # 统计
    for row in tqdm.tqdm(data):
        if total == -1:
            total += 1
            continue
        total += 1
        temp = {}
        text = row[4]
        # 分词
        cut_line = jieba.cut(text, cut_all=True)
        for word in cut_line:
            temp[word] = 1
        # 统计
        for key in temp:
            cnt = all_key.get(key, 0)
            all_key[key] = cnt + 1
corpus = np.zeros([1, 2], dtype=str)
print("Calculating")
punc = string.punctuation
c_punc = [' ', ' ', '\n', '\t', '，', '。', '%', '《', '》', '？',
          '“', '”', '（', '）', '：', '％', '、', '-', '·', '　']
# 计算每次词语的idf
for key in tqdm.tqdm(all_key):
    # 排除一些符号
    if not key in punc and not key in c_punc:
        # print(key)
        k = key
        p = '%0.10f' % (np.log10(total * 1.0 / (all_key[key] + 1)))
        corpus = np.vstack([corpus, [k, p]])
print("Saving")
# 需要手动去除一些符号
np.savetxt('new_corpus.txt', corpus[1:], fmt="%s", delimiter=' ', encoding='utf-8')