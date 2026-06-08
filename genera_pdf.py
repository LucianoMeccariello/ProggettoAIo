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
DARK_BLUE   = HexColor("#1a2e4a")
ACCENT_BLUE = HexColor("#2e6da4")
LIGHT_BLUE  = HexColor("#d6e4f0")
VERY_LIGHT  = HexColor("#eef3f9")
CODE_BG     = HexColor("#f4f4f4")
CODE_BORDER = HexColor("#cccccc")
TABLE_HEAD  = HexColor("#2e6da4")
ROW_EVEN    = HexColor("#f0f4f8")
ROW_ODD     = HexColor("#ffffff")
DARK_TEXT    = HexColor("#1a1a1a")
MUTED_TEXT   = HexColor("#555555")
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
        fontSize=20,
        textColor=white,
        alignment=TA_CENTER,
        leading=26,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name='CoverCourse',
        fontName='Helvetica',
        fontSize=14,
        textColor=white,
        alignment=TA_CENTER,
        leading=20,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name='CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=28,
        textColor=DARK_BLUE,
        alignment=TA_CENTER,
        leading=34,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name='CoverSubtitle',
        fontName='Helvetica-Oblique',
        fontSize=14,
        textColor=ACCENT_BLUE,
        alignment=TA_CENTER,
        leading=20,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name='CoverInfo',
        fontName='Helvetica',
        fontSize=13,
        textColor=DARK_TEXT,
        alignment=TA_CENTER,
        leading=20,
        spaceAfter=4,
    ))

    # Header di sezione (H1, H2, H3) usati nel corpo del documento.
    styles.add(ParagraphStyle(
        name='SectionH1',
        fontName='Helvetica-Bold',
        fontSize=16,
        textColor=white,
        alignment=TA_LEFT,
        leading=21,
        spaceBefore=12,
        spaceAfter=8,
        leftIndent=0,
        backColor=DARK_BLUE,
        borderPadding=(6, 9, 6, 9),
    ))
    styles.add(ParagraphStyle(
        name='SectionH2',
        fontName='Helvetica-Bold',
        fontSize=13,
        textColor=DARK_BLUE,
        alignment=TA_LEFT,
        leading=17,
        spaceBefore=10,
        spaceAfter=4,
        borderWidth=0,
        borderColor=ACCENT_BLUE,
        borderPadding=(0, 0, 1, 0),
    ))
    styles.add(ParagraphStyle(
        name='SectionH3',
        fontName='Helvetica-Bold',
        fontSize=11.5,
        textColor=ACCENT_BLUE,
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

    # Blocchi di codice e codice inline (font monospace + sfondo grigio).
    styles.add(ParagraphStyle(
        name='CodeBlock',
        fontName='Courier',
        fontSize=8,
        textColor=DARK_TEXT,
        alignment=TA_LEFT,
        leading=11,
        spaceBefore=4,
        spaceAfter=4,
        leftIndent=6,
        rightIndent=6,
        backColor=CODE_BG,
        borderPadding=(4, 6, 4, 6),
        borderWidth=0.5,
        borderColor=CODE_BORDER,
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
    # Linea orizzontale "spessa" usata come separatore tra sezioni.
    return HRFlowable(
        width="100%", thickness=1, color=ACCENT_BLUE,
        spaceBefore=8, spaceAfter=8
    )


def thin_hr():
    # Linea sottile, usata tra le voci dell'indice.
    return HRFlowable(
        width="100%", thickness=0.5, color=LIGHT_BLUE,
        spaceBefore=2, spaceAfter=2
    )


def make_table(headers, rows, col_widths=None):
    # Crea una tabella con header colorato e righe a zebra.
    # Se non passiamo col_widths, reportlab divide lo spazio in parti uguali.
    data = [headers] + rows
    if col_widths is None:
        col_widths = [None] * len(headers)

    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        # Riga di intestazione: sfondo blu, testo bianco, bold.
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEAD),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9.5),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        # Righe del corpo.
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        # Griglia e allineamento.
        ('GRID', (0, 0), (-1, -1), 0.4, ACCENT_BLUE),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ]
    # Effetto zebra sulle righe.
    for i in range(1, len(data)):
        bg = ROW_EVEN if i % 2 == 0 else ROW_ODD
        style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))

    t.setStyle(TableStyle(style_cmds))
    return t


def code_block(text, styles):
    # Prende del testo e lo renderizza come blocco di codice.
    # Bisogna fare l'escape dei caratteri speciali XML (& < >) altrimenti
    # reportlab li interpreta come tag e crasha.
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return Paragraph(text.replace('\n', '<br/>'), styles['CodeBlock'])


# --- Header e footer di pagina ---
# Vengono richiamati da reportlab su ogni pagina tramite onLaterPages.
def header_footer(canvas, doc):
    canvas.saveState()
    page_num = doc.page

    # Saltiamo la copertina (pagina 1), li' non vogliamo header/footer.
    if page_num > 1:
        # Banda blu in alto con titolo del progetto e ateneo.
        canvas.setFillColor(DARK_BLUE)
        canvas.rect(0, PAGE_H - 22 * mm, PAGE_W, 22 * mm, fill=1, stroke=0)
        canvas.setFillColor(white)
        canvas.setFont('Helvetica', 8)
        canvas.drawString(2 * cm, PAGE_H - 14 * mm,
                          "MedExpert AI — Sistema Esperto di Diagnosi Medica")
        canvas.drawRightString(PAGE_W - 2 * cm, PAGE_H - 14 * mm,
                               "Università degli Studi di Napoli Federico II")

        # Banda chiara in basso con nome corso e numero di pagina.
        canvas.setFillColor(LIGHT_BLUE)
        canvas.rect(0, 0, PAGE_W, 12 * mm, fill=1, stroke=0)
        canvas.setFillColor(DARK_BLUE)
        canvas.setFont('Helvetica', 8)
        canvas.drawString(2 * cm, 4.5 * mm,
                          "Elementi di Intelligenza Artificiale — A.A. 2025/2026")
        canvas.drawRightString(PAGE_W - 2 * cm, 4.5 * mm,
                               f"Pagina {page_num}")
    canvas.restoreState()


