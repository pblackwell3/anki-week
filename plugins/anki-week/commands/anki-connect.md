---
description: Install the `anki` MCP connector into the Claude Desktop config (merges, backs up, verifies) so Anki is reachable from Claude Chat and Claude Cowork.
---

Install and verify the **Anki MCP connector** now. Don't ask the user to paste JSON — do it yourself.

1. **Check the bridge's prerequisite.** Run `npx --version`. Missing → point them at
   <https://nodejs.org> (LTS), then continue.

2. **Write the config.** Run the installer that ships with this plugin:

   ```bash
   node "${CLAUDE_PLUGIN_ROOT}/skills/setup/scripts/install-anki-mcp.mjs"
   ```

   Add `--dry-run` first if the user wants to see the change before it lands. It merges

   ```json
   { "anki": { "command": "npx", "args": ["mcp-remote", "http://127.0.0.1:3141"] } }
   ```

   into `mcpServers` in the Claude Desktop config — macOS
   `~/Library/Application Support/Claude/claude_desktop_config.json`, Windows
   `%APPDATA%\Claude\claude_desktop_config.json` — **preserving every other MCP server**, backing the
   file up first, and refusing to overwrite a config it can't parse.

   Read the exit code: `0` = written or already correct · `2` = their existing config is invalid JSON
   (fix the trailing comma / unbalanced brace *with* them, then re-run — never overwrite) · `3` = the
   write failed (permissions or an unusual install path; try `--path <file>`).

   No shell on this surface → walk them through **Settings ▸ Developer ▸ Edit Config** and add the
   entry by hand, keeping any servers already there.

3. **Connect this surface too**, if `anki` isn't already here:
   `claude mcp add anki -- npx mcp-remote http://127.0.0.1:3141`.

4. **Restart and verify.** If the script printed `RESTART_REQUIRED: yes`, have them **fully quit and
   reopen Claude** (the app, not the window). Then, with **Anki desktop open** and the **Anki MCP
   Server** add-on (AnkiWeb code `124672614`) enabled with its HTTP server on, call a read-only tool
   yourself — `list_decks` — and read their deck names back to them. That's the only proof the
   connection is real.

   Still failing → work the list: Anki not open · HTTP server not enabled (**Tools ▸ AnkiMCP Server
   Settings…**) · Claude not fully restarted · `npx` missing · the add-on itself crashing (see the
   **anki-week-setup** skill for the pydantic_core/distutils recovery).

5. **Close with where to use it.** The connector is now live in **Claude Chat and Claude Cowork** as
   well. Tell them, in one line, to do their weekly builds in **Cowork** — it has a browser, so it
   logs into Blackboard and pulls each week's lecture slides down itself, instead of them downloading
   every lecture by hand.
