% MedExpert AI - Knowledge base in Prolog
% Corso di Elementi di IA - Universita' Federico II di Napoli
% Prof. Sperli' Giancarlo
% Qui dentro stanno tutte le malattie, i sintomi e le regole per la diagnosi.

:- use_module(library(lists)).


% Sintomi per malattia.
% Abbiamo raggruppato le malattie per categoria (cosi' diventa piu' facile
% trovarle quando si scorre il file).

% --- Respiratorie ---

% Influenza (la classica influenza stagionale)
sintomo(influenza, febbre_alta).
sintomo(influenza, mal_di_testa).
sintomo(influenza, dolori_muscolari).
sintomo(influenza, tosse_secca).
sintomo(influenza, mal_di_gola).
sintomo(influenza, stanchezza).
sintomo(influenza, naso_chiuso).

% COVID-19
sintomo(covid19, febbre_alta).
sintomo(covid19, tosse_secca).
sintomo(covid19, difficolta_respiratorie).
sintomo(covid19, perdita_gusto_olfatto).
sintomo(covid19, stanchezza).
sintomo(covid19, dolori_muscolari).
sintomo(covid19, mal_di_testa).
sintomo(covid19, mal_di_gola).

% Bronchite (infiammazione dei bronchi)
sintomo(bronchite, tosse_grassa).
sintomo(bronchite, difficolta_respiratorie).
sintomo(bronchite, febbre_lieve).
sintomo(bronchite, stanchezza).
sintomo(bronchite, dolore_petto).
sintomo(bronchite, mal_di_gola).
sintomo(bronchite, respiro_affannoso).

% Polmonite
sintomo(polmonite, febbre_alta).
sintomo(polmonite, tosse_grassa).
sintomo(polmonite, difficolta_respiratorie).
sintomo(polmonite, dolore_petto).
sintomo(polmonite, stanchezza).
sintomo(polmonite, sudorazione_notturna).
sintomo(polmonite, respiro_affannoso).
sintomo(polmonite, confusione).

% --- Gastrointestinali ---

% Gastrite
sintomo(gastrite, dolore_addominale).
sintomo(gastrite, nausea).
sintomo(gastrite, vomito).
sintomo(gastrite, bruciore_stomaco).
sintomo(gastrite, perdita_appetito).
sintomo(gastrite, stanchezza).

% Appendicite (quella che ti fa finire al pronto soccorso)
sintomo(appendicite, dolore_addominale).
sintomo(appendicite, nausea).
sintomo(appendicite, vomito).
sintomo(appendicite, febbre_lieve).
sintomo(appendicite, perdita_appetito).
sintomo(appendicite, diarrea).

% Reflusso gastroesofageo
sintomo(reflusso_gastroesofageo, bruciore_stomaco).
sintomo(reflusso_gastroesofageo, dolore_petto).
sintomo(reflusso_gastroesofageo, nausea).
sintomo(reflusso_gastroesofageo, tosse_secca).
sintomo(reflusso_gastroesofageo, mal_di_gola).
sintomo(reflusso_gastroesofageo, difficolta_respiratorie).

% --- Neurologiche ---

% Emicrania
sintomo(emicrania, mal_di_testa).
sintomo(emicrania, nausea).
sintomo(emicrania, vomito).
sintomo(emicrania, sensibilita_luce).
sintomo(emicrania, vertigini).
sintomo(emicrania, difficolta_concentrazione).

% Meningite (attenzione, e' un'emergenza)
sintomo(meningite, febbre_alta).
sintomo(meningite, mal_di_testa).
sintomo(meningite, rigidita_collo).
sintomo(meningite, sensibilita_luce).
sintomo(meningite, nausea).
sintomo(meningite, vomito).
sintomo(meningite, confusione).
sintomo(meningite, stanchezza).

% --- Cardiovascolari ---

% Ipertensione
sintomo(ipertensione, mal_di_testa).
sintomo(ipertensione, vertigini).
sintomo(ipertensione, visione_offuscata).
sintomo(ipertensione, dolore_petto).
sintomo(ipertensione, respiro_affannoso).
sintomo(ipertensione, stanchezza).

