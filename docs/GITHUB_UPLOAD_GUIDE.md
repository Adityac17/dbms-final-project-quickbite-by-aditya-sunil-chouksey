# Uploading QuickBite to GitHub: Step-by-Step

These steps take you from this folder to a public (or private) GitHub repository. Run every command in **Terminal** from the project folder.

```bash
cd "/Users/adityac17/Documents/DBMS/final project"
```

> The folder name contains a space, so the quotes around the path are required.

---

## Step 0: Checks before you upload

Tick off each item:

- [ ] **Your details are in the README.** Add your name, roll number and section near the top of `README.md`, e.g.:
  ```markdown
  **Submitted by:** Your Name · Roll No. XXXX · B.Tech CSE (AI) 2025–29, Section X
  ```
- [ ] **Everything builds cleanly.** Run `./run_all.sh`. It should end with `Done.` and print no `ERROR` lines.
- [ ] **The README matches the outputs.** Re-running `./run_all.sh` changes the index-demo timings. If you re-run it, update the two millisecond values in the README's indexing table to match `outputs/05_index_demo_output.txt`.
- [ ] **No secrets.** This project has no passwords or API keys, and the sample emails use `example.com`. Keep it that way.
- [ ] **`.gitignore` exists.** It's already in the folder and keeps the macOS `.DS_Store` file out of the repo.

---

## Step 1: Check that Git is installed and configured

```bash
git --version
```

If it prints a version, Git is installed. If not, macOS will offer to install the Command Line Tools. Accept that.

Then check your identity, since it appears on every commit:

```bash
git config --global user.name
```

```bash
git config --global user.email
```

If either one is empty, set it. Use the same email as your GitHub account:

```bash
git config --global user.name "Your Name"
```

```bash
git config --global user.email "you@example.com"
```

---

## Step 2: Turn the folder into a Git repository

```bash
git init -b main
```

`-b main` names the first branch `main`, which is GitHub's default.

---

## Step 3: Stage the files and check what will be uploaded

```bash
git add .
```

```bash
git status
```

You should see **these 24 files**, and **no** `.DS_Store`:

```
.gitignore
README.md
run_all.sh
docs/CODE_WALKTHROUGH.md
docs/GITHUB_UPLOAD_GUIDE.md
docs/PRESENTATION_SCRIPT.md
docs/QUERY_PRACTICE.md
docs/VIVA_NOTES.md
docs/er_diagram.png
docs/er_diagram.svg
docs/er_diagram_chen.drawio
docs/er_diagram_chen.png
docs/er_diagram_chen.svg
docs/normalization.md
outputs/00_row_counts.txt
outputs/04_queries_output.txt
outputs/05_index_demo_output.txt
outputs/06_integrity_tests_output.txt
sql/01_schema.sql
sql/02_indexes.sql
sql/03_seed_data.sql
sql/04_queries.sql
sql/05_index_demo.sql
sql/06_integrity_tests.sql
```

If something is listed that shouldn't be, unstage it with `git rm --cached <file>` and add it to `.gitignore`.

---

## Step 4: Make the first commit

```bash
git commit -m "QuickBite DBMS case study: schema, data, queries, index demo, docs"
```

---

## Step 5: Create the repository on GitHub

**Option A: GitHub CLI (fastest).** You're already logged in to the `gh` CLI. This command creates the repo, connects it and pushes, all at once:

```bash
gh repo create quickbite-dbms --public --source=. --remote=origin --push
```

- Use `--private` instead of `--public` if only you (and people you invite) should see it.
- Change `quickbite-dbms` to any repo name you like.
- If you used this option, **skip Step 6.**

**Option B: Website.**
1. Go to https://github.com/new
2. Enter the repository name `quickbite-dbms`, choose Public or Private, and **leave every "Initialize" box unticked**. No README, no .gitignore, no license. You already have these files, and an initialised repo causes a "rejected" error in Step 6.
3. Click **Create repository**, then copy the HTTPS URL it shows.

---

## Step 6: Connect and push (Option B only)

```bash
git remote add origin https://github.com/Adityac17/quickbite-dbms.git
```

```bash
git push -u origin main
```

`-u` remembers the connection, so later you only need to type `git push`.

If you're asked for a password, GitHub **does not accept your account password**. Use one of these instead:
- Run `gh auth login`, then push again. *(Easiest.)*
- Or create a **Personal Access Token** at GitHub → Settings → Developer settings → Tokens, and paste it as the password.

---

## Step 7: Check the repository on GitHub

Open `https://github.com/Adityac17/quickbite-dbms` and check that:
- The README shows on the front page, with the **ER diagram image** displayed.
- The links in the deliverables table open the right files.
- `docs/QUERY_PRACTICE.md` shows collapsible **Hint** and **Solution** sections.

Then prove it works from a fresh download. This clones into a temporary folder and rebuilds under a different DB name, so your own `quickbite` database is left alone:

```bash
cd /tmp && git clone https://github.com/Adityac17/quickbite-dbms.git && cd quickbite-dbms && DB=quickbite_clonetest ./run_all.sh
```

It should end with `Done.` Then clean up the test database:

```bash
dropdb quickbite_clonetest
```

---

## Updating the repository later

Whenever you change something:

```bash
git add .
```

```bash
git commit -m "Describe what you changed"
```

```bash
git push
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `fatal: not a git repository` | You're in the wrong folder. `cd` into the project folder (Step 0). |
| `! [rejected] main -> main (fetch first)` | The GitHub repo was created with a README. Run `git pull origin main --rebase`, then `git push`. |
| `remote origin already exists` | Run `git remote set-url origin <correct URL>` |
| `Permission denied` / `Authentication failed` | Run `gh auth login`, or use a Personal Access Token instead of your password. |
| `./run_all.sh: Permission denied` after cloning | Run `chmod +x run_all.sh`, then commit and push. |
| `.DS_Store` got committed | Run `git rm --cached .DS_Store`, then `git commit -m "Remove .DS_Store"`, then `git push`. |
| `psql: command not found` on another machine | Install PostgreSQL: `brew install postgresql@18`, then `brew services start postgresql@18`. |
