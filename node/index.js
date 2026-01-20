const express = require("express");
const path = require("path");
const session = require("express-session");

const { authenticateUser, createUser } = require("../database/db");

const app = express();
const port = process.env.PORT || 3000;

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));
app.use(express.urlencoded({ extended: false }));

// Session middleware for server-side auth.
app.use(
  session({
    secret: process.env.SECRET_KEY || "dev",
    resave: false,
    saveUninitialized: false,
  })
);

app.get("/", (req, res) => {
  res.render("public/home");
});

app.get("/login", (req, res) => {
  res.render("public/login", { error: "" });
});

app.post("/login", async (req, res) => {
  const email = (req.body.email || "").trim();
  const password = req.body.password || "";

  if (!email || !password) {
    return res.render("public/login", { error: "Inserisci email e password" });
  }

  if (!(await authenticateUser(email, password))) {
    return res.render("public/login", { error: "Credenziali non valide" });
  }

  req.session.userEmail = email;
  res.redirect("/private");
});

app.get("/register", (req, res) => {
  res.render("public/register", { error: "" });
});

app.post("/register", async (req, res) => {
  const email = (req.body.email || "").trim();
  const password = req.body.password || "";
  const confirm = req.body.password_confirm || "";

  if (!email || !password || !confirm) {
    return res.render("public/register", { error: "Completa tutti i campi" });
  }

  if (password !== confirm) {
    return res.render("public/register", { error: "Le password non coincidono" });
  }

  if (!(await createUser(email.split("@")[0], email, password))) {
    return res.render("public/register", { error: "Email già registrata" });
  }

  req.session.userEmail = email;
  res.redirect("/private");
});

app.get("/private", (req, res) => {
  const email = req.session.userEmail;
  if (!email) return res.redirect("/login");

  res.render("private/private", {
    username: email.split("@")[0],
  });
});

app.get("/logout", (req, res) => {
  req.session.destroy(() => res.redirect("/"));
});

app.use((req, res) => {
  res.status(404).render("public/404");
});

app.listen(port, () => {
  console.log(`Server running on http://127.0.0.1:${port}`);
});