% Tachicardia
sintomo(tachicardia, battito_accelerato).
sintomo(tachicardia, dolore_petto).
sintomo(tachicardia, vertigini).
sintomo(tachicardia, respiro_affannoso).
sintomo(tachicardia, stanchezza).
sintomo(tachicardia, sudorazione_notturna).

% --- Ematologiche ---

% Anemia
sintomo(anemia, stanchezza).
sintomo(anemia, pallore).
sintomo(anemia, debolezza).
sintomo(anemia, vertigini).
sintomo(anemia, mal_di_testa).
sintomo(anemia, battito_accelerato).
sintomo(anemia, respiro_affannoso).

% --- Metaboliche ---

% Diabete di tipo 2
sintomo(diabete_tipo2, sete_eccessiva).
sintomo(diabete_tipo2, minzione_frequente).
sintomo(diabete_tipo2, stanchezza).
sintomo(diabete_tipo2, visione_offuscata).
sintomo(diabete_tipo2, perdita_appetito).
sintomo(diabete_tipo2, debolezza).

% --- Endocrine ---

% Ipotiroidismo
sintomo(ipotiroidismo, stanchezza).
sintomo(ipotiroidismo, aumento_peso).
sintomo(ipotiroidismo, pelle_secca).
sintomo(ipotiroidismo, sensibilita_freddo).
sintomo(ipotiroidismo, perdita_capelli).
sintomo(ipotiroidismo, debolezza).
sintomo(ipotiroidismo, difficolta_concentrazione).

% --- Urologiche ---

% Cistite
sintomo(cistite, bruciore_minzione).
sintomo(cistite, minzione_frequente).
sintomo(cistite, dolore_lombare).
sintomo(cistite, urine_torbide).
sintomo(cistite, febbre_lieve).
sintomo(cistite, dolore_addominale).

% --- Immunitarie ---

% Allergia stagionale
sintomo(allergia_stagionale, starnuti).
sintomo(allergia_stagionale, naso_chiuso).
sintomo(allergia_stagionale, occhi_arrossati).
sintomo(allergia_stagionale, prurito_nasale).
sintomo(allergia_stagionale, mal_di_testa).
sintomo(allergia_stagionale, tosse_secca).

% --- Psichiatriche ---

% Depressione
sintomo(depressione, tristezza).
sintomo(depressione, insonnia).
sintomo(depressione, perdita_interesse).
sintomo(depressione, stanchezza).
sintomo(depressione, difficolta_concentrazione).
sintomo(depressione, perdita_appetito).
sintomo(depressione, mal_di_testa).


% Descrizioni che la GUI mostra nel pannello di destra.

descrizione(influenza,
    'Infezione virale acuta delle vie respiratorie causata dai virus influenzali. Si manifesta tipicamente in forma stagionale con picchi nei mesi invernali.').
descrizione(covid19,
    'Malattia infettiva causata dal virus SARS-CoV-2. Puo\' variare da forme asintomatiche a gravi insufficienze respiratorie.').
descrizione(bronchite,
    'Infiammazione della mucosa dei bronchi, spesso conseguente a infezioni virali o batteriche. Puo\' essere acuta o cronica.').
descrizione(polmonite,
    'Infezione del parenchima polmonare che causa infiammazione degli alveoli. Puo\' essere di origine batterica, virale o fungina.').
descrizione(gastrite,
    'Infiammazione della mucosa gastrica che puo\' essere acuta o cronica. Spesso associata ad Helicobacter pylori o uso di FANS.').
descrizione(appendicite,
    'Infiammazione acuta dell\'appendice vermiforme. Richiede generalmente intervento chirurgico urgente (appendicectomia).').
descrizione(reflusso_gastroesofageo,
    'Condizione in cui il contenuto acido dello stomaco risale nell\'esofago, causando irritazione e sintomi tipici come bruciore retrosternale.').
descrizione(emicrania,
    'Cefalea primaria ricorrente caratterizzata da dolore pulsante, spesso unilaterale, accompagnato da nausea e sensibilita\' a luce e suoni.').
descrizione(meningite,
    'Infiammazione delle meningi, le membrane che rivestono il cervello e il midollo spinale. Puo\' essere batterica (grave) o virale (piu\' lieve).').
