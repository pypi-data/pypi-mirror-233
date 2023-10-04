class SelectionSort:
    def sort(self, arr):
        """
        Perform selection sort on the input list 'arr' in-place.

        :param arr: The input list to be sorted.
        :return: arr -- The sorted array.
        """
        n = len(arr)
        sorted_arr = arr.copy()

        for i in range(n - 1):
            min_index = i

            # Find the index of the minimum element in the unsorted part of the list
            for j in range(i + 1, n):
                if sorted_arr[j] < sorted_arr[min_index]:
                    min_index = j

            # Swap the minimum element with the first element of the unsorted part
            sorted_arr[i], sorted_arr[min_index] = sorted_arr[min_index], sorted_arr[i]
        return sorted_arr


# Example usage:
if __name__ == "__main__":
    my_list = [64, 34, 25, 12, 22, 11, 90]
    selection_sort = SelectionSort()
    sorted_list = selection_sort.sort(my_list)

    print("Original List:", my_list)
    print("Sorted List:", sorted_list)
