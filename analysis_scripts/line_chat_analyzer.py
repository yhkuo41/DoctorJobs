import csv
from pprint import pprint

import numpy as np

import msg_filter
from analysis_scripts.line_chat_msg import LineChatMsg, str2set

ALGO_CSV = "data/line_chat_20220307_algo.csv"
MAN_CSV = "data/line_chat_20220307_man.csv"


def read_msg_from_file(file: str) -> list[LineChatMsg]:
    msg_list = []
    with open(file, 'r', encoding='UTF-8') as f:
        reader = csv.reader(f)
        next(reader)  # skip first row
        for row in reader:
            utc_ts = int(row[0])
            user = row[1]
            content = row[2]
            is_recruitment = row[3] == "T"
            city_tags = set()
            dept_tags = set()
            if len(row) > 4:
                city_tags = str2set(row[4])
            if len(row) > 5:
                dept_tags = str2set(row[5])
            msg_list.append(LineChatMsg(utc_ts, user, content, city_tags, dept_tags, is_recruitment))
    return msg_list


def print_list(mlist):
    for m in mlist:
        pprint(vars(m))


def tpfp(predictions: np.ndarray,
         ground_truth: np.ndarray,
         negative: int = 0.0,
         positive: int = 1.0,
         normalize: bool = True) -> dict:
    """
    Return a dictionary of accuracy and true/false negative/positive guesses.
    Args:
        predictions: an array of predicted labels
        ground_truth: an array of ground truth labels
        negative: a sentinel value indicating a negative label
        positive: a sentinel value indicating a positive label
        normalize: whether to normalize the tpfp values by the label counts
    Returns: a dictionary of metrics:
        'acc': the binary classification accuracy
        'tp':  the amount of true positives
        'tn':  the amount of true negatives
        'fp':  the amount of false positives
        'fn':  the amount of false negatives
    """
    # compute the raw accuracy
    acc = np.mean(predictions == ground_truth)
    # accumulate the true/false negative/positives
    tp = np.sum(np.logical_and(predictions == positive, ground_truth == positive))
    tn = np.sum(np.logical_and(predictions == negative, ground_truth == negative))
    fp = np.sum(np.logical_and(predictions == positive, ground_truth == negative))
    fn = np.sum(np.logical_and(predictions == negative, ground_truth == positive))

    # normalize the true/false negative/positives to a percentages if
    # normalization is enabled
    if normalize:
        # calculate the total number of positive guesses
        total_positive = np.sum(predictions == positive)
        if total_positive == 0:
            # avoid divide by zero
            tp = 0
            fp = 0
        else:
            # normalize by the total number of positive guesses
            tp = tp / total_positive
            fp = fp / total_positive

        # calculate the total number of negative guesses
        total_negative = np.sum(predictions == negative)
        if total_negative == 0:
            # avoid divide by zero
            tn = 0
            fn = 0
        else:
            # normalize by the total number of negative guesses
            tn = tn / total_negative
            fn = fn / total_negative

    # return a dictionary of the raw accuracy and true/false positive/negative
    # values
    return {
        'acc': acc,
        'tp': tp,
        'tn': tn,
        'fp': fp,
        'fn': fn
    }


if __name__ == '__main__':
    man_msgs = read_msg_from_file(MAN_CSV)
    algo_msgs = read_msg_from_file(ALGO_CSV)

    truth = np.array([m.is_recruitment for m in man_msgs])
    algo = np.array([m.is_recruitment for m in algo_msgs])

    print("過濾條件, 以下皆須滿足才判斷為職缺訊息:")
    for i in range(len(msg_filter.filters)):
        print(f"{i + 1}. {msg_filter.filters[i].filter_condition()}")
    print(f"判別結果: {tpfp(algo, truth)}\n")

    fn_msgs = []
    fp_msgs = []
    for i in range(len(man_msgs)):
        if man_msgs[i].is_recruitment and not algo_msgs[i].is_recruitment:
            fn_msgs.append(algo_msgs[i])
        elif not man_msgs[i].is_recruitment and algo_msgs[i].is_recruitment:
            fp_msgs.append(algo_msgs[i])

    print("========= fn 訊息(人工判斷為職缺，但簡易過濾判斷非職缺) =========")
    print_list(fn_msgs)
    print("========= fp 訊息(人工判斷為非職缺，但簡易過濾判斷職缺) =========")
    print_list(fp_msgs)