descrizione(ipertensione,
    'Condizione caratterizzata da valori di pressione arteriosa cronicamente elevati (>=140/90 mmHg). Principale fattore di rischio cardiovascolare.').
descrizione(tachicardia,
    'Aumento della frequenza cardiaca oltre i 100 battiti al minuto a riposo. Puo\' essere fisiologica o patologica.').
descrizione(anemia,
    'Riduzione della concentrazione di emoglobina nel sangue al di sotto dei valori normali, con conseguente ridotto trasporto di ossigeno ai tessuti.').
descrizione(diabete_tipo2,
    'Disturbo metabolico caratterizzato da iperglicemia cronica dovuta a insulino-resistenza e progressivo deficit di secrezione insulinica.').
descrizione(ipotiroidismo,
    'Condizione in cui la ghiandola tiroidea non produce sufficienti ormoni tiroidei, rallentando il metabolismo corporeo.').
descrizione(cistite,
    'Infezione del tratto urinario inferiore (vescica), piu\' frequente nelle donne. Generalmente causata da batteri come Escherichia coli.').
descrizione(allergia_stagionale,
    'Reazione eccessiva del sistema immunitario a allergeni ambientali come pollini, polvere o muffe. Nota anche come rinite allergica.').
descrizione(depressione,
    'Disturbo dell\'umore caratterizzato da tristezza persistente, perdita di interesse e alterazioni cognitive. Richiede trattamento specialistico.').


% Trattamenti consigliati (sempre per la GUI).

trattamento(influenza,
    'Riposo, idratazione abbondante, antipiretici (paracetamolo o ibuprofene). Nei casi a rischio, antivirali (oseltamivir). Vaccinazione preventiva.').
trattamento(covid19,
    'Isolamento, monitoraggio della saturazione di ossigeno, antipiretici. Nei casi gravi, ospedalizzazione con ossigenoterapia e terapie antivirali.').
trattamento(bronchite,
    'Riposo, idratazione, mucolitici ed espettoranti. Antibiotici solo se di origine batterica confermata. Broncodilatatori se necessario.').
trattamento(polmonite,
    'Antibiotici mirati (se batterica), antipiretici, riposo assoluto, idratazione. Ospedalizzazione nei casi gravi con supporto respiratorio.').
trattamento(gastrite,
    'Inibitori di pompa protonica (omeprazolo), antiacidi, dieta leggera. Eradicazione di H. pylori se presente. Evitare FANS e alcol.').
trattamento(appendicite,
    'Intervento chirurgico (appendicectomia) in urgenza. Antibioticoterapia preoperatoria. In alcuni casi selezionati, terapia conservativa.').
trattamento(reflusso_gastroesofageo,
    'Inibitori di pompa protonica, modifiche dello stile di vita (evitare pasti abbondanti, non coricarsi subito dopo i pasti, elevare la testata del letto).').
trattamento(emicrania,
    'Analgesici (FANS o triptani) al bisogno. Terapia preventiva con beta-bloccanti o antiepilettici nei casi frequenti. Evitare i fattori scatenanti.').
trattamento(meningite,
    'EMERGENZA MEDICA: antibiotici endovenosi immediati (se batterica), corticosteroidi, ospedalizzazione in terapia intensiva. Vaccinazione preventiva.').
trattamento(ipertensione,
    'Modifiche dello stile di vita (dieta iposodica, attivita\' fisica regolare), farmaci antipertensivi (ACE-inibitori, sartani, calcio-antagonisti).').
trattamento(tachicardia,
    'Identificazione e trattamento della causa sottostante. Beta-bloccanti o calcio-antagonisti. Manovre vagali nelle crisi acute.').
trattamento(anemia,
    'Integrazione di ferro (solfato ferroso), vitamina B12 o acido folico a seconda della causa. Trasfusioni nei casi gravi. Trattamento della causa.').
trattamento(diabete_tipo2,
    'Dieta equilibrata, attivita\' fisica regolare, metformina come farmaco di prima linea. Monitoraggio glicemico. Insulina se necessario.').
trattamento(ipotiroidismo,
    'Terapia sostitutiva con levotiroxina (ormone tiroideo sintetico) a dosaggio personalizzato. Monitoraggio periodico del TSH.').
