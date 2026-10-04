# App Template

A reusable, Python-first development template for turning a business idea into
a well-planned, tested software project. It provides a safe development
baseline, GitHub-based delivery workflow, and an optional integration with
OpenAI's upstream Symphony preview.

Start from the [V1 release](https://github.com/successbycs/template/releases/tag/v1.0.0),
not from a blank repository.

## What this template gives you

- A reproducible Python 3.12, `uv`, Docker Compose, and VS Code Dev Container
  development environment.
- Built-in quality checks: Ruff, pytest, Markdown-link checking, and a safe
  local self-test/demo.
- A bootstrap command that changes the project name, Python package name, and
  GitHub target when you create a new product repository.
- GitHub Issue templates and a lightweight, specification-driven workflow for
  moving from requirements to milestones, small reviewable tasks, and releases.
- Optional upstream [OpenAI Symphony](https://github.com/openai/symphony)
  v0.0.3 coordination for deliberately assigned Codex work.

It deliberately does **not** include a business application, production
website, customer data, cloud deployment, credentials, or automatic deployment
pipeline. Those belong in the product repository you create from this template.

## The simple model

```text
Business idea
    ↓
Requirements and MVP scope
    ↓
Architecture and delivery plan
    ↓
GitHub milestones and dependency-ordered Issues
    ↓
Codex or optional Symphony implementation
    ↓
Human review, integration, and product release
```

GitHub is the durable source of truth for code, Issues, milestones, and review
history. Chat helps create and execute the work; it is not the record of the
product decision.

## Start a new product

1. Create a new repository from the V1 release. Do not build the product in
   this template repository.
2. Clone the new repository, then start the development environment using
   [Getting Started](GETTING_STARTED.md).
3. Bootstrap the copied repository with its own identity:

   ```bash
   python scripts/bootstrap_template.py \
     --project-name business-website \
     --package-name business_website \
     --github-repository OWNER/business-website
   ```

4. Create the product documents and turn them into approved, dependency-ordered
   GitHub Issues.
5. Implement one reviewed Issue at a time, verify it, and keep the reviewer in
   control of merging and release.

The full step-by-step process, including prompts you can use with Codex, is in
the [New Project Guide](docs/template/NEW_PROJECT_GUIDE.md).

## Run this template locally

The supported development baseline is Windows with WSL2, Docker Desktop, and
VS Code Dev Containers. Keep the checkout in the WSL filesystem.

From the repository root:

```bash
docker compose build
docker compose run --rm app uv sync --locked --group dev
docker compose run --rm app uv run python scripts/verify.py
docker compose run --rm app uv run app-template health
docker compose run --rm app uv run app-template self-test
docker compose run --rm app uv run app-template demo --no-op
```

The self-test and demo use only a local SQLite audit database. They do not call
an external service. See [Getting Started](GETTING_STARTED.md) for setup,
troubleshooting, bootstrap details, and the optional Dev Container workflow.

## Optional Symphony coordination

Symphony is optional. It is an upstream scheduler that can select one
deliberately eligible GitHub Issue, give its context to Codex in an isolated
workspace, and return the resulting change for human review.

The V1 baseline intentionally keeps this conservative:

- one worker at a time;
- an operator starts it deliberately;
- only explicitly eligible Issues can run;
- no automatic merge, deployment, customer contact, or approval;
- GitHub remains the queue and review record.

It does not replace product planning, architecture decisions, testing, or human
accountability. Read the [Symphony Operator Guide](docs/guides/SYMPHONY_OPERATOR.md)
before enabling it.

## Where Docker and volumes fit

Docker here is a **development environment**, not a public website deployment.
It helps every developer run the same tools locally. A future product—such as
`business-website`—may later add its own production Docker image and hosting
configuration when its requirements are known.

A [Docker volume](https://docs.docker.com/engine/storage/volumes/) is optional
persistent storage for a development workspace on the Docker host. It is useful
when you later run a private remote development container. The volume is not
the V1 master copy and does not synchronise itself with GitHub:

```text
GitHub release/tag = portable source of truth and history
Docker volume      = one host's persistent working copy
Production image   = the separately built, deployable product
```

Commit and push code regularly; do not rely on a Docker volume as the only
backup of a project.

## Learn more

- [Getting Started](GETTING_STARTED.md) — install, run, verify, and bootstrap.
- [New Project Guide](docs/template/NEW_PROJECT_GUIDE.md) — turn a business
  idea into a product repository and delivery plan.
- [Documentation index](docs/INDEX.md) — architecture, workflows, operations,
  and quality guidance.
- [AGENTS.md](AGENTS.md) — instructions for coding agents working in this
  repository.
