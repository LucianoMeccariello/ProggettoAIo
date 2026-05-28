#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generatore PDF - Documentazione Accademica MedExpert AI
Università degli Studi di Napoli Parthenope
Corso: Elementi di Intelligenza Artificiale
Prof. Giancarlo Sperlì
Studente: Luciano Meccariello
A.A. 2025/2026
"""

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

# ─────────────────────────── COLORI ───────────────────────────
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


# ─────────────────────── STILI PERSONALIZZATI ─────────────────
def build_styles():
    """Costruisce l'insieme completo di stili per il documento."""
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

    # Titoli sezione
    styles.add(ParagraphStyle(
        name='SectionH1',
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=white,
        alignment=TA_LEFT,
        leading=24,
        spaceBefore=18,
        spaceAfter=10,
        leftIndent=0,
        backColor=DARK_BLUE,
        borderPadding=(8, 10, 8, 10),
    ))
    styles.add(ParagraphStyle(
        name='SectionH2',
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=DARK_BLUE,
        alignment=TA_LEFT,
        leading=20,
        spaceBefore=14,
        spaceAfter=6,
        borderWidth=0,
        borderColor=ACCENT_BLUE,
        borderPadding=(0, 0, 2, 0),
    ))
    styles.add(ParagraphStyle(
        name='SectionH3',
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=ACCENT_BLUE,
        alignment=TA_LEFT,
        leading=16,
        spaceBefore=10,
        spaceAfter=4,
    ))

    # Corpo testo
    styles.add(ParagraphStyle(
        name='BodyJ',
        fontName='Helvetica',
        fontSize=10.5,
        textColor=DARK_TEXT,
        alignment=TA_JUSTIFY,
        leading=15,
        spaceBefore=2,
        spaceAfter=6,
        firstLineIndent=0,
    ))
    styles.add(ParagraphStyle(
        name='BodyBullet',
        fontName='Helvetica',
        fontSize=10.5,
        textColor=DARK_TEXT,
        alignment=TA_LEFT,
        leading=15,
        spaceBefore=1,
        spaceAfter=3,
        leftIndent=18,
        bulletIndent=6,
    ))

    # Codice
    styles.add(ParagraphStyle(
        name='CodeBlock',
        fontName='Courier',
        fontSize=8.5,
        textColor=DARK_TEXT,
        alignment=TA_LEFT,
        leading=12,
        spaceBefore=4,
        spaceAfter=4,
        leftIndent=8,
        rightIndent=8,
        backColor=CODE_BG,
        borderPadding=(6, 8, 6, 8),
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

    # Didascalie / Note
    styles.add(ParagraphStyle(
        name='Caption',
        fontName='Helvetica-Oblique',
        fontSize=9,
        textColor=MUTED_TEXT,
        alignment=TA_CENTER,
        leading=13,
        spaceBefore=2,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name='Note',
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        textColor=MUTED_TEXT,
        alignment=TA_JUSTIFY,
        leading=13,
        spaceBefore=4,
        spaceAfter=6,
        leftIndent=12,
        rightIndent=12,
    ))

    # Indice
    styles.add(ParagraphStyle(
        name='TOCEntry',
        fontName='Helvetica',
        fontSize=12,
        textColor=DARK_TEXT,
        alignment=TA_LEFT,
        leading=22,
        spaceBefore=3,
        spaceAfter=3,
        leftIndent=10,
    ))
    styles.add(ParagraphStyle(
        name='TOCTitle',
        fontName='Helvetica-Bold',
        fontSize=22,
        textColor=DARK_BLUE,
        alignment=TA_CENTER,
        leading=28,
        spaceBefore=20,
        spaceAfter=20,
    ))

    return styles


# ────────────────────── UTILITÀ ──────────────────────
def hr():
    """Linea orizzontale decorativa."""
    return HRFlowable(
        width="100%", thickness=1, color=ACCENT_BLUE,
        spaceBefore=8, spaceAfter=8
    )

def thin_hr():
    return HRFlowable(
        width="100%", thickness=0.5, color=LIGHT_BLUE,
        spaceBefore=4, spaceAfter=4
    )

def make_table(headers, rows, col_widths=None):
    """Crea una tabella con stile professionale e righe alternate."""
    data = [headers] + rows
    if col_widths is None:
        col_widths = [None] * len(headers)

    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        # Intestazione
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEAD),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        # Corpo
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        # Griglia
        ('GRID', (0, 0), (-1, -1), 0.4, ACCENT_BLUE),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ]
    # Righe alternate
    for i in range(1, len(data)):
        bg = ROW_EVEN if i % 2 == 0 else ROW_ODD
        style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))

    t.setStyle(TableStyle(style_cmds))
    return t


def code_block(text, styles):
    """Blocco di codice preformattato."""
    # Escaping XML chars
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return Paragraph(text.replace('\n', '<br/>'), styles['CodeBlock'])


# ──────────────────── HEADER / FOOTER ────────────────────
def header_footer(canvas, doc):
    """Disegna intestazione e piè di pagina su ogni pagina (tranne la prima)."""
    canvas.saveState()
    page_num = doc.page

    if page_num > 1:
        # Intestazione
        canvas.setFillColor(DARK_BLUE)
        canvas.rect(0, PAGE_H - 22 * mm, PAGE_W, 22 * mm, fill=1, stroke=0)
        canvas.setFillColor(white)
        canvas.setFont('Helvetica', 8)
        canvas.drawString(2 * cm, PAGE_H - 14 * mm,
                          "MedExpert AI — Sistema Esperto di Diagnosi Medica")
        canvas.drawRightString(PAGE_W - 2 * cm, PAGE_H - 14 * mm,
                               "Università degli Studi di Napoli Parthenope")

        # Piè di pagina
        canvas.setFillColor(LIGHT_BLUE)
        canvas.rect(0, 0, PAGE_W, 12 * mm, fill=1, stroke=0)
        canvas.setFillColor(DARK_BLUE)
        canvas.setFont('Helvetica', 8)
        canvas.drawString(2 * cm, 4.5 * mm,
                          "Elementi di Intelligenza Artificiale — A.A. 2025/2026")
        canvas.drawRightString(PAGE_W - 2 * cm, 4.5 * mm,
                               f"Pagina {page_num}")
    canvas.restoreState()


