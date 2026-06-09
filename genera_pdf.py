#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Script che genera la documentazione PDF del progetto MedExpert AI.
# Si usa reportlab: si costruisce una "story" di paragrafi, tabelle e codice e
# poi la libreria si occupa di impaginarla in A4.
# Corso di Elementi di IA - Universita' Federico II di Napoli - A.A. 2025/2026.

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, Preformatted, KeepTogether, Image
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# --- Palette colori del documento ---
DARK_BLUE   = HexColor("#0f2847")   # navy profondo per titoli
ACCENT_BLUE = HexColor("#2563eb")   # blu moderno per accenti
LIGHT_BLUE  = HexColor("#e0e7ff")   # azzurro tenue per bande chiare
VERY_LIGHT  = HexColor("#f5f7fb")   # sfondo "carta"
CODE_BG       = HexColor("#1e1e2e")   # sfondo scuro dei blocchi codice
CODE_BAR_BG   = HexColor("#15151f")   # barra titolo (stile terminale macOS)
CODE_BORDER   = HexColor("#313244")   # bordo dei blocchi codice
CODE_TEXT     = HexColor("#e6edf3")   # testo del codice (chiaro)
CODE_COMMENT  = HexColor("#6a9955")   # commenti in verde muto (stile VS Code)
TABLE_HEAD  = HexColor("#0f2847")   # intestazione tabella in navy
ROW_EVEN    = HexColor("#f5f7fb")
ROW_ODD     = HexColor("#ffffff")
SOFT_LINE   = HexColor("#dbe1ea")   # linee sottili (header/footer/tabelle)
DARK_TEXT    = HexColor("#0b1220")
MUTED_TEXT   = HexColor("#5b6779")
SUCCESS_GREEN = HexColor("#28a745")
WARNING_RED   = HexColor("#dc3545")

PAGE_W, PAGE_H = A4


# --- Stili dei paragrafi ---
# Tutti gli stili sono definiti qui per non sparpagliarli nelle varie sezioni.
def build_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='CoverUniversity',
        fontName='Helvetica-Bold',
        fontSize=16,
        textColor=DARK_BLUE,
        alignment=TA_CENTER,
        leading=22,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name='CoverCourse',
        fontName='Helvetica',
        fontSize=12,
        textColor=MUTED_TEXT,
        alignment=TA_CENTER,
        leading=16,
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name='CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=36,
        textColor=DARK_BLUE,
        alignment=TA_CENTER,
        leading=42,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name='CoverSubtitle',
        fontName='Helvetica-Oblique',
        fontSize=13,
        textColor=ACCENT_BLUE,
        alignment=TA_CENTER,
        leading=18,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name='CoverInfoLabel',
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=MUTED_TEXT,
        alignment=TA_CENTER,
        leading=14,
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name='CoverInfo',
        fontName='Helvetica',
        fontSize=12,
        textColor=DARK_TEXT,
        alignment=TA_CENTER,
        leading=18,
        spaceAfter=2,
    ))

    # Titoli di sezione: testo grosso in navy + linea d'accento sotto (gestita
    # esternamente con HRFlowable in section_header()).
    styles.add(ParagraphStyle(
        name='SectionH1',
        fontName='Helvetica-Bold',
        fontSize=22,
        textColor=DARK_BLUE,
        alignment=TA_LEFT,
        leading=26,
        spaceBefore=0,
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name='SectionH2',
        fontName='Helvetica-Bold',
        fontSize=13,
        textColor=ACCENT_BLUE,
        alignment=TA_LEFT,
        leading=17,
        spaceBefore=10,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name='SectionH3',
        fontName='Helvetica-Bold',
        fontSize=11.5,
        textColor=DARK_BLUE,
        alignment=TA_LEFT,
        leading=14,
        spaceBefore=6,
        spaceAfter=3,
    ))

    # Stili per il corpo del testo: paragrafo giustificato e bullet point.
    styles.add(ParagraphStyle(
        name='BodyJ',
        fontName='Helvetica',
        fontSize=10,
        textColor=DARK_TEXT,
        alignment=TA_JUSTIFY,
        leading=13.5,
        spaceBefore=2,
        spaceAfter=5,
        firstLineIndent=0,
    ))
    styles.add(ParagraphStyle(
        name='BodyBullet',
        fontName='Helvetica',
        fontSize=10,
        textColor=DARK_TEXT,
        alignment=TA_LEFT,
        leading=13.5,
        spaceBefore=1,
        spaceAfter=3,
        leftIndent=16,
        bulletIndent=5,
    ))

    # Blocchi di codice (font monospace, tema scuro).
    # Bordo e sfondo sono gestiti dalla Table in code_block(), qui solo testo.
    styles.add(ParagraphStyle(
        name='CodeBlock',
        fontName='Courier-Bold',
        fontSize=8.5,
        textColor=CODE_TEXT,
        alignment=TA_LEFT,
        leading=12,
        spaceBefore=0,
        spaceAfter=0,
    ))
    styles.add(ParagraphStyle(
        name='CodeBar',
        fontName='Helvetica',
        fontSize=10,
        textColor=CODE_TEXT,
        alignment=TA_LEFT,
        leading=12,
    ))
    styles.add(ParagraphStyle(
        name='CodeInline',
        fontName='Courier',
        fontSize=9,
        textColor=DARK_TEXT,
        backColor=CODE_BG,
    ))

    # Didascalia (sotto tabelle e listati) e note in corsivo.
    styles.add(ParagraphStyle(
        name='Caption',
        fontName='Helvetica-Oblique',
        fontSize=9,
        textColor=MUTED_TEXT,
        alignment=TA_CENTER,
        leading=12,
        spaceBefore=2,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name='Note',
        fontName='Helvetica-Oblique',
        fontSize=9,
        textColor=MUTED_TEXT,
        alignment=TA_JUSTIFY,
        leading=11,
        spaceBefore=2,
        spaceAfter=3,
        leftIndent=12,
        rightIndent=12,
    ))

    # Stili dell'indice (voci + titolo).
    styles.add(ParagraphStyle(
        name='TOCEntry',
        fontName='Helvetica',
        fontSize=11,
        textColor=DARK_TEXT,
        alignment=TA_LEFT,
        leading=16,
        spaceBefore=1,
        spaceAfter=1,
        leftIndent=10,
    ))
    styles.add(ParagraphStyle(
        name='TOCTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=DARK_BLUE,
        alignment=TA_CENTER,
        leading=24,
        spaceBefore=10,
        spaceAfter=10,
    ))

    return styles


