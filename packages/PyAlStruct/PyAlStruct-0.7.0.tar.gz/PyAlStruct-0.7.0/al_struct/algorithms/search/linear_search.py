class LinearSearch:
    """
    Apply linear search for a target in an array.
    """
    def __init__(self, array):
        self._array = array

    @property
    def array(self):
        return self._array

    def exists(self, target) -> bool:
        """
        Return boolean value about the existence of the target.
        :param target: The target to search for.
        :return: bool -- True if target exists, otherwise False.
        """
        for element in self._array:
            if element == target:
                return True
        return False

    def find_index(self, target) -> int:
        """
        Return the index of target if exists in the array.
        :param target: The target to search for.
        :return: int -- The index of target if exists, otherwise return '-1'.
        """
        for element in self._array:
            if element == target:
                return self._array.index(target)
        return -1

    def find_element(self, target):
        """
        Return the element if exists in the array.
        :param target: The target to search for.
        :return: The element if exists, otherwise 'None'.
        """
        for element in self._array:
            if element == target:
                return element
        return None