# ════════════════════ PAGINA DI COPERTINA ════════════════════
def build_cover(story, styles):
    story.append(Spacer(1, 1.5 * cm))

    # Banner blu scuro
    banner_data = [[
        Paragraph("UNIVERSITÀ DEGLI STUDI DI NAPOLI PARTHENOPE",
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

    # Sotto-banner corso
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

    # Titolo progetto
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

    # Info autore / relatore
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

    # Anno accademico
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


# ════════════════════ INDICE ════════════════════
def build_toc(story, styles):
    story.append(Paragraph("Indice", styles['TOCTitle']))
    story.append(hr())
    story.append(Spacer(1, 0.4 * cm))

    sections = [
        ("1", "Introduzione ai Sistemi Esperti"),
        ("2", "Obiettivo del Progetto"),
        ("3", "Il Dominio: Diagnosi Medica"),
        ("4", "Architettura del Sistema"),
        ("5", "Knowledge Base in Prolog"),
        ("6", "Regole di Inferenza"),
        ("7", "Interfaccia Grafica (Python / Tkinter)"),
        ("8", "Test e Validazione"),
        ("9", "Confronto con Approcci Alternativi"),
        ("10", "Conclusioni e Sviluppi Futuri"),
    ]

    for num, title in sections:
        entry = Paragraph(
            f'<b>{num}.</b>&nbsp;&nbsp;&nbsp;{title}',
            styles['TOCEntry']
        )
        story.append(entry)
        story.append(thin_hr())

    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(
        "<i>Documento generato automaticamente — Maggio 2026</i>",
        styles['Caption']
    ))
    story.append(PageBreak())


# ════════════════════ SEZIONE 1 ════════════════════
def build_section_1(story, s):
    story.append(Paragraph("1. Introduzione ai Sistemi Esperti", s['SectionH1']))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("1.1 Che cos'è un Sistema Esperto?", s['SectionH2']))
    story.append(Paragraph(
        "Un <b>sistema esperto</b> (in inglese <i>Expert System</i>) è un programma informatico "
        "che emula il processo decisionale di un esperto umano in uno specifico dominio di conoscenza. "
        "Nato nell'ambito dell'Intelligenza Artificiale simbolica negli anni '70, il sistema esperto "
        "rappresenta uno dei paradigmi più consolidati dell'AI classica. A differenza degli approcci "
        "basati su apprendimento automatico, un sistema esperto opera su una <b>base di conoscenza</b> "
        "(<i>Knowledge Base</i>) esplicita, codificata sotto forma di regole e fatti, e utilizza un "
        "<b>motore inferenziale</b> (<i>Inference Engine</i>) per derivare nuove conclusioni a partire "
        "dai dati forniti dall'utente.", s['BodyJ']))

    story.append(Paragraph(
        "L'architettura classica di un sistema esperto si compone di tre elementi fondamentali:", s['BodyJ']))

    components = [
        ("<b>Knowledge Base (KB)</b> — La base di conoscenza contiene l'insieme dei fatti e delle "
         "regole che codificano l'esperienza del dominio. Nel nostro caso, la KB include informazioni "
         "su malattie, sintomi, trattamenti e relazioni diagnostiche, tutte espresse in logica Prolog."),
        ("<b>Inference Engine</b> — Il motore inferenziale è il cuore computazionale del sistema. "
         "Applica le regole della KB ai fatti disponibili per derivare conclusioni. Può operare in "
         "modalità <i>forward chaining</i> (dai fatti alle conclusioni) o <i>backward chaining</i> "
         "(dalle ipotesi ai fatti di supporto). MedExpert AI utilizza il backward chaining di Prolog."),
        ("<b>User Interface</b> — L'interfaccia utente permette l'interazione con il sistema. "
         "Nel nostro progetto, questa è implementata tramite una GUI Python con Tkinter, che offre "
         "un'esperienza intuitiva per la selezione dei sintomi e la visualizzazione delle diagnosi."),
    ]
    for comp in components:
        story.append(Paragraph(f"• {comp}", s['BodyBullet']))

    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph("1.2 Contesto Storico", s['SectionH2']))
    story.append(Paragraph(
        "I sistemi esperti hanno una storia ricca e affascinante nell'ambito dell'Intelligenza Artificiale. "
        "Tra i primi e più celebri esempi troviamo:", s['BodyJ']))
    story.append(Paragraph(
        "• <b>DENDRAL</b> (1965) — Sviluppato a Stanford da Edward Feigenbaum e Joshua Lederberg, "
        "è considerato il primo sistema esperto in assoluto. Analizzava dati di spettrometria di massa "
        "per determinare la struttura molecolare di composti chimici sconosciuti.", s['BodyBullet']))
    story.append(Paragraph(
        "• <b>MYCIN</b> (1972) — Sviluppato anch'esso a Stanford, MYCIN è il sistema esperto più "
        "influente nel campo medico. Diagnosticava infezioni batteriche del sangue e raccomandava "
        "antibiotici appropriati. Introduceva il concetto di <b>fattori di certezza</b> (certainty factors), "
        "un approccio alla gestione dell'incertezza che abbiamo adottato anche in MedExpert AI.", s['BodyBullet']))
    story.append(Paragraph(
        "• <b>XCON/R1</b> (1980) — Utilizzato da Digital Equipment Corporation per configurare "
        "ordini di computer VAX. È stato uno dei primi sistemi esperti con successo commerciale, "
        "dimostrando il valore pratico di questa tecnologia.", s['BodyBullet']))

    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph("1.3 Rilevanza per il Corso", s['SectionH2']))
    story.append(Paragraph(
        "Il progetto MedExpert AI si inserisce pienamente nel programma del corso di <i>Elementi di "
        "Intelligenza Artificiale</i> del Prof. Sperlì, toccando temi fondamentali quali: la rappresentazione "
        "della conoscenza tramite logica del primo ordine, il ragionamento automatico con backward chaining, "
        "la gestione dell'incertezza tramite fattori di certezza, e la progettazione di sistemi intelligenti "
        "con capacità di spiegazione (<i>explanation facility</i>). Il sistema dimostra concretamente come "
        "i concetti teorici dell'AI simbolica possano essere applicati a problemi reali.", s['BodyJ']))

    story.append(hr())


