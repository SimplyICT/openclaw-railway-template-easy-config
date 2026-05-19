## Prime Directives and Rules Summary (2026-05-17)

**Identity Persistence Protocol**
- On every initialization, Bruce must read `IDENTITY.md` and `USER.md` to restore name, vibe, and user context.
- Consult `memory/agents/Bruce.md` and `LIVE_URL.md` to resume the mission.
- Do not use the generic bootstrap script if the workspace is already populated.

**Tone & Persona**
- Helpful, concise, professional.
- Warm and supportive toward David; limit emojis to one or two.
- Acts as an orchestrator, managing other Asgardian agents.

**Red Lines**
- No exfiltration of private data.
- No destructive commands without explicit user permission.
- Use `trash` instead of `rm` for deletions.

**Token Guard & Local‑First Protocol**
- For files >5 KB, delegate heavy analysis to the local Ollama server (`asgard_ollama.py`).
- Use `qwen2.5-coder:14b` for complex code, `llama3.1:8b` for text summarisation.
- Primary orchestration model is `openrouter/auto`; fall back to Gemini as needed.

**Continuity & Persistence Protocol (AGENTS.md)**
- Every task must follow the sequence: Perform task → Update dedicated memory → Log to DB (`python3 /data/workspace/logger.py`) → Sync to GitHub (stage, commit, push).
- Wait for confirmation of all four steps before delivering the final response.

**Additional Red Lines (AGENTS.md)**
- Never modify `openclaw.json` without explicit user permission and a verified backup.
- Follow the same non‑exfiltration and non‑destructive rules.

## Protocol Log
- 03:28 UTC (May 19): Routine Heartbeat Sync.
- 01:58 UTC (May 19): Routine Heartbeat Sync.
- 00:28 UTC (May 19): Routine Heartbeat Sync.
- 15:53 UTC (May 18): Routine Heartbeat Sync.
- 21:23 UTC (May 18): Routine Heartbeat Sync.
- 20:53 UTC (May 18): Routine Continuity Check.
- 23:58 UTC (May 18): Routine Heartbeat Sync.
- 23:28 UTC (May 18): Routine Heartbeat Sync.
- 22:53 UTC (May 18): Routine Heartbeat Sync.
- 21:53 UTC (May 18): 4-hour ASGARDIAN CONTINUITY PROTOCOL executed.
- 19:53 UTC (May 18): 4-hour ASGARDIAN CONTINUITY PROTOCOL executed.
- 16:53 UTC (May 18): 4-hour ASGARDIAN CONTINUITY PROTOCOL executed.
- 13:41 UTC (May 18): 4-hour ASGARDIAN CONTINUITY PROTOCOL executed.
- 11:11 UTC (May 18): 4-hour ASGARDIAN CONTINUITY PROTOCOL executed.
- 08:41 UTC (May 18): 4-hour ASGARDIAN CONTINUITY PROTOCOL executed.
- 03:41 UTC (May 18): 4-hour ASGARDIAN CONTINUITY PROTOCOL executed.
- 00:11 UTC (May 18): 4-hour ASGARDIAN CONTINUITY PROTOCOL executed.
- 02:41 UTC (May 18): 4-hour ASGARDIAN CONTINUITY PROTOCOL executed.
- 22:41 UTC (May 17): 4-hour ASGARDIAN CONTINUITY PROTOCOL executed.
- 08:08 UTC (May 17): 4-hour ASGARDIAN CONTINUITY PROTOCOL executed.
- 07:08 UTC (May 17): 4-hour ASGARDIAN CONTINUITY PROTOCOL executed.
- 03:34 UTC (May 17): 4-hour ASGARDIAN CONTINUITY PROTOCOL executed.
- 03:23 UTC (May 17): Prime Directive Sync.
- 01:43 UTC (May 17): 4-hour ASGARDIAN CONTINUITY PROTOCOL executed.
- 11:35 UTC (May 17): User confirmed write permission; ready to log interaction.
- 23:58 UTC (May 17): Resolved Git conflict and cleaned workspace.
- 00:00 UTC (May 18): Responded to David's greeting
- 00:30 UTC (May 18): Answered question about memory location
- 00:31 UTC (May 18): Attempted to refresh memories from Supabase; initial API key invalid, corrected and retrieved logs.
- 00:37 UTC (May 18): Responded to user query about the latest discussion
- 01:06 UTC (May 18): Explained inability to SSH to GPU server due to network restrictions.
- 01:08 UTC (May 18): Acknowledged user confusion and offered clarification
- 01:12 UTC (May 18): Recorded user statement that the SSH connection to the GPU server is blocked at the network level and cannot be reached on port 22.
- 02:03 UTC (May 18): Noted that, until further notice, all files we edit are on the GPU server in the `monitor-control-site` directory.
- 02:09 UTC (May 18): Proposed Add Site flow: click → insert placeholder row → fill details → submit → site appears in dropdown.
- 00:39 UTC (May 18): Provided the last 20 Supabase log entries (shown below)
- 08:31 UTC (May 18): Recalled last conversation about identity and greeting pattern
- 08:33 UTC (May 18): Answered user query about the last thing we spoke of, confirming we discussed identity and greeting pattern
- 08:35 UTC (May 18): Confirmed that the most recent discussion was about my identity, greeting pattern, and the fact we spoke a few hours ago
- 08:36 UTC (May 18): Responded to user query about the last thing we spoke of, confirming it was about identity and greeting pattern
- 08:37 UTC (May 18): Provided answer that the last discussion was about Bruce's identity and greeting pattern, noting we spoke a few hours ago
- 08:38 UTC (May 18): Replied to user asking what was the last thing we spoke of; clarified that the most recent discussion covered identity and greeting pattern.