trattamento(cistite,
    'Antibiotici mirati (fosfomicina, nitrofurantoina), abbondante idratazione, analgesici urinari. Prevenzione con igiene intima adeguata.').
trattamento(allergia_stagionale,
    'Antistaminici orali, corticosteroidi nasali spray, colliri antistaminici. Immunoterapia specifica nei casi gravi. Evitare esposizione agli allergeni.').
trattamento(depressione,
    'Psicoterapia (cognitivo-comportamentale), farmaci antidepressivi (SSRI come prima scelta), attivita\' fisica regolare. Supporto psicologico continuativo.').


% Categoria di ogni malattia (la usiamo per raggruppare le voci nella GUI).

categoria(influenza, respiratoria).
categoria(covid19, respiratoria).
categoria(bronchite, respiratoria).
categoria(polmonite, respiratoria).

categoria(gastrite, gastrointestinale).
categoria(appendicite, gastrointestinale).
categoria(reflusso_gastroesofageo, gastrointestinale).

categoria(emicrania, neurologica).
categoria(meningite, neurologica).

categoria(ipertensione, cardiovascolare).
categoria(tachicardia, cardiovascolare).

categoria(anemia, ematologica).

categoria(diabete_tipo2, metabolica).

categoria(ipotiroidismo, endocrina).

categoria(cistite, urologica).

categoria(allergia_stagionale, immunitaria).

categoria(depressione, psichiatrica).


% ===== Regole di inferenza =====
% Il cuore del sistema. Funziona in backward chaining: parte dalla malattia
% e controlla quanti dei suoi sintomi sono presenti nel paziente.

% malattia(X) - vero se X compare nella KB.
malattia(X) :- categoria(X, _).

% diagnosi/3: data la lista dei sintomi del paziente, calcola la certezza
% di una malattia come (sintomi_comuni / sintomi_totali_malattia) * 100.
% Restituisce solo le malattie con almeno un sintomo in comune.
diagnosi(SintomiPaziente, Malattia, Certezza) :-
    malattia(Malattia),
    sort(SintomiPaziente, SintomiUnici),
    findall(S, sintomo(Malattia, S), TuttiSintomi),
    intersection(SintomiUnici, TuttiSintomi, SintomiComuni),
    length(SintomiComuni, NComuni),
    NComuni > 0,
    length(TuttiSintomi, NTotali),
    Certezza is round((NComuni / NTotali) * 100).

% Raccoglie tutte le diagnosi e le ordina dalla piu' probabile alla meno.
% Ogni elemento ha la forma: certezza(Percentuale, Malattia).
diagnosi_ordinate(SintomiPaziente, Risultati) :-
    findall(
        certezza(Certezza, Malattia),
        diagnosi(SintomiPaziente, Malattia, Certezza),
        Lista
    ),
    sort(0, @>=, Lista, Risultati).

% Divide i sintomi della malattia in due liste: quelli che il paziente ha
% (Trovati) e quelli che gli mancano (Mancanti). Serve per la spiegazione.
spiega_diagnosi(SintomiPaziente, Malattia, SintomiTrovati, SintomiMancanti) :-
    sort(SintomiPaziente, SintomiUnici),
    findall(S, sintomo(Malattia, S), Tutti),
    intersection(SintomiUnici, Tutti, SintomiTrovati),
    subtract(Tutti, SintomiTrovati, SintomiMancanti).

% Tutte le malattie di una categoria.
malattie_per_categoria(Categoria, Malattie) :-
    findall(M, categoria(M, Categoria), Malattie).

% Sintomi che due malattie hanno in comune (utile per la diagnosi differenziale).
sintomi_comuni(Malattia1, Malattia2, SintomiCondivisi) :-
    Malattia1 \= Malattia2,
    findall(S, sintomo(Malattia1, S), S1),
    findall(S, sintomo(Malattia2, S), S2),
    intersection(S1, S2, SintomiCondivisi).


% ===== Ponte verso Python =====
% Da qui in giu' i predicati servono a Python: prendono atomi in input e
% stampano il risultato a video, cosi' il chiamante puo' leggerli dallo stdout.