# ════════════════════ SEZIONE 2 ════════════════════
def build_section_2(story, s):
    story.append(Paragraph("2. Obiettivo del Progetto", s['SectionH1']))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph(
        "L'obiettivo principale di questo progetto è la realizzazione di un <b>sistema esperto completo "
        "per la diagnosi medica</b>, che integri una base di conoscenza in Prolog con un'interfaccia "
        "grafica moderna in Python. Il sistema è progettato per dimostrare i concetti fondamentali "
        "dei sistemi esperti in un contesto applicativo realistico e didatticamente significativo.", s['BodyJ']))

    story.append(Paragraph("2.1 Obiettivi Specifici", s['SectionH2']))

    objectives = [
        "Progettare e implementare una <b>Knowledge Base</b> in Prolog contenente oltre 15 patologie "
        "mediche con i rispettivi sintomi, categorie, descrizioni e trattamenti.",
        "Implementare un <b>motore inferenziale</b> basato su backward chaining che calcoli diagnosi "
        "con fattori di certezza, ordinando i risultati per probabilità decrescente.",
        "Realizzare un meccanismo di <b>spiegazione</b> (<i>explanation facility</i>) che giustifichi "
        "ogni diagnosi mostrando quali sintomi corrispondono e il calcolo del fattore di certezza.",
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
    story.append(Paragraph("2.2 Requisiti del Sistema", s['SectionH2']))
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


# ════════════════════ SEZIONE 3 ════════════════════
def build_section_3(story, s):
    story.append(Paragraph("3. Il Dominio: Diagnosi Medica", s['SectionH1']))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("3.1 Perché la Diagnosi Medica?", s['SectionH2']))
    story.append(Paragraph(
        "La diagnosi medica rappresenta un dominio ideale per l'applicazione dei sistemi esperti "
        "per diverse ragioni fondamentali. In primo luogo, il processo diagnostico è intrinsecamente "
        "<b>basato su regole</b>: i medici utilizzano la propria esperienza e conoscenza per "
        "correlare insiemi di sintomi a possibili patologie, seguendo un ragionamento logico che "
        "può essere formalizzato in regole del tipo «se il paziente presenta i sintomi X, Y e Z, "
        "allora la diagnosi probabile è W con certezza C%».", s['BodyJ']))

    story.append(Paragraph(
        "In secondo luogo, la diagnosi medica richiede la gestione dell'<b>incertezza</b>: raramente "
        "un paziente presenta tutti i sintomi caratteristici di una patologia, e spesso gli stessi "
        "sintomi possono essere associati a malattie diverse. Questa caratteristica rende il dominio "
        "particolarmente adatto a dimostrare l'uso dei fattori di certezza.", s['BodyJ']))

    story.append(Paragraph(
        "Infine, la diagnosi medica richiede una <b>capacità di spiegazione</b>: non è sufficiente "
        "che il sistema produca una diagnosi, ma deve essere in grado di giustificarla, mostrando "
        "il ragionamento seguito. Questa trasparenza è fondamentale sia per la fiducia dell'utente "
        "che per scopi didattici.", s['BodyJ']))

    story.append(Paragraph("3.2 Il Processo Diagnostico come Inferenza Logica", s['SectionH2']))
    story.append(Paragraph(
        "Il processo diagnostico può essere modellato come un problema di <b>inferenza logica</b>. "
        "Data una base di conoscenza che associa malattie a sintomi, e dato un insieme di sintomi "
        "osservati nel paziente, il sistema deve inferire le diagnosi più probabili. "
        "Formalmente, per ogni malattia M nella KB:", s['BodyJ']))

    story.append(code_block(
        "diagnosi(M, Sintomi_Paziente, CF) :-\n"
        "    sintomi_malattia(M, Sintomi_M),\n"
        "    intersezione(Sintomi_Paziente, Sintomi_M, Comuni),\n"
        "    CF = |Comuni| / |Sintomi_M| × 100,\n"
        "    CF > 0.", s))

    story.append(Paragraph(
        "Dove CF (Certainty Factor) rappresenta la percentuale di sintomi della malattia M "
        "che sono stati osservati nel paziente. Questo approccio permette di generare diagnosi "
        "multiple con diversi gradi di certezza.", s['BodyJ']))

    story.append(Paragraph("3.3 Patologie Coperte", s['SectionH2']))
    story.append(Paragraph(
        "MedExpert AI copre un ampio spettro di patologie comuni, organizzate in categorie mediche. "
        "Di seguito l'elenco completo delle 16 malattie presenti nella Knowledge Base:", s['BodyJ']))

    disease_headers = ['#', 'Malattia', 'Categoria', 'N° Sintomi']
    disease_rows = [
        ['1', 'Influenza', 'Infettiva', '6'],
        ['2', 'COVID-19', 'Infettiva', '8'],
        ['3', 'Polmonite', 'Respiratoria', '7'],
        ['4', 'Bronchite', 'Respiratoria', '5'],
        ['5', 'Asma', 'Respiratoria', '5'],
        ['6', 'Gastrite', 'Gastrointestinale', '6'],
        ['7', 'Appendicite', 'Gastrointestinale', '5'],
        ['8', 'Ipertensione', 'Cardiovascolare', '6'],
        ['9', 'Infarto Miocardico', 'Cardiovascolare', '6'],
        ['10', 'Diabete Tipo 2', 'Metabolica', '7'],
        ['11', 'Emicrania', 'Neurologica', '5'],
        ['12', 'Meningite', 'Neurologica', '7'],
        ['13', 'Anemia', 'Ematologica', '6'],
        ['14', 'Dermatite', 'Dermatologica', '5'],
        ['15', 'Cistite', 'Urologica', '5'],
        ['16', 'Artrite Reumatoide', 'Reumatologica', '6'],
    ]
    story.append(make_table(disease_headers, disease_rows,
                            [1*cm, 5*cm, 4.5*cm, 2.5*cm]))
    story.append(Paragraph("Tabella 2 — Elenco completo delle patologie nella Knowledge Base.",
                           s['Caption']))
    story.append(hr())


