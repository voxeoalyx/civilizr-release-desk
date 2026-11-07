# Civilizr Release Desk

**Flip the Switch** · Personal / Creative track · human-gated release room for indie music & art.

> Agents prep the pack. I decide.

A Switch room where a release agent reads a local `release.json`, posts a
checklist + proposed Instagram caption + **READY/BLOCKED**, and only writes
`APPROVED` to an approval log after a human ✅.

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────────┐
│ Mattermost  │◄───►│    Switch    │◄───►│ civilizr-release    │
│ (or Discord)│     │  room+bridge │     │ agent (Claude/Codex)│
└─────────────┘     └──────────────┘     └──────────┬──────────┘
                                                    │
                                         python3 scripts/release_check.py
                                                    │
                                         data/release.json
                                         data/approval-log.jsonl
                                                    ▲
                     human ✅ in thread ─────────────┘ (only path to APPROVED)
```

Flow: **chat → Switch room → release agent → checklist/caption → human ✅ → approval log.**

## Why Switch is central

Without Switch there is no shared room, no chat-native agent teammate, and no
human gate in the same thread as the checklist. The Python CLI is the brain of
the check; Switch is how a person and that agent finish the task together.

## Repo layout

| Path | Role |
| --- | --- |
| `data/release.json` | Sample release pack (ships BLOCKED — lyrics missing) |
| `data/release.ready.json` | Fixture with required assets present |
| `data/approval-log.jsonl` | Append-only APPROVED events |
| `scripts/release_check.py` | `/release-check` logic + `--approve` (simulates ✅) |
| `switch/civilizr-release-desk.template.yaml` | Importable Switch room+agent template |
| `docs/RESEARCH.md` | Hackathon/docs notes, install commands, blockers |

## Local CLI (works without Switch)

```bash
python3 scripts/release_check.py
python3 scripts/release_check.py --release data/release.ready.json
python3 scripts/release_check.py --release data/release.ready.json --approve --by alyx
```

Exit code `0` = READY, `1` = BLOCKED (or refused approve).

## Mac install (Alyx, home ~9:30 AM ET Thu Nov 5)

1. Install **Docker Desktop for Mac (Apple silicon)**: https://www.docker.com/products/docker-desktop/ → open it, wait for "Engine running".
2. Download **Switch Console arm64 .dmg** from https://github.com/sandbox-quantum/switch/releases/latest → drag to Applications → open (right-click → Open if Gatekeeper complains).
3. Console → **Run a server on this computer** → Start (bundled Mattermost).
4. `git clone [repo] ~/civilizr-release-desk` and `python3 scripts/release_check.py` to confirm the CLI.
5. Import `switch/civilizr-release-desk.template.yaml`, set `directory` to the clone, bridge = Mattermost. Then follow step 7+ below.

## Switch setup (Mattermost — recommended)

**On the Grok Bot Linux box:** Docker Engine is installed (`docker` 29.x). There is no systemd here (PID 1 is `tini`), so if the daemon is down run `sudo box-docker-start`. User `box` is in the `docker` group (`sg docker -c '…'` or a new login). **Switch Console was not installed** — it is an Electron GUI and is not useful headless; run Console on a machine with a screen (macOS preferred) pointing at this repo.

1. Install **Docker** and keep it running.
2. Install **Switch Console** for your OS:
   - macOS / Windows / Linux builds: https://github.com/sandbox-quantum/switch/releases/latest
   - Linux x64: `sudo apt install ./switch-console-amd64.deb`
3. Open Console → **Run a server on this computer** → Start.
   Mattermost is created and connected for you. Use **Sign-in details…** on
   the Messaging apps row to open Mattermost.
4. Sign in / link an AI coding agent (Claude Code, Codex, Cursor, OpenCode, …).
5. Clone this repo to the machine Console will run the agent on.
6. Templates → **Import template** →
   `switch/civilizr-release-desk.template.yaml` → set `directory` to the clone
   → create room (bridge = Mattermost).
7. In the Mattermost channel, say `/release-check` or `@civilizr-release check release`.
8. On READY, react ✅ (or reply `APPROVE`). The agent re-checks and appends
   the approval log.

### Discord (optional, slower)

Needs a Discord Developer Portal application: bot token, guild id, privileged
intents (Server Members + Message Content), scopes `bot` + `applications.commands`,
permissions including Manage Webhooks and Add Reactions. See
https://docs.switchagents.ai/switch-rooms/deploy/messaging-apps/discord

## Demo script (~75s)

| Time | Screen | Voiceover |
| --- | --- | --- |
| 0–10s | Civilizr IG / cover art | "I run Civilizr, a small music and art project. My release agents went dormant because I didn't trust them to ship." |
| 10–20s | Switch Console → Mattermost room | "With Switch, the release agent is a teammate in my chat room." |
| 20–35s | `/release-check` → BLOCKED (lyrics ❌) | "It reads my release file and tells me what's missing." |
| 35–50s | fix `lyrics.present`, re-check → READY + caption | "Fix it, re-run: READY, with a drafted Instagram caption." |
| 50–65s | react ✅ → APPROVED line in `approval-log.jsonl` | "Nothing is approved until I react. Then it's logged." |
| 65–75s | README diagram + repo link | "Agents prep, I decide. Repo: [repo]." |

## Built during the hackathon vs. prior work

**Prior (Civilizr ops, before Nov 4):** the idea of music/art/Distrokid/IG agents and my manual release checklist habits.

**Built Nov 4–7 for Flip the Switch:** this repo — `release_check.py` (checklist, READY/BLOCKED, caption, ✅-gated approval log), sample release fixtures, the Switch room template, Mattermost room wiring, README and demo.

## Hackathon notes

- Event: https://www.wemakedevs.org/hackathons/switch
- Deadline: **Sat Nov 7, 2026, 11:59 PM IST** (~1:29 PM ET)
- Submit: https://www.wemakedevs.org/hackathons/switch/submit
- Existing agents/workflows OK; Switch setup + this workflow built during Nov 4–7.
- **Do not submit until Alyx explicitly says to.**

## License

Demo code in this folder: use freely for the hackathon entry. Switch itself is
Apache-2.0 + Commons Clause — see https://github.com/sandbox-quantum/switch
