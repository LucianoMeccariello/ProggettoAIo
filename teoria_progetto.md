# Fondamenti Teorici del Sistema Esperto Medico
*(Basato sul testo "Intelligenza Artificiale" del Prof. Ciro Gallucci)*

Questo documento descrive i fondamenti teorici dell'Intelligenza Artificiale Classica (Simbolica) alla base del sistema esperto per la diagnosi medica implementato. Tutti i concetti sono allineati con il materiale didattico del corso.

---

## 1. Rappresentazione della Conoscenza e First-Order Logic (FOL)

Nel nostro sistema, la conoscenza medica è rappresentata sfruttando i principi della **First-Order Logic (Logica di Primo Ordine)**.
Il libro definisce una **Knowledge Base (KB)** come un insieme di espressioni, o *sentences*, che descrivono il dominio in modo formale. 

Nel Prolog, la KB è costituita da:
* **Fatti (Assiomi)**: Conoscenze incondizionatamente vere (es. `sintomo(influenza, febbre_alta).`). Come descrive Gallucci, "Gli assiomi sono forniti al programma logico da un esperto del dominio di interesse... per stabilire quali sono le verità assiomatiche del caso".
* **Regole (Clausole di Horn)**: Implicazioni logiche che permettono di inferire nuova conoscenza. Una clausola di Horn definita ha un solo letterale positivo (la conclusione) e una serie di precondizioni in AND.

---

## 2. Il Motore Inferenziale e il Backward Chaining (BC)

L'anima del sistema esperto è il suo motore inferenziale. Come specificato nel testo (Capitolo 9 e 10), per dedurre nuova conoscenza si possono usare due approcci: il *Forward Chaining* (guidato dai dati) o il *Backward Chaining* (guidato dall'obiettivo).

Prolog utilizza un approccio **Goal-driven (Backward Chaining)**:
* Partendo da una *query* specifica (l'obiettivo, ovvero trovare la `diagnosi`), il motore va a ritroso per cercare di dimostrare le precondizioni (i sintomi) che renderebbero vera la conclusione.
* **Profondità e Backtracking:** Come citato dal testo: *"Prolog utilizza un approccio goal-driven... Scelto un percorso, si comincia a scendere lungo tale percorso (depth-first)"*. Se una strada non porta a una dimostrazione (ad esempio se i sintomi non unificano con quelli della malattia), il motore fa *fail* e innesca il *backtracking*, riprovando con una regola o un fatto alternativo (la fase di *redo*).
* Il grande vantaggio del BC è la sua **efficienza rispetto al problema**: *"Con la BC non sono state fatte tutte le inferenze, solo quelle che sono di particolare interesse"*, limitando l'esplosione combinatoria tipica della FOL.

---

## 3. Unificazione e Pattern Matching

Per applicare le regole generali ai casi specifici dei pazienti, il sistema sfrutta l'**Unificazione** (Unify) e il concetto di *Sostituzione* ($\theta$). 
L'unificazione è il processo mediante il quale variabili astratte (come `Malattia` o `Sintomo`) vengono "sostituite" o legate a costanti reali (come `influenza` o `febbre_alta`) per far corrispondere una regola della base di conoscenza all'input del paziente.

Nel Prolog, questo processo è invisibile ma costante. Quando l'utente inserisce una lista di sintomi, Prolog esplora la Knowledge Base e applica il **Modus Ponens Generalizzato (GMP)**, trovando la sostituzione corretta che unifica la query con un fatto o una regola presente nel file `diagnosi_medica.pl`.

---

## 4. Incertezza e Sistemi Esperti: La Prospettiva Moderna (Machine Learning)

Sebbene questo progetto sia una fedele riproduzione dei classici Sistemi Esperti medici basati su regole, è fondamentale inquadrarlo storicamente all'interno del corso di IA.

Come sottolinea il testo a Pagina 127: *"Sono stati scritti molti sistemi esperti in Prolog nei domini legale, medico... Tuttavia, tutto ciò che era legato al Prolog è stato poi soppiantato dall'apprendimento per esempi (Machine Learning)"*.

Le ragioni teoriche dietro questa evoluzione, coperte nel corso, sono:
1. **Acquisizione della conoscenza (Knowledge Acquisition Bottleneck):** Negli approcci puramente logici come questo, ogni sintomo e regola deve essere codificato manualmente da un "esperto di dominio". 
2. **Incertezza complessa:** Il nostro sistema utilizza una formula matematica basata sull'incidenza percentuale per simulare i *Certainty Factors* (Fattori di Certezza). La moderna Intelligenza Artificiale risolve l'incertezza e la diagnosi medica tramite la **Probabilità (Reti Bayesiane)** o l'apprendimento supervisionato (reti neurali e SVM, come descritto nelle slide "Uncertainty" e dal Cap. 11 del libro), dove l'algoritmo estrae autonomamente i pattern dai dati senza richiedere regole if-then cablate.

Il nostro sistema rappresenta dunque l'eccellenza dell'**Intelligenza Artificiale Simbolica**, ponendo basi solide sui fondamenti della Logica di Primo Ordine prima di passare agli approcci sub-simbolici (Machine Learning).
