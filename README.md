# 🏥 MedExpert AI — Sistema Esperto di Diagnosi Medica

**Progetto di Elementi di Intelligenza Artificiale**  
Prof. Giancarlo Sperlì · Università degli Studi di Napoli Federico II  
A.A. 2025/2026

---

## 📋 Descrizione

MedExpert AI è un **sistema esperto di diagnosi medica** implementato in **Prolog** con
interfaccia grafica premium in **Python/Tkinter**.

Il sistema utilizza una Knowledge Base di **17 malattie organizzate in 10 categorie** con i
relativi sintomi, e attraverso **regole di inferenza** e l'**Indice di Copertura Sintomatica
(ICS)**, è in grado di suggerire le diagnosi candidate dato un insieme di sintomi selezionati
dall'utente.

### Caratteristiche principali:
- 🧬 **Knowledge Base** con 17 malattie, 44 sintomi unici, descrizioni e trattamenti
- 🔍 **Motore di inferenza** goal-driven (backward chaining) con calcolo dell'ICS
- 💡 **Explanation facility** — espone sintomi trovati e mancanti per ogni diagnosi
- 🖥️ **Interfaccia grafica** moderna con tema medico premium
- 📄 **Documentazione** PDF accademica completa

---

## 🚀 Requisiti

- **Python 3.8+** con Tkinter (incluso di default)
- **SWI-Prolog** (per il motore di inferenza)
- **reportlab** (solo per generare il PDF)

### Installazione SWI-Prolog:
```bash
# macOS (Homebrew)
brew install swi-prolog

# Ubuntu/Debian
sudo apt install swi-prolog

# Windows
# Scarica da: https://www.swi-prolog.org/download/stable
```

### Installazione reportlab (per PDF):
```bash
pip3 install reportlab
```

---

## ▶️ Avvio

### Avviare l'interfaccia grafica:
```bash
python3 interfaccia.py
```

### Eseguire la suite di test automatizzata:
```bash
swipl -g "test_diagnosi, halt" diagnosi_medica.pl
```

### Uso Interattivo (Prolog puro da terminale):
Per interrogare direttamente il motore senza interfaccia grafica, avvia l'ambiente Prolog caricando il file:
```bash
swipl -s diagnosi_medica.pl
```
Una volta dentro la console (vedrai il prompt `?-`), puoi lanciare i seguenti comandi (ricorda sempre il punto finale `.`):

- **Vedere tutte le malattie:** `mostra_malattie.`
- **Dettagli su una malattia:** `mostra_info(influenza).`
- **Eseguire una diagnosi partendo dai sintomi:** `query_diagnosi('febbre_alta,tosse_secca,mal_di_testa').`
- **Spiegare una diagnosi:** `query_spiega(influenza, 'febbre_alta,tosse_secca').`
- **Diagnosi differenziale (confronto):** `diagnosi_differenziale(influenza, covid19).`
- **Uscire dall'ambiente:** `halt.`




---

## 🎮 Come si usa

1. **Seleziona i sintomi** dalla checklist a sinistra (organizzati per categoria)
2. Clicca **🔍 ANALIZZA SINTOMI**
3. Le diagnosi candidate appariranno ordinate per **ICS** (%) — Indice di Copertura Sintomatica
4. **Clicca su una diagnosi** per vedere i dettagli nel pannello destro:
   - Sintomi trovati ✅
   - Sintomi mancanti ❌
   - Descrizione della malattia
   - Trattamento consigliato

---

## 📁 Struttura del Progetto

```
PROGETTO AI FINALE/
├── diagnosi_medica.pl       # Knowledge Base + Regole di Inferenza (Prolog)
├── interfaccia.py           # Interfaccia Grafica (Python/Tkinter)
├── Documentazione_MedExpert.pdf  # PDF generato
└── README.md                # Questo file
```

---

## 🏛️ Architettura

```
┌─────────────────────────────────────────────────┐
│              INTERFACCIA UTENTE                  │
│           (Python / Tkinter)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │ Sintomi  │  │ Diagnosi │  │  Dettagli    │   │
│  │ Checklist│  │  Cards   │  │  Spiegazione │   │
│  └──────────┘  └──────────┘  └──────────────┘   │
└─────────────────────┬───────────────────────────┘
                      │ subprocess
┌─────────────────────▼───────────────────────────┐
│           MOTORE DI INFERENZA                    │
│              (SWI-Prolog)                        │
│  ┌──────────────────────────────────────────┐   │
│  │  diagnosi/3         →  Backward Chaining │   │
│  │  ICS                →  Copertura sintomi │   │
│  │  spiega_diagnosi/4  →  Explanation       │   │
│  └──────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────┐   │
│  │  KNOWLEDGE BASE                          │   │
│  │  17 malattie · 44 sintomi · 10 categorie │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

---

## 👨‍💻 Autore

**Luciano Meccariello**  
Università degli Studi di Napoli Federico II  
Corso di Elementi di Intelligenza Artificiale  
Prof. Giancarlo Sperlì