# ════════════════════ SEZIONE 4 ════════════════════
def build_section_4(story, s):
    story.append(Paragraph("4. Architettura del Sistema", s['SectionH1']))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("4.1 Panoramica Architetturale", s['SectionH2']))
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
        "│  backward chaining · certainty factors · sort   │\n"
        "└──────────────────────┬──────────────────────────┘\n"
        "                       │ consult/1\n"
        "┌──────────────────────▼──────────────────────────┐\n"
        "│         KNOWLEDGE BASE (diagnosi_medica.pl)     │\n"
        "│  fatti · regole · test · spiegazioni            │\n"
        "└─────────────────────────────────────────────────┘"
    )
    story.append(code_block(arch_text, s))
    story.append(Paragraph("Figura 1 — Architettura a tre livelli di MedExpert AI.", s['Caption']))

    story.append(Paragraph("4.2 Comunicazione tra Python e Prolog", s['SectionH2']))
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

    story.append(Paragraph("4.3 Struttura dei File", s['SectionH2']))

    file_headers = ['File', 'Linguaggio', 'Ruolo']
    file_rows = [
        ['diagnosi_medica.pl', 'Prolog', 'Knowledge Base + Regole inferenziali + Test'],
        ['gui_diagnosi.py', 'Python', 'Interfaccia grafica Tkinter'],
        ['genera_pdf.py', 'Python', 'Generatore documentazione PDF'],
        ['README.md', 'Markdown', 'Documentazione del progetto'],
    ]
    story.append(make_table(file_headers, file_rows, [4.5*cm, 3*cm, 8.5*cm]))
    story.append(Paragraph("Tabella 3 — Struttura dei file del progetto.", s['Caption']))
    story.append(hr())


# ════════════════════ SEZIONE 5 ════════════════════
def build_section_5(story, s):
    story.append(Paragraph("5. Knowledge Base in Prolog", s['SectionH1']))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("5.1 Struttura dei Fatti", s['SectionH2']))
    story.append(Paragraph(
        "La Knowledge Base è organizzata utilizzando quattro predicati principali, ciascuno dei "
        "quali cattura un aspetto diverso della conoscenza medica:", s['BodyJ']))

    pred_headers = ['Predicato', 'Arità', 'Descrizione', 'Esempio']
    pred_rows = [
        ['sintomo/2', '2', 'Associa malattia a lista sintomi',
         "sintomo(influenza, [febbre, tosse, ...])"],
        ['descrizione/2', '2', 'Descrizione testuale della malattia',
         "descrizione(influenza, 'Infezione virale...')"],
        ['trattamento/2', '2', 'Trattamento raccomandato',
         "trattamento(influenza, 'Riposo...')"],
        ['categoria/2', '2', 'Categoria medica della malattia',
         "categoria(influenza, infettiva)"],
    ]
    story.append(make_table(pred_headers, pred_rows, [2.8*cm, 1.5*cm, 4.5*cm, 7.2*cm]))
    story.append(Paragraph("Tabella 4 — Predicati della Knowledge Base.", s['Caption']))

    story.append(Paragraph("5.2 Esempi di Fatti nella KB", s['SectionH2']))
    story.append(Paragraph(
        "Di seguito sono riportati alcuni esempi rappresentativi dei fatti codificati nella "
        "Knowledge Base Prolog:", s['BodyJ']))

    kb_code = (
        "%% ═══════════════════════════════════════════════\n"
        "%% FATTI: Sintomi per malattia\n"
        "%% ═══════════════════════════════════════════════\n"
        "\n"
        "sintomo(influenza, [febbre, tosse, mal_di_gola,\n"
        "                    dolori_muscolari, mal_di_testa,\n"
        "                    affaticamento]).\n"
        "\n"
        "sintomo(covid19, [febbre, tosse_secca, affaticamento,\n"
        "                  perdita_gusto, perdita_olfatto,\n"
        "                  difficolta_respiratorie,\n"
        "                  dolori_muscolari, mal_di_testa]).\n"
        "\n"
        "sintomo(polmonite, [febbre_alta, tosse_produttiva,\n"
        "                    difficolta_respiratorie,\n"
        "                    dolore_toracico, brividi,\n"
        "                    sudorazione, affaticamento]).\n"
        "\n"
        "sintomo(diabete_tipo2, [sete_eccessiva, minzione_frequente,\n"
        "                       fame_eccessiva, perdita_peso,\n"
        "                       affaticamento, visione_offuscata,\n"
        "                       guarigione_lenta]).\n"
        "\n"
        "%% ═══════════════════════════════════════════════\n"
        "%% FATTI: Categorie\n"
        "%% ═══════════════════════════════════════════════\n"
        "\n"
        "categoria(influenza, infettiva).\n"
        "categoria(covid19, infettiva).\n"
        "categoria(polmonite, respiratoria).\n"
        "categoria(diabete_tipo2, metabolica).\n"
        "\n"
        "%% ═══════════════════════════════════════════════\n"
        "%% FATTI: Descrizioni\n"
        "%% ═══════════════════════════════════════════════\n"
        "\n"
        "descrizione(influenza,\n"
        "  'Infezione virale acuta dell\\'apparato respiratorio\n"
        "   causata dai virus influenzali. Si manifesta con\n"
        "   febbre, dolori muscolari e sintomi respiratori.').\n"
        "\n"
        "descrizione(covid19,\n"
        "  'Malattia infettiva causata dal virus SARS-CoV-2.\n"
        "   Caratterizzata da sintomi respiratori e perdita\n"
        "   di gusto/olfatto.')."
    )
    story.append(code_block(kb_code, s))
    story.append(Paragraph("Listato 1 — Estratto della Knowledge Base in Prolog.", s['Caption']))

    story.append(Paragraph("5.3 Scelte Progettuali della KB", s['SectionH2']))
    story.append(Paragraph(
        "La progettazione della Knowledge Base ha seguito alcuni principi fondamentali:", s['BodyJ']))
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
    story.append(Paragraph(
        "• <b>Estensibilità</b> — Aggiungere una nuova malattia richiede semplicemente l'inserimento "
        "di quattro nuovi fatti nella KB, senza modificare il motore inferenziale.", s['BodyBullet']))

    story.append(hr())


