# Ćwiczenia praktyczne 1 
# 1. Utwórz klasę Logger, która:
# przy wejściu do kontekstu (__enter__) wypisuje „Start sekcji logowania”,
# przy wyjściu (__exit__) wypisuje „Koniec sekcji logowania”.
# Użyj jej w bloku with, wypisując coś w środku.
class Logger:
    def __enter__(self):
        print("Start sekcji logowania")
        return self

    def __exit__(self, exc_type, exc_value, traceback): #exit zawsze musi przyjmowac te 3 argumenty!!!
        print("Koniec sekcji logowania")

with Logger() as log:
    print("Coś się dzieje w środku")

#--------------------------------------
# 2. Napisz klasę FileWriter, która:
# w __init__ przyjmuje ścieżkę do pliku,
# w __enter__ otwiera plik do zapisu i zwraca uchwyt (file handle),
# w __exit__ zamyka plik niezależnie od tego, czy wystąpił wyjątek.
# Przetestuj zapis tekstu do pliku w bloku with

# 3. Zmodyfikuj FileWriter, tak by:
# gdy w środku bloku with wystąpi wyjątek, __exit__ wypisał komunikat: „Błąd podczas zapisu: <treść wyjątku>”.
# wyjątek nie był tłumiony (czyli dalej przerywał program).

class FileWriter:
    def __init__(self, path):
        self.path=path
        self.file=None

    def __enter__(self):
        self.file= open(self.path, 'w', encoding='utf-8') 
        return self.file                                   

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()  
        if exc_value is not None:
            print(f"Błąd podczas zapisu: {exc_value}")
        else:
            print("plik zamknięty")
        return False  # wyjatek nie jest tlumiony               


with FileWriter('testowy.txt') as f:
    f.write("pierwsza linijka\n")
    f.write("druga\n")
    # raise ValueError("cos nie tak") 

#-----------------------------------------------------------------------
# 4. Napisz klasę SafeDivision, która:
# w __enter__ zwraca samą siebie. 
# ma metodę divide(a, b) dzielącą liczby,
# w __exit__ tłumi wyjątki typu ZeroDivisionError, wypisując komunikat „Nie można dzielić przez zero”

class SafeDivision:
    def __init__(self, a, b):
        self.a=a
        self.b=b

    def __enter__(self):
        return self

    def divide(self, a, b):
        return a/b

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is ZeroDivisionError:
            print("Nie można dzielić przez zero")
            return True # tlumimy tylko ZeroDivisionError
        return False    #inne wyjatki nie sa tlumione

with SafeDivision(10, 2) as sd:
    print(sd.divide(10, 2)) #ok

with SafeDivision(1, 0) as sd:
    print(sd.divide(1, 0))  #nie można dzielić przez zero

with SafeDivision('1', 'a') as sd:
    print(sd.divide(1, 0)) 