# --- Funzioni di utilita' ---

def hr():
    # Linea orizzontale fine come separatore tra sezioni; un cm circa di
    # respiro dopo, cosi' i capitoli che condividono la pagina (es. 1+2)
    # restano ben distinti. Il PageBreak ignora spaceAfter, quindi non
    # influisce sui capitoli che iniziano in pagina nuova.
    return HRFlowable(
        width="100%", thickness=0.5, color=SOFT_LINE,
        spaceBefore=12, spaceAfter=28
    )


def thin_hr():
    # Linea molto sottile, usata tra le voci dell'indice.
    return HRFlowable(
        width="100%", thickness=0.4, color=SOFT_LINE,
        spaceBefore=2, spaceAfter=2
    )


def section_header(title, styles):
    # Restituisce una lista di flowables: titolo grosso in navy, una linea blu
    # spessa subito sotto (accent), poi un piccolo respiro.
    return [
        Paragraph(title, styles['SectionH1']),
        HRFlowable(width="100%", thickness=2, color=ACCENT_BLUE,
                   spaceBefore=2, spaceAfter=0),
        HRFlowable(width="100%", thickness=0.4, color=SOFT_LINE,
                   spaceBefore=1, spaceAfter=10),
    ]


_CELL_STYLE = ParagraphStyle(
    'TableCell', fontName='Helvetica', fontSize=9, leading=11,
    textColor=DARK_TEXT, alignment=TA_LEFT,
)


def _wrap_cell(value):
    # Se il contenuto della cella e' una stringa, lo avvolgiamo in un Paragraph
    # cosi' reportlab fa il word-wrap (altrimenti spezza per caratteri quando
    # una parola non entra nella colonna).
    if isinstance(value, str):
        text = value.replace('\n', '<br/>')
        return Paragraph(text, _CELL_STYLE)
    return value


