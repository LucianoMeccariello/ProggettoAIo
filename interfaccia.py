#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Progetto di Intelligenza Artificiale
Sistema Esperto per la diagnosi medica usando Tkinter e Prolog
Studente: Luciano Meccariello
"""

import os
import subprocess
import threading
import tkinter as tk
from tkinter import font as tkfont

# Colori del tema scuro
BG_ROOT  = '#0a1628'
BG_PANEL = '#0f1f35'
BG_CARD  = '#152840'
BG_INPUT = '#1a3050'
TEAL     = '#00bcd4'
TEAL_DARK = '#00838f'
GREEN    = '#4caf50'
GREEN_DARK = '#2e7d32'
RED      = '#ef5350'
GOLD     = '#ffc107'
TEXT     = '#e0e8ff'
DIM      = '#5a7a9a'
BORDER   = '#1e3a5a'

# Liste delle categorie e sintomi associati
SYMPTOM_CATEGORIES = [
    ('🫁 Respiratori', [
        'febbre_alta', 'febbre_lieve', 'tosse_secca', 'tosse_grassa',
        'mal_di_gola', 'naso_chiuso', 'starnuti',
        'difficolta_respiratorie', 'respiro_affannoso',
    ]),
    ('🧠 Neurologici', [
        'mal_di_testa', 'vertigini', 'confusione',
        'rigidita_collo', 'sensibilita_luce', 'difficolta_concentrazione',
    ]),
    ('🫀 Cardiovascolari', [
        'dolore_petto', 'battito_accelerato',
    ]),
    ('🍽️ Gastrointestinali', [
        'nausea', 'vomito', 'dolore_addominale', 'diarrea',
        'bruciore_stomaco', 'perdita_appetito',
    ]),
    ('💪 Generali', [
        'dolori_muscolari', 'stanchezza', 'debolezza', 'pallore',
        'sudorazione_notturna', 'aumento_peso', 'pelle_secca',
        'sensibilita_freddo', 'perdita_capelli',
    ]),
    ('🔬 Sensoriali', [
        'perdita_gusto_olfatto', 'occhi_arrossati',
        'prurito_nasale', 'visione_offuscata',
    ]),
    ('🧪 Urinari', [
        'bruciore_minzione', 'dolore_lombare', 'urine_torbide',
        'minzione_frequente', 'sete_eccessiva',
    ]),
    ('🧠 Psicologici', [
        'tristezza', 'insonnia', 'perdita_interesse',
    ]),
]


def pretty_label(symptom: str) -> str:
    """Convert 'mal_di_testa' → 'Mal di testa'."""
    return symptom.replace('_', ' ').capitalize()


# Classe per gestire la comunicazione con Prolog
class PrologEngine:
    PL_FILE = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'diagnosi_medica.pl'
    )

    def __init__(self):
        self.swipl = self._find_swipl()

    @staticmethod
    def _find_swipl():
        for p in ['swipl', '/opt/homebrew/bin/swipl', '/usr/local/bin/swipl']:
            try:
                subprocess.run([p, '--version'], capture_output=True, timeout=3)
                return p
            except Exception:
                continue
        return 'swipl'

    def _run(self, goal):
        try:
            r = subprocess.run(
                [self.swipl, '-q', '-g', goal, '-t', 'halt', self.PL_FILE],
                capture_output=True, text=True, timeout=10,
            )
            return r.stdout.strip()
        except Exception:
            return ''

    def diagnosi(self, sintomi):
        """Returns list of (malattia, certezza) tuples sorted by certezza desc."""
        if not sintomi:
            return []
        sintomi_str = ','.join(sintomi)
        goal = f"query_diagnosi('{sintomi_str}')"
        raw = self._run(goal)
        results = []
        for line in raw.strip().split('\n'):
            if ':' in line:
                parts = line.split(':')
                malattia = parts[0].strip()
                try:
                    certezza = int(parts[1].strip())
                except ValueError:
                    continue
                results.append((malattia, certezza))
        return sorted(results, key=lambda x: x[1], reverse=True)

    def spiega(self, malattia, sintomi):
        # Chiede a Prolog i dettagli (sintomi trovati, mancanti, ecc.)
        sintomi_str = ','.join(sintomi)
        goal = f"query_spiega('{malattia}', '{sintomi_str}')"
        raw = self._run(goal)
        info = {}
        for line in raw.strip().split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                info[key.strip().lower()] = val.strip()
        return info


# Funzione per disegnare rettangoli arrotondati
def round_rect(canvas, x1, y1, x2, y2, radius=12, **kwargs):
    """Draw a rounded rectangle on a Tk Canvas."""
    r = radius
    points = [
        x1 + r, y1,   x2 - r, y1,
        x2, y1,       x2, y1 + r,
        x2, y2 - r,   x2, y2,
        x2 - r, y2,   x1 + r, y2,
        x1, y2,       x1, y2 - r,
        x1, y1 + r,   x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


# Classe della GUI Principale
class MedExpertApp:
    ANIM_DURATION_MS = 500       # certainty bar animation time
    ANIM_STEPS       = 25        # animation steps

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title('MedExpert AI — Diagnosi Medica')
        self.root.configure(bg=BG_ROOT)

        # ── window geometry ──
        w, h = 1200, 800
        sx = (self.root.winfo_screenwidth()  - w) // 2
        sy = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f'{w}x{h}+{sx}+{sy}')
        self.root.minsize(900, 600)

        # ── fullscreen ──
        self._fullscreen = False
        self.root.bind('<F11>', lambda e: self._toggle_fullscreen())
        self.root.bind('<Escape>', lambda e: self._exit_fullscreen())

        # ── fonts ──
        self.fnt_title   = tkfont.Font(family='Helvetica', size=22, weight='bold')
        self.fnt_sub     = tkfont.Font(family='Helvetica', size=11)
        self.fnt_small   = tkfont.Font(family='Helvetica', size=9)
        self.fnt_section = tkfont.Font(family='Helvetica', size=13, weight='bold')
        self.fnt_cat     = tkfont.Font(family='Helvetica', size=11, weight='bold')
        self.fnt_sym     = tkfont.Font(family='Helvetica', size=10)
        self.fnt_card_t  = tkfont.Font(family='Helvetica', size=14, weight='bold')
        self.fnt_card_s  = tkfont.Font(family='Helvetica', size=10)
        self.fnt_pct     = tkfont.Font(family='Helvetica', size=11, weight='bold')
        self.fnt_btn     = tkfont.Font(family='Helvetica', size=12, weight='bold')
        self.fnt_detail_t = tkfont.Font(family='Helvetica', size=16, weight='bold')
        self.fnt_detail   = tkfont.Font(family='Helvetica', size=10)
        self.fnt_detail_h = tkfont.Font(family='Helvetica', size=11, weight='bold')
        self.fnt_credit   = tkfont.Font(family='Helvetica', size=8)

        # ── engine ──
        self.engine = PrologEngine()

        # ── state ──
        self.symptom_vars: dict[str, tk.BooleanVar] = {}
        self.results: list[tuple[str, int]] = []
        self.selected_disease: str | None = None
        self._category_open: dict[str, bool] = {}
        self._category_widgets: dict[str, list[tk.Widget]] = {}
        self._card_canvases: list[tk.Canvas] = []
        self._anim_jobs: list[str] = []

        # ── build UI ──
        self._build_header()
        self._build_body()
        self._build_footer()

    # Costruzione della parte superiore (Header)
    def _build_header(self):
        hdr = tk.Frame(self.root, bg=BG_PANEL, padx=20, pady=12)
        hdr.pack(fill='x', side='top')

        # accent line
        tk.Frame(hdr, bg=TEAL, height=3).pack(fill='x', side='top', pady=(0, 10))

        title = tk.Label(hdr, text='MedExpert AI', font=self.fnt_title,
                         fg=TEAL, bg=BG_PANEL)
        title.pack(anchor='w')

        sub = tk.Label(hdr, text='Sistema Esperto di Diagnosi Medica',
                       font=self.fnt_sub, fg=TEXT, bg=BG_PANEL)
        sub.pack(anchor='w')

        credit = tk.Label(
            hdr,
            text='Elementi di Intelligenza Artificiale · Prof. Sperlì Giancarlo',
            font=self.fnt_credit, fg=DIM, bg=BG_PANEL,
        )
        credit.pack(anchor='w', pady=(2, 0))

        # bottom border
        tk.Frame(hdr, bg=BORDER, height=1).pack(fill='x', side='bottom')

    # Corpo centrale dell'app con le 3 colonne
    def _build_body(self):
        body = tk.Frame(self.root, bg=BG_ROOT)
        body.pack(fill='both', expand=True, padx=6, pady=6)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        self._build_left_panel(body)
        self._build_center_panel(body)
        self._build_right_panel(body)

    # Pannello di sinistra per scegliere i sintomi
    def _build_left_panel(self, parent):
        left = tk.Frame(parent, bg=BG_PANEL, width=320, bd=0, highlightthickness=0)
        left.grid(row=0, column=0, sticky='ns', padx=(0, 3))
        left.grid_propagate(False)
        left.configure(width=320)

        # title
        tf = tk.Frame(left, bg=BG_PANEL, padx=14, pady=10)
        tf.pack(fill='x')
        tk.Label(tf, text='🩺 SELEZIONA SINTOMI', font=self.fnt_section,
                 fg=TEAL, bg=BG_PANEL).pack(anchor='w')
        tk.Frame(tf, bg=TEAL_DARK, height=1).pack(fill='x', pady=(6, 0))

        # scrollable area
        container = tk.Frame(left, bg=BG_PANEL)
        container.pack(fill='both', expand=True)

        canvas = tk.Canvas(container, bg=BG_PANEL, bd=0, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient='vertical', command=canvas.yview,
                                 bg=BG_PANEL, troughcolor=BG_PANEL,
                                 activebackground=TEAL_DARK)
        self._sym_inner = tk.Frame(canvas, bg=BG_PANEL, padx=10, pady=6)

        self._sym_inner.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all')),
        )

        canvas.create_window((0, 0), window=self._sym_inner, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)

        # mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(-1 * (event.delta // 120 or (1 if event.delta > 0 else -1)), 'units')

        canvas.bind_all('<MouseWheel>', _on_mousewheel, add='+')
        # macOS trackpad
        canvas.bind_all('<Button-4>', lambda e: canvas.yview_scroll(-3, 'units'), add='+')
        canvas.bind_all('<Button-5>', lambda e: canvas.yview_scroll(3, 'units'), add='+')

        self._populate_symptoms()

    def _populate_symptoms(self):
        # Store ordered references: list of (hdr_frame, sym_frame, arrow_var, count_var)
        self._cat_frames: list[tuple[tk.Frame, tk.Frame, tk.StringVar, tk.StringVar, str]] = []

        for cat_label, symptoms in SYMPTOM_CATEGORIES:
            self._category_open[cat_label] = True
            self._category_widgets[cat_label] = []

            # category header button
            hdr_frame = tk.Frame(self._sym_inner, bg=BG_CARD, padx=8, pady=6)
            hdr_frame.pack(fill='x', pady=(8, 2))

            arrow_var = tk.StringVar(value='▼')
            arrow = tk.Label(hdr_frame, textvariable=arrow_var,
                             font=self.fnt_cat, fg=TEAL, bg=BG_CARD)
            arrow.pack(side='left', padx=(0, 6))

            lbl = tk.Label(hdr_frame, text=cat_label, font=self.fnt_cat,
                           fg=TEXT, bg=BG_CARD, cursor='hand2')
            lbl.pack(side='left')

            # count badge
            count_var = tk.StringVar(value='0')
            badge = tk.Label(hdr_frame, textvariable=count_var,
                             font=self.fnt_small, fg=BG_PANEL, bg=TEAL,
                             padx=5, pady=1)
            badge.pack(side='right')

            sym_frame = tk.Frame(self._sym_inner, bg=BG_PANEL, padx=16)
            sym_frame.pack(fill='x')

            self._cat_frames.append((hdr_frame, sym_frame, arrow_var, count_var, cat_label))

            for symptom in symptoms:
                var = tk.BooleanVar(value=False)
                self.symptom_vars[symptom] = var

                cb_frame = tk.Frame(sym_frame, bg=BG_INPUT, padx=8, pady=3)
                cb_frame.pack(fill='x', pady=1)

                cb = tk.Checkbutton(
                    cb_frame, text=pretty_label(symptom),
                    variable=var, font=self.fnt_sym,
                    fg=TEXT, bg=BG_INPUT,
                    selectcolor=BG_INPUT,
                    activebackground=BG_INPUT, activeforeground=TEAL,
                    highlightthickness=0, bd=0,
                    cursor='hand2',
                    command=lambda cl=cat_label, cv=count_var: self._update_cat_count(cl, cv),
                )
                cb.pack(anchor='w')
                self._category_widgets[cat_label].append(cb_frame)

            # bind toggle
            def make_toggle(cl=cat_label, sf=sym_frame, av=arrow_var):
                def toggle(event=None):
                    is_open = self._category_open[cl]
                    if is_open:
                        sf.pack_forget()
                        av.set('▶')
                    else:
                        av.set('▼')
                        self._repack_all_categories()
                    self._category_open[cl] = not is_open
                return toggle

            toggle_fn = make_toggle(cat_label, sym_frame, arrow_var)
            hdr_frame.bind('<Button-1>', toggle_fn)
            lbl.bind('<Button-1>', toggle_fn)
            arrow.bind('<Button-1>', toggle_fn)

            # hover
            for w in (hdr_frame, lbl, arrow):
                w.bind('<Enter>', lambda e, f=hdr_frame: f.configure(bg='#1a3555') or [
                    c.configure(bg='#1a3555') for c in f.winfo_children()])
                w.bind('<Leave>', lambda e, f=hdr_frame: f.configure(bg=BG_CARD) or [
                    c.configure(bg=BG_CARD) for c in f.winfo_children()])

    def _repack_all_categories(self):
        """Repack all category headers and symptom frames in the correct order."""
        # Unpack everything first
        for hdr_frame, sym_frame, _, _, _ in self._cat_frames:
            hdr_frame.pack_forget()
            sym_frame.pack_forget()

        # Repack in order
        for hdr_frame, sym_frame, arrow_var, _, cl in self._cat_frames:
            hdr_frame.pack(fill='x', pady=(8, 2))
            if self._category_open[cl]:
                sym_frame.pack(fill='x')
                arrow_var.set('▼')
            else:
                arrow_var.set('▶')

    def _update_cat_count(self, cat_label, count_var):
        """Update the badge count for a category."""
        cat_symptoms = []
        for cl, syms in SYMPTOM_CATEGORIES:
            if cl == cat_label:
                cat_symptoms = syms
                break
        count = sum(1 for s in cat_symptoms if self.symptom_vars.get(s) and self.symptom_vars[s].get())
        count_var.set(str(count))

    # Pannello centrale con i risultati della diagnosi
    def _build_center_panel(self, parent):
        center = tk.Frame(parent, bg=BG_PANEL, bd=0, highlightthickness=0)
        center.grid(row=0, column=1, sticky='nsew', padx=3)

        tf = tk.Frame(center, bg=BG_PANEL, padx=14, pady=10)
        tf.pack(fill='x')
        tk.Label(tf, text='📊 DIAGNOSI', font=self.fnt_section,
                 fg=TEAL, bg=BG_PANEL).pack(anchor='w')
        tk.Frame(tf, bg=TEAL_DARK, height=1).pack(fill='x', pady=(6, 0))

        # scrollable results area
        container = tk.Frame(center, bg=BG_PANEL)
        container.pack(fill='both', expand=True)

        self._res_canvas = tk.Canvas(container, bg=BG_PANEL, bd=0, highlightthickness=0)
        res_sb = tk.Scrollbar(container, orient='vertical', command=self._res_canvas.yview,
                              bg=BG_PANEL, troughcolor=BG_PANEL, activebackground=TEAL_DARK)
        self._res_inner = tk.Frame(self._res_canvas, bg=BG_PANEL, padx=14, pady=6)

        self._res_inner.bind(
            '<Configure>',
            lambda e: self._res_canvas.configure(scrollregion=self._res_canvas.bbox('all')),
        )
        self._res_canvas.create_window((0, 0), window=self._res_inner, anchor='nw')
        self._res_canvas.configure(yscrollcommand=res_sb.set)

        res_sb.pack(side='right', fill='y')
        self._res_canvas.pack(side='left', fill='both', expand=True)

        # placeholder
        self._show_placeholder()

    def _show_placeholder(self):
        for w in self._res_inner.winfo_children():
            w.destroy()
        self._card_canvases.clear()

        ph = tk.Frame(self._res_inner, bg=BG_PANEL, pady=80)
        ph.pack(fill='both', expand=True)
        tk.Label(ph, text='🩺', font=tkfont.Font(family='Helvetica', size=48),
                 fg=DIM, bg=BG_PANEL).pack()
        tk.Label(ph, text='Nessuna analisi effettuata',
                 font=self.fnt_sub, fg=DIM, bg=BG_PANEL).pack(pady=(10, 4))
        tk.Label(ph, text='Seleziona i sintomi e premi "Analizza Sintomi"',
                 font=self.fnt_small, fg=DIM, bg=BG_PANEL).pack()

    def _show_no_results(self):
        for w in self._res_inner.winfo_children():
            w.destroy()
        self._card_canvases.clear()

        ph = tk.Frame(self._res_inner, bg=BG_PANEL, pady=80)
        ph.pack(fill='both', expand=True)
        tk.Label(ph, text='❌', font=tkfont.Font(family='Helvetica', size=48),
                 fg=RED, bg=BG_PANEL).pack()
        tk.Label(ph, text='Nessuna diagnosi trovata',
                 font=self.fnt_sub, fg=RED, bg=BG_PANEL).pack(pady=(10, 4))
        tk.Label(ph, text='Prova a selezionare sintomi diversi',
                 font=self.fnt_small, fg=DIM, bg=BG_PANEL).pack()

    def _show_prolog_error(self):
        for w in self._res_inner.winfo_children():
            w.destroy()
        self._card_canvases.clear()

        ph = tk.Frame(self._res_inner, bg=BG_PANEL, pady=80)
        ph.pack(fill='both', expand=True)
        tk.Label(ph, text='⚠️', font=tkfont.Font(family='Helvetica', size=48),
                 fg=GOLD, bg=BG_PANEL).pack()
        tk.Label(ph, text='SWI-Prolog non trovato',
                 font=self.fnt_sub, fg=GOLD, bg=BG_PANEL).pack(pady=(10, 4))
        tk.Label(ph, text='Assicurati che swipl sia installato e nel PATH',
                 font=self.fnt_small, fg=DIM, bg=BG_PANEL).pack()

    def _display_results(self, results: list[tuple[str, int]]):
        """Render diagnosis cards in the center panel."""
        for w in self._res_inner.winfo_children():
            w.destroy()
        self._card_canvases.clear()
        for job in self._anim_jobs:
            try:
                self.root.after_cancel(job)
            except Exception:
                pass
        self._anim_jobs.clear()

        if not results:
            self._show_no_results()
            return

        # Update inner frame width when canvas resizes
        def on_canvas_configure(event):
            self._res_canvas.itemconfigure(
                self._res_canvas.find_all()[0], width=event.width
            )

        self._res_canvas.bind('<Configure>', on_canvas_configure)

        for idx, (malattia, certezza) in enumerate(results):
            self._create_diagnosis_card(malattia, certezza, idx)

    def _create_diagnosis_card(self, malattia: str, certezza: int, index: int):
        """Create a single diagnosis result card with animated bar."""
        card = tk.Frame(self._res_inner, bg=BG_CARD, padx=16, pady=14,
                        highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill='x', pady=6)

        # Disease name
        name_label = pretty_label(malattia)
        tk.Label(card, text=name_label, font=self.fnt_card_t,
                 fg=TEXT, bg=BG_CARD, anchor='w').pack(fill='x')

        # Category line
        cat_text = self._guess_category(malattia)
        if certezza > 70:
            cat_color = GREEN
        elif certezza > 40:
            cat_color = GOLD
        else:
            cat_color = RED
        tk.Label(card, text=cat_text, font=self.fnt_small,
                 fg=cat_color, bg=BG_CARD, anchor='w').pack(fill='x', pady=(2, 8))

        # Certainty bar container
        bar_frame = tk.Frame(card, bg=BG_CARD)
        bar_frame.pack(fill='x')

        bar_canvas = tk.Canvas(bar_frame, height=22, bg=BG_INPUT,
                               bd=0, highlightthickness=0)
        bar_canvas.pack(side='left', fill='x', expand=True, padx=(0, 10))

        pct_label = tk.Label(bar_frame, text='0%', font=self.fnt_pct,
                             fg=cat_color, bg=BG_CARD, width=5, anchor='e')
        pct_label.pack(side='right')

        self._card_canvases.append(bar_canvas)

        # animate the bar
        self._animate_bar(bar_canvas, pct_label, certezza, cat_color, index)

        # click binding
        def on_click(event, m=malattia):
            self._on_card_click(m)

        for widget in (card, name_label if isinstance(name_label, tk.Widget) else card):
            pass
        card.bind('<Button-1>', on_click)
        for child in card.winfo_children():
            child.bind('<Button-1>', on_click)
            for grandchild in child.winfo_children():
                grandchild.bind('<Button-1>', on_click)

        # hover
        def on_enter(e):
            card.configure(bg='#1c3555', highlightbackground=TEAL)
            for c in card.winfo_children():
                try:
                    c.configure(bg='#1c3555')
                except tk.TclError:
                    pass

        def on_leave(e):
            card.configure(bg=BG_CARD, highlightbackground=BORDER)
            for c in card.winfo_children():
                try:
                    c.configure(bg=BG_CARD)
                except tk.TclError:
                    pass

        card.bind('<Enter>', on_enter)
        card.bind('<Leave>', on_leave)

    def _animate_bar(self, canvas: tk.Canvas, pct_label: tk.Label,
                     target: int, color: str, index: int):
        """Animate certainty bar from 0 to target over ANIM_DURATION_MS."""
        step_delay = self.ANIM_DURATION_MS // self.ANIM_STEPS
        start_delay = index * 80  # stagger cards

        def step(current_step):
            if current_step > self.ANIM_STEPS:
                return
            progress = current_step / self.ANIM_STEPS
            # ease-out
            progress = 1 - (1 - progress) ** 3
            current_val = int(target * progress)

            canvas.delete('bar')
            canvas.update_idletasks()
            w = canvas.winfo_width()
            h = canvas.winfo_height()
            if w < 2:
                w = 300
            bar_w = int((w - 4) * current_val / 100)
            if bar_w > 0:
                # gradient effect: draw two overlapping rects
                canvas.create_rectangle(2, 2, 2 + bar_w, h - 2,
                                        fill=color, outline='', tags='bar')
                # lighter overlay on top half
                lighter = self._lighten(color, 0.25)
                canvas.create_rectangle(2, 2, 2 + bar_w, h // 2,
                                        fill=lighter, outline='', tags='bar')

            pct_label.configure(text=f'{current_val}%')

            job = self.root.after(step_delay, step, current_step + 1)
            self._anim_jobs.append(job)

        job = self.root.after(start_delay, step, 0)
        self._anim_jobs.append(job)

    @staticmethod
    def _lighten(hex_color: str, factor: float) -> str:
        """Lighten a hex color by factor (0-1)."""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16)
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        return f'#{r:02x}{g:02x}{b:02x}'

    @staticmethod
    def _guess_category(malattia: str) -> str:
        """Map a disease to a rough category label for display."""
        cat_map = {
            'influenza': 'Malattia infettiva',
            'raffreddore': 'Infezione virale',
            'covid': 'Malattia infettiva',
            'bronchite': 'Malattia respiratoria',
            'polmonite': 'Malattia respiratoria',
            'asma': 'Malattia respiratoria',
            'meningite': 'Malattia neurologica',
            'emicrania': 'Disturbo neurologico',
            'gastrite': 'Disturbo gastrointestinale',
            'gastroenterite': 'Disturbo gastrointestinale',
            'appendicite': 'Urgenza chirurgica',
            'reflusso': 'Disturbo gastrointestinale',
            'anemia': 'Disturbo ematologico',
            'ipotiroidismo': 'Disturbo endocrino',
            'diabete': 'Malattia metabolica',
            'ipertensione': 'Malattia cardiovascolare',
            'cistite': 'Infezione urinaria',
            'calcoli': 'Patologia urinaria',
            'allergia': 'Reazione immunitaria',
            'depressione': 'Disturbo psicologico',
        }
        ml = malattia.lower()
        for key, val in cat_map.items():
            if key in ml:
                return val
        return 'Patologia generale'

    def _on_card_click(self, malattia: str):
        """Handle click on a diagnosis card → populate right panel."""
        self.selected_disease = malattia
        sintomi = self._get_selected_symptoms()
        self._set_status('Caricamento dettagli...')

        def worker():
            info = self.engine.spiega(malattia, sintomi)
            self.root.after(0, lambda: self._populate_details(malattia, info))

        threading.Thread(target=worker, daemon=True).start()

    # Pannello di destra con i dettagli della malattia selezionata
    def _build_right_panel(self, parent):
        right = tk.Frame(parent, bg=BG_PANEL, width=280, bd=0, highlightthickness=0)
        right.grid(row=0, column=2, sticky='ns', padx=(3, 0))
        right.grid_propagate(False)
        right.configure(width=280)

        tf = tk.Frame(right, bg=BG_PANEL, padx=14, pady=10)
        tf.pack(fill='x')
        tk.Label(tf, text='🔍 DETTAGLI DIAGNOSI', font=self.fnt_section,
                 fg=TEAL, bg=BG_PANEL).pack(anchor='w')
        tk.Frame(tf, bg=TEAL_DARK, height=1).pack(fill='x', pady=(6, 0))

        # scrollable details area
        container = tk.Frame(right, bg=BG_PANEL)
        container.pack(fill='both', expand=True)

        self._det_canvas = tk.Canvas(container, bg=BG_PANEL, bd=0, highlightthickness=0)
        det_sb = tk.Scrollbar(container, orient='vertical', command=self._det_canvas.yview,
                              bg=BG_PANEL, troughcolor=BG_PANEL, activebackground=TEAL_DARK)
        self._det_inner = tk.Frame(self._det_canvas, bg=BG_PANEL, padx=14, pady=10)

        self._det_inner.bind(
            '<Configure>',
            lambda e: self._det_canvas.configure(scrollregion=self._det_canvas.bbox('all')),
        )
        self._det_canvas.create_window((0, 0), window=self._det_inner, anchor='nw')
        self._det_canvas.configure(yscrollcommand=det_sb.set)

        det_sb.pack(side='right', fill='y')
        self._det_canvas.pack(side='left', fill='both', expand=True)

        self._show_detail_placeholder()

    def _show_detail_placeholder(self):
        for w in self._det_inner.winfo_children():
            w.destroy()
        ph = tk.Frame(self._det_inner, bg=BG_PANEL, pady=60)
        ph.pack(fill='both', expand=True)
        tk.Label(ph, text='🔍', font=tkfont.Font(family='Helvetica', size=36),
                 fg=DIM, bg=BG_PANEL).pack()
        tk.Label(ph, text='Seleziona una\ndiagnosi per\nvedere i dettagli',
                 font=self.fnt_detail, fg=DIM, bg=BG_PANEL, justify='center').pack(pady=10)

    def _populate_details(self, malattia: str, info: dict):
        """Fill the right panel with disease details."""
        for w in self._det_inner.winfo_children():
            w.destroy()

        # disease name
        tk.Label(self._det_inner, text=pretty_label(malattia),
                 font=self.fnt_detail_t, fg=TEAL, bg=BG_PANEL,
                 anchor='w', wraplength=240).pack(fill='x', pady=(0, 6))

        # separator
        tk.Frame(self._det_inner, bg=TEAL_DARK, height=1).pack(fill='x', pady=6)

        # Descrizione
        desc = info.get('descrizione', info.get('Descrizione', ''))
        if desc:
            tk.Label(self._det_inner, text='📝 Descrizione', font=self.fnt_detail_h,
                     fg=GOLD, bg=BG_PANEL, anchor='w').pack(fill='x', pady=(6, 3))
            tk.Label(self._det_inner, text=desc, font=self.fnt_detail,
                     fg=TEXT, bg=BG_PANEL, anchor='w', justify='left',
                     wraplength=240).pack(fill='x', pady=(0, 8))

        # Certezza
        certezza = None
        for m, c in self.results:
            if m == malattia:
                certezza = c
                break
        if certezza is not None:
            tk.Label(self._det_inner, text='📊 Fattore di Certezza', font=self.fnt_detail_h,
                     fg=GOLD, bg=BG_PANEL, anchor='w').pack(fill='x', pady=(6, 3))
            if certezza > 70:
                cf_color = GREEN
                cf_text = f'{certezza}% — Certezza alta'
            elif certezza > 40:
                cf_color = GOLD
                cf_text = f'{certezza}% — Certezza media'
            else:
                cf_color = RED
                cf_text = f'{certezza}% — Certezza bassa'
            tk.Label(self._det_inner, text=cf_text, font=self.fnt_detail,
                     fg=cf_color, bg=BG_PANEL, anchor='w').pack(fill='x', pady=(0, 8))

        # Sintomi trovati
        trovati = info.get('trovati', info.get('Trovati', ''))
        if trovati:
            tk.Label(self._det_inner, text='✅ Sintomi Trovati', font=self.fnt_detail_h,
                     fg=GREEN, bg=BG_PANEL, anchor='w').pack(fill='x', pady=(6, 3))
            for s in trovati.split(','):
                s = s.strip()
                if s:
                    row = tk.Frame(self._det_inner, bg=BG_PANEL)
                    row.pack(fill='x', pady=1)
                    tk.Label(row, text='  ✔', font=self.fnt_detail,
                             fg=GREEN, bg=BG_PANEL).pack(side='left')
                    tk.Label(row, text=pretty_label(s), font=self.fnt_detail,
                             fg=TEXT, bg=BG_PANEL, anchor='w').pack(side='left', padx=4)

        # Sintomi mancanti
        mancanti = info.get('mancanti', info.get('Mancanti', ''))
        if mancanti:
            tk.Label(self._det_inner, text='❌ Sintomi Mancanti', font=self.fnt_detail_h,
                     fg=RED, bg=BG_PANEL, anchor='w').pack(fill='x', pady=(10, 3))
            for s in mancanti.split(','):
                s = s.strip()
                if s:
                    row = tk.Frame(self._det_inner, bg=BG_PANEL)
                    row.pack(fill='x', pady=1)
                    tk.Label(row, text='  ✘', font=self.fnt_detail,
                             fg=RED, bg=BG_PANEL).pack(side='left')
                    tk.Label(row, text=pretty_label(s), font=self.fnt_detail,
                             fg=DIM, bg=BG_PANEL, anchor='w').pack(side='left', padx=4)

        # Trattamento
        tratt = info.get('trattamento', info.get('Trattamento', ''))
        if tratt:
            tk.Frame(self._det_inner, bg=TEAL_DARK, height=1).pack(fill='x', pady=10)
            tk.Label(self._det_inner, text='💊 Trattamento Consigliato', font=self.fnt_detail_h,
                     fg=GOLD, bg=BG_PANEL, anchor='w').pack(fill='x', pady=(0, 3))
            tk.Label(self._det_inner, text=tratt, font=self.fnt_detail,
                     fg=TEXT, bg=BG_PANEL, anchor='w', justify='left',
                     wraplength=240).pack(fill='x')

        # If info was empty, show a fallback
        if not any([desc, trovati, mancanti, tratt]):
            tk.Label(self._det_inner,
                     text='Nessun dettaglio disponibile\nda Prolog per questa diagnosi.',
                     font=self.fnt_detail, fg=DIM, bg=BG_PANEL,
                     justify='center').pack(pady=30)

        self._set_status(f'Dettagli: {pretty_label(malattia)}')

    # Barra inferiore con i bottoni
    def _build_footer(self):
        foot = tk.Frame(self.root, bg=BG_PANEL, padx=16, pady=10)
        foot.pack(fill='x', side='bottom')

        tk.Frame(foot, bg=BORDER, height=1).pack(fill='x', side='top', pady=(0, 8))

        btn_frame = tk.Frame(foot, bg=BG_PANEL)
        btn_frame.pack(fill='x')

        # ANALIZZA button
        self.btn_analyze = tk.Button(
            btn_frame, text='🔍 ANALIZZA SINTOMI', font=self.fnt_btn,
            fg='white', bg=TEAL_DARK, activebackground=TEAL, activeforeground='white',
            relief='flat', padx=24, pady=8, cursor='hand2',
            command=self._on_analyze,
        )
        self.btn_analyze.pack(side='left', padx=(0, 8))
        self._bind_hover(self.btn_analyze, TEAL, TEAL_DARK)

        # RESET button
        btn_reset = tk.Button(
            btn_frame, text='🗑️ RESET', font=self.fnt_btn,
            fg='white', bg='#7f1d1d', activebackground=RED, activeforeground='white',
            relief='flat', padx=16, pady=8, cursor='hand2',
            command=self._on_reset,
        )
        btn_reset.pack(side='left', padx=(0, 8))
        self._bind_hover(btn_reset, RED, '#7f1d1d')

        # FULLSCREEN button
        btn_fs = tk.Button(
            btn_frame, text='⛶ FULLSCREEN', font=self.fnt_btn,
            fg=TEXT, bg='#2a3a50', activebackground='#3a5070', activeforeground=TEXT,
            relief='flat', padx=16, pady=8, cursor='hand2',
            command=self._toggle_fullscreen,
        )
        btn_fs.pack(side='left')
        self._bind_hover(btn_fs, '#3a5070', '#2a3a50')

        # STATUS label
        self._status_var = tk.StringVar(value='Pronto — seleziona i sintomi')
        status = tk.Label(btn_frame, textvariable=self._status_var,
                          font=self.fnt_small, fg=DIM, bg=BG_PANEL, anchor='e')
        status.pack(side='right')

    @staticmethod
    def _bind_hover(button: tk.Button, hover_bg: str, normal_bg: str):
        button.bind('<Enter>', lambda e: button.configure(bg=hover_bg))
        button.bind('<Leave>', lambda e: button.configure(bg=normal_bg))

    # ─────────────── ACTIONS ───────────────
    def _get_selected_symptoms(self) -> list[str]:
        return [s for s, v in self.symptom_vars.items() if v.get()]

    def _set_status(self, msg: str):
        self._status_var.set(msg)

    def _on_analyze(self):
        sintomi = self._get_selected_symptoms()
        if not sintomi:
            self._set_status('⚠ Seleziona almeno un sintomo!')
            return

        self._set_status(f'Analisi in corso… ({len(sintomi)} sintomi)')
        self.btn_analyze.configure(state='disabled', text='⏳ ANALISI…')

        def worker():
            try:
                results = self.engine.diagnosi(sintomi)
            except Exception:
                results = None
            self.root.after(0, lambda: self._on_analysis_done(results))

        threading.Thread(target=worker, daemon=True).start()

    def _on_analysis_done(self, results):
        self.btn_analyze.configure(state='normal', text='🔍 ANALIZZA SINTOMI')

        if results is None:
            self._show_prolog_error()
            self._set_status('❌ Errore: SWI-Prolog non raggiungibile')
            return

        self.results = results
        self.selected_disease = None
        self._show_detail_placeholder()

        if results:
            self._display_results(results)
            self._set_status(f'✅ {len(results)} diagnosi trovate')
        else:
            self._show_no_results()
            self._set_status('Nessuna diagnosi corrispondente')

    def _on_reset(self):
        # clear checkboxes
        for v in self.symptom_vars.values():
            v.set(False)
        # reset panels
        self.results.clear()
        self.selected_disease = None
        self._show_placeholder()
        self._show_detail_placeholder()
        self._set_status('Pronto — seleziona i sintomi')

    # ─────────────── FULLSCREEN ───────────────
    def _toggle_fullscreen(self):
        self._fullscreen = not self._fullscreen
        self.root.attributes('-fullscreen', self._fullscreen)

    def _exit_fullscreen(self):
        self._fullscreen = False
        self.root.attributes('-fullscreen', False)


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
def main():
    root = tk.Tk()

    # Attempt to set dark title bar on macOS/Windows
    try:
        root.tk.call('tk', 'scaling', 1.5)
    except tk.TclError:
        pass

    app = MedExpertApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
