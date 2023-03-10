import csv
from matplotlib import pyplot as plt
import numpy as np

from analysis_scripts.line_chat_msg import LineChatMsg
from analysis_scripts.msg_filter import JobMsgFilter

msg_filter = JobMsgFilter({"徵", "職缺"})


def remove_outliers(data, q1_, q3_):
    iqr = q3_ - q1_
    x_min = q1_ - 1.5 * iqr
    x_max = q3_ + 1.5 * iqr
    return [x for x in data if x_min <= x <= x_max]


if __name__ == '__main__':
    msg_list = []
    with open('data/line_chat_20220307.csv', 'r', encoding='UTF-8') as f:
        reader = csv.reader(f)
        next(reader)  # skip first row
        for row in reader:
            msg_list.append(LineChatMsg(row[0], row[1], row[2]))
    msg_list.sort(key=lambda _: len(_.content))

    msg_lens = np.array([len(msg.content) for msg in msg_list])
    q1 = np.quantile(msg_lens, 0.25)
    q3 = np.quantile(msg_lens, 0.75)
    msg_lens = remove_outliers(msg_lens, q1, q3)

    possible_job_msg_lens = np.array([len(msg.content) for msg in msg_list if msg_filter.apply(msg)])
    possible_job_msg_lens = remove_outliers(possible_job_msg_lens, q1, q3)

    plt.xlim(0, 310)
    plt.title("Msg Len Histogram")
    plt.ylabel("Frequency")
    plt.xlabel("Msg len")
    plt.hist(msg_lens, bins=100, alpha=0.5, label="raw data (without outliers)")
    plt.hist(possible_job_msg_lens, bins=100, alpha=0.5, label="msg after filter")
    plt.legend(loc='upper right')
    plt.savefig("msg_len.png")

    print("字數 訊息")
    for m in msg_list:
        if msg_filter.apply(m):
            print(len(m.content), m.content)
