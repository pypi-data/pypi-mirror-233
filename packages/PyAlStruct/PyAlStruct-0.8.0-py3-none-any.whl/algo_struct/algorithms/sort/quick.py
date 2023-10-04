class QuickSort:
    def _quick_sort(self, arr, low, high):
        """
        Helper function for quick sort.
        :param arr: The array to be sorted.
        :param low: The first index in the list.
        :param high: The last index in the list.
        """
        if low < high:
            pivot = arr[high]
            i = low - 1
            for j in range(low, high):
                if arr[j] < pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            pivot_index = i + 1
            self._quick_sort(arr, low, pivot_index - 1)
            self._quick_sort(arr, pivot_index + 1, high)

    def sort(self, arr):
        """
        Perform quick sort on the input list 'arr' in-place.

        :param arr: The input list to be sorted.
        :return: arr -- The sorted array.
        """
        sorted_arr = arr.copy()
        self._quick_sort(sorted_arr, 0, len(sorted_arr) - 1)
        return sorted_arr


# Example usage:
if __name__ == "__main__":
    my_list = [64, 34, 25, 12, 22, 11, 90]
    merge_sort = QuickSort()
    sorted_list = merge_sort.sort(my_list)

    print("Original List:", my_list)
    print("Sorted List:", sorted_list)
