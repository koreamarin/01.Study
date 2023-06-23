import threading, time

def aaa() :
    a = 0
    while(True) :
        a += 1
        print(a)
        time.sleep(0.1)

def bbb() :
    print(111)
    time.sleep(0.1)
    print(222)
    time.sleep(0.1)
    print(333)
    time.sleep(0.1)

# threading.Thread(target=aaa).start()
# aaa()
# threading.Thread(target=bbb).start()
# bbb()

a = threading.Thread(target=aaa)
# 데몬을 True로 하면 프로세스가 종료될 때 쓰레드도 종료된다.
a.daemon = True
b = threading.Thread(target=bbb)
a.start()
b.start()