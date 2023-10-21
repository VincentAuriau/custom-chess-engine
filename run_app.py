import sys

sys.path.append("python/")

from interface.interface import MyApp

if __name__ == "__main__":
    MyApp(play_with_ai=True).run()
