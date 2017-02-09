import multiprocessing, time

def calc_square(numbers, q):
    for n in numbers:
        q.put(n*n)
        time.sleep(.2)

def calc_double(q):
    a = 2
    while a>1:
        num = q.get()
        print(num*2)

if __name__ == "__main__":
    numbers = [2, 3, 5]
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=calc_square, args=(numbers, q))
    p2 = multiprocessing.Process(target=calc_double, args=(q,))

    p.start()
    p2.start()

    p.join() 
    p2.join()
