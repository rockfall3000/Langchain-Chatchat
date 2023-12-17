import np


def zigzag_sort(arr):
    """
    :type arr: List[int]
    :rtype: List[int]
    """
    if len(arr) <= 1:
        return arr
    left = 0
    right = len(arr) - 1
    mid = (left + right) // 2
    left_arr = arr[:mid]
    right_arr = arr[mid:]
    left_arr.reverse()
    right_arr.reverse()
    return left_arr + right_arr


print(zigzag_sort([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))