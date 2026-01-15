const express = require("express");
const bodyParser = require("body-parser");
const fs = require("fs");
const path = require("path");

const app = express();
app.use(bodyParser.json());
app.use(express.static("public"));

const FILE_PATH = path.join(__dirname, "db/todos.json");

let todos = [];

// Lade vorhandene Aufgaben aus der JSON-Datei
function loadTodos() {
  if (fs.existsSync(FILE_PATH)) {
    const data = fs.readFileSync(FILE_PATH, "utf-8");
    todos = JSON.parse(data);
  }
}

// Speichere aktuelle Aufgaben in die JSON-Datei
function saveTodos() {
  fs.writeFileSync(FILE_PATH, JSON.stringify(todos, null, 2));
}

loadTodos();

// Endpunkte
app.get("/todos", (req, res) => {
  const { search } = req.query;
  if (search) {
    const filteredTodos = todos.filter((todo) =>
      todo.title.toLowerCase().includes(search.toLowerCase())
    );
    return res.json(filteredTodos);
  }
  res.json(todos);
});

app.post("/todos", (req, res) => {
  const { title, category } = req.body;
  if (!title || !category) {
    return res.status(400).json({ error: "Title and category are required" });
  }
  const newTodo = { id: Date.now(), title, category, completed: false };
  todos.push(newTodo);
  saveTodos();
  res.status(201).json(newTodo);
});

app.put("/todos/:id", (req, res) => {
  const { id } = req.params;
  const { title } = req.body;
  const todo = todos.find((t) => t.id == id);
  if (!todo) {
    return res.status(404).json({ error: "Todo not found" });
  }
  if (title) {
    todo.title = title;
  }
  todo.completed = !todo.completed;
  saveTodos();
  res.json(todo);
});

app.delete("/todos/:id", (req, res) => {
  const { id } = req.params;
  todos = todos.filter((t) => t.id != id);
  saveTodos();
  res.status(204).send();
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
