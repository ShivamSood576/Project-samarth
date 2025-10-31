# 🚀 Hugging Face Spaces Setup (Streamlit)

This is the exact process I use to get Project Samarth live on a public URL in ~15 minutes.

## 1) Create a Space
- Go to https://huggingface.co/new-space
- Name: `project-samarth` (or your choice)
- License: MIT
- SDK: `Streamlit`
- Hardware: `CPU basic` (free)
- Visibility: Public (or Private)
- Create Space → you’ll land on an empty repo page

## 2) Add code to the Space
You can push with git or upload via web. I prefer git:

```powershell
# from your local project root
# initialize if needed
git init

# commit everything
git add .
git commit -m "Deploy Project Samarth to HF Spaces"

# add HF remote (replace with your username/space)
git remote add hf https://huggingface.co/spaces/prashant001110/project-samarth

# push main branch
git push hf main
```

### If you see “Invalid credentials”

Hugging Face uses access tokens as your Git password. Create one and retry:

```powershell
# 1) Create a write token at: https://huggingface.co/settings/tokens

# 2) Clear any cached bad credentials (Windows)
git credential-manager erase https://huggingface.co

# 3) (Optional) Login once for CLI usage
huggingface-cli login

# 4) Push again — when prompted:
#    - Username: your HF username (e.g., prashant001110)
#    - Password: the access token you created
git push hf main
```

Alternatively, upload these files via the web UI:
- `app.py`
- `requirements.txt`
- `.streamlit/` (folder)
- `src/` (folder)
- `config/` (folder)
- `README.md` (this repo’s README)

## 3) Add secrets (CRITICAL)
In your Space → Settings → Repository secrets:

```
DATA_GOV_IN_API_KEY = <your data.gov.in key>
GEMINI_API_KEY      = <your Google Gemini key>
```

Save each secret. These are injected into the environment at runtime.

## 4) Build and first run
- After push, HF will auto-build the environment from `requirements.txt`
- First build takes ~2–5 minutes. See the Logs tab if something fails.
- When the Space turns green, click “App” to open the live URL.

## 5) Quick checks
- Try an example from the sidebar to validate data.gov.in connectivity
- If answers return but feel too generic, check that Gemini key is valid
- If API calls are slow, that’s expected on free tier; caching is planned

## Troubleshooting
- "Module not found": ensure the `src/` and `config/` folders were pushed
- "Rate limit exceeded": reduce repeated queries; free tier has throttling
- "Blank page": look at the Logs tab; usually a missing secret or dependency

### Seeing Docker instructions on the Space page?
That means the Space was created with the **Docker SDK**. Either switch it to **Streamlit** in Space → Settings → “Space SDK”, or create a new Space with “Streamlit”. You do not need Docker for this app.

## Cost and limits
- Free tier (CPU basic) is fine for demos
- Spaces auto-sleep after inactivity and wake on first request

## Updating the app
- Make changes locally → `git commit` → `git push hf main`
- The Space rebuilds automatically

---

That’s it. If you hit any issues, open the Logs tab in your Space and scan for the first error — it’s usually a missing secret, a typo in a path, or a version mismatch.