def make_table(headers, rows, col_widths=None):
    # Crea una tabella con header colorato e righe a zebra.
    # Se non passiamo col_widths, reportlab divide lo spazio in parti uguali.
    wrapped_rows = [[_wrap_cell(c) for c in row] for row in rows]
    data = [headers] + wrapped_rows
    if col_widths is None:
        col_widths = [None] * len(headers)

    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        # Intestazione: navy con testo bianco maiuscolo.
        ('BACKGROUND',    (0, 0), (-1, 0), TABLE_HEAD),
        ('TEXTCOLOR',     (0, 0), (-1, 0), white),
        ('FONTNAME',      (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING',    (0, 0), (-1, 0), 8),
        ('LEFTPADDING',   (0, 0), (-1, 0), 8),
        ('RIGHTPADDING',  (0, 0), (-1, 0), 8),
        # Corpo.
        ('FONTNAME',      (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE',      (0, 1), (-1, -1), 9),
        ('TEXTCOLOR',     (0, 1), (-1, -1), DARK_TEXT),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('TOPPADDING',    (0, 1), (-1, -1), 6),
        ('LEFTPADDING',   (0, 1), (-1, -1), 8),
        ('RIGHTPADDING',  (0, 1), (-1, -1), 8),
        # Linee orizzontali sottili (no griglia piena: piu' moderno).
        ('LINEBELOW',     (0, 0), (-1, 0),  0.8, ACCENT_BLUE),
        ('LINEBELOW',     (0, 1), (-1, -1), 0.3, SOFT_LINE),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN',         (0, 0), (-1,  0), 'LEFT'),
    ]
    # Zebra: righe pari leggermente colorate per facilitare la lettura.
    for i in range(1, len(data)):
        bg = ROW_EVEN if i % 2 == 0 else ROW_ODD
        style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))

    t.setStyle(TableStyle(style_cmds))
    # Un po' di respiro attorno alla tabella, ma poco.
    t.spaceBefore = 4
    t.spaceAfter = 4
    return t


def code_block(text, styles, label='prolog'):
    # Blocco di codice in stile terminale: barra titolo scura con tre pallini
    # rosso/giallo/verde (macOS) e label del linguaggio a destra, poi il codice
    # su sfondo scuro con commenti in verde muto.
    escaped = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    comment_color = CODE_COMMENT.hexval().replace('0x', '#')

    # Sostituiamo le spaziature iniziali con &nbsp; cosi' l'indentazione non
    # viene collassata dal motore HTML di reportlab; evidenziamo i commenti
    # Prolog (qualunque riga che inizia con %).
    out_lines = []
    for line in escaped.split('\n'):
        stripped = line.lstrip(' ')
        leading_nbsp = '&nbsp;' * (len(line) - len(stripped))
        if stripped.startswith('%'):
            out_lines.append(
                f'{leading_nbsp}<font color="{comment_color}"><i>{stripped}</i></font>'
            )
        else:
            out_lines.append(leading_nbsp + stripped)
    body = Paragraph('<br/>'.join(out_lines), styles['CodeBlock'])

    # Barra superiore stile macOS: pallini rosso/giallo/verde + label a destra.
    bar = Paragraph(
        '<font color="#ff5f56">●</font>&nbsp;'
        '<font color="#ffbd2e">●</font>&nbsp;'
        '<font color="#27c93f">●</font>'
        f'&nbsp;&nbsp;<font color="#7a7c8a" size="7">{label}</font>',
        styles['CodeBar']
    )

    # Tabella a due righe: barra titolo sopra, codice sotto.
    t = Table([[bar], [body]], colWidths=[None])
    t.setStyle(TableStyle([
        # Barra titolo (riga 0).
        ('BACKGROUND',    (0, 0), (0, 0), CODE_BAR_BG),
        ('LEFTPADDING',   (0, 0), (0, 0), 10),
        ('RIGHTPADDING',  (0, 0), (0, 0), 10),
        ('TOPPADDING',    (0, 0), (0, 0), 5),
        ('BOTTOMPADDING', (0, 0), (0, 0), 4),
        # Corpo del codice (riga 1).
        ('BACKGROUND',    (0, 1), (0, 1), CODE_BG),
        ('LEFTPADDING',   (0, 1), (0, 1), 12),
        ('RIGHTPADDING',  (0, 1), (0, 1), 12),
        ('TOPPADDING',    (0, 1), (0, 1), 10),
        ('BOTTOMPADDING', (0, 1), (0, 1), 10),
        # Bordo esterno e allineamento.
        ('BOX',           (0, 0), (-1, -1), 0.4, CODE_BORDER),
        ('LINEBELOW',     (0, 0), (0, 0), 0.4, CODE_BORDER),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    # Un po' di respiro sopra e sotto il blocco, senza esagerare.
    t.spaceBefore = 6
    t.spaceAfter = 6
    return t


# --- Header e footer di pagina ---
# Header minimalista: solo una sottile linea blu e testo discreto.
def header_footer(canvas, doc):
    canvas.saveState()
    page_num = doc.page

    # Saltiamo la copertina (pagina 1).
    if page_num > 1:
        # Header: piccolo testo in alto + linea sottile.
        canvas.setFillColor(MUTED_TEXT)
        canvas.setFont('Helvetica', 8)
        canvas.drawString(2 * cm, PAGE_H - 1.3 * cm,
                          "MedExpert AI · Diagnosi Medica")
        canvas.drawRightString(PAGE_W - 2 * cm, PAGE_H - 1.3 * cm,
                               "Università di Napoli Federico II")
        canvas.setStrokeColor(SOFT_LINE)
        canvas.setLineWidth(0.4)
        canvas.line(2 * cm, PAGE_H - 1.5 * cm,
                    PAGE_W - 2 * cm, PAGE_H - 1.5 * cm)

        # Footer: linea sottile + corso a sx, numero pagina con accent a dx.
        canvas.setStrokeColor(SOFT_LINE)
        canvas.line(2 * cm, 1.3 * cm, PAGE_W - 2 * cm, 1.3 * cm)
        canvas.setFillColor(MUTED_TEXT)
        canvas.setFont('Helvetica', 8)
        canvas.drawString(2 * cm, 0.8 * cm,
                          "Elementi di Intelligenza Artificiale · A.A. 2025/2026")
        canvas.setFillColor(ACCENT_BLUE)
        canvas.setFont('Helvetica-Bold', 8)
        canvas.drawRightString(PAGE_W - 2 * cm, 0.8 * cm, f"— {page_num} —")
    canvas.restoreState()


# ===== Pagina di copertina =====
def build_cover(story, styles):
    # Linea decorativa in alto.
    story.append(Spacer(1, 1.0 * cm))
    story.append(HRFlowable(width="100%", thickness=3, color=ACCENT_BLUE,
                             spaceBefore=0, spaceAfter=0))
    story.append(HRFlowable(width="100%", thickness=0.5, color=SOFT_LINE,
                             spaceBefore=2, spaceAfter=0))

    story.append(Spacer(1, 1.5 * cm))

    # Università e corso, testo pulito senza banner pesanti.
    story.append(Paragraph(
        "UNIVERSITÀ DEGLI STUDI DI NAPOLI FEDERICO II",
        styles['CoverUniversity']
    ))
    story.append(Paragraph(
        "Corso di Elementi di Intelligenza Artificiale",
        styles['CoverCourse']
    ))

    story.append(Spacer(1, 3.0 * cm))

    # Titolo grande del progetto.
    story.append(Paragraph("MedExpert AI", styles['CoverTitle']))
    story.append(Paragraph(
        "Sistema Esperto di Diagnosi Medica",
        ParagraphStyle('BigSub', parent=styles['CoverTitle'],
                       fontSize=18, leading=24, textColor=ACCENT_BLUE,
                       fontName='Helvetica')
    ))
    story.append(Spacer(1, 0.4 * cm))
    story.append(HRFlowable(width="40%", thickness=1.5, color=ACCENT_BLUE,
                             spaceBefore=2, spaceAfter=10, hAlign='CENTER'))
    story.append(Paragraph(
        "Implementazione in Prolog con Interfaccia Grafica Python",
        styles['CoverSubtitle']
    ))

    story.append(Spacer(1, 2.4 * cm))

    # Tabella docente / studenti, leggera, solo linee orizzontali.
    info_data = [
        [Paragraph("DOCENTE", styles['CoverInfoLabel']),
         Paragraph("STUDENTI", styles['CoverInfoLabel'])],
        [Paragraph("Prof. Giancarlo Sperlì", styles['CoverInfo']),
         Paragraph("Luciano Meccariello &nbsp; N46007465<br/>"
                   "Gaspare Tortora &nbsp; N46007942<br/>"
                   "Andrea Francesco Bruno &nbsp; N46007639",
                   styles['CoverInfo'])],
    ]
    info_table = Table(info_data, colWidths=[7.5 * cm, 7.5 * cm])
    info_table.setStyle(TableStyle([
        ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING',    (0, 0), (-1,  0), 6),
        ('BOTTOMPADDING', (0, 0), (-1,  0), 4),
        ('TOPPADDING',    (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('LINEABOVE',     (0, 0), (-1,  0), 0.5, SOFT_LINE),
        ('LINEBELOW',     (0, 0), (-1,  0), 0.5, SOFT_LINE),
        ('LINEBELOW',     (0, 1), (-1,  1), 0.5, SOFT_LINE),
    ]))
    story.append(info_table)

    story.append(Spacer(1, 1.5 * cm))

    # Anno accademico, semplice testo centrato con linee sopra/sotto.
    story.append(HRFlowable(width="20%", thickness=0.6, color=ACCENT_BLUE,
                             spaceBefore=0, spaceAfter=6, hAlign='CENTER'))
    story.append(Paragraph(
        "Anno Accademico 2025/2026",
        ParagraphStyle('AA', parent=styles['CoverInfo'],
                       fontName='Helvetica-Bold', fontSize=11,
                       textColor=DARK_BLUE)
    ))
    story.append(HRFlowable(width="20%", thickness=0.6, color=ACCENT_BLUE,
                             spaceBefore=6, spaceAfter=0, hAlign='CENTER'))

    story.append(PageBreak())


# ===== Indice =====
def build_toc(story, styles):
    story.append(Spacer(1, 0.4 * cm))
    story.extend(section_header("Indice", styles))

    sections = [
        ("1", "Obiettivo del Progetto"),
        ("2", "Il Dominio: Diagnosi Medica"),
        ("3", "Architettura del Sistema"),
        ("4", "Knowledge Base in Prolog"),
        ("5", "Regole di Inferenza"),
        ("6", "Interfaccia Grafica (Python / Tkinter)"),
        ("7", "Test e Validazione"),
        ("8", "Conclusioni"),
    ]

    # L'indice come tabella a due colonne: numero in accent_blue, titolo in dark.
    rows = []
    for num, title in sections:
        rows.append([
            Paragraph(f'<font color="{ACCENT_BLUE.hexval().replace("0x", "#")}">'
                      f'<b>{num}</b></font>', styles['TOCEntry']),
            Paragraph(title, styles['TOCEntry']),
        ])
    toc_table = Table(rows, colWidths=[1.5 * cm, 14 * cm])
    style_cmds = [
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING',   (0, 0), (-1, -1), 4),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 4),
        ('TOPPADDING',    (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]
    for i in range(len(sections)):
        style_cmds.append(('LINEBELOW', (0, i), (-1, i), 0.3, SOFT_LINE))
    toc_table.setStyle(TableStyle(style_cmds))
    story.append(toc_table)

    story.append(PageBreak())


# --- Sezione 1: Obiettivo del progetto ---
def build_section_1(story, s):
    story.extend(section_header("1. Obiettivo del Progetto", s))

    story.append(Paragraph(
        "Il progetto realizza un <b>sistema esperto per la diagnosi medica</b> che combina una "
        "Knowledge Base in Prolog con un'interfaccia grafica in Python/Tkinter. L'obiettivo è "
        "mostrare in modo concreto i concetti del corso (rappresentazione della conoscenza, "
        "backward chaining, sistemi a regole) applicandoli a un dominio realistico.", s['BodyJ']))

    objectives = [
        "Codificare in Prolog <b>17 patologie</b> con sintomi, categorie, descrizioni e trattamenti.",
        "Implementare un motore <b>goal-driven</b> che ordini le diagnosi candidate per "
        "<b>Indice di Copertura Sintomatica (ICS)</b>.",
        "Fornire una <b>explanation facility</b> che esponga sintomi trovati e mancanti.",
        "Offrire una <b>GUI interattiva</b> usabile anche da utenti non tecnici.",
        "Validare il sistema con una <b>suite di test automatizzati</b> in Prolog.",
    ]
    for i, obj in enumerate(objectives, 1):
        story.append(Paragraph(f"<b>{i}.</b> {obj}", s['BodyBullet']))

    story.append(hr())


# --- Sezione 2: Dominio della diagnosi medica ---
def build_section_2(story, s):
    story.extend(section_header("2. Il Dominio: Diagnosi Medica", s))

    story.append(Paragraph(
        "La diagnosi medica è un dominio adatto ai sistemi esperti: il ragionamento clinico si "
        "formalizza naturalmente in regole del tipo «se i sintomi sono X, Y, Z allora la malattia "
        "candidata è W». Raramente un paziente presenta tutti i sintomi tipici di una patologia e "
        "gli stessi sintomi possono essere associati a malattie diverse: serve un <b>ranking</b> "
        "delle diagnosi, non una risposta binaria.", s['BodyJ']))

    story.append(Paragraph(
        "Per ogni malattia M della KB il sistema calcola un <b>Indice di Copertura Sintomatica</b>:", s['BodyJ']))

    story.append(code_block(
        "ICS(M) = round( |Sintomi_Paziente ∩ Sintomi_M| / |Sintomi_M| × 100 )",
        s, label='formula'))

    story.append(Paragraph(
        "L'ICS misura quale frazione dei sintomi tipici di M è presente nel paziente. Le diagnosi "
        "vengono presentate ordinate per ICS decrescente; la decisione clinica finale resta del "
        "medico. La KB copre 17 patologie su 10 categorie mediche:", s['BodyJ']))

    disease_headers = ['Categoria', 'Patologie']
    disease_rows = [
        ['Respiratorie',     'Influenza, COVID-19, Bronchite, Polmonite'],
        ['Gastrointestinali','Gastrite, Appendicite, Reflusso gastroesofageo'],
        ['Neurologiche',     'Emicrania, Meningite'],
        ['Cardiovascolari',  'Ipertensione, Tachicardia'],
        ['Altre',            'Anemia, Diabete tipo 2, Ipotiroidismo, Cistite, '
                             'Allergia stagionale, Depressione'],
    ]
    story.append(make_table(disease_headers, disease_rows, [4*cm, 12.5*cm]))
    story.append(Paragraph("Tabella 1 — Patologie nella Knowledge Base (17 totali).", s['Caption']))
    story.append(hr())


# --- Sezione 3: Architettura del sistema ---
def build_section_3(story, s):
    story.append(PageBreak())
    story.extend(section_header("3. Architettura del Sistema", s))

    story.append(Paragraph(
        "Il sistema è organizzato su tre livelli. La GUI Python raccoglie i sintomi dall'utente "
        "e costruisce le query; SWI-Prolog, lanciato in <i>subprocess</i>, esegue l'inferenza "
        "sulla KB e restituisce le diagnosi ordinate su stdout; Python interpreta l'output e "
        "popola la GUI. La scelta di subprocess (al posto di bridge come PySwip) elimina "
        "dipendenze esterne e rende il tutto portabile.", s['BodyJ']))

    arch_text = (
        "┌─────────────────────────────────────────────────┐\n"
        "│          INTERFACCIA UTENTE (Python/Tkinter)    │\n"
        "└──────────────────────┬──────────────────────────┘\n"
        "                       │ subprocess (stdin/stdout)\n"
        "┌──────────────────────▼──────────────────────────┐\n"
        "│         MOTORE INFERENZIALE (SWI-Prolog)        │\n"
        "│    backward chaining · ICS · findall · sort     │\n"
        "└──────────────────────┬──────────────────────────┘\n"
        "                       │ consult/1\n"
        "┌──────────────────────▼──────────────────────────┐\n"
        "│         KNOWLEDGE BASE (diagnosi_medica.pl)     │\n"
        "│       fatti · regole · spiegazioni · test       │\n"
        "└─────────────────────────────────────────────────┘"
    )
    story.append(code_block(arch_text, s, label='architettura'))
    story.append(Paragraph("Figura 1 — Architettura a tre livelli.", s['Caption']))

    file_headers = ['File', 'Linguaggio', 'Ruolo']
    file_rows = [
        ['diagnosi_medica.pl', 'Prolog', 'Knowledge Base + regole + test'],
        ['interfaccia.py',     'Python', 'GUI Tkinter + ponte verso swipl'],
    ]
    story.append(make_table(file_headers, file_rows, [4.5*cm, 3*cm, 8.5*cm]))
    story.append(Paragraph("Tabella 2 — File del progetto.", s['Caption']))
    story.append(hr())


# --- Sezione 4: Knowledge base in Prolog ---
def build_section_4(story, s):
    story.append(PageBreak())
    story.extend(section_header("4. Knowledge Base in Prolog", s))

    story.append(Paragraph(
        "La KB usa <b>fatti atomici</b> (un fatto per ogni coppia malattia–sintomo, descrizione, "
        "trattamento, categoria) più un predicato derivato <i>malattia/1</i>. È la rappresentazione "
        "più naturale per Prolog: il motore accede ai sintomi di una malattia con <i>findall/3</i> "
        "e aggiungere un sintomo significa aggiungere una sola riga.", s['BodyJ']))

    pred_headers = ['Predicato', 'Descrizione', 'Esempio']
    pred_rows = [
        ['sintomo/2',     'Associa una malattia a un sintomo.',
         "sintomo(influenza, febbre_alta)."],
        ['categoria/2',   'Categoria medica della malattia.',
         "categoria(influenza, respiratoria)."],
        ['descrizione/2', 'Descrizione testuale.',
         "descrizione(influenza, '...')."],
        ['trattamento/2', 'Trattamento raccomandato.',
         "trattamento(influenza, '...')."],
        ['malattia/1',    'Predicato derivato (esistenza).',
         "malattia(X) :- categoria(X, _)."],
    ]
    story.append(make_table(pred_headers, pred_rows, [2.8*cm, 5.2*cm, 8*cm]))
    story.append(Paragraph("Tabella 3 — Predicati della Knowledge Base.", s['Caption']))

    kb_code = (
        "%% Sintomi: un fatto per ogni coppia (malattia, sintomo).\n"
        "sintomo(influenza, febbre_alta).\n"
        "sintomo(influenza, tosse_secca).\n"
        "sintomo(influenza, mal_di_testa).\n"
        "%% ...\n"
        "\n"
        "%% Categorie.\n"
        "categoria(influenza, respiratoria).\n"
        "categoria(covid19, respiratoria).\n"
        "\n"
        "%% Predicato derivato.\n"
        "malattia(X) :- categoria(X, _)."
    )
    story.append(code_block(kb_code, s))
    story.append(Paragraph("Listato 1 — Estratto della Knowledge Base.", s['Caption']))
    story.append(hr())


# --- Sezione 5: Regole di inferenza ---
def build_section_5(story, s):
    story.append(PageBreak())
    story.extend(section_header("5. Regole di Inferenza", s))

    story.append(Paragraph(
        "Prolog è un linguaggio di <b>programmazione logica</b> basato sulle clausole di Horn. "
        "Un programma Prolog è una <i>knowledge base</i> di fatti e regole; un'interrogazione "
        "(<i>query</i>) viene risolta dal motore inferenziale tramite due meccanismi fondamentali: "
        "l'<b>unificazione</b> (cerca una sostituzione di variabili che renda due termini "
        "sintatticamente identici) e la <b>risoluzione SLD</b> (sceglie una clausola la cui testa "
        "unifichi con il goal corrente e sostituisce il goal con il body della clausola).", s['BodyJ']))

    story.append(Paragraph(
        "Questa strategia è detta <b>goal-driven</b> o <i>backward chaining</i>: si parte dalla "
        "conclusione da dimostrare e si procede all'indietro verso i fatti. È l'opposto del "
        "<i>forward chaining</i>, che parte dai fatti e ne deriva conseguenze. Per la diagnosi medica "
        "il backward chaining è naturale: l'utente domanda «quali malattie sono compatibili con i "
        "sintomi X, Y, Z?» e il motore lavora a ritroso per verificare ogni candidato.", s['BodyJ']))

    story.append(Paragraph("5.1 La regola principale: diagnosi/3", s['SectionH2']))
    story.append(Paragraph(
        "<b>Nota sulla notazione.</b> In Prolog ogni predicato è identificato dalla coppia "
        "<i>nome/arità</i>, dove l'<b>arità</b> è il numero di argomenti. Così <i>diagnosi/3</i> è "
        "una regola a 3 argomenti, <i>spiega_diagnosi/4</i> ne ha 4, <i>findall/3</i> è il "
        "built-in <i>findall</i> a 3 argomenti. Lo stesso nome con arità diversa indica predicati "
        "distinti.", s['BodyJ']))
    story.append(Paragraph(
        "La regola <b>diagnosi/3</b> implementa il calcolo dell'Indice di Copertura Sintomatica "
        "(ICS) per una malattia, dato l'insieme dei sintomi osservati nel paziente:", s['BodyJ']))

    diag_code = (
        "%% diagnosi(+SintomiPaziente, ?Malattia, -Certezza)\n"
        "diagnosi(SintomiPaziente, Malattia, Certezza) :-\n"
        "    malattia(Malattia),\n"
        "    sort(SintomiPaziente, SintomiUnici),\n"
        "    findall(S, sintomo(Malattia, S), TuttiSintomi),\n"
        "    intersection(SintomiUnici, TuttiSintomi, SintomiComuni),\n"
        "    length(SintomiComuni, NComuni),\n"
        "    NComuni > 0,\n"
        "    length(TuttiSintomi, NTotali),\n"
        "    Certezza is round((NComuni / NTotali) * 100)."
    )
    story.append(code_block(diag_code, s))
    story.append(Paragraph("Listato 2 — La regola diagnosi/3.", s['Caption']))

    story.append(Paragraph(
        "La testa <i>diagnosi(SintomiPaziente, Malattia, Certezza)</i> dichiara una relazione "
        "fra tre argomenti, con modi <i>+</i> (input), <i>?</i> (libero in input/output) e "
        "<i>-</i> (output). Il body è una congiunzione di sotto-goal che Prolog risolve nell'ordine "
        "scritto, sfruttando i built-in standard:", s['BodyJ']))

    story.append(Paragraph(
        "• <b>malattia(Malattia)</b> — unifica <i>Malattia</i> con un identificatore di malattia "
        "esistente nella KB. Tramite <i>backtracking</i> il motore prova tutte le malattie "
        "alternative, generando una soluzione per ognuna.", s['BodyBullet']))
    story.append(Paragraph(
        "• <b>sort/2</b> — ordina la lista dei sintomi del paziente eliminando i duplicati. La "
        "regola è quindi <i>idempotente</i> rispetto alle ripetizioni dell'utente.", s['BodyBullet']))
    story.append(Paragraph(
        "• <b>findall/3</b> — raccoglie in una lista <i>tutti</i> i termini S che rendono vero "
        "<i>sintomo(Malattia, S)</i>. È il meta-predicato canonico per materializzare una "
        "relazione come collezione.", s['BodyBullet']))
    story.append(Paragraph(
        "• <b>intersection/3 e length/2</b> — calcolano l'insieme dei sintomi comuni e la sua "
        "cardinalità, secondo la definizione di ICS.", s['BodyBullet']))
    story.append(Paragraph(
        "• <b>NComuni &gt; 0</b> — vincolo che <i>taglia</i> le malattie senza alcun sintomo "
        "in comune: il motore fallisce immediatamente e fa backtracking sulla scelta di "
        "<i>Malattia</i>.", s['BodyBullet']))
    story.append(Paragraph(
        "• <b>is/2</b> — valuta l'espressione aritmetica a destra e unifica il risultato con "
        "<i>Certezza</i>. È l'unico punto in cui Prolog si comporta in modo «procedurale».", s['BodyBullet']))

    story.append(Paragraph("5.2 Esempio di risoluzione passo-passo", s['SectionH2']))
    story.append(Paragraph(
        "Supponiamo che la query sia <i>diagnosi([febbre_alta, tosse_secca, stanchezza], influenza, C)</i> "
        "e che nella KB siano definiti 7 sintomi per l'influenza. Il motore esegue questi passi:", s['BodyJ']))

    story.append(Paragraph(
        "<b>1.</b> Unifica <i>Malattia</i> con <i>influenza</i> tramite <i>malattia(influenza)</i>, "
        "che riesce perché <i>categoria(influenza, respiratoria)</i> è un fatto della KB.", s['BodyBullet']))
    story.append(Paragraph(
        "<b>2.</b> <i>sort</i> normalizza la lista in <i>[febbre_alta, stanchezza, tosse_secca]</i>.", s['BodyBullet']))
    story.append(Paragraph(
        "<b>3.</b> <i>findall</i> interroga ripetutamente <i>sintomo(influenza, S)</i> e raccoglie "
        "i 7 sintomi tipici dell'influenza in <i>TuttiSintomi</i>.", s['BodyBullet']))
    story.append(Paragraph(
        "<b>4.</b> <i>intersection</i> calcola <i>SintomiComuni = [febbre_alta, stanchezza, tosse_secca]</i> "
        "(3 elementi).", s['BodyBullet']))
    story.append(Paragraph(
        "<b>5.</b> <i>NComuni = 3</i>, <i>NTotali = 7</i>, dunque <i>Certezza is round(3/7 × 100) = 43</i>. "
        "La query ha successo con <i>C = 43</i>.", s['BodyBullet']))

    story.append(Paragraph("5.3 Spiegazione della diagnosi: spiega_diagnosi/4", s['SectionH2']))
    story.append(Paragraph(
        "Un sistema esperto, secondo la definizione classica, non si limita a produrre una "
        "conclusione: deve essere capace di <b>spiegare</b> il proprio ragionamento. In Prolog "
        "questo è particolarmente naturale, perché la stessa knowledge base che ha generato il "
        "risultato può essere interrogata per scomporlo. La regola <b>spiega_diagnosi/4</b> "
        "fornisce esattamente questa explanation facility, dividendo i sintomi della malattia in "
        "<i>trovati</i> (intersezione con il quadro del paziente) e <i>mancanti</i> (differenza "
        "insiemistica):", s['BodyJ']))

    explain_code = (
        "%% spiega_diagnosi(+SintomiPaziente, +Malattia, -Trovati, -Mancanti)\n"
        "spiega_diagnosi(SintomiPaziente, Malattia, Trovati, Mancanti) :-\n"
        "    sort(SintomiPaziente, SintomiUnici),\n"
        "    findall(S, sintomo(Malattia, S), Tutti),\n"
        "    intersection(SintomiUnici, Tutti, Trovati),\n"
        "    subtract(Tutti, Trovati, Mancanti)."
    )
    story.append(code_block(explain_code, s))
    story.append(Paragraph("Listato 3 — La regola spiega_diagnosi/4.", s['Caption']))

    story.append(Paragraph(
        "Le due liste vengono poi mostrate nella GUI per ogni diagnosi selezionata, rendendo "
        "trasparente all'utente <i>perché</i> il sistema propone quella conclusione e quali "
        "sintomi mancanti potrebbero rafforzarla o smentirla.", s['BodyJ']))
    story.append(hr())


# --- Sezione 6: Interfaccia grafica ---
def build_section_6(story, s):
    story.extend(section_header("6. Interfaccia Grafica (Python / Tkinter)", s))

    story.append(Paragraph(
        "La GUI è organizzata in tre aree affiancate: selezione sintomi (sinistra), risultati come "
        "card cliccabili ordinate per ICS (centro), dettagli della diagnosi selezionata (destra). "
        "L'utente spunta i sintomi, clicca «Analizza Sintomi» e ottiene le diagnosi candidate; "
        "cliccando su una card vede sintomi trovati e mancanti, descrizione e trattamento.", s['BodyJ']))

    story.append(Paragraph(
        "Il codice in <font face='Courier'>interfaccia.py</font> è organizzato in due classi: "
        "<b>MedExpertApp</b> costruisce la finestra Tkinter e gestisce eventi e stato; "
        "<b>PrologEngine</b> fa da ponte verso <font face='Courier'>swipl</font> via "
        "<i>subprocess</i>, invia le query e fa il parsing dell'output testuale. La diagnosi viene "
        "lanciata in un thread separato per non bloccare la UI.", s['BodyJ']))

    story.append(hr())


# --- Sezione 7: Test e validazione ---
def build_section_7(story, s):
    story.append(PageBreak())
    story.extend(section_header("7. Test e Validazione", s))

    story.append(Paragraph(
        "La validazione è affidata a una suite di <b>7 test automatizzati</b> in Prolog, integrati "
        "nel file della KB. Coprono i casi rilevanti: corrispondenza esatta e parziale, diagnosi "
        "multiple, sintomi inesistenti, duplicati, spiegazione, ordinamento. Si lancia con:", s['BodyJ']))

    story.append(code_block(
        "swipl -g \"test_diagnosi, halt\" diagnosi_medica.pl", s, label='shell'))

    test_headers = ['#', 'Nome', 'Scopo', 'Esito atteso']
    test_rows = [
        ['1', 'Corrispondenza esatta',
         "Tutti e 7 i sintomi dell'influenza in input",
         'ICS(influenza) = 100%'],
        ['2', 'Corrispondenza parziale',
         "3 sintomi su 7 dell'influenza",
         'ICS = round(3/7·100) = 43%'],
        ['3', 'Diagnosi multiple',
         'Sintomi condivisi tra più malattie',
         '≥ 2 diagnosi restituite'],
        ['4', 'Nessuna corrispondenza',
         'Sintomi non presenti nella KB',
         '0 diagnosi'],
        ['5', 'Gestione duplicati',
         "Stesso sintomo ripetuto nell'input",
         'ICS invariata'],
        ['6', 'Spiegazione',
         "spiega_diagnosi/4 con 2 sintomi dell'influenza",
         '2 trovati, 5 mancanti'],
        ['7', 'Ordinamento',
         'diagnosi_ordinate/2 con 4 sintomi',
         'Lista ordinata per ICS decrescente'],
    ]
    story.append(make_table(test_headers, test_rows,
                            [0.8*cm, 3.5*cm, 6.7*cm, 5*cm]))
    story.append(Paragraph("Tabella 4 — Suite di test.", s['Caption']))

    story.append(Paragraph(
        "Output reale: <font face='Courier'>RIEPILOGO: 7/7 superati, 0 falliti</font>. La suite "
        "serve anche come <b>regression test</b>: ogni modifica alla KB viene verificata in "
        "automatico.", s['BodyJ']))

    story.append(hr())


# --- Sezione 8: Conclusioni ---
def build_section_8(story, s):
    story.extend(section_header("8. Conclusioni", s))

    story.append(Paragraph(
        "MedExpert AI applica i temi centrali del corso — rappresentazione della conoscenza in una "
        "KB, inferenza nella logica del primo ordine con <i>backward chaining</i>, Prolog come "
        "linguaggio basato su clausole di Horn — a un dominio concreto e realistico. Combinando "
        "la KB Prolog con una GUI Python, il sistema mostra che l'AI simbolica resta uno strumento "
        "efficace quando spiegabilità, trasparenza e determinismo sono requisiti imprescindibili, "
        "come nella diagnostica medica.", s['BodyJ']))

    # Chiusura del documento: divisore minimale + firma autori centrata.
    story.append(Spacer(1, 0.6 * cm))
    story.append(HRFlowable(width="30%", thickness=1, color=ACCENT_BLUE,
                             spaceBefore=0, spaceAfter=14, hAlign='CENTER'))
    story.append(Paragraph(
        "<b>Luciano Meccariello N46007465</b><br/>"
        "<b>Gaspare Tortora N46007942</b><br/>"
        "<b>Andrea Francesco Bruno N46007639</b>",
        ParagraphStyle('Author', parent=s['BodyJ'], alignment=TA_CENTER,
                       fontSize=12, textColor=DARK_BLUE, fontName='Helvetica-Bold',
                       leading=18)
    ))


# --- Main ---
def main():
    # Mettiamo il PDF nella stessa cartella dello script.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "Documentazione_MedExpert.pdf")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=2.4 * cm,
        bottomMargin=1.8 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        title="MedExpert AI — Documentazione di Progetto",
        author="Luciano Meccariello N46007465, Gaspare Tortora N46007942, Andrea Francesco Bruno N46007639",
        subject="Sistema Esperto di Diagnosi Medica",
    )

    styles = build_styles()
    story = []

    # Costruiamo il documento accodando alla story tutte le sezioni in ordine.
    build_cover(story, styles)
    build_toc(story, styles)
    build_section_1(story, styles)
    build_section_2(story, styles)
    build_section_3(story, styles)
    build_section_4(story, styles)
    build_section_5(story, styles)
    build_section_6(story, styles)
    build_section_7(story, styles)
    build_section_8(story, styles)

    # A questo punto reportlab si occupa di impaginare tutto.
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"✅ PDF generato con successo: {output_path}")
    print(f"   Dimensione: {os.path.getsize(output_path) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
