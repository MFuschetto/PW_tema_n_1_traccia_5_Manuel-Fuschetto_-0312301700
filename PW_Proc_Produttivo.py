"""
Sviluppare un codice python che dovrà:
1)Presentare una funzione per generare casualmente le quantità da produrre per ogni tipo di prodotto (considerare almeno 3 prodotti differenti);

2)Presentare una funzione per generare casualmente i parametri da configurare, come il tempo di produzione per unità e tipologia di prodotto, 
capacità massima di produzione giornaliera per tipologia di prodotto e complessiva.

3)Restituire come output il tempo di produzione complessivo dell'intero lotto di produzione.
"""

import math
import random
from typing import Dict, List, Tuple

# Definiamo una configurazione di base Inserendo dei parametri (liberamente modificabili)

NOMI_PRODOTTI: List[str] = ["A", "B", "C"]  # almeno 3 prodotti
RANGE_QUANTITA: Tuple[int, int] = (700, 2500)     # unità richieste per prodotto
RANGE_T_UNIT_H: Tuple[float, float] = (0.04, 0.12)  # ore per unità 
RANGE_CAP_PROD: Tuple[int, int] = (1000, 4000)    # capacità per prodotto
RANGE_CAP_TOTALE_H: Tuple[float, float] = (14.0, 20.0)  # capacità impianto 
SEED: int = 42  # per rendere l’esperimento ripetibile

#PRIMA FUNZIONE

# Scriviamo la prima funzione per definire casualmente le quantità da produrre 

def genera_quantita(nomi: List[str],
                    q_range: Tuple[int, int],
                    rng: random.Random) -> Dict[str, int]:
  
    q_min, q_max = q_range
    return {nome: rng.randint(q_min, q_max) for nome in nomi}

# Otteniamo le quantità con valori casuali nell'intervallo fornito

# SECONDA FUNZIONE

# Scriviamo la seconda funzione per generare, sempre casualemente, i parametri operativi

def genera_parametri(nomi: List[str],
                     t_range: Tuple[float, float],
                     cap_prod_range: Tuple[int, int],
                     cap_tot_range: Tuple[float, float],
                     rng: random.Random) -> Tuple[Dict[str, Dict[str, float]], float]:
    
    t_min, t_max = t_range
    cmin, cmax = cap_prod_range
    T_min, T_max = cap_tot_range

    parametri: Dict[str, Dict[str, float]] = {}
    for nome in nomi:
        t_unit = rng.uniform(t_min, t_max)       # tempo unitario 
        cap_g = rng.randint(cmin, cmax)          # capacità (unità/giorno)
        parametri[nome] = {"t_unit": t_unit, "cap_giorno": float(cap_g)}

    cap_tot_ore_giorno = rng.uniform(T_min, T_max)
    return parametri, cap_tot_ore_giorno

# Otteniamo i parametri genereati casulamente e le ore disponibili al giorno per l'impianto

# TERZA FUNZIONE

# Scriviamo la terza funzione per la stima del tempo complessivo (makespan) per completare il lotto

def calcola_makespan(quantita: Dict[str, int],
                     parametri: Dict[str, Dict[str, float]],
                     cap_tot_ore_giorno: float) -> Dict[str, float]:
   
    # Tempo totale richiesto (in ore)
    tempo_totale_ore = 0.0
    for nome, Q in quantita.items():
        t_unit = parametri[nome]["t_unit"]
        tempo_totale_ore += Q * t_unit

    # Giorni minimi imposti dal vincolo di ore/giorno dell’impianto
    giorni_min_per_tempo = tempo_totale_ore / cap_tot_ore_giorno

    # Giorni minimi imposti dalle capacità per-prodotto
    giorni_min_per_prodotto = 0.0
    for nome, Q in quantita.items():
        cap_giorno = parametri[nome]["cap_giorno"]
        giorni_necessari = Q / cap_giorno
        if giorni_necessari > giorni_min_per_prodotto:
            giorni_min_per_prodotto = giorni_necessari

    # Makespan: il sistema deve rispettare i vincoli imposti
    makespan_giorni = math.ceil(max(giorni_min_per_tempo, giorni_min_per_prodotto))

    return {
        "tempo_totale_ore": tempo_totale_ore,
        "giorni_min_per_tempo": giorni_min_per_tempo,
        "giorni_min_per_prodotto": giorni_min_per_prodotto,
        "makespan_giorni": float(makespan_giorni),
        "ore_per_giorno": cap_tot_ore_giorno,
    }

"""""
il makespan viene calcolato come il massimo tra: giorni richiesti dal tempo totale di lavorazione (ore totali / ore/giorno) e
giorni richiesti dal prodotto più “lento” rispetto alla sua capacità giornaliera
il risultato è calcolato in giornate intere.
"""

# Simulazione (riportando prima un riepilogo dello scenario e in seguito i risultati prodotti in output)

def stampa_report(nomi: List[str],
                  quantita: Dict[str, int],
                  parametri: Dict[str, Dict[str, float]],
                  cap_tot_ore_giorno: float,
                  risultati: Dict[str, float]) -> None:
    #Stampa riepilogativa del nostro scenario 
    print(" RIEPILOGO SCENARIO: ")
    print(f"Capacità complessiva impianto: {cap_tot_ore_giorno:.2f} ore/giorno\n")

    print("Parametri per prodotto:")
    for nome in nomi:
        t = parametri[nome]["t_unit"]
        cap = parametri[nome]["cap_giorno"]
        print(f" - {nome}: t_unit={t:.3f} h/u, cap_giorno={cap:.0f} u/g")

    print("\nQuantità richieste e tempo per prodotto:")
    for nome in nomi:
        q = quantita[nome]
        t = parametri[nome]["t_unit"]
        print(f" - {nome}: Q={q} u  ⇒  tempo ≈ {q * t:.2f} h")
    #Stampa dei risultati in output
    print("\n RISULTATI IN OUTPUT: ")
    print(f"Tempo totale di lavorazione: {risultati['tempo_totale_ore']:.2f} ore")
    print(f"Giorni min (vincolo tempo): {risultati['giorni_min_per_tempo']:.2f}")
    print(f"Giorni min (vincolo per-prodotto): {risultati['giorni_min_per_prodotto']:.2f}")
    print(f"Makespan (giornate operative intere): {int(risultati['makespan_giorni'])} "
          f"(con {risultati['ore_per_giorno']:.2f} ore/giorno)")

"""
Le righe di codice riportate di seguito vengono sfruttate solo se il file è lanciato direttamente 
Esegue la simulazione, seguendo i passi in questo modo : genera i dati; calcola il makespan e per finire stampa i risultati.

"""

if __name__ == "__main__":
    # Random con seme prefissato per avere sempre lo stesso esempio(eventuale possibilità di modifica riga riga 16)
    rng = random.Random(SEED)

    # Quantità del lotto (casuali entro un dato intervallo)
    Q = genera_quantita(NOMI_PRODOTTI, RANGE_QUANTITA, rng)

    # Parametri operativi (tempi unitari, capacità per-prodotto e capacità impianto)
    P, CAP_TOT_H = genera_parametri(
        NOMI_PRODOTTI, RANGE_T_UNIT_H, RANGE_CAP_PROD, RANGE_CAP_TOTALE_H, rng
    )

    # Calcolo del makespan
    RIS = calcola_makespan(Q, P, CAP_TOT_H)

    # Report (stampa output)
    stampa_report(NOMI_PRODOTTI, Q, P, CAP_TOT_H, RIS)