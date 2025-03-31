# 🤖 XO GitHub Bot Integration — `NFTonymontana`

This guide outlines how to activate and use the GitHub user [`NFTonymontana`](https://github.com/NFTonymontana) as an **automated commit agent** for Genesis, AppAgent, or any local LLMs (e.g. Ollama, AutoGPTQ).

---

## 📌 When To Use the Bot

Use `NFTonymontana` to commit changes **not authored manually**, such as:

- Local LLM-generated code or config
- Agent0 or AppAgent output files
- Genesis mission logs or state snapshots
- XO-Dy user-generated content (kids' drawings, missions, etc.)
- VaultBot updates to `.env`, secrets templates, or notes

---

## 🔐 Step 1: Generate a Personal Access Token (PAT)

From the `NFTonymontana` GitHub account:

1. Go to **Settings → Developer Settings → Personal access tokens → Tokens (classic)**
2. Click **"Generate new token"**
3. Name it: `XO Auto Commit`
4. Select scopes:
   - `repo` ✅
   - `workflow` ✅
   - *(optional)* `admin:repo_hook` if webhook needed

Copy the token and store it securely in:
- `.env` as `GITHUB_BOT_TOKEN`
- Or Replit Secrets / HashiCorp Vault

---

## ⚙️ Step 2: Configure Git for Bot Identity

In your environment (Fabric, container, etc.):

```bash
git config --global user.name "XO Assistant"
git config --global user.email "NFTonymontana@users.noreply.github.com"