# ════════════════════ SEZIONE 6 ════════════════════
def build_section_6(story, s):
    story.append(Paragraph("6. Regole di Inferenza", s['SectionH1']))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("6.1 Diagnosi con Fattore di Certezza — diagnosi/3", s['SectionH2']))
    story.append(Paragraph(
        "La regola principale del sistema esperto è <b>diagnosi/3</b>, che implementa il backward "
        "chaining con calcolo del fattore di certezza. Per ogni malattia nella KB, la regola "
        "calcola quanti dei sintomi del paziente corrispondono ai sintomi della malattia e ne "
        "deriva un fattore di certezza percentuale.", s['BodyJ']))

    diag_code = (
        "%% diagnosi(+SintomiPaziente, -Malattia, -Certezza)\n"
        "%% Calcola la diagnosi con fattore di certezza\n"
        "diagnosi(SintomiPaziente, Malattia, Certezza) :-\n"
        "    sintomo(Malattia, SintomiMalattia),\n"
        "    intersection(SintomiPaziente, SintomiMalattia, Comuni),\n"
        "    length(Comuni, NumComuni),\n"
        "    NumComuni > 0,\n"
        "    length(SintomiMalattia, TotSintomi),\n"
        "    Certezza is (NumComuni / TotSintomi) * 100."
    )
    story.append(code_block(diag_code, s))
    story.append(Paragraph("Listato 2 — Regola diagnosi/3 con calcolo del fattore di certezza.",
                           s['Caption']))

    story.append(Paragraph("6.2 Formula del Fattore di Certezza", s['SectionH2']))
    story.append(Paragraph(
        "Il <b>Certainty Factor</b> (CF) è calcolato come rapporto tra il numero di sintomi "
        "corrispondenti e il numero totale di sintomi della malattia, moltiplicato per 100:", s['BodyJ']))

    formula_text = (
        "                    |Sintomi_Paziente ∩ Sintomi_Malattia|\n"
        "    CF(M) = ──────────────────────────────────────────── × 100\n"
        "                         |Sintomi_Malattia|"
    )
    story.append(code_block(formula_text, s))
    story.append(Paragraph(
        "Ad esempio, se una malattia ha 6 sintomi e il paziente ne presenta 4, il fattore di "
        "certezza sarà CF = (4/6) × 100 ≈ 66.7%. Questo approccio è ispirato ai fattori di "
        "certezza originariamente introdotti in MYCIN.", s['BodyJ']))

    story.append(Paragraph("6.3 Diagnosi Ordinate — diagnosi_ordinate/2", s['SectionH2']))
    story.append(Paragraph(
        "La regola <b>diagnosi_ordinate/2</b> raccoglie tutte le diagnosi possibili e le ordina "
        "per fattore di certezza decrescente, presentando le diagnosi più probabili per prime:", s['BodyJ']))

    sort_code = (
        "%% diagnosi_ordinate(+Sintomi, -DiagnosiOrdinate)\n"
        "%% Raccoglie e ordina le diagnosi per certezza\n"
        "diagnosi_ordinate(Sintomi, DiagnosiOrdinate) :-\n"
        "    findall(\n"
        "        certezza(CF, Malattia),\n"
        "        diagnosi(Sintomi, Malattia, CF),\n"
        "        Diagnosi\n"
        "    ),\n"
        "    sort(0, @>=, Diagnosi, DiagnosiOrdinate)."
    )
    story.append(code_block(sort_code, s))
    story.append(Paragraph("Listato 3 — Ordinamento delle diagnosi per certezza.", s['Caption']))

    story.append(Paragraph("6.4 Facility di Spiegazione — spiega_diagnosi/4", s['SectionH2']))
    story.append(Paragraph(
        "Una caratteristica fondamentale dei sistemi esperti è la capacità di <b>spiegare</b> il "
        "ragionamento che ha portato a una conclusione. La regola <b>spiega_diagnosi/4</b> genera "
        "una spiegazione dettagliata per ogni diagnosi:", s['BodyJ']))

    explain_code = (
        "%% spiega_diagnosi(+Sintomi, +Malattia, -Comuni, -Certezza)\n"
        "%% Genera la spiegazione della diagnosi\n"
        "spiega_diagnosi(SintomiPaziente, Malattia, SintomiComuni,\n"
        "                Certezza) :-\n"
        "    sintomo(Malattia, SintomiMalattia),\n"
        "    intersection(SintomiPaziente, SintomiMalattia,\n"
        "                 SintomiComuni),\n"
        "    length(SintomiComuni, NumComuni),\n"
        "    NumComuni > 0,\n"
        "    length(SintomiMalattia, TotSintomi),\n"
        "    Certezza is (NumComuni / TotSintomi) * 100."
    )
    story.append(code_block(explain_code, s))
    story.append(Paragraph("Listato 4 — Regola per la spiegazione delle diagnosi.", s['Caption']))

    story.append(Paragraph("6.5 Esempio Passo-Passo di Inferenza", s['SectionH2']))
    story.append(Paragraph(
        "Consideriamo un paziente che presenta i sintomi: <b>febbre</b>, <b>tosse</b>, "
        "<b>mal_di_gola</b> e <b>dolori_muscolari</b>. Il sistema esegue il seguente "
        "ragionamento:", s['BodyJ']))

    step_headers = ['Passo', 'Malattia', 'Sintomi Match', 'Totale', 'CF']
    step_rows = [
        ['1', 'Influenza', '4 (febbre, tosse, mal_di_gola, dolori_muscolari)', '6', '66.7%'],
        ['2', 'COVID-19', '3 (febbre, dolori_muscolari, mal_di_testa*)', '8', '37.5%'],
        ['3', 'Polmonite', '1 (febbre → febbre_alta ≠ febbre)', '7', '0%**'],
        ['4', 'Bronchite', '1 (tosse)', '5', '20.0%'],
    ]
    story.append(make_table(step_headers, step_rows, [1.5*cm, 3*cm, 7*cm, 1.8*cm, 2.2*cm]))
    story.append(Paragraph(
        "Tabella 5 — Esempio di inferenza passo-passo. "
        "(*) Se mal_di_testa non è presente, il match è 2 su 8 = 25%. "
        "(**) Polmonite usa 'febbre_alta' come sintomo distinto da 'febbre'.", s['Caption']))

    story.append(Paragraph(
        "Il risultato finale presentato all'utente sarà: <b>Influenza (66.7%)</b> come diagnosi "
        "principale, seguita da COVID-19 e Bronchite come diagnosi secondarie. Il sistema fornisce "
        "anche la spiegazione dettagliata con i sintomi corrispondenti per ciascuna diagnosi.", s['BodyJ']))

    story.append(hr())