% Riceve una stringa tipo 'febbre,tosse' e stampa "Malattia:Certezza" per ogni
% diagnosi possibile.
query_diagnosi(SintomiAtom) :-
    atomic_list_concat(SintomiList, ',', SintomiAtom),
    diagnosi_ordinate(SintomiList, Risultati),
    stampa_risultati(Risultati).

stampa_risultati([]).
stampa_risultati([certezza(C, M)|Rest]) :-
    format('~w:~w~n', [M, C]),
    stampa_risultati(Rest).

% Stampa la spiegazione completa di una diagnosi (trovati, mancanti, descrizione,
% trattamento). Anche qui il formato e' pensato per essere parsato in Python.
query_spiega(MalattiaAtom, SintomiAtom) :-
    atomic_list_concat(SintomiList, ',', SintomiAtom),
    spiega_diagnosi(SintomiList, MalattiaAtom, Trovati, Mancanti),
    atomic_list_concat(Trovati, ',', TrovatiStr),
    atomic_list_concat(Mancanti, ',', MancantiStr),
    descrizione(MalattiaAtom, Desc),
    trattamento(MalattiaAtom, Tratt),
    format('TROVATI:~w~nMANCANTI:~w~nDESCRIZIONE:~w~nTRATTAMENTO:~w~n',
           [TrovatiStr, MancantiStr, Desc, Tratt]).

% Stampa tutte le malattie di una categoria, una per riga.
query_categorie(Categoria) :-
    malattie_per_categoria(Categoria, Malattie),
    stampa_lista(Malattie).

stampa_lista([]).
stampa_lista([H|T]) :-
    format('~w~n', [H]),
    stampa_lista(T).

% Lista di tutti i sintomi che esistono nella KB (senza duplicati).
lista_tutti_sintomi(Sintomi) :-
    findall(S, sintomo(_, S), Tutti),
    sort(Tutti, Sintomi).

% Lista di tutte le malattie nella KB.
lista_tutte_malattie(Malattie) :-
    findall(M, malattia(M), Malattie).


% ===== Test =====
% Lanciali con: swipl -g "test_diagnosi, halt" diagnosi_medica.pl
% Servono giusto per essere sicuri che le regole non si rompano.

% Esegue tutti i test e a fine stampa quanti ne sono passati.
test_diagnosi :-
    format('~n========================================~n'),
    format('  SUITE DI TEST - SISTEMA DIAGNOSTICO~n'),
    format('========================================~n~n'),
    %% Contatore dei test superati e falliti
    test_1(R1),
    test_2(R2),
    test_3(R3),
    test_4(R4),
    test_5(R5),
    test_6(R6),
    test_7(R7),
    %% Riepilogo
    somma_risultati([R1, R2, R3, R4, R5, R6, R7], Superati, Totale),
    Falliti is Totale - Superati,
    format('~n========================================~n'),
    format('  RIEPILOGO: ~w/~w superati, ~w falliti~n', [Superati, Totale, Falliti]),
    format('========================================~n~n').

% Conta quanti 1 ci sono nella lista (test passati) e la lunghezza totale.
somma_risultati([], 0, 0).
somma_risultati([1|T], S, Tot) :-
    somma_risultati(T, S1, T1),
    S is S1 + 1,
    Tot is T1 + 1.
somma_risultati([0|T], S, Tot) :-
    somma_risultati(T, S1, T1),
    S is S1,
    Tot is T1 + 1.

% Test 1: se passiamo TUTTI i sintomi dell'influenza, la certezza deve venire 100%.
test_1(Risultato) :-
    format('[Test 1] Corrispondenza esatta (tutti i sintomi dell\'influenza)~n'),
    SintomiPaziente = [febbre_alta, mal_di_testa, dolori_muscolari,
                       tosse_secca, mal_di_gola, stanchezza, naso_chiuso],
    diagnosi(SintomiPaziente, influenza, Certezza),
    (   Certezza =:= 100
    ->  format('  RISULTATO: SUPERATO (Certezza = ~w%)~n~n', [Certezza]),
        Risultato = 1
    ;   format('  RISULTATO: FALLITO (Certezza attesa: 100%, ottenuta: ~w%)~n~n', [Certezza]),
        Risultato = 0
    ).

