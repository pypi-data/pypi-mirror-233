class InsertionSort:
    def sort(self, arr):
        """
        Perform insertion sort on the input list 'arr' in-place.

        :param arr: The input list to be sorted.
        :return: arr -- The sorted array.
        """
        sorted_arr = arr.copy()
        for i in range(1, len(arr)):
            key = sorted_arr[i]
            j = i - 1

            # Move elements of arr[0..i-1], that are greater than key, one position ahead
            while j >= 0 and key < sorted_arr[j]:
                sorted_arr[j + 1] = sorted_arr[j]
                j -= 1

            sorted_arr[j + 1] = key
        return sorted_arr


# Example usage:
if __name__ == "__main__":
    my_list = [64, 34, 25, 12, 22, 11, 90]
    insertion_sort = InsertionSort()
    sorted_list = insertion_sort.sort(my_list)

    print("Original List:", my_list)
    print("Sorted List:", sorted_list)
