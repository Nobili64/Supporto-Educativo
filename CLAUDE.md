# Supporto Educativo — indicazioni per Claude Code

Progetto di uno psicologo che segue ragazzi e ragazze di scuola media con disturbi specifici dell’apprendimento (DSA): analisi di casi, progettazione di interventi, strumenti per i compiti e il metodo di studio. Si lavora e si scrive **in italiano**.

## Riservatezza

- La cartella `Casi/` contiene dati di ragazzi reali: **non aprirla, non citarla, non copiarla** in archivi o servizi esterni.
- Negli strumenti non entrano nomi, diagnosi, scuole o altri dati personali. Gli esempi sono inventati.

## Strumenti per il metodo di studio

| Cartella | Stato | Che cosa è |
|---|---|---|
| `Percorsi di studio DSA/` | superata | Prima versione, giudicata non utilizzabile: testi troppo sintetici. Serve solo come inventario (`manutenzione/guide-*.json`, `mappe.json`, `temi-mappe.json`). |
| `Percorsi di studio DSA - prototipo/` | **congelata** | *Cinque percorsi guidati*: 5 percorsi, una idea per schermata. Testi approvati. Non modificarla: viene usata nella prova con i ragazzi (`Griglia di osservazione.md`). |
| `Percorsi di studio DSA - versione completa/` | **in corso** | Stesso impianto esteso a 207 lavori e 34 mappe. Lo stato aggiornato è in `RIPRESA IN LOCALE.md` nella radice. |

## Versione completa: come è fatta

Tutto il lavoro avviene in `Percorsi di studio DSA - versione completa/manutenzione/`:

- `contenuti/<CODICE>.json` — un file per percorso. **È l’unico posto in cui si scrivono i testi.**
- `contratto-scrittura.md` — regole di scrittura obbligatorie (destinatari, fasi, leggibilità, correttezza, immagini, mappe). Leggerlo prima di scrivere o correggere un percorso.
- `catalogo.json`, `fonti.json` — elenco dei percorsi e delle fonti.
- `app.js`, `stile.css` — interfaccia comune; `costruisci.mjs` produce `../Metodo di studio DSA.html`.
- `valida.mjs` — controllo di ogni percorso (fasi, 8-18 schermate, frasi ≤ 25 parole, indice Gulpease ≥ 60, parole da evitare, limiti di mappe e tabelle).
- `verifica-browser.cjs` — tutte le schermate nel browser, senza connessione, su schermo largo e stretto.
- `da-fare.json` e `da-fare.mjs` — percorsi ancora da scrivere, divisi in gruppi; `prompt-agenti.md` — istruzioni da dare a un agente per un gruppo.

Comandi, da `manutenzione`:

```
node valida.mjs [CODICE ...]
node costruisci.mjs
node verifica-browser.cjs [CODICE ...]
node da-fare.mjs
```

Un percorso entra nel file solo se `valida.mjs` non segnala errori. Dopo ogni gruppo di percorsi: `costruisci.mjs`, poi `verifica-browser.cjs` sui codici nuovi. Il progetto non usa più GitHub: prima di un’ondata di lavoro, fare una copia di sicurezza di `contenuti/`.

## Modo di lavorare richiesto dall’utente

- Prima di iniziare un lavoro, indicare brevemente modello e livello di impegno consigliati.
- Mettere in discussione le scelte dell’utente quando ci sono ragioni per farlo, con argomenti.
- Chiudere le questioni aperte con domande a risposta multipla.
- Poche sigle e poche forme contratte.
- I controlli automatici dicono che un percorso è ben formato e leggibile, non che funziona con un ragazzo: dirlo sempre in modo esplicito.
