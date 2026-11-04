# Broken Access Control

Repozytorium zawiera materiały praktyczne oraz prezentacje o podatności Broken Access Control (błędy kontroli dostępu). Celem zajęć jest zrozumienie, jak działa ten atak w praktyce oraz jak się przed nim chronić.

## Jak korzystać z repozytorium?

Potrzebujesz tylko Pythona i biblioteki Flask. Sklonuj repozytorium lub pobierz je jako plik ZIP, a następnie uruchom aplikację:

```bash
pip install flask
python zadania.py
```

Otwórz w przeglądarce http://127.0.0.1:5000 i zaloguj się jako `alice` / `alice123`.

> ⚠️ Aplikacja jest celowo podatna. Uruchamiaj ją tylko lokalnie.

## Zadania

Przygotowaliśmy trzy scenariusze testowe, bezpośrednio nawiązujące do przypadków z wykładu. Szczegółowe polecenia znajdziesz w [zadania.md](zadania.md).

1. **Zadanie 1: Faktury** - Zobaczysz, jak zmiana jednej liczby w adresie pozwala wejść w cudze dane.
2. **Zadanie 2: Panel administratora** - Sprawdzisz, dlaczego ukrycie przycisku nie chroni strony, do której można wejść wprost.
3. **Zadanie 3: Reset hasła** - Przekonasz się, co się dzieje, gdy aplikacja ufa informacjom z przeglądarki.

W każdym zadaniu najpierw wykorzystujesz lukę, a potem naprawiasz kod.

## Najważniejsza zasada

Sprawdzaj uprawnienia przy każdym żądaniu, po stronie serwera.
