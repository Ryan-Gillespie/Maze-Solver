class PriorityQueue(object):
    def __init__(self):
        self.queue = []
        self.max_len = 0

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def is_empty(self):
        return len(self.queue) == 0

    def len(self):
        return len(self.queue)

    def contains(self, target):
        for item in self.queue:
            if item['state'] == target:
                return True
        return False

    def enqueue(self, state_dict):
        in_open = False

        for item in self.queue:
            if item['state'] == state_dict['state']:
                # update the item in open to be the new node if the cost to get there is less
                if state_dict['g'] < item['g']:
                    item['parent'] = state_dict['parent']
                    item['g'] = state_dict['g']
                    item['h'] = state_dict['h']
                    item['f'] = state_dict['f']
                in_open = True
                break

        if not in_open:
            self.queue.append(state_dict)

            # track the maximum queue length, do not increase this if already in_open is true
            if len(self.queue) > self.max_len:
                self.max_len = len(self.queue)

    def requeue(self, from_closed):
        self.queue.append(from_closed)

        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)

    def pop(self):
        mindex = 0
        for i in range(1, len(self.queue)):
            if self.queue[i]['f'] < self.queue[mindex]['f']:
                mindex = i
        state = self.queue[mindex]
        del self.queue[mindex]
        return state


class Queue(object):
    def __init__(self):
        self.queue = []
        self.maxlen = 0
        self.len = 0

    # get whether or not the queue is empty
    def isempty(self):
        return len(self.queue) == 0

    # get the length of the stack
    def __len__(self):
        return self.len

    # enqueue states and their parents onto the queue
    def enqueue(self, node):
        self.queue.append(node)

        # update the length
        self.len += 1
        if self.len > self.maxlen:
            self.maxlen += 1

    # get the first item inserted to the queue and delete it
    def dequeue(self):
        self.len -= 1
        return self.queue.pop(0)


class Stack(object):
    def __init__(self):
        self.stack = []
        self.len = 0
        self.maxlen = 0

    # get whether the stack is empty
    def isempty(self):
        return len(self.stack) == 0

    # get the length of the stack
    def __len__(self):
        return self.len

    # push node to the top of the stack
    def push(self, node):
        self.stack.append(node)

        # update the length
        self.len += 1
        if self.len > self.maxlen:
            self.maxlen += 1

    # get the last pushed item from the stack and delete it
    def pop(self):
        self.len -= 1
        return self.stack.pop()