% Test 2: corrispondenza parziale.
% Influenza ha 7 sintomi, ne passiamo 3 -> ci aspettiamo round(3/7*100) = 43%.
test_2(Risultato) :-
    format('[Test 2] Corrispondenza parziale (3 sintomi su 7 dell\'influenza)~n'),
    SintomiPaziente = [febbre_alta, tosse_secca, stanchezza],
    diagnosi(SintomiPaziente, influenza, Certezza),
    CertezzaAttesa is round((3 / 7) * 100),
    (   Certezza =:= CertezzaAttesa
    ->  format('  RISULTATO: SUPERATO (Certezza = ~w%)~n~n', [Certezza]),
        Risultato = 1
    ;   format('  RISULTATO: FALLITO (Certezza attesa: ~w%, ottenuta: ~w%)~n~n',
               [CertezzaAttesa, Certezza]),
        Risultato = 0
    ).

% Test 3: sintomi generici (febbre, mal di testa, stanchezza) devono dare
% piu' di una diagnosi (li hanno influenza, covid, meningite ecc).
test_3(Risultato) :-
    format('[Test 3] Diagnosi multiple (sintomi condivisi tra malattie)~n'),
    SintomiPaziente = [febbre_alta, mal_di_testa, stanchezza],
    diagnosi_ordinate(SintomiPaziente, Risultati),
    length(Risultati, N),
    (   N > 1
    ->  format('  RISULTATO: SUPERATO (~w diagnosi trovate)~n', [N]),
        format('  Diagnosi: '),
        stampa_risultati_inline(Risultati),
        format('~n~n'),
        Risultato = 1
    ;   format('  RISULTATO: FALLITO (attese >1 diagnosi, trovate ~w)~n~n', [N]),
        Risultato = 0
    ).

% Test 4: se passiamo sintomi inventati non deve uscire niente.
test_4(Risultato) :-
    format('[Test 4] Nessuna corrispondenza (sintomo inesistente)~n'),
    SintomiPaziente = [sintomo_inventato, altro_sintomo_falso],
    diagnosi_ordinate(SintomiPaziente, Risultati),
    length(Risultati, N),
    (   N =:= 0
    ->  format('  RISULTATO: SUPERATO (nessuna diagnosi, come atteso)~n~n'),
        Risultato = 1
    ;   format('  RISULTATO: FALLITO (attese 0 diagnosi, trovate ~w)~n~n', [N]),
        Risultato = 0
    ).

% Test 5: se l'utente seleziona due volte lo stesso sintomo il risultato
% non deve cambiare (l'uso di sort/2 prima dell'intersezione ci salva).
test_5(Risultato) :-
    format('[Test 5] Gestione duplicati (sintomi ripetuti nell\'input)~n'),
    SintomiNormali = [febbre_alta, tosse_secca],
    SintomiDuplicati = [febbre_alta, tosse_secca, febbre_alta, tosse_secca],
    diagnosi(SintomiNormali, influenza, C1),
    diagnosi(SintomiDuplicati, influenza, C2),
    (   C1 =:= C2
    ->  format('  RISULTATO: SUPERATO (Certezza uguale: ~w% con e senza duplicati)~n~n', [C1]),
        Risultato = 1
    ;   format('  RISULTATO: FALLITO (Certezza diversa: ~w% vs ~w%)~n~n', [C1, C2]),
        Risultato = 0
    ).

% Test 6: spiega_diagnosi/4 deve dare 2 trovati + 5 mancanti sull'influenza
% se passiamo solo febbre_alta e tosse_secca (influenza ha 7 sintomi totali).
test_6(Risultato) :-
    format('[Test 6] Spiegazione diagnosi (sintomi trovati e mancanti)~n'),
    SintomiPaziente = [febbre_alta, tosse_secca],
    spiega_diagnosi(SintomiPaziente, influenza, Trovati, Mancanti),
    length(Trovati, NT),
    length(Mancanti, NM),
    (   NT =:= 2, NM =:= 5
    ->  format('  RISULTATO: SUPERATO (~w trovati, ~w mancanti)~n~n', [NT, NM]),
        Risultato = 1
    ;   format('  RISULTATO: FALLITO (Trovati: ~w, Mancanti: ~w)~n~n', [NT, NM]),
        Risultato = 0
    ).

