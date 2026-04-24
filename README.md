# 🌐 Language Learning Resource Finder
 ---
### Semester IV · Introduction to Agentic AI Systems
A fully deployed, end-to-end AI agent that finds personalised language learning
resources and drafts a 30-day study plan — using **Gemini API (free)** +
**Tavily Search (free)** + **LLM-as-Judge**.

---

## 🏗️ Architecture

```
User Input (language + level)
        │
        ▼
┌──────────────────────┐
│  Agent 1             │  ← calls Tavily Search (real web results)
│  Resource Finder     │  ← sends results to Gemini for synthesis
└──────────┬───────────┘
           │ 6 resources
           ▼
┌──────────────────────┐
│  Agent 2             │  ← picks best 3 for the learner's level
│  Curator             │  ← explains why each one fits
└──────────┬───────────┘
           │ curated pack
           ▼
┌──────────────────────┐
│  Agent 3             │  ← writes a 4-week, 20-30 min/day plan
│  Plan Writer         │
└──────────┬───────────┘
           │ plan
           ▼
┌──────────────────────┐
│  LLM-as-Judge        │  ← scores on 3 rubric dimensions (0–100)
│  Quality Evaluator   │  ← returns verdict + improvement tips
└──────────────────────┘
```

## 📁 Project Structure

```
language-agent/
├── app.py                    # Streamlit UI + agent pipeline
├── requirements.txt
├── Procfile                  # Railway deployment
├── .gitignore
├── .streamlit/
│   ├── config.toml           # Theme + server config
│   └── secrets.toml          # API keys (DO NOT commit)
└── agents/
    ├── __init__.py
    ├── llm.py                # Shared Gemini client
    ├── resource_finder.py    # Agent 1 — Tavily Search + Gemini
    ├── curator.py            # Agent 2 — pick best 3
    ├── plan_writer.py        # Agent 3 — 30-day plan
    └── judge.py              # LLM-as-Judge — rubric scoring
```

## 🔑 Free API Keys (required)

### 1. Gemini API Key (Google AI Studio)
1. Go to https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click **"Create API key"**
4. Copy the key — it's free (15 requests/min, 1M tokens/day)

### 2. Tavily Search API Key
1. Go to https://app.tavily.com
2. Sign up for free
3. Copy your API key from the dashboard
4. Free tier: 1,000 searches/month

---

## 🖥️ Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/language-agent.git
cd language-agent

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API keys to .streamlit/secrets.toml
#    (this file is gitignored — safe to edit locally)
#    Edit .streamlit/secrets.toml and paste your keys

# 5. Run
streamlit run app.py
```

Open http://localhost:8501 in your browser.
public host:-https://language-learning-resource-finder.streamlit.app/

---

## 🚀 Deploy to Railway (recommended — free tier)

Railway gives you a free public URL with zero config.

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/YOUR_USERNAME/language-agent.git
git push -u origin main
```

### Step 2 — Deploy on Railway
1. Go to https://railway.app and sign in with GitHub
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repo
4. Railway auto-detects the `Procfile` and deploys

### Step 3 — Add environment variables
In your Railway project → **Variables** tab, add:
```
GEMINI_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

### Step 4 — Get your public URL
Railway gives you a URL like `https://language-agent-production.up.railway.app`
That's your submission URL! ✅

---

## 🚀 Deploy to Streamlit Cloud (alternative — also free)

1. Push your code to GitHub (same as above)
2. Go to https://share.streamlit.io
3. Connect your GitHub and select this repo + `app.py`
4. Under **Advanced settings → Secrets**, paste:
```toml
GEMINI_API_KEY = "your_key_here"
TAVILY_API_KEY = "your_key_here"
```
5. Click **Deploy** — you get a free public URL ✅

---

## ⚖️ LLM-as-Judge Rubric

| Dimension | What it measures | Weight |
|---|---|---|
| Resource Quality | Resources matched to level & language | 33% |
| Plan Structure | Realistic, clear, actionable 30-day plan | 33% |
| Personalization | Tailored to the specific learner | 33% |

Scores are 0–100 per dimension. The judge also returns a one-line verdict and 2–3 improvement suggestions.

---

## 🛠️ Tech Stack

| Component | Tool | Cost |
|---|---|---|
| LLM | Gemini 1.5 Flash | Free (Google AI Studio) |
| Web Search | Tavily Search | Free (1000 searches/month) |
| UI | Streamlit | Free |
| Deployment | Railway or Streamlit Cloud | Free |

---

## 👥 Team

| Role | Responsibility |
|---|---|
| Architect & Integrator | Problem definition, architecture, API integrations |
| Builder & Deployer | Agent implementation, UI, deployment |

---

*Semester IV · B.E. Electronics & Communication · Introduction to Agentic AI Systems*
