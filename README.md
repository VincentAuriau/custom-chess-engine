
```python
from interface.interface import MyApp

if __name__ == '__main__':
    MyApp().run()

```

![](interface_example.PNG)

Python methods to play a game:

```python
import sys
sys.path.append("python/")
import python.engine as engine

game = engine.engine.Game()
game.move_from_coordinates(game.player1, 1, 4, 3, 4)
game.move_from_coordinates(game.player2, 6, 0, 5, 0)
```
