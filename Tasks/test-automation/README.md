# Cypress-Testaufgabe: To-Do App

Willkommen zu Deiner Testaufgabe! Deine Aufgabe ist es, Cypress-Tests für eine einfache To-Do-App zu schreiben. Die App ermöglicht es, Aufgaben hinzuzufügen, zu bearbeiten, zu löschen, als erledigt zu markieren und nach Aufgaben zu suchen. `http://localhost:3000`

## Anforderungen

### 1. Testfälle erstellen

Schreibe Testfälle für die folgenden Funktionen:

- **Aufgabe hinzufügen**: Teste, ob eine neue Aufgabe hinzugefügt werden kann und korrekt angezeigt wird.
- **Aufgabe abschließen**: Teste, ob eine Aufgabe als "completed" markiert wird und die Darstellung sich entsprechend ändert.
- **Aufgabe löschen**: Teste, ob eine Aufgabe gelöscht werden kann und nicht mehr sichtbar ist.
- **Aufgabe bearbeiten**: Teste, ob der Titel einer bestehenden Aufgabe bearbeitet werden kann.
- **Aufgaben suchen**: Teste die Suchfunktion, indem Du nach bestimmten Aufgaben suchst.
- **Datenpersistenz**: Teste, ob Aufgaben auch nach einem Seiten-Reload erhalten bleiben.

### 2. Fehlertests

- Teste, dass keine leeren Aufgaben hinzugefügt werden können.

### 3. Teststrategie

- Struktur: Organisiere die Tests logisch.
- Kommentare: Kommentiere die wichtigsten Schritte in Deinem Code.

### 4. Nutzung von Cypress

- Nutze die relevanten Cypress-Befehle wie `cy.get()`, `cy.contains()`, `cy.should()` usw.
- Falls nötig, erstelle benutzerdefinierte Befehle in `cypress/support/commands.js`.

---

## Setup

### Vorbereitung

1. Die To-Do-App läuft unter der Adresse `http://localhost:3000`. Stelle sicher, dass die Anwendung lokal gestartet ist.
2. Starten von Cypress:
   ```bash
   npx cypress open
   ```