# ===== Pagina di copertina =====
def build_cover(story, styles):
    story.append(Spacer(1, 1.5 * cm))

    # Banner scuro in alto con il nome dell'universita'.
    banner_data = [[
        Paragraph("UNIVERSITÀ DEGLI STUDI DI NAPOLI FEDERICO II",
                  styles['CoverUniversity'])
    ]]
    banner = Table(banner_data, colWidths=[PAGE_W - 4 * cm])
    banner.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), DARK_BLUE),
        ('TOPPADDING', (0, 0), (-1, -1), 18),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 18),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(banner)
    story.append(Spacer(1, 0.3 * cm))

    # Banner piu' chiaro col nome del corso.
    sub_data = [[
        Paragraph("Corso di Elementi di Intelligenza Artificiale",
                  styles['CoverCourse'])
    ]]
    sub = Table(sub_data, colWidths=[PAGE_W - 4 * cm])
    sub.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), ACCENT_BLUE),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(sub)

    story.append(Spacer(1, 2.5 * cm))

    # Titolo del progetto, ben grosso al centro.
    story.append(Paragraph(
        "MedExpert AI",
        styles['CoverTitle']
    ))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        "Sistema Esperto di Diagnosi Medica",
        ParagraphStyle(
            'BigSub', parent=styles['CoverTitle'],
            fontSize=20, leading=26, textColor=ACCENT_BLUE,
        )
    ))
    story.append(Spacer(1, 0.6 * cm))

    story.append(HRFlowable(width="60%", thickness=2, color=ACCENT_BLUE,
                             spaceBefore=4, spaceAfter=4))

    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph(
        "Implementazione in Prolog con Interfaccia Grafica Python",
        styles['CoverSubtitle']
    ))

    story.append(Spacer(1, 3.5 * cm))

    # Tabella docente / studente.
    info_data = [
        [Paragraph("<b>Docente:</b>", styles['CoverInfo']),
         Paragraph("<b>Studente:</b>", styles['CoverInfo'])],
        [Paragraph("Prof. Giancarlo Sperlì", styles['CoverInfo']),
         Paragraph("Luciano Meccariello", styles['CoverInfo'])],
    ]
    info_table = Table(info_data, colWidths=[7.5 * cm, 7.5 * cm])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, ACCENT_BLUE),
    ]))
    story.append(info_table)

    story.append(Spacer(1, 2.5 * cm))

    # Riga finale con l'anno accademico.
    aa_data = [[Paragraph("Anno Accademico 2025/2026", styles['CoverInfo'])]]
    aa_table = Table(aa_data, colWidths=[PAGE_W - 4 * cm])
    aa_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BLUE),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(aa_table)

    story.append(PageBreak())


# ===== Indice =====
def build_toc(story, styles):
    story.append(Paragraph("Indice", styles['TOCTitle']))
    story.append(hr())
    story.append(Spacer(1, 0.4 * cm))

    sections = [
        ("1", "Obiettivo del Progetto"),
        ("2", "Il Dominio: Diagnosi Medica"),
        ("3", "Architettura del Sistema"),
        ("4", "Knowledge Base in Prolog"),
        ("5", "Regole di Inferenza"),
        ("6", "Interfaccia Grafica (Python / Tkinter)"),
        ("7", "Test e Validazione"),
        ("8", "Conclusioni e Sviluppi Futuri"),
    ]

    for num, title in sections:
        entry = Paragraph(
            f'<b>{num}.</b>&nbsp;&nbsp;&nbsp;{title}',
            styles['TOCEntry']
        )
        story.append(entry)
        story.append(thin_hr())

    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(
        "<i>Documento generato automaticamente — Maggio 2026</i>",
        styles['Caption']
    ))
    story.append(PageBreak())


# --- Sezione 1: Obiettivo del progetto ---
def build_section_1(story, s):
    story.append(Paragraph("1. Obiettivo del Progetto", s['SectionH1']))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph(
        "L'obiettivo principale di questo progetto è la realizzazione di un <b>sistema esperto completo "
        "per la diagnosi medica</b>, che integri una base di conoscenza in Prolog con un'interfaccia "
        "grafica moderna in Python. Il sistema è progettato per dimostrare i concetti fondamentali "
        "dei sistemi esperti in un contesto applicativo realistico e didatticamente significativo.", s['BodyJ']))

    story.append(Paragraph("1.1 Obiettivi Specifici", s['SectionH2']))

    objectives = [
        "Progettare e implementare una <b>Knowledge Base</b> in Prolog contenente 17 patologie "
        "mediche con i rispettivi sintomi, categorie, descrizioni e trattamenti.",
        "Implementare un <b>motore inferenziale</b> goal-driven (backward chaining) che calcoli, "
        "per ogni malattia, un <b>indice di copertura sintomatica</b> e ordini i risultati per "
        "valore decrescente.",
        "Realizzare un meccanismo di <b>spiegazione</b> (<i>explanation facility</i>) che, per ogni "
        "diagnosi, espliciti quali sintomi della malattia sono stati trovati nel paziente e quali "
        "risultano mancanti.",
        "Sviluppare un'<b>interfaccia grafica</b> intuitiva con tema medicale scuro, che permetta la "
        "selezione interattiva dei sintomi e la visualizzazione chiara dei risultati diagnostici.",
        "Integrare Prolog e Python tramite <b>subprocess</b>, dimostrando l'interoperabilità tra "
        "paradigmi di programmazione (logico e imperativo).",
        "Predisporre una <b>suite di test automatizzati</b> in Prolog per validare la correttezza "
        "delle diagnosi prodotte dal sistema.",
    ]
    for i, obj in enumerate(objectives, 1):
        story.append(Paragraph(f"<b>{i}.</b> {obj}", s['BodyBullet']))

    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("1.2 Requisiti del Sistema", s['SectionH2']))
    story.append(Paragraph(
        "Il sistema deve soddisfare i seguenti requisiti funzionali e non funzionali:", s['BodyJ']))

    req_headers = ['Tipo', 'Requisito', 'Descrizione']
    req_rows = [
        ['Funzionale', 'Diagnosi multipla', 'Generare più diagnosi ordinate per certezza'],
        ['Funzionale', 'Spiegazione', 'Fornire giustificazione per ogni diagnosi'],
        ['Funzionale', 'Categorizzazione', 'Classificare le malattie per categoria medica'],
        ['Non-funz.', 'Usabilità', 'Interfaccia intuitiva senza formazione necessaria'],
        ['Non-funz.', 'Estensibilità', 'Aggiunta facile di nuove malattie alla KB'],
        ['Non-funz.', 'Portabilità', 'Esecuzione su sistemi con Python 3 e SWI-Prolog'],
    ]
    story.append(make_table(req_headers, req_rows, [2.5*cm, 3.5*cm, 10*cm]))
    story.append(Paragraph("Tabella 1 — Requisiti funzionali e non funzionali del sistema.",
                           s['Caption']))
    story.append(hr())


