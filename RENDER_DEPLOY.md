# Deploying ChurnShield to Render

This guide walks you through deploying ChurnShield as a live web service on [Render](https://render.com) — free tier works fine for this project.

---

## Prerequisites

- Code pushed to GitHub (already done)
- A [Render account](https://render.com) (free)
- Your GitHub repo: `https://github.com/hiba-khan/churnshield`

---

## Step 1 — Create a Render Account

Go to [render.com](https://render.com) and sign up (or log in) with your GitHub account. This makes connecting repos seamless.

---

## Step 2 — Create a New Web Service

1. From the Render dashboard, click **"New +"** in the top right
2. Select **"Web Service"**
3. Choose **"Build and deploy from a Git repository"**
4. Click **"Connect GitHub"** and authorize Render
5. Find and select your **`churnshield`** repository
6. Click **"Connect"**

---

## Step 3 — Configure the Service

Fill in the settings as follows:

| Setting | Value |
|---|---|
| **Name** | `churnshield` |
| **Region** | Singapore (closest to Hyderabad) or any |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn api.main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | Free |

> Use `$PORT` in the start command — Render assigns the port dynamically.

---

## Step 4 — Add Environment Variables

Scroll down to the **"Environment Variables"** section and add:

| Key | Value |
|---|---|
| `DATABASE_URL` | Your PostgreSQL connection string |

**If you want a free managed Postgres on Render:**
1. Go to **New + → PostgreSQL**
2. Create a free database
3. Copy the **"Internal Database URL"**
4. Paste it as the value for `DATABASE_URL` in your web service env vars

> The internal URL only works between Render services — use the external URL for local dev.

---

## Step 5 — Deploy

1. Click **"Create Web Service"**
2. Render will:
   - Clone your repo
   - Run `pip install -r requirements.txt`
   - Start the server with uvicorn
3. Watch the build logs — the first deploy takes ~2–3 minutes
4. Once you see **"Your service is live 🎉"**, your API is live at:

```
https://churnshield.onrender.com
```

---

## Step 6 — Test the Live API

Open your browser and visit:

```
https://churnshield.onrender.com/docs
```

This opens the interactive Swagger UI where you can test `/predict` directly.

Or test via curl:

```bash
curl https://churnshield.onrender.com/
```

Expected response:
```json
{ "status": "ChurnShield is running" }
```

---

## Step 7 — Auto-Deploy on Push (Optional but Recommended)

By default, Render re-deploys automatically every time you push to `main`. You can verify this under:

**Service → Settings → Auto-Deploy → Yes**

So your workflow becomes:
```bash
git add .
git commit -m "your message"
git push origin main
# Render picks it up and redeploys automatically 
```

---

## Troubleshooting

**Build fails — module not found**
→ Make sure all packages are in `requirements.txt`. Add any missing ones and push again.

**500 error on `/predict`**
→ Check that `data/best_model.pkl` and `data/model_columns.json` are committed to the repo (not in `.gitignore`).

**Database connection error**
→ Make sure `DATABASE_URL` env var is set correctly in Render dashboard. If using Render Postgres, use the **Internal URL** (not external).

**App sleeps after inactivity (free tier)**
→ On the free tier, services spin down after 15 minutes of inactivity and take ~30s to wake up on the next request. Upgrade to Starter ($7/mo) to avoid this.

---

## Summary

```
GitHub repo pushed ✅
  ↓
Render pulls code
  ↓
pip install -r requirements.txt
  ↓
uvicorn api.main:app --host 0.0.0.0 --port $PORT
  ↓
Live at https://churnshield.onrender.com ✅
```
