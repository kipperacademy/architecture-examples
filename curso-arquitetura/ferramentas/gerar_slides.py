"""Regera as oito aulas a partir dos mecanismos revisados com concept-to-excalidraw."""
from visual_engine import generate
from visuais_01_02 import D as aulas_01_02
from visuais_03_06 import D as aulas_03_06
from visuais_04_05 import D as aulas_04_05
from visuais_07_08 import D as aulas_07_08

if __name__ == "__main__":
    aulas = aulas_01_02 | aulas_03_06 | aulas_04_05 | aulas_07_08
    for pasta in sorted(aulas):
        generate(pasta, aulas[pasta])
