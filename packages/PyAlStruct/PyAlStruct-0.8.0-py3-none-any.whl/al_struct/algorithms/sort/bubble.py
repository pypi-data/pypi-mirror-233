class BubbleSort:
    def sort(self, arr):
        """
        Perform bubble sort on the input list 'arr' in-place.

        :param arr: The input list to be sorted.
        :return: arr -- The sorted array.
        """
        n = len(arr)
        sorted_arr = arr.copy()

        for i in range(n - 1):
            # Flag to check if any swaps were made in this pass
            swapped = False

            # Last i elements are already in place, so we don't need to check them
            for j in range(0, n - i - 1):
                if sorted_arr[j] > sorted_arr[j + 1]:
                    # Swap arr[j] and arr[j+1]
                    sorted_arr[j], sorted_arr[j + 1] = sorted_arr[j + 1], sorted_arr[j]
                    swapped = True

            # If no two elements were swapped in this pass, the list is already sorted
            if not swapped:
                break
        return sorted_arr


# Example usage:
if __name__ == "__main__":
    my_list = [64, 34, 25, 12, 22, 11, 90]
    bubble_sort = BubbleSort()
    sorted_list = bubble_sort.sort(my_list)

    print("Original List:", my_list)
    print("Sorted List:", sorted_list)
