from fabric import task
from invoke import Context
import subprocess
from datetime import datetime
import requests
import os

LOG_FILE = "/mnt/shield/logs/deploy.log"
WEBHOOK_URL = os.getenv("DEPLOY_WEBHOOK_URL")
VAULT_ADDR = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")

def check_vault_unsealed(c):
    try:
        resp = requests.get(f"{VAULT_ADDR}/v1/sys/seal-status", timeout=5)
        if resp.status_code == 200 and not resp.json().get("sealed", True):
            print("🔓 Vault is unsealed and ready.")
            return True
        else:
            print("❌ Vault is sealed. Aborting deployment.")
            return False
    except Exception as e:
        print(f"❌ Failed to contact Vault: {e}")
        return False

def notify(message: str):
    if WEBHOOK_URL:
        try:
            requests.post(WEBHOOK_URL, json={"content": message})
            print("📡 Notification sent.")
        except Exception as e:
            print(f"⚠️ Failed to send webhook: {e}")
    else:
        print("ℹ️ No webhook URL set. Skipping notify.")

def estimate_cost():
    result = subprocess.run(["docker", "ps", "-q"], capture_output=True, text=True)
    num_containers = len(result.stdout.strip().splitlines())
    cost = num_containers * 0.01
    return cost

@task
def all(c: Context):
    """Deploy everything: secrets → restart → healthcheck."""
    if not check_vault_unsealed(c):
        notify("❌ XO Deploy aborted: Vault is sealed or offline.")
        return

    with open(LOG_FILE, "a") as log:
        log.write(f"\n=== 🚀 Deployment started at {datetime.now()} ===\n")

    print("🔐 Loading secrets into Vault...")
    c.run("xo-fab vault.load_secrets", pty=True)

    print("♻️ Restarting all containers...")
    c.run("xo-fab docker.restart_all", pty=True)

    print("❤️‍🔥 Running container healthcheck...")
    c.run("xo-fab infra.container-healthcheck", pty=True)

    cost = estimate_cost()
    notify(f"✅ XO Deploy complete. Estimated cost: ${cost:.2f}")
    notify("✅ XO Deploy complete. Secrets loaded, containers restarted, health verified.")

    with open(LOG_FILE, "a") as log:
        log.write(f"✅ Deployment completed at {datetime.now()}\n")

    print("✅ All systems go. Deployment complete.")

@task
def deploy_dashboard(c, name="xo-dy-mission-ui"):
    """
    Pull latest code and deploy the XO dashboard or mission UI.
    Defaults to 'xo-dy-mission-ui'.
    """
    repo = f"https://github.com/XOwlPost/{name}.git"
    path = f"/mnt/shield/xo-dashboards/{name}"

    print(f"🚀 Deploying dashboard '{name}' to: {path}")
    c.run(f"mkdir -p {path}")

    with c.cd(path):
        if c.run("test -d .git", warn=True).ok:
            c.run("git pull")
        else:
            c.run(f"git clone {repo} .")

        c.run("npm install")
        c.run("npm run build")

    print(f"✅ Deployment complete at {path}")