# --- Sezione 2: Dominio della diagnosi medica ---
def build_section_2(story, s):
    story.append(Paragraph("2. Il Dominio: Diagnosi Medica", s['SectionH1']))
    story.append(Spacer(1, 0.25 * cm))

    story.append(Paragraph("2.1 Perché la Diagnosi Medica?", s['SectionH2']))
    story.append(Paragraph(
        "La diagnosi medica rappresenta un dominio ideale per l'applicazione dei sistemi esperti "
        "per diverse ragioni fondamentali. In primo luogo, il processo diagnostico è intrinsecamente "
        "<b>basato su regole</b>: i medici utilizzano la propria esperienza e conoscenza per "
        "correlare insiemi di sintomi a possibili patologie, seguendo un ragionamento logico che "
        "può essere formalizzato in regole del tipo «se il paziente presenta i sintomi X, Y e Z, "
        "allora una diagnosi candidata è W».", s['BodyJ']))

    story.append(Paragraph(
        "In secondo luogo, la diagnosi medica è un problema di <b>copertura sintomatologica "
        "parziale</b>: raramente un paziente presenta tutti i sintomi caratteristici di una "
        "patologia, e spesso gli stessi sintomi possono essere associati a malattie diverse. Questa "
        "caratteristica si presta naturalmente a un meccanismo di ranking delle diagnosi, anziché "
        "a una risposta binaria.", s['BodyJ']))

    story.append(Paragraph(
        "Infine, la diagnosi medica richiede una <b>capacità di spiegazione</b>: non è sufficiente "
        "che il sistema produca una diagnosi, ma deve essere in grado di giustificarla, mostrando "
        "il ragionamento seguito. Questa trasparenza è fondamentale sia per la fiducia dell'utente "
        "che per scopi didattici.", s['BodyJ']))

    story.append(Paragraph("2.2 Il Processo Diagnostico come Inferenza Logica", s['SectionH2']))
    story.append(Paragraph(
        "Il processo diagnostico può essere modellato come un problema di <b>inferenza logica</b>. "
        "Data una base di conoscenza che associa malattie a sintomi, e dato un insieme di sintomi "
        "osservati nel paziente, il sistema deve enumerare le diagnosi candidate e ordinarle. "
        "Formalmente, per ogni malattia M nella KB:", s['BodyJ']))

    story.append(code_block(
        "ICS(M) = round( |Sintomi_Paziente ∩ Sintomi_M| / |Sintomi_M| × 100 )", s))

    story.append(Paragraph(
        "L'<b>Indice di Copertura Sintomatica</b> (ICS) misura quale frazione dei sintomi tipici "
        "di M è presente nel quadro del paziente. È un indice di ranking, non una probabilità: "
        "le diagnosi a ICS più alto sono quelle che il sistema propone per prime, ma la decisione "
        "clinica finale resta del medico.", s['BodyJ']))

    story.append(Paragraph("2.3 Patologie Coperte", s['SectionH2']))
    story.append(Paragraph(
        "MedExpert AI copre un ampio spettro di patologie comuni, organizzate in categorie mediche. "
        "Di seguito l'elenco completo delle <b>17 malattie</b> presenti nella Knowledge Base, "
        "organizzate in <b>10 categorie</b>:", s['BodyJ']))

    disease_headers = ['#', 'Malattia', 'Categoria', 'N° Sintomi']
    disease_rows = [
        ['1',  'Influenza',                'Respiratoria',      '7'],
        ['2',  'COVID-19',                 'Respiratoria',      '8'],
        ['3',  'Bronchite',                'Respiratoria',      '7'],
        ['4',  'Polmonite',                'Respiratoria',      '8'],
        ['5',  'Gastrite',                 'Gastrointestinale', '6'],
        ['6',  'Appendicite',              'Gastrointestinale', '6'],
        ['7',  'Reflusso gastroesofageo',  'Gastrointestinale', '6'],
        ['8',  'Emicrania',                'Neurologica',       '6'],
        ['9',  'Meningite',                'Neurologica',       '8'],
        ['10', 'Ipertensione',             'Cardiovascolare',   '6'],
        ['11', 'Tachicardia',              'Cardiovascolare',   '6'],
        ['12', 'Anemia',                   'Ematologica',       '7'],
        ['13', 'Diabete di tipo 2',        'Metabolica',        '6'],
        ['14', 'Ipotiroidismo',            'Endocrina',         '7'],
        ['15', 'Cistite',                  'Urologica',         '6'],
        ['16', 'Allergia stagionale',      'Immunitaria',       '6'],
        ['17', 'Depressione',              'Psichiatrica',      '7'],
    ]
    story.append(make_table(disease_headers, disease_rows,
                            [1*cm, 5*cm, 4.5*cm, 2.5*cm]))
    story.append(Paragraph("Tabella 2 — Elenco completo delle patologie nella Knowledge Base.",
                           s['Caption']))

    story.append(Paragraph("2.4 Inquadramento nel Corso", s['SectionH2']))
    story.append(Paragraph(
        "Il progetto si colloca nei <b>capitoli 7-10</b> del corso: rappresentazione della "
        "conoscenza in una base di conoscenza (KB), motore inferenziale, regole di "
        "produzione/inferenza e linguaggio Prolog basato su clausole di Horn. Il dominio medico "
        "è particolarmente naturale per questo paradigma: la conoscenza diagnostica può essere "
        "fornita da un esperto di dominio (il medico) sotto forma di regole tipo «se sono "
        "presenti i sintomi s₁, …, s_n allora la malattia M è una diagnosi candidata», che si "
        "traducono direttamente in fatti e regole Prolog.", s['BodyJ']))
    story.append(Paragraph(
        "Il libro Gallucci ricorda esplicitamente, nel capitolo 10, che <i>«un medico... può "
        "fornire tutto ciò che ha appreso dalla sua esperienza: il ruolo dell'esperto è dunque "
        "cruciale»</i>: MedExpert AI segue letteralmente questa indicazione. Il motore "
        "inferenziale di SWI-Prolog si occupa poi di attivare le regole della KB in modo "
        "goal-driven (equivalente al backward chaining descritto nel cap. 9.4) per rispondere "
        "alle query dell'utente, e la GUI Python svolge il ruolo di interfaccia tra l'utente "
        "non-tecnico e il motore logico.", s['BodyJ']))
    story.append(hr())


# --- Sezione 3: Architettura del sistema ---
def build_section_3(story, s):
    story.append(Paragraph("3. Architettura del Sistema", s['SectionH1']))
    story.append(Spacer(1, 0.25 * cm))

    story.append(Paragraph("3.1 Panoramica Architetturale", s['SectionH2']))
    story.append(Paragraph(
        "MedExpert AI adotta un'architettura a <b>tre livelli</b> (three-tier), in cui ciascun "
        "livello ha responsabilità ben definite. Questa separazione garantisce modularità, "
        "manutenibilità e la possibilità di evolvere ciascun componente indipendentemente.", s['BodyJ']))

    # Diagramma architetturale testuale
    arch_text = (
        "┌─────────────────────────────────────────────────┐\n"
        "│          INTERFACCIA UTENTE (Python/Tkinter)    │\n"
        "│  ┌─────────────┐ ┌──────────┐ ┌─────────────┐  │\n"
        "│  │  Selezione   │ │ Diagnosi │ │  Dettaglio  │  │\n"
        "│  │  Sintomi     │ │  Cards   │ │  Malattia   │  │\n"
        "│  └─────────────┘ └──────────┘ └─────────────┘  │\n"
        "└──────────────────────┬──────────────────────────┘\n"
        "                       │ subprocess (stdin/stdout)\n"
        "┌──────────────────────▼──────────────────────────┐\n"
        "│         MOTORE INFERENZIALE (SWI-Prolog)        │\n"
        "│   backward chaining · ICS · findall · sort      │\n"
        "└──────────────────────┬──────────────────────────┘\n"
        "                       │ consult/1\n"
        "┌──────────────────────▼──────────────────────────┐\n"
        "│         KNOWLEDGE BASE (diagnosi_medica.pl)     │\n"
        "│  fatti · regole · test · spiegazioni            │\n"
        "└─────────────────────────────────────────────────┘"
    )
    story.append(code_block(arch_text, s))
    story.append(Paragraph("Figura 1 — Architettura a tre livelli di MedExpert AI.", s['Caption']))

    story.append(Paragraph("3.2 Comunicazione tra Python e Prolog", s['SectionH2']))
    story.append(Paragraph(
        "L'integrazione tra Python e SWI-Prolog avviene tramite il modulo <b>subprocess</b> della "
        "libreria standard Python. Python avvia un processo SWI-Prolog, invia query formattate "
        "tramite standard input e analizza i risultati restituiti su standard output. Questo "
        "approccio è stato scelto per la sua semplicità, portabilità e assenza di dipendenze "
        "esterne (non richiede librerie di bridging come PySwip).", s['BodyJ']))

    story.append(Paragraph(
        "Il flusso di comunicazione è il seguente: (1) l'utente seleziona i sintomi nella GUI; "
        "(2) Python costruisce una query Prolog con la lista dei sintomi selezionati; "
        "(3) la query viene inviata a SWI-Prolog via subprocess; (4) Prolog esegue il backward "
        "chaining sulla KB e restituisce le diagnosi ordinate; (5) Python analizza l'output e "
        "aggiorna la GUI con i risultati.", s['BodyJ']))

    story.append(PageBreak())
    story.append(Paragraph("3.3 Struttura dei File", s['SectionH2']))

    file_headers = ['File', 'Linguaggio', 'Ruolo']
    file_rows = [
        ['diagnosi_medica.pl', 'Prolog', 'Knowledge Base + Regole inferenziali + Test'],
        ['interfaccia.py', 'Python', 'Interfaccia grafica Tkinter + ponte verso swipl'],
        ['genera_pdf.py', 'Python', 'Generatore documentazione PDF'],
        ['README.md', 'Markdown', 'Documentazione del progetto'],
    ]
    story.append(make_table(file_headers, file_rows, [4.5*cm, 3*cm, 8.5*cm]))
    story.append(Paragraph("Tabella 3 — Struttura dei file del progetto.", s['Caption']))
    story.append(hr())


