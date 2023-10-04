class NodeNotFoundException(Exception):
    def __init__(self, data):
        self.data = data
        super().__init__(f"Node with data '{data}' not found in the linked list")


class EmptyListException(Exception):
    def __init__(self):
        super().__init__("List is empty")


class EmptyStackException(Exception):
    def __init__(self):
        super().__init__("Stack is empty")


class EmptyQueueException(Exception):
    def __init__(self):
        super().__init__("Queue is empty")
