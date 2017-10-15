import pymongo, re
import numpy as np
import matplotlib.pyplot as plt
from snownlp import SnowNLP
from collections import Counter
import pymysql
import mysql.connector

def readmysql():
    commentlist = []
    textlist = []
    # conn = pymongo.MongoClient(host='localhost', port=27017, charset="utf8")
    conn = pymysql.connect(host='localhost',user='root',password='root',charset="utf8")
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM sina.sinacomment")
        rows = cur.fetchall()
        # 去重
        for row in rows:
            row = list(row)
            # del row[0]
            if row not in commentlist:
                commentlist.append([row[0], row[1], row[2], row[3], row[4]])
                id = row[0]
                post_id = row[1]
                comment = row[2]
                refer = row[3]
                like_counts = row[4]
                if comment:
                    textlist.append(comment)
                print("id:%s post_id:%s comment:%s refer:%s like_counts:%s"
                         % (id, post_id, comment, refer, like_counts))
    return textlist


def snowanalysis(textlist):
    sentimentslist = []
    for li in textlist:
        s = SnowNLP(li)

        # pos_add_file = open("pos_add.txt", 'a', encoding="utf-8")
        # neg_add_file = open("neg_add.txt", 'a', encoding="utf-8")
        # if s.sentiments > 0.5:
        #     print("存入pos评论: %s" % li)
        #     pos_add_file.write(li + "\n")
        # elif s.sentiments < 0.5:
        #     print("存入neg评论: %s" % li)
        #     neg_add_file.write(li + "\n")
        # pos_add_file.close()
        # neg_add_file.close()

        sentimentslist.append(s.sentiments)
    fig1 = plt.figure("sentiment")
    plt.hist(sentimentslist, bins=np.arange(0, 1, 0.02))
    plt.show()


if __name__ == '__main__':
    textlist = readmysql()
    snowanalysis(textlist)
