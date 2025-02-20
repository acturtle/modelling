import sys
import time
from cashflower import start
from settings import settings


if __name__ == "__main__":
    beg = time.time()
    output = start("basic_term", settings, sys.argv)
    fin = time.time()
    print("Elapsed seconds =", fin-beg)
