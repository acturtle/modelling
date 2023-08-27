import time
import sys
from cashflower import start
from settings import settings


if __name__ == "__main__":
    beg = time.time()
    output = start("basic_term_e", settings, sys.argv)
    fin = time.time()
    print("Elapsed seconds =", fin-beg)
