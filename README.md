# Test rozumowania przez analogię
 
1) Wartości parametrów w pliku xlsx wygenerowanym przez general_experiment.py:
    
    Każdy wiersz oznacza trial, który zostanie wyświetlony na ekranie
    
    A) BLOCK_NUMBER
    - liczba naturalna dodatnia, która określa do którego bloku należy dany trial
    - bloki zostaną wyświetlone kolejno od najniższego numeru do najwyższego
    - triale należące do tego samego bloku nie muszą się znajdować bezpośrednio po sobą
    - kolejność występowania triali w bloku określa kolejność wyświetlenia ich podczas eksperymentu (chyba, że zostanie włączona opcja randomizacji)

    B) TYPE
    - może przyjmować trzy wartości
        * instruction (zawiera tylko i wyłącznie informacje w kolumnie A, B, C, G)
        * training
        * experiment

    C) SHOW_TIME
    - liczba naturalna dodatnia
    - czas prezentacji triala określony w .........

    D) RELATIONS
    - może przyjmować wartości 2, 3 albo 4
    - określa w ilu figurach w matrycy zmieniono cechy percepcyjne

    E) FEEDB
    - może przyjmować wartości 0, 1 albo 2
        * 0 (nie wyświetlaj informacji o poprawności rozwiązania tego triala)
        * 1 (wyświetl informację o poprawności rozwiązania tego triala)
        * 2 (na koniec testu podaj całkowity wynik wszystkich rozwiązanych triali)

    F) WAIT_TIME
    - liczba naturalna
        * 0 ( po trialu wyświetla napis „naciśnij przycisk” i czeka na reakcję badanego- czas na odpoczynek)
        * inne (czas przerwy pomiędzy próbami określony w .........)

    G) TIP
    - link do pliku
    - plik w formacie txt, bmp, jpg
    - przed trialem wyświetla informację znajdująca się w pliku

    H) TIP_TIME
    - czas prezentacji wskazówki
    - w przypadku trialu typu instruction czas wyświetlania informacji z TIP jest podany w SHOW_TIME

    J) Weryfikacja
    - określa czy dane w wierszu zostały poprawnie wprowadzone (przy założeniu, że użytkownik jest inteligentny)
        * 1 (dane wprowadzone poprawnie)
        * 0 (dane wprowadzone błędnie)
    - pierwsza liczba w kolumnie określa ile triali zostało wprowadzonych poprawnie

2) Wartości parametrów w pliku yaml wygenerowanym przez concrete_experiment.py:

    - informacje w pliku są podawane zgodnie z kolejnością wyświetlania
    - struktura ma postać drzewiastą. Spis elementów poczynając od najbardziej ogólnych
        * experiment
            + name (nazwa osoby badanej w postaci ID+SEX+AGE)
            + list_of_blocks (lista występujących kolejno po sobie bloków)
        * experiment_elements (lista elementów w danym bloku)
            + może zawierać trzy typy elementów (TYPE)
        * instruction
            + instruction_type (text, image)
            + path (ścieżka do pliku zawierającego instrukcję, TIP)
            + time (SHOW_TIME)
        * experiment, training
            + poza elementami opisanymi w podpunkcie 1 zawiera matrix_info
        * matrix_info (macierz)
            + name
                @ zawiera macierze w kolejności, która ma byc wyświetlona na ekranie
                    A   matrix_info[3]  matrix_info[4]  matrix_info[5]
                    B   matrix_info[6]  matrix_info[7]  matrix_info[8]
                    C
                @ macierze A, B, C są macierzami opisanymi w dokumentacji projektu
                @ macierze D1-6 są różnymi wariantami modyfikacji macierzy C
                @ kolejne cyfry przy literze D oznaczają kolejne modyfikacje C zgodnie z dokumentacja projektu
            + parameters (określa parametry kolejnych figur w macierzy)
        * parameters (figura)
            + brightness: ('white', 'gray', 'slate')
            + figure (1-20 numery odpowiadają kolejnym figurą opisanym w dokumentacji)
            + frame ('thin', 'narrow', 'wide')
            + rotation (0, 90, 180, 270)
            + elements_changed
                @ zawiera spis parametrów, które się zmieniły (frame, rotation, brightness)
                @ dla każdego parametru określony jest poziom jego zmiany
                @ poziomy danego parametru sa różne dla każdej figury w matrycy
                @ W matrycy B elements_changed określa zmianę względem matrycy A
                @ W matrycach D1-6 elements_changed określa zmianę względem matrycy C
