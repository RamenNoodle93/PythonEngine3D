# Silnik graficzny z OpenGL
## Tworzenie niestandardowych obiektów
Przykładowy kod tworzenia obiektu
```
import numpy as np
from Tools.Objects.object import Object #podstawowa klasa obiektu

class Nazwa(Object):
  def __init__(self, position = np.array([0, 0, 0], float), rotation = np.array([0, 0, 0], float), scale = 1, color = (255, 255, 255)):
    #Zawarcie domyślnych wartości w konstruktorze jest ważne, ponieważ klasa Object ich nie posiada;
    #Oczywiście przy deklaracji obiektu w głównym programie gry te wartości zawsze powinny być podane, jednak taka implementacja pomaga zapobiec błędom;
    super().__init__(position, rotation, scale, color)

    self.AddNodes([[x, y, z]])
    #Metoda AddNodes() jako argument przyjmuje dwuwymiarową tablicę o rozmiarze (ilość punktów, 3);
    #Wartości x, y, z powinny być w zakresie <-1, 1>;

    self.AddEdges([[a, b]])
    #Metoda AddEdges() jako argument przyjmuje dwuwymiarową tablicę o rozmiarze (ilość brzegów, 2);
    #Wartości a i b, to indeksy punktów, które chcemy połączyć w tablicy self.nodes;

    self.CreateHitbox()
    #Ta metoda nie wymaga argumentów;
    #Automatycznie tworzy hitbox danego obiektu, domyślnie o kształcie prostopadłościanu;
