import sys

sys.path.append("python/")

from pyalapin.interface.interface import MyApp

if __name__ == "__main__":
    MyApp(play_with_ai=True).run()
