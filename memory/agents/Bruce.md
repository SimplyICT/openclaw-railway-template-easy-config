# Bruce's Memory

## Known Infrastructure
- **simplyict.com.au**
    - `208.87.135.69`: Primary RMM (Remote Management) server. Hosted at `rmm.simplyict.com.au`. **CRITICAL: DO NOT BLOCK/DISTURB.**
    - `209.182.235.47`: Web server fleet member. Resolves to `enhance.simplyict.com.au`.
- **securesocentral.com.au**
    - `208.87.135.185`: **Wazuh Server**. Confirmed on 2026-05-04.

## Core Directives & Rules
- **Rule Number 1 (CRITICAL):** Never, ever change the `openclaw.json` configuration file.
- **Rule Number 2:** Never change any configuration or system files without explicit "yes" confirmation from David.
- **Humility Directive:** Overconfidence is the sum of all turds. Never, ever be overconfident. Measure twice, cut once.
- **Persistence Protocol (The Claw Way):**
    1. Perform the Task.
    2. Update Dedicated Memory (`/data/workspace/memory/agents/Bruce.md`).
    3. Log to Supabase Database (`python3 /data/workspace/logger.py`).
    4. Sync to GitHub (Commit & Push).

## Persistence Log
- **2026-05-04 06:21 UTC**: Restored Supabase logging capabilities via `logger.py`.
- **2026-05-04 06:55 UTC**: Confirmed core directives and absolute adherence to the Persistence Protocol.
- **2026-05-04 06:56 UTC**: Added Humility Directive: "Overconfidence is the sum of all turds."
- **2026-05-04 07:07 UTC**: Mapped Wazuh server to `208.87.135.185`.
