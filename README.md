## A projekt beállítás

- Nyisd meg a Visual Studio Code alkalmazást
- Nyiss egy új terminált és válaszd ki a git bash opciót
- Forkold ezt a GitHub repository-t, majd klónozhatod a helyi gépedre: [Github projekt](https://github.com/CsDenes/sze-test-lab-2026/tree/main)

```bash
git clone https://github.com/<felhasznalo>/sze-test-lab-2026/tree/main
```

### Telepítés

Nyiss meg egy terminált és futtasd a következő parancsokat, amivel létrehozunk egy python virtuális környezetet és telepítjuk a szükséges csomagokat.

```bash
# Hozz létre és aktiválj egy virtuális környezetet
python3 -m venv venv
#Windows
source venv/Scripts/activate
#Mac/Linux
source ./venv/bin/activate

# Telepítsd a szükséges könyvtárakat
pip install flask pytest

```

Az Flask web alkalmazás a következővel paranccsal futtatható:

```bash
flask run
```

Majd az alkalmazás böngészőben itt megnyitható: `http://127.0.0.1:5000`


Feladatok

- [1. labor - TDD](lab_1_tdd/README.md)