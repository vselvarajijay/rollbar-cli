import fire, sys
from flows.boot import Boot



if __name__ == '__main__':
    if len(sys.argv) == 1:
        boot = Boot()
        boot.start()
    else:
        fire.Fire()
