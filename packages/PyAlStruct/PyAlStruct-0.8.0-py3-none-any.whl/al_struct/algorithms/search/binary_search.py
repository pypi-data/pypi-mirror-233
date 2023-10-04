from al_struct.algorithms.sort import *


class BinarySearch:
    """
    Apply binary search for a target in an array.
    Default sort algorithm is selection sort.
    """
    def __init__(self, array, sort='selection'):
        match sort:
            case 'selection':
                self._sort = SelectionSort()
            case 'insertion':
                self._sort = InsertionSort()
            case 'bubble':
                self._sort = BubbleSort()
        self._array = self._sort.sort(array)

    @property
    def array(self):
        return self._array

    def exists(self, target) -> bool:
        """
        Return boolean value about the existence of the target.
        :param target: The target to search for.
        :return: bool -- True if target exists, otherwise False.
        """
        left, right = 0, len(self._array) - 1
        while left <= right:
            mid = left + (right - left) // 2
            if self._array[mid] == target:
                return True
            elif self._array[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return False

    def find_index(self, target) -> int:
        """
        Return the index of target if exists in the array.
        :param target: The target to search for.
        :return: int -- The index of target if exists, otherwise return '-1'.
        """
        left, right = 0, len(self._array) - 1
        while left <= right:
            mid = left + (right - left) // 2
            if self._array[mid] == target:
                return self._array.index(mid)
            elif self._array[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    def find_element(self, target):
        """
        Return the element if exists in the array.
        :param target: The target to search for.
        :return: The element if exists, otherwise 'None'.
        """
        left, right = 0, len(self._array) - 1
        while left <= right:
            mid = left + (right - left) // 2
            if self._array[mid] == target:
                return self._array[mid]
            elif self._array[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return None