# --- Sezione 4: Knowledge base in Prolog ---
def build_section_4(story, s):
    story.append(Paragraph("4. Knowledge Base in Prolog", s['SectionH1']))
    story.append(Spacer(1, 0.25 * cm))

    story.append(Paragraph("4.1 Struttura dei Fatti", s['SectionH2']))
    story.append(Paragraph(
        "La Knowledge Base è organizzata utilizzando quattro predicati di fatti più un predicato "
        "derivato, ciascuno dei quali cattura un aspetto diverso della conoscenza medica:", s['BodyJ']))

    pred_headers = ['Predicato', 'Arità', 'Descrizione', 'Esempio']
    pred_rows = [
        ['sintomo/2', '2',
         "Associa una malattia a un singolo sintomo. Si dichiarano più fatti per la stessa malattia.",
         "sintomo(influenza, febbre_alta)."],
        ['categoria/2', '2', 'Categoria medica della malattia.',
         "categoria(influenza, respiratoria)."],
        ['descrizione/2', '2', 'Descrizione testuale della malattia.',
         "descrizione(influenza, '...')."],
        ['trattamento/2', '2', 'Trattamento raccomandato.',
         "trattamento(influenza, '...')."],
        ['malattia/1', '1',
         "Predicato derivato: vero se la malattia esiste nella KB.",
         "malattia(X) :- categoria(X, _)."],
    ]
    story.append(make_table(pred_headers, pred_rows, [2.4*cm, 1.2*cm, 5.4*cm, 7*cm]))
    story.append(Paragraph("Tabella 4 — Predicati della Knowledge Base.", s['Caption']))

    story.append(Paragraph("4.2 Esempi di Fatti nella KB", s['SectionH2']))
    story.append(Paragraph(
        "Di seguito sono riportati alcuni esempi rappresentativi dei fatti codificati nella "
        "Knowledge Base Prolog:", s['BodyJ']))

    kb_code = (
        "%% Sintomi: un fatto per ogni coppia (malattia, sintomo).\n"
        "sintomo(influenza, febbre_alta).\n"
        "sintomo(influenza, mal_di_testa).\n"
        "sintomo(influenza, dolori_muscolari).\n"
        "sintomo(influenza, tosse_secca).\n"
        "sintomo(influenza, mal_di_gola).\n"
        "sintomo(influenza, stanchezza).\n"
        "sintomo(influenza, naso_chiuso).\n"
        "\n"
        "sintomo(covid19, febbre_alta).\n"
        "sintomo(covid19, tosse_secca).\n"
        "sintomo(covid19, difficolta_respiratorie).\n"
        "sintomo(covid19, perdita_gusto_olfatto).\n"
        "sintomo(covid19, stanchezza).\n"
        "%% ...\n"
        "\n"
        "%% Categorie.\n"
        "categoria(influenza, respiratoria).\n"
        "categoria(covid19, respiratoria).\n"
        "categoria(diabete_tipo2, metabolica).\n"
        "\n"
        "%% Predicato derivato.\n"
        "malattia(X) :- categoria(X, _)."
    )
    story.append(code_block(kb_code, s))
    story.append(Paragraph("Listato 1 — Estratto della Knowledge Base in Prolog.", s['Caption']))

    story.append(Paragraph("4.3 Scelte Progettuali della KB", s['SectionH2']))
    story.append(Paragraph(
        "La progettazione della Knowledge Base ha seguito alcuni principi fondamentali:", s['BodyJ']))
    story.append(Paragraph(
        "• <b>Fatti atomici anziché liste</b> — La scelta di codificare i sintomi come fatti separati "
        "(<font face='Courier'>sintomo(influenza, febbre_alta).</font>) riflette lo stile dichiarativo "
        "di Prolog: ogni fatto è un'unità minima di conoscenza, indipendentemente assertabile, e il "
        "motore di inferenza accede all'insieme dei sintomi di una malattia tramite <i>findall/3</i>. "
        "Questa rappresentazione facilita l'estensione della KB (aggiungere un nuovo sintomo a una "
        "malattia significa aggiungere una sola riga) e si presta naturalmente all'uso di predicati "
        "derivati come <i>malattia/1</i>.", s['BodyBullet']))
    story.append(Paragraph(
        "• <b>Modularità</b> — Ogni aspetto della conoscenza (sintomi, descrizioni, trattamenti, "
        "categorie) è codificato in predicati separati, facilitando l'aggiornamento e l'estensione.", s['BodyBullet']))
    story.append(Paragraph(
        "• <b>Uniformità</b> — Tutti i fatti seguono la stessa convenzione di naming: il primo "
        "argomento è sempre l'identificatore della malattia (atomo Prolog), il secondo contiene "
        "l'informazione associata.", s['BodyBullet']))
    story.append(Paragraph(
        "• <b>Completezza</b> — Per ogni malattia sono forniti tutti e quattro i tipi di "
        "informazione (sintomi, descrizione, trattamento, categoria), garantendo che il sistema "
        "possa sempre fornire una risposta completa.", s['BodyBullet']))

    story.append(hr())