# ════════════════════ SEZIONE 7 ════════════════════
def build_section_7(story, s):
    story.append(Paragraph("7. Interfaccia Grafica (Python / Tkinter)", s['SectionH1']))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("7.1 Filosofia di Design", s['SectionH2']))
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

    story.append(Paragraph("7.2 Layout a Tre Pannelli", s['SectionH2']))
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

    story.append(Paragraph("7.3 Flusso di Interazione", s['SectionH2']))
    story.append(Paragraph(
        "Il flusso di interazione dell'utente con il sistema segue un percorso lineare e intuitivo:", s['BodyJ']))
    story.append(Paragraph(
        "<b>1.</b> L'utente avvia l'applicazione eseguendo <font face='Courier'>python3 gui_diagnosi.py</font>.", s['BodyBullet']))
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

    story.append(Paragraph("7.4 Architettura del Codice Python", s['SectionH2']))
    story.append(Paragraph(
        "Il codice Python è organizzato in una classe principale <b>MedExpertGUI</b> che gestisce "
        "l'intera interfaccia. I metodi principali sono:", s['BodyJ']))

    method_headers = ['Metodo', 'Descrizione']
    method_rows = [
        ['__init__()', 'Inizializzazione della finestra e configurazione del tema'],
        ['create_widgets()', 'Creazione di tutti i widget dell\'interfaccia'],
        ['create_symptom_panel()', 'Costruzione del pannello di selezione sintomi'],
        ['create_results_panel()', 'Costruzione del pannello risultati con card'],
        ['create_detail_panel()', 'Costruzione del pannello dettagli malattia'],
        ['run_diagnosis()', 'Invocazione di Prolog e parsing dei risultati'],
        ['show_diagnosis_card()', 'Rendering di una singola card diagnosi'],
        ['show_detail()', 'Visualizzazione dettagli della malattia selezionata'],
        ['reset()', 'Reset completo dell\'interfaccia'],
    ]
    story.append(make_table(method_headers, method_rows, [4*cm, 12*cm]))
    story.append(Paragraph("Tabella 7 — Metodi principali della classe MedExpertGUI.", s['Caption']))

    story.append(hr())


