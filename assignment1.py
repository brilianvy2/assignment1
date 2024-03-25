import random
import threading
import queue

MAX_COUNT = 10
LOWER_NUM = 1
UPPER_NUM = 100

class Producer(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        for _ in range(MAX_COUNT):
            num = random.randint(LOWER_NUM, UPPER_NUM)
            self.queue.put(num)
            with open("all.txt", "a") as file:
                file.write(str(num) + "\n")
        self.queue.put(None)  # Signal to Consumer that Producer is done


class Consumer(threading.Thread):
    def __init__(self, queue, even):
        super().__init__()
        self.queue = queue
        self.even = even

    def run(self):
        while True:
            num = self.queue.get()
            if num is None:  # If Producer is done
                break
            if (num % 2 == 0 and self.even) or (num % 2 != 0 and not self.even):
                filename = "even.txt" if self.even else "odd.txt"
                with open(filename, "a") as file:
                    file.write(str(num) + "\n")


def main():
    q = queue.Queue()
    producer = Producer(q)
    consumer_even = Consumer(q, True)
    consumer_odd = Consumer(q, False)

    producer.start()
    consumer_even.start()
    consumer_odd.start()

    producer.join()
    consumer_even.join()
    consumer_odd.join()


if __name__ == "__main__":
    main()