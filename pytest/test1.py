import time
import multiprocessing

def update_progress(progress, sleep_time=1):
    bar_length = 20
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(bar_length*progress))
    text = "\rPercent: [{0}] {1}% {2}".format("#"*block + "-"*(bar_length-block), progress*100, status)
    print(text, end="")
    time.sleep(sleep_time)


if __name__ == '__main__':
    #pool = multiprocessing.Pool(2)
    for i in range(101):
        update_progress(i/100)
        #temp_send = pool.apply_async(update_progress,(i/100))