# 🏥 MedExpert AI — Sistema Esperto di Diagnosi Medica

**Progetto di Elementi di Intelligenza Artificiale**  
Prof. Giancarlo Sperlì · Università degli Studi di Napoli Parthenope  
A.A. 2025/2026

---

## 📋 Descrizione

MedExpert AI è un **sistema esperto di diagnosi medica** implementato in **Prolog** con
interfaccia grafica premium in **Python/Tkinter**.

Il sistema utilizza una Knowledge Base di **15+ malattie** con i relativi sintomi, e attraverso
**regole di inferenza** e **fattori di certezza**, è in grado di suggerire le possibili diagnosi
dato un insieme di sintomi selezionati dall'utente.

### Caratteristiche principali:
- 🧬 **Knowledge Base** ricca con 15+ malattie, 40+ sintomi, descrizioni e trattamenti
- 🔍 **Motore di inferenza** con backward chaining e fattori di certezza
- 💡 **Explanation facility** — spiega il ragionamento dietro ogni diagnosi
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

### Testare solo il Prolog da terminale:
```bash
swipl -g "test_diagnosi, halt" diagnosi_medica.pl
```

### Generare il PDF di documentazione:
```bash
python3 genera_pdf.py
```

---

## 🎮 Come si usa

1. **Seleziona i sintomi** dalla checklist a sinistra (organizzati per categoria)
2. Clicca **🔍 ANALIZZA SINTOMI**
3. Le diagnosi possibili appariranno ordinate per **certezza** (%)
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
├── genera_pdf.py            # Generatore documentazione PDF
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
│  │  diagnosi/3    →  Backward Chaining      │   │
│  │  certezza      →  Fattori di Certezza    │   │
│  │  spiega/4      →  Explanation Facility   │   │
│  └──────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────┐   │
│  │  KNOWLEDGE BASE                          │   │
│  │  15+ malattie · 40+ sintomi · regole     │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

---

## 👨‍💻 Autore

**Luciano Meccariello**  
Università degli Studi di Napoli Parthenope  
Corso di Elementi di Intelligenza Artificiale  
Prof. Giancarlo Sperlì
