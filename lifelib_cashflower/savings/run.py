import time
import sys
from cashflower import start
from settings import settings


if __name__ == "__main__":
    beg = time.time()
    output = start("savings", settings, sys.argv)
    fin = time.time()
    print("Elapsed seconds =", fin-beg)
