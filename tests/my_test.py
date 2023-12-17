import numpy as np
import time


def test_argsort():
    #all_scores= [ [[98, 95, 92, 99, 78], [95, 85, 68, 48, 45], [98, 95, 92, 99, 25], [98, 72, 58, 99, 75], [98, 95, 92, 99, 48] ]]
    all_scores= [ 1,3,4,8,2, 10, 5]
    length = len(all_scores)
    print(all_scores)
    indeies = np.argsort(all_scores)[::-1]
    print(indeies)
    result = list(range(0, length))
    for i in range(length):
        print('i=%d,score=%d', i, all_scores[indeies[i]])
        if i % 2 == 0:
            idx = i//2
        else:
            idx = length-1-i//2
        result[idx] = all_scores[indeies[i]]
    print(result)


def test_time():
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(now)
    now = time.strftime("%Y%m%d%H%M%S", time.localtime())
    print(now)


test_argsort()


