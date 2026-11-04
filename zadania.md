## Przygotowanie
```
pip install flask
python zadania.py          # http://127.0.0.1:5000
```
Konta: `alice / alice123`, `bob / bob123`. **Zaloguj się jako alice** i rozwiązuj zadania w tej roli.
Poprawki wprowadzaj w pliku `zadania.py` (serwer przeładuje się sam).
Zepsułeś dane? Zrestartuj serwer (dane są tylko w pamięci).

---

## Zadanie 1: Faktury (funkcja `invoice`)
1. Po zalogowaniu jako alice kliknij swoją fakturę 101. Zobacz adres: `/invoice/101`.
2. Zmień w pasku adresu `101` na `201` i wciśnij Enter.
3. **Zapisz kwotę faktury 201.** Do kogo należy ta faktura?

**Pytanie:** Skąd serwer miał wiedzieć, że alice nie powinna jej widzieć?

**Naprawa:** w funkcji `invoice()` sprawdź, czy `inv["owner_id"]` jest równe `uid` (zalogowanemu użytkownikowi). Jeśli nie, zwróć `abort(404)`.

**Test:** `/invoice/101` działa, `/invoice/201` zwraca 404.

---

## Zadanie 2: Panel administratora (funkcje `admin_panel`, `admin_delete_invoice`)
1. Na stronie głównej alice nie ma linku do panelu admina.
2. Wpisz ręcznie `http://127.0.0.1:5000/admin`. Co widzisz?
3. Kliknij „usuń” przy fakturze 202 (należy do Boba).
4. Wyloguj się, zaloguj jako bob i sprawdź, czy faktura 202 zniknęła.

**Pytanie:** Czy ukrycie linku zabezpiecza stronę? Ile endpointów `/admin/...` jest w kodzie?

**Naprawa:** w **obu** funkcjach sprawdź rolę z danych serwera: `user["role"] != "admin"` → `abort(403)`.
**Bonus:** wyciągnij to do dekoratora `@admin_required`. Co by się stało, gdybyś zapomniał o jednej funkcji?

**Test:** alice dostaje 403 na `/admin` i na `/admin/delete-invoice/202`, a admin nadal ma dostęp.

---

## Zadanie 3: Reset hasła (funkcja `reset_password`)
1. Jako alice wejdź na `http://127.0.0.1:5000/manage/reset-password/3`. Otrzymasz „Brak uprawnień”.
2. Otwórz F12 → **Application** (Chrome) lub **Storage** (Firefox) → **Cookies**.
3. Zmień wartość ciasteczka `is_admin` z `false` na `true`.
4. Odśwież `/manage/reset-password/3`. Co się stało?
5. Wyloguj się i zaloguj jako `admin` hasłem `reset123`.

**Pytanie:** Kto ustala wartość tego ciasteczka? Dlaczego serwer nie powinien mu ufać?

**Naprawa:** w `reset_password()` przestań czytać `request.cookies`. Sprawdzaj rolę z danych serwera (`user["role"]`). Usuń też linię z `set_cookie("is_admin", ...)` w funkcji `login()`.

**Test:** alice z ciasteczkiem `is_admin=true` nadal dostaje 403, a admin może zresetować hasło.

---
