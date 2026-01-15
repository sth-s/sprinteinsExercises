describe("To-Do App - Cypress Tests", () => {
  beforeEach(() => {
    // Besuche die App vor jedem Test
    cy.visit("/");
  });

  it("should add a new task", () => {
    // Aufgabe: Schreibe einen Test, um sicherzustellen, dass eine neue Aufgabe hinzugefügt wird.
  });

  it("should mark a task as completed", () => {
    // Aufgabe: Schreibe einen Test, um sicherzustellen, dass eine Aufgabe als "completed" markiert wird.
  });

  it("should delete a task", () => {
    // Aufgabe: Schreibe einen Test, um sicherzustellen, dass eine Aufgabe gelöscht wird.
  });

  it("should edit a task", () => {
    // Aufgabe: Schreibe einen Test, um sicherzustellen, dass der Titel einer Aufgabe bearbeitet werden kann.
  });

  it("should search for tasks", () => {
    // Aufgabe: Schreibe einen Test, um sicherzustellen, dass die Suchfunktion korrekt funktioniert.
  });

  it("should persist tasks after page reload", () => {
    // Aufgabe: Schreibe einen Test, um sicherzustellen, dass Aufgaben nach einem Seiten-Reload erhalten bleiben.
  });

  it("should show validation error for empty input", () => {
    // Aufgabe: Schreibe einen Test, um sicherzustellen, dass keine leeren Aufgaben hinzugefügt werden können.
  });
});
