# How to publish this repo on GitHub

You don't need the command line if you don't want it — option A is fully in the browser.

## Option A — browser only (easiest)
1. Go to github.com → **New repository**.
2. Name it `amex-campus-challenge-2026` (or similar). Set it **Public**. Don't add a README (this repo has one).
3. On the empty repo page, click **uploading an existing file**.
4. Drag in every file/folder from this repo **except** the `data/` folder and `predictions.csv` (never upload the competition data).
5. Commit. Done — your live link is `github.com/<your-username>/amex-campus-challenge-2026`.

## Option B — command line
```bash
cd amex-campus-challenge-2026
git init
git add README.md experiment_log.md requirements.txt .gitignore src/
git commit -m "Profitability framework: reverse-engineering via controlled experiments"
git branch -M main
git remote add origin https://github.com/<your-username>/amex-campus-challenge-2026.git
git push -u origin main
```
(The `.gitignore` already blocks `data/`, `*.csv` and `*.xlsx`, so the dataset can't be pushed by accident.)

## On your resume / LinkedIn
Link it as: **[GitHub](https://github.com/<your-username>/amex-campus-challenge-2026)** next to the project bullet.
Pin the repo on your GitHub profile so it shows up first.

## Before you make it public — a 2-minute checklist
- [ ] No data files committed (check the repo shows only code + markdown).
- [ ] README renders correctly (GitHub shows it automatically on the repo home).
- [ ] Your name is in the README footer (add it).
- [ ] Update `<your-username>` in any links.
