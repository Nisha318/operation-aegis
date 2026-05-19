# Operation Aegis 🛡️
### DevSecOps Capstone — Skyline Financial Tech

> A fully automated, end-to-end security pipeline built on GitHub Actions.
> Four phases of defence protecting a vulnerable demo banking API.

![Phase 1 SAST + SCA](https://img.shields.io/github/actions/workflow/status/YOUR_USERNAME/operation-aegis/phase1-sast-sca.yml?label=Phase%201%20SAST%2BSCA&style=flat-square)
![Phase 2 DAST](https://img.shields.io/github/actions/workflow/status/YOUR_USERNAME/operation-aegis/phase2-dast.yml?label=Phase%202%20DAST&style=flat-square)
![Phase 3 Secrets](https://img.shields.io/github/actions/workflow/status/YOUR_USERNAME/operation-aegis/phase3-secrets.yml?label=Phase%203%20Secrets&style=flat-square)
![Phase 4 Reporting](https://img.shields.io/github/actions/workflow/status/YOUR_USERNAME/operation-aegis/phase4-reporting.yml?label=Phase%204%20Reporting&style=flat-square)

---

## Repo structure

```
operation-aegis/
├── .github/
│   └── workflows/
│       ├── phase1-sast-sca.yml       # CodeQL + Semgrep + Trivy
│       ├── phase2-dast.yml           # OWASP ZAP + Nikto  (Week 2)
│       ├── phase3-secrets.yml        # Gitleaks + TruffleHog  (Week 3)
│       └── phase4-reporting.yml      # Aggregated reports + Slack  (Week 4)
├── app/
│   ├── main.py                       # FastAPI demo app (intentionally vulnerable)
│   ├── requirements.txt              # Pinned deps — includes outdated packages
│   └── Dockerfile                    # Container image for scanning + DAST
├── tests/
│   └── test_api.py                   # Smoke tests (pytest)
├── docs/
│   └── threat-model.md               # Architecture threat model (Week 4)
└── README.md
```

---

## Intentional vulnerabilities (learning targets)

| ID | Type | Location | Detected by |
|----|------|----------|-------------|
| VULN-001 | Hardcoded credentials | `app/main.py` L14-16 | Gitleaks, TruffleHog, Semgrep |
| VULN-002 | SQL injection | `GET /account/balance` | CodeQL, Semgrep |
| VULN-003 | Command injection | `GET /admin/ping` | CodeQL, Semgrep |
| VULN-004 | Broken authentication | `POST /transfer` | Semgrep, ZAP |
| VULN-005 | Sensitive data exposure | `GET /transaction/{id}` | Semgrep, ZAP |
| VULN-006 | Outdated dependency CVEs | `requirements.txt` | Trivy SCA |
| VULN-007 | Container runs as root | `Dockerfile` | Trivy, Checkov |
| VULN-008 | Debug mode in production | `Dockerfile` CMD | Trivy |

> **All vulnerabilities are intentional.** This repo exists to generate real
> scanner findings for the capstone write-up. Do not deploy.

---

## Pipeline phases

| Phase | Workflow | Triggers | Tools |
|-------|----------|----------|-------|
| 1 — SAST + SCA | `phase1-sast-sca.yml` | PR, push to main, schedule, manual | CodeQL, Semgrep, Trivy |
| 2 — DAST | `phase2-dast.yml` | Push to main, manual | OWASP ZAP, Nikto |
| 3 — Secrets | `phase3-secrets.yml` | PR, push to main, schedule, manual | Gitleaks, TruffleHog |
| 4 — Reporting | `phase4-reporting.yml` | After Phase 1-3, manual | Aggregator, Slack |

---

## Quick start

```bash
# Clone and enter the repo
git clone https://github.com/YOUR_USERNAME/operation-aegis.git
cd operation-aegis

# Run the demo app locally
cd app
pip install -r requirements.txt
uvicorn main:app --reload

# Run tests
cd ..
pip install pytest httpx
pytest tests/ -v

# Build and inspect the container
docker build -t skyline-api ./app
docker run -p 8000:8000 skyline-api
```

Then visit `http://localhost:8000/docs` for the interactive Swagger UI.

---

## Required GitHub secrets

Add these in **Settings → Secrets and variables → Actions** before running workflows:

| Secret | Used by | Notes |
|--------|---------|-------|
| `SEMGREP_APP_TOKEN` | Phase 1 — Semgrep | Free at semgrep.dev — optional but enables dashboard |
| `SLACK_WEBHOOK_URL` | Phase 4 — Reporting | Incoming webhook from your Slack workspace |

---

## Blog post

*Coming soon — Hashnode / dev.to*

---

*DevSec Blueprint capstone · #DevSecBlueprint*