# --- Sezione 5: Regole di inferenza ---
def build_section_5(story, s):
    story.append(Paragraph("5. Regole di Inferenza", s['SectionH1']))
    story.append(Spacer(1, 0.25 * cm))

    story.append(Paragraph(
        "Il motore inferenziale di Prolog risolve i goal in modo <b>goal-driven</b> "
        "(Gallucci, sez. 9.4.2 e 10.3): a partire dal goal viene cercato un fatto o una regola "
        "la cui testa unifica con esso, e si tenta ricorsivamente di dimostrare le precondizioni "
        "nel body. Questo schema corrisponde al <i>backward chaining</i> della logica del primo "
        "ordine. Prolog è, citando il libro, <i>«pensato da principio per essere goal-driven "
        "come BC»</i>.", s['BodyJ']))
    story.append(Paragraph(
        "In questo progetto la regola principale <i>diagnosi/3</i> sfrutta questo schema nel modo "
        "seguente: dato il goal <i>diagnosi(SintomiPaziente, Malattia, Certezza)</i>, l'interprete "
        "tenta di unificare <i>Malattia</i> con una malattia legittima della KB (tramite il "
        "predicato derivato <i>malattia/1</i>), raccoglie i suoi sintomi con <i>findall/3</i> e "
        "calcola l'ICS. La \"catena\" inferenziale qui non è multilivello — non ci sono regole di "
        "produzione che generano fatti intermedi inseriti nella KB — ma è la catena standard di "
        "unificazione e risoluzione interna a Prolog.", s['BodyJ']))

    story.append(Paragraph("5.1 Indice di Copertura Sintomatica — diagnosi/3", s['SectionH2']))
    story.append(Paragraph(
        "La regola principale del sistema esperto è <b>diagnosi/3</b>, che sfrutta lo schema "
        "goal-driven di Prolog (backward chaining) per calcolare, per ogni malattia della KB, "
        "un indice di copertura sintomatica a partire dai sintomi forniti dall'utente.", s['BodyJ']))

    diag_code = (
        "%% diagnosi(+SintomiPaziente, ?Malattia, -Certezza)\n"
        "%% Calcola l'indice di copertura sintomatica per una malattia.\n"
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
    story.append(Paragraph("Listato 2 — Regola diagnosi/3 estratta da diagnosi_medica.pl.",
                           s['Caption']))

    story.append(Paragraph(
        "Alcuni dettagli implementativi che è utile commentare:", s['BodyJ']))
    story.append(Paragraph(
        "• <i>sort/2</i> rimuove eventuali sintomi duplicati dall'input dell'utente prima del "
        "confronto, rendendo la regola idempotente rispetto alle ripetizioni.", s['BodyBullet']))
    story.append(Paragraph(
        "• <i>findall/3</i> raccoglie <i>tutti</i> i sintomi associati alla malattia interrogando "
        "ripetutamente <i>sintomo/2</i>, restituendo una lista. È il punto in cui si materializza "
        "l'insieme dei sintomi a partire dai fatti atomici della KB.", s['BodyBullet']))
    story.append(Paragraph(
        "• Il risultato è <b>arrotondato all'intero</b> (<i>round</i>) anziché lasciato in decimali, "
        "per coerenza con i valori mostrati nella GUI.", s['BodyBullet']))
    story.append(Paragraph(
        "• La clausola <i>NComuni &gt; 0</i> esclude le malattie senza alcun sintomo in comune con "
        "il paziente, evitando di mostrare diagnosi totalmente irrilevanti.", s['BodyBullet']))

    story.append(Paragraph("5.2 Indice di Copertura Sintomatica (ICS)", s['SectionH2']))
    story.append(Paragraph(
        "Per ogni malattia M nella Knowledge Base, il sistema calcola un <b>Indice di Copertura "
        "Sintomatica</b> definito come:", s['BodyJ']))

    formula_text = (
        "                |S_paziente ∩ S_M|\n"
        "    ICS(M) = round( ───────────────── × 100 )\n"
        "                     |S_M|"
    )
    story.append(code_block(formula_text, s))
    story.append(Paragraph(
        "dove S_paziente è l'insieme dei sintomi selezionati dall'utente, S_M è l'insieme dei "
        "sintomi associati alla malattia M nella KB, e l'arrotondamento è all'intero più vicino.",
        s['BodyJ']))
    story.append(Paragraph(
        "L'ICS misura <b>in che proporzione i sintomi tipici di M sono presenti nel paziente</b>. "
        "In termini statistici è una grandezza affine al <i>recall</i> della malattia M rispetto "
        "ai sintomi: non penalizza i sintomi del paziente che non sono associati a M. Per questo "
        "motivo l'ICS va inteso come <b>strumento di ranking diagnostico</b>, non come probabilità "
        "a posteriori di M dato il quadro sintomatologico. Il ranking è prodotto da "
        "<i>diagnosi_ordinate/2</i>, che aggrega le diagnosi e le ordina per ICS decrescente.",
        s['BodyJ']))
    story.append(Paragraph(
        "<b>Esempio.</b> Se l'influenza ha 7 sintomi nella KB e il paziente ne presenta 3 "
        "corrispondenti, ICS(influenza) = round(3/7 × 100) = 43%.", s['BodyJ']))

    story.append(Paragraph("5.3 Diagnosi Ordinate — diagnosi_ordinate/2", s['SectionH2']))
    story.append(Paragraph(
        "La regola <b>diagnosi_ordinate/2</b> raccoglie tutte le diagnosi possibili e le ordina "
        "per ICS decrescente, presentando le diagnosi a copertura più alta per prime:", s['BodyJ']))

    sort_code = (
        "%% diagnosi_ordinate(+Sintomi, -DiagnosiOrdinate)\n"
        "%% Raccoglie le diagnosi e le ordina per ICS decrescente.\n"
        "diagnosi_ordinate(Sintomi, DiagnosiOrdinate) :-\n"
        "    findall(\n"
        "        certezza(CF, Malattia),\n"
        "        diagnosi(Sintomi, Malattia, CF),\n"
        "        Diagnosi\n"
        "    ),\n"
        "    sort(0, @>=, Diagnosi, DiagnosiOrdinate)."
    )
    story.append(code_block(sort_code, s))
    story.append(Paragraph(
        "Listato 3 — Ordinamento delle diagnosi (il termine <i>certezza/2</i> e la variabile "
        "<i>CF</i> sono identificatori interni al codice Prolog).", s['Caption']))

    story.append(Paragraph("5.4 Facility di Spiegazione — spiega_diagnosi/4", s['SectionH2']))
    story.append(Paragraph(
        "Una caratteristica fondamentale dei sistemi esperti è la capacità di <b>spiegare</b> il "
        "ragionamento che ha portato a una conclusione. La regola <b>spiega_diagnosi/4</b> divide "
        "i sintomi della malattia in due liste: quelli effettivamente <i>trovati</i> nel paziente "
        "e quelli <i>mancanti</i>.", s['BodyJ']))

    explain_code = (
        "%% spiega_diagnosi(+SintomiPaziente, +Malattia, -Trovati, -Mancanti)\n"
        "%% Divide i sintomi della malattia in trovati nel paziente e mancanti.\n"
        "spiega_diagnosi(SintomiPaziente, Malattia, Trovati, Mancanti) :-\n"
        "    sort(SintomiPaziente, SintomiUnici),\n"
        "    findall(S, sintomo(Malattia, S), Tutti),\n"
        "    intersection(SintomiUnici, Tutti, Trovati),\n"
        "    subtract(Tutti, Trovati, Mancanti)."
    )
    story.append(code_block(explain_code, s))
    story.append(Paragraph("Listato 4 — Regola spiega_diagnosi/4 estratta da diagnosi_medica.pl.",
                           s['Caption']))

    story.append(Paragraph(
        "La facility di spiegazione restituisce due liste: i <b>sintomi trovati</b>, cioè quelli "
        "del paziente che sono effettivamente associati alla malattia M, e i <b>sintomi mancanti</b>, "
        "cioè quelli associati a M che il paziente non ha riportato. Questa rappresentazione è "
        "quella consumata direttamente dalla GUI per il pannello \"Dettagli\", che mostra "
        "esplicitamente sia il match sia ciò che resta inspiegato — un elemento di trasparenza "
        "diagnostica.", s['BodyJ']))

    story.append(Paragraph("5.5 Esempio Passo-Passo di Inferenza", s['SectionH2']))
    story.append(Paragraph(
        "Si consideri un paziente che presenta i seguenti tre sintomi: <b>febbre_alta</b>, "
        "<b>tosse_secca</b>, <b>stanchezza</b>. Il sistema esegue la regola <i>diagnosi/3</i> "
        "per ciascuna malattia della KB e produce l'output ordinato che segue (valori ottenuti "
        "eseguendo davvero la query <i>diagnosi_ordinate/2</i> sul codice).", s['BodyJ']))

    step_headers = ['Malattia', 'N° sintomi totali', 'Sintomi corrispondenti', 'ICS']
    step_rows = [
        ['Influenza',  '7', '3 (febbre_alta, tosse_secca, stanchezza)', '43%'],
        ['COVID-19',   '8', '3 (febbre_alta, tosse_secca, stanchezza)', '38%'],
        ['Polmonite',  '8', '2 (febbre_alta, stanchezza)', '25%'],
        ['Meningite',  '8', '2 (febbre_alta, stanchezza)', '25%'],
        ['Tachicardia',          '6', '1 (stanchezza)', '17%'],
        ['Reflusso gastroesofageo','6','1 (tosse_secca)', '17%'],
        ['Bronchite',  '7', '1 (stanchezza)', '14%'],
        ['…',          '…', '…', '…'],
    ]
    story.append(make_table(step_headers, step_rows, [3.8*cm, 2.6*cm, 7.6*cm, 1.6*cm]))
    story.append(Paragraph(
        "Tabella 5 — Output reale di diagnosi_ordinate/2 per il quadro sintomatologico "
        "{febbre_alta, tosse_secca, stanchezza}. Sono mostrate le 7 diagnosi a copertura più alta; "
        "il sistema restituisce in totale 14 candidate.", s['Caption']))

    story.append(Paragraph(
        "Il risultato finale presentato all'utente è <b>Influenza (43%)</b> come diagnosi più "
        "probabile, seguita da COVID-19 e dalle altre diagnosi a copertura inferiore. Il sistema "
        "fornisce inoltre, per ogni diagnosi cliccata, l'elenco dei sintomi <i>trovati</i> e "
        "<i>mancanti</i> tramite la facility di spiegazione (<i>spiega_diagnosi/4</i>).", s['BodyJ']))

    story.append(hr())


# --- Sezione 6: Interfaccia grafica ---
def build_section_6(story, s):
    story.append(Paragraph("6. Interfaccia Grafica (Python / Tkinter)", s['SectionH1']))
    story.append(Spacer(1, 0.25 * cm))

    story.append(Paragraph("6.1 Filosofia di Design", s['SectionH2']))
    story.append(Paragraph(
        "L'interfaccia grafica di MedExpert AI è stata progettata seguendo una filosofia di "
        "<b>dark medical theme</b>, ispirata alle interfacce professionali dei software medici. "
        "La scelta di un tema scuro è motivata da considerazioni di usabilità: riduce l'affaticamento "
        "visivo durante sessioni prolungate e conferisce un aspetto professionale al sistema.", s['BodyJ']))

    story.append(Paragraph(
        "La palette cromatica è basata su tonalità di blu scuro e accenti ciano, con testi chiari "
        "su sfondo scuro. I colori principali utilizzati sono:", s['BodyJ']))

    color_headers = ['Elemento', 'Colore', 'Codice Hex', 'Utilizzo']
    color_rows = [
        ['Sfondo principale', 'Blu molto scuro', '#0a0e17', 'Background della finestra'],
        ['Pannelli', 'Blu scuro', '#111827', 'Sfondo dei pannelli laterali'],
        ['Accento primario', 'Ciano', '#00d4ff', 'Bordi, titoli, elementi attivi'],
        ['Accento secondario', 'Ciano chiaro', '#00e5ff', 'Hover, selezioni'],
        ['Testo primario', 'Bianco', '#ffffff', 'Titoli e testi principali'],
        ['Testo secondario', 'Grigio chiaro', '#94a3b8', 'Testi descrittivi'],
        ['Successo', 'Verde', '#00ff88', 'Certezza alta, conferme'],
        ['Attenzione', 'Giallo', '#ffaa00', 'Certezza media, avvisi'],
    ]
    story.append(make_table(color_headers, color_rows, [3.2*cm, 3*cm, 2.5*cm, 7.3*cm]))
    story.append(Paragraph("Tabella 6 — Palette cromatica dell'interfaccia.", s['Caption']))

    story.append(Paragraph("6.2 Layout a Tre Pannelli", s['SectionH2']))
    story.append(Paragraph(
        "L'interfaccia è organizzata in un layout a <b>tre pannelli</b> affiancati, ciascuno "
        "con una funzione specifica:", s['BodyJ']))

    layout_text = (
        "┌──────────────┬──────────────────┬──────────────────┐\n"
        "│              │                  │                  │\n"
        "│   PANNELLO   │    PANNELLO      │    PANNELLO      │\n"
        "│   SINISTRO   │    CENTRALE      │    DESTRO        │\n"
        "│              │                  │                  │\n"
        "│  Selezione   │   Risultati      │   Dettaglio      │\n"
        "│  Sintomi     │   Diagnosi       │   Malattia       │\n"
        "│              │                  │                  │\n"
        "│  □ Febbre    │  ┌────────────┐  │  Nome: ...       │\n"
        "│  □ Tosse     │  │ Influenza  │  │  Categoria: ...  │\n"
        "│  □ Mal di    │  │   66.7%    │  │  Descrizione:    │\n"
        "│    testa     │  └────────────┘  │  ...             │\n"
        "│  □ Dolori    │  ┌────────────┐  │  Trattamento:    │\n"
        "│    muscolari │  │ COVID-19   │  │  ...             │\n"
        "│  ...         │  │   37.5%    │  │                  │\n"
        "│              │  └────────────┘  │  Sintomi Match:  │\n"
        "│  [Diagnosi]  │                  │  • febbre        │\n"
        "│  [Reset]     │                  │  • tosse         │\n"
        "│              │                  │  • ...           │\n"
        "└──────────────┴──────────────────┴──────────────────┘"
    )
    story.append(code_block(layout_text, s))
    story.append(Paragraph("Figura 2 — Layout a tre pannelli dell'interfaccia grafica.", s['Caption']))

    story.append(Paragraph(
        "<b>Pannello sinistro</b> — Contiene la lista completa dei sintomi disponibili, ciascuno "
        "con una checkbox per la selezione. I sintomi sono presentati con nomi leggibili (con "
        "spazi al posto degli underscore). Include i pulsanti «Esegui Diagnosi» e «Reset».", s['BodyBullet']))
    story.append(Paragraph(
        "<b>Pannello centrale</b> — Mostra i risultati della diagnosi sotto forma di «card» "
        "interattive. Ogni card visualizza il nome della malattia, la categoria e il fattore di "
        "certezza con una barra di progresso colorata (verde per CF ≥ 70%, giallo per CF ≥ 40%, "
        "rosso per CF &lt; 40%).", s['BodyBullet']))
    story.append(Paragraph(
        "<b>Pannello destro</b> — Visualizza i dettagli completi della malattia selezionata, "
        "includendo descrizione, trattamento raccomandato, elenco dei sintomi corrispondenti e "
        "la spiegazione del ragionamento diagnostico.", s['BodyBullet']))

    story.append(Paragraph("6.3 Flusso di Interazione", s['SectionH2']))
    story.append(Paragraph(
        "Il flusso di interazione dell'utente con il sistema segue un percorso lineare e intuitivo:", s['BodyJ']))
    story.append(Paragraph(
        "<b>1.</b> L'utente avvia l'applicazione eseguendo <font face='Courier'>python3 interfaccia.py</font>.", s['BodyBullet']))
    story.append(Paragraph(
        "<b>2.</b> Nel pannello sinistro, seleziona i sintomi presenti spuntando le checkbox corrispondenti.", s['BodyBullet']))
    story.append(Paragraph(
        "<b>3.</b> Clicca il pulsante «Esegui Diagnosi» per avviare l'analisi.", s['BodyBullet']))
    story.append(Paragraph(
        "<b>4.</b> Il sistema invia la query a Prolog via subprocess e riceve i risultati.", s['BodyBullet']))
    story.append(Paragraph(
        "<b>5.</b> Le diagnosi appaiono nel pannello centrale come card cliccabili.", s['BodyBullet']))
    story.append(Paragraph(
        "<b>6.</b> Cliccando su una card, il pannello destro mostra i dettagli completi.", s['BodyBullet']))
    story.append(Paragraph(
        "<b>7.</b> L'utente può premere «Reset» per cancellare tutto e ricominciare.", s['BodyBullet']))

    story.append(Paragraph("6.4 Architettura del Codice Python", s['SectionH2']))
    story.append(Paragraph(
        "Il codice in <font face='Courier'>interfaccia.py</font> è organizzato attorno a due "
        "classi: <b>MedExpertApp</b>, che costruisce la finestra Tkinter e ne gestisce eventi e "
        "stato, e <b>PrologEngine</b>, che fa da ponte verso <font face='Courier'>swipl</font>. "
        "I metodi principali di <b>MedExpertApp</b> sono:", s['BodyJ']))

    method_headers = ['Metodo', 'Descrizione']
    method_rows = [
        ['__init__()',
         "Inizializza finestra, font, palette, stato dell'app e istanzia PrologEngine."],
        ['_build_header() / _build_body() /\n_build_footer()',
         'Costruzione dei tre blocchi principali della UI.'],
        ['_build_left_panel()',
         'Pannello sinistro con le checkbox dei sintomi raggruppate per categoria.'],
        ['_build_center_panel()',
         'Area centrale che ospita le card delle diagnosi.'],
        ['_build_right_panel()',
         'Pannello destro dei dettagli della malattia selezionata.'],
        ['_on_analyze()',
         'Lancia la diagnosi in un thread separato per non bloccare la UI.'],
        ['_on_analysis_done(results)',
         'Callback che aggiorna la UI con i risultati.'],
        ['_on_card_click(malattia)',
         'Click su una card: richiede a Prolog la spiegazione e popola il pannello destro.'],
        ['_on_reset()',
         'Resetta checkbox e pannelli.'],
        ['_toggle_fullscreen() /\n_exit_fullscreen()',
         'Gestione fullscreen (F11 / Esc).'],
    ]
    story.append(make_table(method_headers, method_rows, [5.5*cm, 11*cm]))
    story.append(Paragraph("Tabella 7 — Metodi principali di MedExpertApp.", s['Caption']))

    story.append(Spacer(1, 0.2 * cm))
    aux_headers = ['Classe', 'Descrizione']
    aux_rows = [
        ['PrologEngine',
         "Ponte verso swipl: avvia il processo via subprocess, esegue query_diagnosi e "
         "query_spiega sul file diagnosi_medica.pl, fa il parsing dell'output testuale."],
    ]
    story.append(make_table(aux_headers, aux_rows, [3.5*cm, 13*cm]))
    story.append(Paragraph("Tabella 7b — Classe ausiliaria di interfaccia.py.", s['Caption']))

    story.append(hr())


# --- Sezione 7: Test e validazione ---
def build_section_7(story, s):
    story.append(PageBreak())
    story.append(Paragraph("7. Test e Validazione", s['SectionH1']))
    story.append(Spacer(1, 0.25 * cm))

    story.append(Paragraph("7.1 Suite di Test", s['SectionH2']))
    story.append(Paragraph(
        "MedExpert AI include una suite di test automatizzati scritta direttamente in Prolog, "
        "integrata nel file della Knowledge Base. I test verificano la correttezza del motore "
        "inferenziale per diverse combinazioni di sintomi e per i casi limite (input duplicato, "
        "sintomi inesistenti, ordinamento dei risultati).", s['BodyJ']))

    story.append(Paragraph(
        "Per eseguire la suite di test si usa il seguente comando:", s['BodyJ']))

    story.append(code_block(
        "swipl -g \"test_diagnosi, halt\" diagnosi_medica.pl", s))

    story.append(Paragraph("7.2 Casi di Test", s['SectionH2']))
    story.append(Paragraph(
        "Di seguito i 7 test reali presenti nella KB con lo scopo di ciascuno e l'esito atteso. "
        "Tutti i valori numerici sono stati verificati eseguendo la suite sul codice reale.",
        s['BodyJ']))

    test_headers = ['#', 'Nome', 'Scopo', 'Esito atteso']
    test_rows = [
        ['1', 'Corrispondenza esatta',
         "Tutti e 7 i sintomi dell'influenza in input",
         'ICS(influenza) = 100%'],
        ['2', 'Corrispondenza parziale',
         '3 sintomi su 7 dell\'influenza',
         'ICS(influenza) = round(3/7·100) = 43%'],
        ['3', 'Diagnosi multiple',
         'Sintomi condivisi: febbre_alta, mal_di_testa, stanchezza',
         '≥ 2 diagnosi restituite'],
        ['4', 'Nessuna corrispondenza',
         'Sintomi inventati / non presenti nella KB',
         '0 diagnosi'],
        ['5', 'Gestione duplicati',
         'Stesso sintomo ripetuto nell\'input',
         'Stessa ICS della versione senza duplicati'],
        ['6', 'Spiegazione diagnosi',
         'spiega_diagnosi/4 con 2 sintomi dell\'influenza',
         '2 trovati, 5 mancanti'],
        ['7', 'Ordinamento risultati',
         'diagnosi_ordinate/2 con 4 sintomi misti',
         'Lista ordinata per ICS decrescente'],
    ]
    story.append(make_table(test_headers, test_rows,
                            [0.8*cm, 3.2*cm, 6.5*cm, 5.5*cm]))
    story.append(Paragraph("Tabella 8 — Suite di test (test_1 … test_7).", s['Caption']))

    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("7.3 Codice di Test in Prolog", s['SectionH2']))
    story.append(Spacer(1, 0.15 * cm))

    test_code = (
        "%% Test runner principale.\n"
        "test_diagnosi :-\n"
        "    format('  SUITE DI TEST - SISTEMA DIAGNOSTICO~n'),\n"
        "    test_1(R1), test_2(R2), test_3(R3),\n"
        "    test_4(R4), test_5(R5), test_6(R6), test_7(R7),\n"
        "    somma_risultati([R1,R2,R3,R4,R5,R6,R7], Sup, Tot),\n"
        "    Fail is Tot - Sup,\n"
        "    format('  RIEPILOGO: ~w/~w superati, ~w falliti~n',\n"
        "           [Sup, Tot, Fail]).\n"
        "\n"
        "%% Esempio: test_2 verifica la corrispondenza parziale.\n"
        "%% Influenza ha 7 sintomi, ne passiamo 3 -> ICS attesa = 43%.\n"
        "test_2(Risultato) :-\n"
        "    SintomiPaziente = [febbre_alta, tosse_secca, stanchezza],\n"
        "    diagnosi(SintomiPaziente, influenza, Certezza),\n"
        "    CertezzaAttesa is round((3 / 7) * 100),\n"
        "    (   Certezza =:= CertezzaAttesa\n"
        "    ->  Risultato = 1\n"
        "    ;   Risultato = 0\n"
        "    )."
    )
    story.append(code_block(test_code, s))
    story.append(Paragraph("Listato 5 — Estratto della suite di test in Prolog.", s['Caption']))

    story.append(Paragraph("7.4 Risultati della Validazione", s['SectionH2']))
    story.append(Paragraph(
        "Tutti i 7 test case sono stati eseguiti con successo (output reale: "
        "<font face='Courier'>RIEPILOGO: 7/7 superati, 0 falliti</font>). Il sistema produce "
        "diagnosi con valori di ICS coerenti con la sovrapposizione tra sintomi del paziente e "
        "sintomi delle malattie. La suite serve anche come <b>regression testing</b>: a ogni "
        "modifica della KB i test verificano che le diagnosi precedentemente corrette non siano "
        "state compromesse. Il predicato <i>somma_risultati/3</i> produce un riepilogo finale "
        "<i>superati / totale</i>.", s['BodyJ']))

    story.append(hr())


