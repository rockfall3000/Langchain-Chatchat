import numpy as np
import time


def test_argsort():
    #all_scores= [ [[98, 95, 92, 99, 78], [95, 85, 68, 48, 45], [98, 95, 92, 99, 25], [98, 72, 58, 99, 75], [98, 95, 92, 99, 48] ]]
    all_scores= [ 1,3,4,8,2, 10, 5]
    print(all_scores)
    indeies = np.argsort(all_scores)[::-1]
    print(indeies)
    for i in range(len(all_scores)):
        print(all_scores[indeies[i]])


def test_time():
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(now)
    now = time.strftime("%Y%m%d%H%M%S", time.localtime())
    print(now)





