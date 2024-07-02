import time

from TestLongCallStrategy import test_long_call_strategy


def main():
    start = time.time()
    test_long_call_strategy()
    end = time.time()
    print(f"TIME: {end - start}")


if __name__ == '__main__':
    main()
