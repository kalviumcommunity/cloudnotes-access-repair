# CA 2 — Repair CloudNotes Access and Verify Its Data

## Problem statement

CloudNotes runs locally with PostgreSQL, but its web page is unreachable and its database port is unnecessarily published. Fix both settings, then prove a saved note survives an application restart.

**Duration:** 30 minutes after setup · **Marks:** 20 · **Submission:** one PDF.

Use free local Docker Engine with Compose v2 and Python 3.10+ on your computer. No cloud account or paid service required. Setup/downloads must finish before assessment starts.

## Broken repository

https://github.com/kalviumcommunity/cloudnotes-access-repair

Clone or download repository, enter its folder and run:

```sh
docker compose build
docker compose up -d --wait
```

This starts the supplied app and database. The initial host request failure is intentional. Host ports 18095 and 15495 must be available. Do not use real credentials; repository contains disposable local demo credentials only.

**Allowed edits:** only `BIND` and the database `ports` entry in `compose.yaml`. Preserve application code, database credentials, internal ports, health checks, network and named volume. Do not change your computer's firewall.

## Task 1 — Restore application access (6 marks, 8 minutes)

1. Run `python3 client.py list` and capture original connection failure.
2. Confirm app responds inside its container:
   ```sh
   docker compose exec -T app python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8080/notes').read().decode())"
   ```
3. Correct app's `BIND` value so it accepts traffic through its published port. Recreate it using `docker compose up -d --wait app`.
4. Run `python3 client.py list` again; show HTTP 200. Explain loopback-only binding versus accepting container-network traffic in one sentence.

**Screenshot label: Task 1 — Before and after access.** Include failure, inside response, successful host response and corrected setting; use multiple screenshots if needed.

## Task 2 — Remove direct database exposure (7 marks, 8 minutes)

1. Run `python3 probe_db.py`; capture the initially reachable host database port.
2. Remove database service's host `ports` publication only. Keep app host port and internal database connection unchanged. Run `docker compose up -d --wait`.
3. Run `python3 probe_db.py` again; it must report host database port closed. Show `docker compose ps` with database running but no host-port mapping for it.
4. Run `python3 client.py list`; show app still reads notes successfully. Explain in one sentence that the app reaches PostgreSQL using its service name/internal port, not the removed host port.

**Screenshot label: Task 2 — Database restricted, app still works.** Include before/after probe, service status, corrected configuration and successful app read.

This proves removal of this local host-port publication, not a test from a real public internet machine or proof of a complete firewall policy. Internal `5432/tcp` in status is normal; it must not show `15495->5432`.

## Task 3 — Verify note persistence (7 marks, 9 minutes)

1. Run `python3 client.py add "CA2 persistence check"`. Record returned note ID and text.
2. Run `docker compose restart app`, wait up to 5 seconds for startup, then run `python3 client.py list`.
3. Show the same ID and text remain readable. Include `docker compose ps` showing both services running.
4. Write two short findings: (a) why restarting app does not delete PostgreSQL data; (b) why this test alone does not prove recovery after losing database storage, and why a backup is needed.

**Screenshot label: Task 3 — Same note after restart.** Include created note, actual restart command, later read and service status. Compare the exact ID/text; an unrelated note is not persistence proof.

## Submission guidelines (5 minutes reserved)

Upload **one PDF only**, with three task headings, labelled genuine terminal screenshots, short requested explanations and corrected `compose.yaml` (text or readable screenshot) once. Multiple screenshots per task allowed; show all requested results readably. No repo URL, fork, branch, video, ZIP or separate code submission required. No extra marks for filename or presentation.

Cleanup after capturing evidence: `docker compose down`. Do not use `down -v`; it deletes exercise database volume. Do not remove unrelated containers/volumes.