# --- Sezione 8: Conclusioni e sviluppi futuri ---
def build_section_8(story, s):
    story.append(Paragraph("8. Conclusioni e Sviluppi Futuri", s['SectionH1']))
    story.append(Spacer(1, 0.25 * cm))

    story.append(Paragraph("8.1 Riepilogo dei Risultati", s['SectionH2']))
    story.append(Paragraph(
        "Il progetto MedExpert AI ha dimostrato con successo la fattibilità e l'efficacia di un "
        "sistema esperto per la diagnosi medica, implementato combinando la potenza della "
        "programmazione logica in Prolog con l'accessibilità di un'interfaccia grafica Python. "
        "I principali risultati ottenuti sono:", s['BodyJ']))

    story.append(Paragraph(
        "• <b>Knowledge Base completa</b> — È stata sviluppata una KB contenente 17 patologie "
        "distribuite su 10 categorie mediche, con 44 sintomi distinti, descrizioni dettagliate "
        "e trattamenti raccomandati.", s['BodyBullet']))
    story.append(Paragraph(
        "• <b>Motore inferenziale funzionale</b> — Lo schema goal-driven di Prolog (backward "
        "chaining), combinato con il calcolo dell'<b>Indice di Copertura Sintomatica</b>, produce "
        "una lista di diagnosi candidate ordinate, come confermato dalla suite di test.",
        s['BodyBullet']))
    story.append(Paragraph(
        "• <b>Explanation Facility</b> — Il sistema è in grado di spiegare ogni diagnosi, mostrando "
        "esplicitamente i sintomi <i>trovati</i> e i sintomi <i>mancanti</i> della malattia, "
        "soddisfacendo un requisito fondamentale dei sistemi esperti.", s['BodyBullet']))
    story.append(Paragraph(
        "• <b>Interfaccia utente professionale</b> — La GUI con tema medicale scuro offre "
        "un'esperienza utente intuitiva e visivamente accattivante, rendendo il sistema accessibile "
        "anche a utenti non tecnici.", s['BodyBullet']))
    story.append(Paragraph(
        "• <b>Integrazione multi-paradigma</b> — L'integrazione tra Prolog (paradigma logico) e "
        "Python (paradigma imperativo/OOP) dimostra la complementarità dei diversi approcci alla "
        "programmazione nell'ambito dell'AI.", s['BodyBullet']))

    story.append(Paragraph("8.2 Sviluppi Futuri", s['SectionH2']))
    story.append(Paragraph(
        "Il sistema può essere esteso e migliorato in diverse direzioni:", s['BodyJ']))

    future_headers = ['Area', 'Sviluppo Proposto', 'Impatto']
    future_rows = [
        ['Knowledge Base', 'Espansione a 50+ malattie con\nsintomi più granulari',
         'Maggiore copertura diagnostica'],
        ['Inferenza', 'Introduzione di reti bayesiane\nper gestione incertezza avanzata',
         'Diagnosi più accurate con\ncorrelazioni tra sintomi'],
        ['Inferenza', 'Forward chaining per diagnosi\nproattiva basata su profilo paziente',
         'Rilevamento precoce di\npatologie'],
        ['GUI', 'Interfaccia web con Flask/Django\nper accesso remoto',
         'Accessibilità da qualsiasi\ndispositivo'],
        ['GUI', 'Visualizzazione grafica delle\nrelazioni sintomo-malattia',
         'Migliore comprensione del\nragionamento'],
        ['Dati', 'Integrazione con database medici\n(ICD-10, SNOMED CT)',
         'Standard clinici e\ninteroperabilità'],
        ['AI ibrida', 'Combinazione con ML per\napprendimento da casi clinici',
         'Miglioramento continuo\ndella KB'],
        ['NLP', 'Input in linguaggio naturale\nper descrizione sintomi',
         'Interazione più naturale\ncon l\'utente'],
    ]
    story.append(make_table(future_headers, future_rows, [2.5*cm, 5.5*cm, 5*cm]))
    story.append(Paragraph("Tabella 9 — Possibili sviluppi futuri del sistema.", s['Caption']))

    story.append(Paragraph("8.3 Connessione ai Temi del Corso", s['SectionH2']))
    story.append(Paragraph(
        "In conclusione, MedExpert AI rappresenta un'applicazione concreta dei concetti dei "
        "<b>capitoli 7-10 del libro Gallucci</b>: rappresentazione della conoscenza in una KB "
        "come insieme di sentence (cap. 7), inferenza nella logica del primo ordine con "
        "<i>forward</i> e <i>backward chaining</i> (cap. 9.4), e Prolog come linguaggio basato su "
        "clausole di Horn con motore inferenziale goal-driven (cap. 10). Il progetto realizza "
        "esattamente l'architettura del sistema formale descritta nel libro: KB + esperto di "
        "dominio (l'autore in veste di knowledge engineer medico) + motore inferenziale "
        "(SWI-Prolog).", s['BodyJ']))

    story.append(Paragraph(
        "Il sistema dimostra che l'AI simbolica, nonostante l'attuale predominanza degli approcci "
        "basati su apprendimento automatico, mantiene un ruolo fondamentale in applicazioni dove "
        "la spiegabilità, la trasparenza e il determinismo sono requisiti imprescindibili — come "
        "nel caso della diagnosi medica. La combinazione di Prolog per il ragionamento logico e "
        "Python per l'interfaccia utente rappresenta un esempio efficace di come diversi paradigmi "
        "di programmazione possano essere integrati per realizzare sistemi AI completi e funzionali.", s['BodyJ']))

    story.append(Spacer(1, 0.3 * cm))
    story.append(hr())
    story.append(Spacer(1, 0.2 * cm))

    # Frase di chiusura + firma.
    story.append(Paragraph(
        "<i>«L'intelligenza artificiale non è un sostituto dell'intelligenza umana, "
        "ma uno strumento per amplificarla.»</i>",
        ParagraphStyle('Quote', parent=s['BodyJ'], alignment=TA_CENTER,
                       fontSize=11, textColor=ACCENT_BLUE, fontName='Helvetica-Oblique',
                       spaceBefore=10, spaceAfter=10)
    ))

    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(
        "Napoli, Maggio 2026",
        ParagraphStyle('Closing', parent=s['BodyJ'], alignment=TA_CENTER,
                       fontSize=11, textColor=MUTED_TEXT)
    ))
    story.append(Paragraph(
        "<b>Luciano Meccariello</b>",
        ParagraphStyle('Author', parent=s['BodyJ'], alignment=TA_CENTER,
                       fontSize=12, textColor=DARK_BLUE, fontName='Helvetica-Bold')
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
        author="Luciano Meccariello",
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