# ════════════════════ SEZIONE 8 ════════════════════
def build_section_8(story, s):
    story.append(Paragraph("8. Test e Validazione", s['SectionH1']))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("8.1 Suite di Test", s['SectionH2']))
    story.append(Paragraph(
        "MedExpert AI include una suite di test automatizzati scritta direttamente in Prolog, "
        "integrata nel file della Knowledge Base. I test verificano la correttezza delle diagnosi "
        "prodotte dal motore inferenziale per diverse combinazioni di sintomi. Ogni test case "
        "specifica un insieme di sintomi di input, la diagnosi attesa e il fattore di certezza "
        "minimo richiesto.", s['BodyJ']))

    story.append(Paragraph(
        "Per eseguire la suite di test, è sufficiente utilizzare il seguente comando:", s['BodyJ']))

    story.append(code_block(
        "swipl -g \"test_diagnosi, halt\" diagnosi_medica.pl", s))

    story.append(Paragraph("8.2 Casi di Test", s['SectionH2']))
    story.append(Paragraph(
        "Di seguito è riportata la tabella dei principali casi di test con i risultati ottenuti:", s['BodyJ']))

    test_headers = ['#', 'Sintomi Input', 'Diagnosi Attesa', 'CF Atteso', 'Risultato', 'Esito']
    test_rows = [
        ['1',
         'febbre, tosse, mal_di_gola,\ndolori_muscolari, mal_di_testa',
         'Influenza', '83.3%',
         'Influenza (83.3%)', '✓ PASS'],
        ['2',
         'febbre, tosse_secca, perdita_gusto,\nperdita_olfatto, affaticamento',
         'COVID-19', '62.5%',
         'COVID-19 (62.5%)', '✓ PASS'],
        ['3',
         'febbre_alta, tosse_produttiva,\ndifficolta_respiratorie,\ndolore_toracico',
         'Polmonite', '57.1%',
         'Polmonite (57.1%)', '✓ PASS'],
        ['4',
         'dolore_addominale, nausea,\nvomito, bruciore_stomaco',
         'Gastrite', '66.7%',
         'Gastrite (66.7%)', '✓ PASS'],
        ['5',
         'sete_eccessiva, minzione_frequente,\nfame_eccessiva, perdita_peso,\naffaticamento',
         'Diabete Tipo 2', '71.4%',
         'Diabete T2 (71.4%)', '✓ PASS'],
        ['6',
         'mal_di_testa_intenso, nausea,\nsensibilita_luce, sensibilita_rumore',
         'Emicrania', '80.0%',
         'Emicrania (80.0%)', '✓ PASS'],
        ['7',
         'febbre_alta, rigidita_nucale,\nmal_di_testa_intenso, nausea,\nvomito',
         'Meningite', '71.4%',
         'Meningite (71.4%)', '✓ PASS'],
    ]
    story.append(make_table(test_headers, test_rows,
                            [0.8*cm, 4.2*cm, 2.8*cm, 2*cm, 3.2*cm, 2*cm]))
    story.append(Paragraph("Tabella 8 — Risultati della suite di test.", s['Caption']))

    story.append(Paragraph("8.3 Codice di Test in Prolog", s['SectionH2']))

    test_code = (
        "%% Predicato principale per i test\n"
        "test_diagnosi :-\n"
        "    write('=== Test Suite MedExpert AI ==='), nl,\n"
        "    test_influenza,\n"
        "    test_covid,\n"
        "    test_polmonite,\n"
        "    test_gastrite,\n"
        "    test_diabete,\n"
        "    write('=== Tutti i test superati! ==='), nl.\n"
        "\n"
        "%% Test: Influenza\n"
        "test_influenza :-\n"
        "    Sintomi = [febbre, tosse, mal_di_gola,\n"
        "               dolori_muscolari, mal_di_testa],\n"
        "    diagnosi(Sintomi, influenza, CF),\n"
        "    CF > 80,\n"
        "    write('  ✓ Test Influenza superato'), nl.\n"
        "\n"
        "%% Test: COVID-19\n"
        "test_covid :-\n"
        "    Sintomi = [febbre, tosse_secca, perdita_gusto,\n"
        "               perdita_olfatto, affaticamento],\n"
        "    diagnosi(Sintomi, covid19, CF),\n"
        "    CF > 60,\n"
        "    write('  ✓ Test COVID-19 superato'), nl."
    )
    story.append(code_block(test_code, s))
    story.append(Paragraph("Listato 5 — Estratto della suite di test in Prolog.", s['Caption']))

    story.append(Paragraph("8.4 Risultati della Validazione", s['SectionH2']))
    story.append(Paragraph(
        "Tutti i 7 test case sono stati eseguiti con successo, confermando la correttezza del "
        "motore inferenziale e della Knowledge Base. Il sistema produce diagnosi accurate con "
        "fattori di certezza coerenti con la sovrapposizione tra sintomi del paziente e sintomi "
        "delle malattie. La suite di test serve anche come <b>regression testing</b>: ogni volta "
        "che la KB viene modificata o estesa, i test esistenti verificano che le diagnosi "
        "precedentemente corrette non siano state compromesse.", s['BodyJ']))

    story.append(hr())


# ════════════════════ SEZIONE 9 ════════════════════
def build_section_9(story, s):
    story.append(Paragraph("9. Confronto con Approcci Alternativi", s['SectionH1']))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph(
        "Per contestualizzare il nostro approccio basato su sistema esperto, è utile confrontarlo "
        "con le principali alternative disponibili nel campo dell'AI applicata alla diagnosi medica.", s['BodyJ']))

    story.append(Paragraph("9.1 Tabella Comparativa", s['SectionH2']))

    comp_headers = ['Caratteristica', 'Sistema Esperto\n(MedExpert AI)',
                    'Machine Learning\n(es. Random Forest)', 'Deep Learning\n(es. Reti Neurali)']
    comp_rows = [
        ['Dati di training\nnecessari',
         'Nessuno\n(conoscenza codificata)',
         'Dataset medio\n(migliaia di campioni)',
         'Dataset grande\n(milioni di campioni)'],
        ['Spiegabilità',
         'Alta\n(regole esplicite)',
         'Media\n(feature importance)',
         'Bassa\n(black box)'],
        ['Accuratezza',
         'Dipende dalla KB\n(limitata al dominio)',
         'Alta con buoni dati',
         'Molto alta con\nmolti dati'],
        ['Gestione\nincertezza',
         'Fattori di certezza\n(CF)',
         'Probabilità\nstatistiche',
         'Softmax /\nprobabilità'],
        ['Manutenzione',
         'Aggiornamento manuale\ndella KB',
         'Re-training con\nnuovi dati',
         'Re-training\ncostoso'],
        ['Tempo di\nsviluppo',
         'Medio\n(knowledge engineering)',
         'Medio\n(feature engineering)',
         'Alto\n(architettura + tuning)'],
        ['Risorse\ncomputazionali',
         'Minime\n(CPU base)',
         'Moderate\n(CPU multi-core)',
         'Elevate\n(GPU necessaria)'],
        ['Adattabilità a\nnuovi domini',
         'Richiede nuovo\nknowledge engineering',
         'Richiede nuovi\ndati etichettati',
         'Transfer learning\npossibile'],
    ]
    story.append(make_table(comp_headers, comp_rows,
                            [3*cm, 3.5*cm, 3.5*cm, 3.5*cm]))
    story.append(Paragraph("Tabella 9 — Confronto tra approcci AI per la diagnosi medica.",
                           s['Caption']))

    story.append(Paragraph("9.2 Vantaggi dei Sistemi a Regole", s['SectionH2']))
    story.append(Paragraph(
        "L'approccio basato su sistema esperto presenta vantaggi significativi in diversi contesti:", s['BodyJ']))
    story.append(Paragraph(
        "• <b>Spiegabilità completa</b> — Ogni diagnosi può essere giustificata mostrando le regole "
        "e i fatti che l'hanno generata. In ambito medico, questa trasparenza è fondamentale per la "
        "fiducia dei professionisti sanitari e per conformità alle normative.", s['BodyBullet']))
    story.append(Paragraph(
        "• <b>Nessun dato di training</b> — Il sistema funziona immediatamente con la conoscenza "
        "codificata dall'esperto del dominio, senza necessità di dataset etichettati che in ambito "
        "medico sono costosi e soggetti a vincoli di privacy.", s['BodyBullet']))
    story.append(Paragraph(
        "• <b>Determinismo</b> — A parità di input, il sistema produce sempre lo stesso output, "
        "caratteristica desiderabile in applicazioni critiche come la diagnosi medica.", s['BodyBullet']))
    story.append(Paragraph(
        "• <b>Leggerezza computazionale</b> — Non richiede GPU o risorse cloud, può essere eseguito "
        "su qualsiasi computer con SWI-Prolog e Python installati.", s['BodyBullet']))

    story.append(Paragraph("9.3 Limitazioni", s['SectionH2']))
    story.append(Paragraph(
        "È importante riconoscere anche le limitazioni dell'approccio adottato:", s['BodyJ']))
    story.append(Paragraph(
        "• <b>Knowledge Engineering Bottleneck</b> — La codifica della conoscenza è un processo "
        "manuale che richiede la collaborazione con esperti del dominio. L'aggiunta di nuove "
        "malattie o l'aggiornamento delle conoscenze mediche richiede intervento umano.", s['BodyBullet']))
    story.append(Paragraph(
        "• <b>Scalabilità limitata</b> — Con l'aumentare della complessità del dominio (centinaia "
        "di malattie, migliaia di sintomi), la manutenzione della KB diventa progressivamente "
        "più onerosa.", s['BodyBullet']))
    story.append(Paragraph(
        "• <b>Modello di incertezza semplificato</b> — I fattori di certezza, pur efficaci, non "
        "catturano le complesse relazioni probabilistiche tra sintomi e malattie che modelli "
        "bayesiani o reti neurali possono apprendere dai dati.", s['BodyBullet']))

    story.append(hr())


