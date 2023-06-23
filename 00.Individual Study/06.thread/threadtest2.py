import threading
from datetime import datetime

class Tread1(threading.Thread) :
    def run(self) :
        for i in range(100) :
            now = datetime.now()
            print(now)

class Tread2(threading.Thread) :
    def run(self) :
        for i in range(1000) :
            print(i)

# t1 = Tread1()
# t1.start()

# t3 = Tread2()
# t3.start()

t2 = Tread2()
t2.daemon=True
t2.start()