from time import *
def printer(text, delay):
    
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)