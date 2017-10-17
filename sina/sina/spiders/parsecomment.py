import numpy as np
import matplotlib.pyplot as plt
from snownlp import SnowNLP
from NlpTencentParse import SelectDataFromMysql


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
    textlist = SelectDataFromMysql()
    snowanalysis(textlist)
