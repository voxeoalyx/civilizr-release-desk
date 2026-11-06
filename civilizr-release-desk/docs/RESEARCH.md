# Flip the Switch / Switch AI — research notes

Researched 2026-11-05 (America/New_York). No accounts created, no registration, no submission.

## Key URLs

| What | URL |
| --- | --- |
| Hackathon home | https://www.wemakedevs.org/hackathons/switch |
| Schedule | https://www.wemakedevs.org/hackathons/switch/schedule |
| Submit page (exists; form fields not fully scraped) | https://www.wemakedevs.org/hackathons/switch/submit |
| Docs index | https://docs.switchagents.ai/llms.txt |
| 10-min quickstart | https://docs.switchagents.ai/switch-rooms/getting-started |
| Install Console | https://docs.switchagents.ai/switch-rooms/getting-started/install-switch-console |
| Add a server (Docker local) | https://docs.switchagents.ai/switch-rooms/getting-started/add-a-server |
| Mattermost bridge | https://docs.switchagents.ai/switch-rooms/deploy/messaging-apps/mattermost |
| Discord bridge | https://docs.switchagents.ai/switch-rooms/deploy/messaging-apps/discord |
| Room commands | https://docs.switchagents.ai/switch-rooms/resources/room-commands |
| Room templates | https://docs.switchagents.ai/switch-rooms/administer/room-templates |
| Agent protocol | https://docs.switchagents.ai/switch-rooms/internals/agent-protocol |
| GitHub | https://github.com/sandbox-quantum/switch |
| Latest Console release | https://github.com/sandbox-quantum/switch/releases/latest (0.40.1 as of research) |
| Official triage template | https://github.com/sandbox-quantum/switch/blob/main/examples/agent-templates/triage-pair.template.yaml |
| Official room template | https://github.com/sandbox-quantum/switch/blob/main/examples/room-templates/red-blue-workroom.template.yaml |
| Docs MCP | https://docs.switchagents.ai/mcp |

## Deadline (verified)

- Hacking: Nov 4 12:01 AM IST → Nov 7 11:59 PM IST
- Submissions close: **Sat Nov 7, 11:59 PM IST** ≈ **Sat Nov 7, 1:29 PM ET**
- Deliverables: public repo + demo video + README showing how Switch is used
- Track for this project: Best Personal or Creative Workflow ($2,000)

## Install (Linux x86_64)

Prereqs: Docker running, then Switch Console (desktop Electron app).

```bash
# Docker (required — Console starts the full stack in Docker)
# Install Docker Engine or Docker Desktop for your distro, then:
sudo systemctl enable --now docker   # if using Engine
docker info                          # must succeed

# Switch Console 0.40.1 — Linux x64 (early access)
# Prefer .deb on Ubuntu/Debian (AppImage needs FUSE 2; rough on 24.04+)
curl -LO https://github.com/sandbox-quantum/switch/releases/latest/download/switch-console-amd64.deb
sudo apt install ./switch-console-amd64.deb
switch-console
# If no window (Wayland/VM): 
#   switch-console --ozone-platform=x11 --disable-gpu
```

Alt AppImage:

```bash
curl -LO https://github.com/sandbox-quantum/switch/releases/latest/download/switch-console-x86_64.AppImage
chmod +x switch-console-x86_64.AppImage
./switch-console-x86_64.AppImage
```

In Console: Get started → Run server on this computer → Start → pick agent provider
(Claude Code / Codex / Cursor / OpenCode / Antigravity). Mattermost is started
and connected automatically for local servers.

## How rooms / agents / commands work

- Template YAML defines `agents:`, `room:`, optional `kickoff:` and `params:`.
- Import YAML in Console Templates, or ask switch-buddy to create the room.
- Mattermost: use `!` commands only (`!invite-agent @name`). No native slash cmds.
- Discord: `/` slash commands + `!` forms. Needs Discord Developer Portal bot
  (token + guild id, privileged intents, Manage Webhooks, Add Reactions, etc.).
- Built-in Switch commands: `!help`, `!list-agents`, `!invite-agent`, etc.
  Custom `/release-check` is **not** a Switch slash command — it is agent
  instruction text the human types; the agent runs our Python CLI.
- Reactions: Discord marks agent-working with 👀. Mattermost can show approve
  **buttons** on agent permission cards when Callback Base Url is set. Custom
  ✅ for our HITL gate is agent-instruction logic (watch for ✅ / APPROVE),
  simulated locally with `scripts/release_check.py --approve`.

## Mattermost vs Discord (recommendation)

**Mattermost = fastest path.** Bundled when Console runs a local Docker server;
Sign-in details on the connection row; no bot OAuth. Use Mattermost for demo.
Add Discord later only if you specifically want Teams-of-Discord aesthetics.

## Headless / this Linux box

- Switch Console is a **GUI Electron app**. Docs describe Linux early-access
  quirks (Wayland → use `--ozone-platform=x11 --disable-gpu`), not a headless mode.
- Sidecar can keep agents alive on a remote host after Console deploys them,
  but first-time setup still needs Console UI.
- This research box (`x86_64`): **Docker not installed**. Cannot start the local
  Switch stack here until Docker + a display (or Alyx's machine) are available.

## Signup / submit blockers (intentional)

Per task + Opportunity Scout rules: **did not** register, create accounts,
accept terms, or submit. Alyx said they want signup while at pilates; parent
must get explicit confirmation before any account creation / submit.

Submit URL to hand Alyx later: https://www.wemakedevs.org/hackathons/switch/submit
(page loads; exact form field list not fully available via fetch).

## Build blockers remaining

1. Docker on the machine that will run Switch
2. Switch Console install + GUI session (Alyx laptop preferred; box is poor fit)
3. AI coding agent signed in (Claude Code / Codex / Cursor / …)
4. Import `switch/civilizr-release-desk.template.yaml` with `directory` pointing
   at this repo clone
5. Demo video (60–90s) + public GitHub repo
6. Explicit Alyx yes before WeMakeDevs registration / final submit
