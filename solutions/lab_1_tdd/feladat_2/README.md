# Feladat 2 – Perzisztens adattárolás SQLite adatbázissal

## Cél

Ebben a feladatban az [Feladat 1](../feladat_1/README.md)-ben elkészített Flask alapú TODO alkalmazást fejlesztjük tovább. Az eddigi memóriában tárolt lista helyett most egy helyi **SQLite adatbázis** fogja tárolni a teendőket, így az adatok az alkalmazás újraindítása után is megmaradnak.

A fejlesztés a TDD (tesztvezérelt fejlesztés) elvét követi:

> **Piros → Zöld → Refaktor**

Először egy hibás (failing) tesztet írunk, majd a minimálisan szükséges kóddal átmenővé (passing) tesszük azt.

---

## Projekt struktúra

```
feladat_2/
├── app.py          # Flask alkalmazás (ezt kell kiegészíteni)
├── schema.sql      # Adatbázis séma (todos tábla definíciója)
├── test_app.py     # Pytest tesztek
└── README.md
```

### `schema.sql`

Az adatbázis sémája egyetlen `todos` táblát definiál:

| Mező | Típus   | Leírás                          |
|------|---------|---------------------------------|
| `id` | INTEGER | Automatikus elsődleges kulcs    |
| `task` | TEXT  | A teendő szövege (kötelező)     |
| `done` | BIT   | Elvégzett-e? (0 = nem, 1 = igen)|

### `app.py`

Az alkalmazás váza már adott: tartalmazza az adatbázis-kapcsolat kezelését (`get_db`, `close_connection`, `init_db`). A feladatod az API végpontok implementálása.

### `test_app.py`

A tesztfájl egy `client` fixture-t definiál, amely:
- minden teszthez egy **ideiglenes SQLite adatbázist** hoz létre,
- inicializálja a sémát (`init_db`),
- a teszt végén törli az ideiglenes fájlt.

---

## Feladatok

### 1. Futtasd a teszteket

```bash
pytest
```

Figyeld meg, hogy a tesztek hibával futnak (piros fázis) – ez helyes, a TDD folyamat első lépése.

### 2. Implementáld a hiányzó végpontokat (zöld fázis)

Egészítsd ki az `app.py` fájlt az alábbi három végponttal, a **lehető legkevesebb kóddal**, ami a tesztek átmenéséhez szükséges:

| Végpont         | Metódus | Leírás                                                   | Várt válasz          |
|-----------------|---------|----------------------------------------------------------|----------------------|
| `/`             | GET     | Üdvözlő oldal                                            | 200, `"Welcome"` szöveg a válaszban |
| `/todos`        | GET     | Az összes teendő listázása JSON formátumban              | 200, JSON tömb       |
| `/todos`        | POST    | Új teendő létrehozása `{"task": "..."}` JSON törzzsel    | 201, az új elem adatai |

**Tipp:** Az adatbázis-kapcsolathoz használd a már meglévő `get_db()` segédfüggvényt.

### 3. Ellenőrzés böngészőből / curl-lel

Indítsd el az alkalmazást:

```bash
flask run
```

Az alkalmazás elérhető itt: [http://127.0.0.1:5000](http://127.0.0.1:5000)

Tesztelés parancssorból:

```bash
# Összes teendő lekérése
curl http://127.0.0.1:5000/todos

# Új teendő hozzáadása
curl -X POST -H "Content-Type: application/json" \
     -d '{"task": "Megírni a ZH-t"}' \
     http://127.0.0.1:5000/todos
```

---

## Az adatbázis inicializálása (első indítás előtt)

Ha az alkalmazást éles módban futtatod (nem tesztelési módban), az adatbázist egyszer létre kell hozni:

```bash
python -c "from feladat_2.app import init_db; init_db()"
```

Ez létrehozza a `todos.db` fájlt az aktuális könyvtárban, a `schema.sql` alapján.

---

## Mi a különbség az 1. feladathoz képest?

| Szempont           | Feladat 1 (memória)         | Feladat 2 (SQLite)                  |
|--------------------|------------------------------|--------------------------------------|
| Adattárolás helye  | Python lista (RAM)           | `todos.db` fájl (lemez)              |
| Adatok megmaradnak | Nem – újraindítás után elvesznek | Igen – perzisztens                |
| Tesztelés          | Egyszerű, nincs külső függőség | Ideiglenes DB-fájl fixture-rel      |
| Valósághoz közelebb | Kevésbé                     | Jobban                               |