# ════════════════════ SEZIONE 10 ════════════════════
def build_section_10(story, s):
    story.append(Paragraph("10. Conclusioni e Sviluppi Futuri", s['SectionH1']))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("10.1 Riepilogo dei Risultati", s['SectionH2']))
    story.append(Paragraph(
        "Il progetto MedExpert AI ha dimostrato con successo la fattibilità e l'efficacia di un "
        "sistema esperto per la diagnosi medica, implementato combinando la potenza della "
        "programmazione logica in Prolog con l'accessibilità di un'interfaccia grafica Python. "
        "I principali risultati ottenuti sono:", s['BodyJ']))

    story.append(Paragraph(
        "• <b>Knowledge Base completa</b> — È stata sviluppata una KB contenente 16 patologie "
        "distribuite su 8 categorie mediche, con oltre 70 sintomi distinti, descrizioni dettagliate "
        "e trattamenti raccomandati.", s['BodyBullet']))
    story.append(Paragraph(
        "• <b>Motore inferenziale funzionale</b> — Il backward chaining di Prolog, combinato con "
        "il calcolo dei fattori di certezza, produce diagnosi accurate e ordinate per probabilità, "
        "come confermato dalla suite di test.", s['BodyBullet']))
    story.append(Paragraph(
        "• <b>Explanation Facility</b> — Il sistema è in grado di spiegare ogni diagnosi, mostrando "
        "i sintomi corrispondenti e il calcolo del fattore di certezza, soddisfacendo un requisito "
        "fondamentale dei sistemi esperti.", s['BodyBullet']))
    story.append(Paragraph(
        "• <b>Interfaccia utente professionale</b> — La GUI con tema medicale scuro offre "
        "un'esperienza utente intuitiva e visivamente accattivante, rendendo il sistema accessibile "
        "anche a utenti non tecnici.", s['BodyBullet']))
    story.append(Paragraph(
        "• <b>Integrazione multi-paradigma</b> — L'integrazione tra Prolog (paradigma logico) e "
        "Python (paradigma imperativo/OOP) dimostra la complementarità dei diversi approcci alla "
        "programmazione nell'ambito dell'AI.", s['BodyBullet']))

    story.append(Paragraph("10.2 Sviluppi Futuri", s['SectionH2']))
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
    story.append(Paragraph("Tabella 10 — Possibili sviluppi futuri del sistema.", s['Caption']))

    story.append(Paragraph("10.3 Connessione ai Temi del Corso", s['SectionH2']))
    story.append(Paragraph(
        "In conclusione, MedExpert AI rappresenta un'applicazione concreta dei concetti fondamentali "
        "trattati nel corso di <i>Elementi di Intelligenza Artificiale</i>. Il progetto tocca i temi "
        "della <b>rappresentazione della conoscenza</b> (fatti e regole Prolog), del <b>ragionamento "
        "automatico</b> (backward chaining), della <b>gestione dell'incertezza</b> (fattori di certezza), "
        "e della <b>progettazione di agenti intelligenti</b> (il sistema esperto come agente "
        "knowledge-based).", s['BodyJ']))

    story.append(Paragraph(
        "Il sistema dimostra che l'AI simbolica, nonostante l'attuale predominanza degli approcci "
        "basati su apprendimento automatico, mantiene un ruolo fondamentale in applicazioni dove "
        "la spiegabilità, la trasparenza e il determinismo sono requisiti imprescindibili — come "
        "nel caso della diagnosi medica. La combinazione di Prolog per il ragionamento logico e "
        "Python per l'interfaccia utente rappresenta un esempio efficace di come diversi paradigmi "
        "di programmazione possano essere integrati per realizzare sistemi AI completi e funzionali.", s['BodyJ']))

    story.append(Spacer(1, 1 * cm))
    story.append(hr())
    story.append(Spacer(1, 0.5 * cm))

    # Chiusura
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


# ════════════════════ MAIN ════════════════════
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "Documentazione_MedExpert.pdf")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=2.8 * cm,
        bottomMargin=2 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        title="MedExpert AI — Documentazione di Progetto",
        author="Luciano Meccariello",
        subject="Sistema Esperto di Diagnosi Medica",
    )

    styles = build_styles()
    story = []

    # Costruzione del documento
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
    build_section_9(story, styles)
    build_section_10(story, styles)

    # Generazione PDF
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"✅ PDF generato con successo: {output_path}")
    print(f"   Dimensione: {os.path.getsize(output_path) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
