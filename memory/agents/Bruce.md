# Bruce's Memory

## Known Infrastructure
- **simplyict.com.au**
    - `208.87.135.69`: Primary RMM (Remote Management) server. Hosted at `rmm.simplyict.com.au`. **CRITICAL: DO NOT BLOCK/DISTURB.**
    - `209.182.235.47`: Web server fleet member. Resolves to `enhance.simplyict.com.au`.

## Persistence Log
- **2026-05-04 06:21 UTC**: Successfully restored Supabase logging capabilities via `logger.py` and confirmed the `agent_memories` table schema. I have committed to the strict sequence: Task -> Memory -> DB -> GitHub for every step to ensure zero data loss during session transitions. This is the Claw Way.
