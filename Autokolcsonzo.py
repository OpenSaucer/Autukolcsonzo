from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime

# ==========================================
# 1. ABSZTRAKT ALAPOSZTÁLY
# ==========================================
class Auto(ABC):
    def __init__(self, rendszam: str, tipus: str, alap_berleti_dij: int):
        self._rendszam = rendszam
        self._tipus = tipus
        self._alap_berleti_dij = alap_berleti_dij

    @property
    def rendszam(self):
        return self._rendszam

    @property
    def tipus(self):
        return self._tipus

    @property
    def alap_berleti_dij(self):
        return self._alap_berleti_dij

    @abstractmethod
    def szamol_berles_dij(self) -> int:
        pass


# ==========================================
# 2. SZÁRMAZTATOTT OSZTÁLYOK
# ==========================================
class Szemelyauto(Auto):
    def __init__(self, rendszam: str, tipus: str, alap_berleti_dij: int, utasok_szama: int):
        super().__init__(rendszam, tipus, alap_berleti_dij)
        self._utasok_szama = utasok_szama

    def szamol_berles_dij(self) -> int:
        return self._alap_berleti_dij


class Teherauto(Auto):
    def __init__(self, rendszam: str, tipus: str, alap_berleti_dij: int, teherbiras: float):
        super().__init__(rendszam, tipus, alap_berleti_dij)
        self._teherbiras = teherbiras

    def szamol_berles_dij(self) -> int:
        return int(self._alap_berleti_dij * 1.2)


# ==========================================
# 3. BÉRLÉS OSZTÁLY
# ==========================================
class Berles:
    def __init__(self, auto: Auto, datum: str):
        self._auto = auto
        self._datum = datum

    @property
    def auto(self):
        return self._auto

    @property
    def datum(self):
        return self._datum

    def __str__(self):
        return f"Autó: {self._auto.tipus} ({self._auto.rendszam}) | Dátum: {self._datum} | Bérleti díj: {self._auto.szamol_berles_dij()} Ft"


# ==========================================
# 4. AUTÓKÖLCSÖNZŐ OSZTÁLY
# ==========================================
class Autokolcsonzo:
    def __init__(self, nev: str):
        self._nev = nev
        self._autok: list[Auto] = []
        self._berlesek: list[Berles] = []

    @property
    def nev(self):
        return self._nev

    def auto_hozzaadas(self, auto: Auto):
        self._autok.append(auto)

    def berles_letrehozas(self, rendszam: str, datum_str: str) -> int:
        try:
            foglalt_datum = datetime.strptime(datum_str, "%Y-%m-%d").date()
            if foglalt_datum < datetime.today().date():
                raise ValueError("Nem lehet múltbéli dátumra autót bérelni!")
        except ValueError as e:
            raise ValueError(f"Hibás dátum! Használd az ÉÉÉÉ-HH-NN formátumot. Hiba: {e}")

        kivalasztott_auto = None
        for auto in self._autok:
            if auto.rendszam == rendszam:
                kivalasztott_auto = auto
                break
        
        if not kivalasztott_auto:
            raise ValueError(f"Sajnáljuk, de nincs '{rendszam}' rendszámú autó a flottánkban.")

        for berles in self._berlesek:
            if berles.auto.rendszam == rendszam and berles.datum == datum_str:
                raise ValueError(f"A(z) {rendszam} rendszámú autó {datum_str} napra már le van foglalva!")

        uj_berles = Berles(kivalasztott_auto, datum_str)
        self._berlesek.append(uj_berles)
        
        return kivalasztott_auto.szamol_berles_dij()

    def berles_lemondas(self, rendszam: str, datum_str: str) -> bool:
        for berles in self._berlesek:
            if berles.auto.rendszam == rendszam and berles.datum == datum_str:
                self._berlesek.remove(berles)
                return True
        raise ValueError(f"Nem található bérlés a(z) {rendszam} autóra a következő dátummal: {datum_str}")

    def berlesek_listazasa(self):
        if not self._berlesek:
            print("\n[Rendszer] Jelenleg nincsenek aktív bérlések.")
            return
        
        print(f"\n--- {self._nev} - Aktuális Bérlések Listája ---")
        for i, berles in enumerate(self._berlesek, 1):
            print(f"{i}. {berles}")


# ==========================================
# 5. ADATOK ELŐKÉSZÍTÉSE
# ==========================================
def rendszer_inicializalas():
    kolcsonzo = Autokolcsonzo("Nikus Autókölcsönző")

    auto1 = Szemelyauto("ABC-123", "Suzuki Swift", 10000, 5)
    auto2 = Teherauto("XYZ-987", "Ford Transit", 25000, 3.5)
    auto3 = Szemelyauto("BMW-001", "BMW 3-as sorozat", 18000, 5)

    kolcsonzo.auto_hozzaadas(auto1)
    kolcsonzo.auto_hozzaadas(auto2)
    kolcsonzo.auto_hozzaadas(auto3)

    kolcsonzo.berles_letrehozas("ABC-123", "2026-06-01")
    kolcsonzo.berles_letrehozas("ABC-123", "2026-06-02")
    kolcsonzo.berles_letrehozas("XYZ-987", "2026-06-01")
    kolcsonzo.berles_letrehozas("BMW-001", "2026-06-15")

    return kolcsonzo


# ==========================================
# 6. FELHASZNÁLÓI INTERFÉSZ
# ==========================================
def main():
    kolcsonzo = rendszer_inicializalas()
    
    while True:
        print(f"\n===== ÜDVÖZLI ÖNT A {kolcsonzo.nev.upper()} =====")
        print("1. Autó bérlése")
        print("2. Bérlés lemondása")
        print("3. Bérlések listázása")
        print("4. Kilépés")
        
        valasztas = input("Kérem válasszon egy menüpontot (1-4): ")

        if valasztas == "1":
            print("\n--- Autó Bérlése ---")
            rendszam = input("Adja meg az autó rendszámát (pl. ABC-123): ").upper()
            datum = input("Adja meg a bérlés dátumát (ÉÉÉÉ-HH-NN, pl. 2026-06-20): ")
            
            try:
                ar = kolcsonzo.berles_letrehozas(rendszam, datum)
                print(f"[SIKER] A bérlés sikeresen rögzítve! A bérlés díja: {ar} Ft.")
            except ValueError as e:
                print(f"[HIBA] Sikertelen bérlés: {e}")

        elif valasztas == "2":
            print("\n--- Bérlés Lemondása ---")
            rendszam = input("Adja meg az autó rendszámát: ").upper()
            datum = input("Adja meg a lemondani kívánt bérlés dátumát (ÉÉÉÉ-HH-NN): ")
            
            try:
                kolcsonzo.berles_lemondas(rendszam, datum)
                print("[SIKER] A bérlést sikeresen töröltük a rendszerből.")
            except ValueError as e:
                print(f"[HIBA] A lemondás nem sikerült: {e}")

        elif valasztas == "3":
            kolcsonzo.berlesek_listazasa()

        elif valasztas == "4":
            print("\nKöszönjük, hogy a mi rendszerünket használta! Viszontlátásra!")
            break
        else:
            print("\n[HIBA] Érvénytelen menüpont! Kérjük, 1 és 4 közötti számot adjon meg.")


if __name__ == "__main__":
    main()