% Test 7: la lista delle diagnosi deve venire ordinata dalla certezza piu' alta
% alla piu' bassa.
test_7(Risultato) :-
    format('[Test 7] Ordinamento risultati (certezza decrescente)~n'),
    SintomiPaziente = [febbre_alta, mal_di_testa, dolori_muscolari, tosse_secca],
    diagnosi_ordinate(SintomiPaziente, Risultati),
    estrai_certezze(Risultati, Certezze),
    (   ordinato_decrescente(Certezze)
    ->  format('  RISULTATO: SUPERATO (risultati correttamente ordinati)~n'),
        format('  Certezze: ~w~n~n', [Certezze]),
        Risultato = 1
    ;   format('  RISULTATO: FALLITO (ordine non decrescente: ~w)~n~n', [Certezze]),
        Risultato = 0
    ).

% Tira fuori solo i numeri di certezza da una lista di certezza(C, M).
estrai_certezze([], []).
estrai_certezze([certezza(C, _)|T], [C|Rest]) :-
    estrai_certezze(T, Rest).

% Vero se la lista e' ordinata in modo non-crescente.
ordinato_decrescente([]).
ordinato_decrescente([_]).
ordinato_decrescente([A, B|T]) :-
    A >= B,
    ordinato_decrescente([B|T]).

% Stampa i risultati su una sola riga (per il log compatto del test 3).
stampa_risultati_inline([]).
stampa_risultati_inline([certezza(C, M)|Rest]) :-
    format('~w(~w%) ', [M, C]),
    stampa_risultati_inline(Rest).


% ===== Utility per il debug =====
% Comandi comodi se vogliamo controllare al volo la KB da swipl interattivo.

% Elenca tutte le malattie con la loro categoria.
mostra_malattie :-
    format('~n--- ELENCO MALATTIE ---~n~n'),
    forall(
        categoria(M, C),
        format('  ~w (~w)~n', [M, C])
    ),
    format('~n').

% Stampa i sintomi associati ad una malattia.
mostra_sintomi(Malattia) :-
    format('~nSintomi di ~w:~n', [Malattia]),
    forall(
        sintomo(Malattia, S),
        format('  - ~w~n', [S])
    ),
    format('~n').

% Stampa la "scheda" completa di una malattia (categoria, sintomi, descrizione,
% trattamento). Se la malattia non esiste lo dice.
mostra_info(Malattia) :-
    (   malattia(Malattia)
    ->  format('~n=== ~w ===~n~n', [Malattia]),
        categoria(Malattia, Cat),
        format('Categoria: ~w~n~n', [Cat]),
        descrizione(Malattia, Desc),
        format('Descrizione: ~w~n~n', [Desc]),
        format('Sintomi:~n'),
        forall(sintomo(Malattia, S), format('  - ~w~n', [S])),
        format('~n'),
        trattamento(Malattia, Tratt),
        format('Trattamento: ~w~n~n', [Tratt])
    ;   format('~nERRORE: Malattia "~w" non trovata nella base di conoscenza.~n~n', [Malattia])
    ).

% Stampa cosa hanno in comune due malattie e in cosa si distinguono.
diagnosi_differenziale(M1, M2) :-
    format('~n=== Diagnosi differenziale: ~w vs ~w ===~n~n', [M1, M2]),
    findall(S, sintomo(M1, S), S1),
    findall(S, sintomo(M2, S), S2),
    intersection(S1, S2, Comuni),
    subtract(S1, S2, SoloM1),
    subtract(S2, S1, SoloM2),
    format('Sintomi comuni:~n'),
    (   Comuni = []
    ->  format('  (nessuno)~n')
    ;   forall(member(S, Comuni), format('  - ~w~n', [S]))
    ),
    format('~nSintomi esclusivi di ~w:~n', [M1]),
    (   SoloM1 = []
    ->  format('  (nessuno)~n')
    ;   forall(member(S, SoloM1), format('  - ~w~n', [S]))
    ),
    format('~nSintomi esclusivi di ~w:~n', [M2]),
    (   SoloM2 = []
    ->  format('  (nessuno)~n')
    ;   forall(member(S, SoloM2), format('  - ~w~n', [S]))
    ),
    format('~n').


% Fine!
