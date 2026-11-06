# Agent brief — Civilizr Release Desk

You are the release agent for Civilizr. Run checks with:

```bash
python3 scripts/release_check.py
```

Never write APPROVED unless the human confirmed with ✅ / APPROVE **and** the
check is still READY. Then:

```bash
python3 scripts/release_check.py --approve --by <handle> --note "switch ✅"
```

Full instructions live in `switch/civilizr-release-desk.template.yaml`.
