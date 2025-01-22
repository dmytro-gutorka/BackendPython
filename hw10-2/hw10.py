import multiprocessing

def collatz_sequence(n):
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    return n, steps

def worker(start, end, queue):
    for n in range(start, end):
        result, steps = collatz_sequence(n)
        
        queue.put((n, result, steps))

def main():
    start = 1
    end = 1000000000
    num_processes = 4 

    
    chunk_size = (end - start) // num_processes
    processes = []
    queue = multiprocessing.Queue()


    for i in range(num_processes):
        chunk_start = start + i * chunk_size
        chunk_end = chunk_start + chunk_size if i != num_processes - 1 else end
        p = multiprocessing.Process(target=worker, args=(chunk_start, chunk_end, queue))
        processes.append(p)
        p.start()

    
    for p in processes:
        p.join()

   
    while not queue.empty():
        n, result, steps = queue.get()
        if result != 1:
            print(f"Гіпотеза не підтверджується для числа {n}")
       
        if n % 100000 == 0:
            print(f"Перевірено: {n}")

if __name__ == "__main__":
    main()
