#!/usr/bin/env node
/**
 * install-anki-mcp.mjs — add the `anki` MCP server to the Claude Desktop config.
 *
 * Writes the entry the anki-week / study-week skills need so the Anki connector shows up in
 * Claude Chat and Claude Cowork:
 *
 *   "anki": { "command": "npx", "args": ["mcp-remote", "http://127.0.0.1:3141"] }
 *
 * Safe by design: it MERGES into the existing file (other MCP servers are preserved), backs the
 * file up before touching it, and refuses to overwrite a config it can't parse.
 *
 * Usage:
 *   node install-anki-mcp.mjs                 # write it
 *   node install-anki-mcp.mjs --dry-run       # show what would change, write nothing
 *   node install-anki-mcp.mjs --path <file>   # non-standard config location
 *   node install-anki-mcp.mjs --url <url>     # non-default Anki MCP URL
 *   node install-anki-mcp.mjs --name <key>    # server key (default: anki)
 *
 * Exit codes: 0 = written or already correct · 2 = existing config is invalid JSON (nothing
 * written) · 3 = write failed.
 */

import { readFileSync, writeFileSync, mkdirSync, copyFileSync, existsSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join } from "node:path";

const argv = process.argv.slice(2);
const flag = (name) => {
  const i = argv.indexOf(`--${name}`);
  return i === -1 ? undefined : argv[i + 1];
};
const has = (name) => argv.includes(`--${name}`);

const DRY_RUN = has("dry-run");
const SERVER_NAME = flag("name") || "anki";
const ANKI_URL = flag("url") || "http://127.0.0.1:3141";

function defaultConfigPath() {
  if (process.platform === "darwin") {
    return join(homedir(), "Library", "Application Support", "Claude", "claude_desktop_config.json");
  }
  if (process.platform === "win32") {
    const appData = process.env.APPDATA || join(homedir(), "AppData", "Roaming");
    return join(appData, "Claude", "claude_desktop_config.json");
  }
  return join(process.env.XDG_CONFIG_HOME || join(homedir(), ".config"), "Claude", "claude_desktop_config.json");
}

const CONFIG_PATH = flag("path") || defaultConfigPath();
const ENTRY = { command: "npx", args: ["mcp-remote", ANKI_URL] };

let config = {};
let existed = existsSync(CONFIG_PATH);

if (existed) {
  const raw = readFileSync(CONFIG_PATH, "utf8");
  if (raw.trim() === "") {
    config = {};
  } else {
    try {
      config = JSON.parse(raw);
    } catch (err) {
      console.error(`ERROR: ${CONFIG_PATH} is not valid JSON — refusing to overwrite it.`);
      console.error(`       ${err.message}`);
      console.error(`       Fix the JSON (usually a trailing comma or an unbalanced brace), then re-run.`);
      process.exit(2);
    }
    if (config === null || typeof config !== "object" || Array.isArray(config)) {
      console.error(`ERROR: ${CONFIG_PATH} does not contain a JSON object — refusing to overwrite it.`);
      process.exit(2);
    }
  }
}

if (typeof config.mcpServers !== "object" || config.mcpServers === null || Array.isArray(config.mcpServers)) {
  config.mcpServers = {};
}

const before = config.mcpServers[SERVER_NAME];
const alreadyCorrect = JSON.stringify(before) === JSON.stringify(ENTRY);
const otherServers = Object.keys(config.mcpServers).filter((k) => k !== SERVER_NAME);

if (alreadyCorrect) {
  console.log(`OK: "${SERVER_NAME}" already points at ${ANKI_URL} in ${CONFIG_PATH}`);
  console.log(`    Other MCP servers present: ${otherServers.length ? otherServers.join(", ") : "(none)"}`);
  console.log(`    RESTART_REQUIRED: no`);
  process.exit(0);
}

config.mcpServers[SERVER_NAME] = ENTRY;
const output = JSON.stringify(config, null, 2) + "\n";

if (DRY_RUN) {
  console.log(`DRY RUN — would write ${CONFIG_PATH}:`);
  console.log(output);
  process.exit(0);
}

try {
  mkdirSync(dirname(CONFIG_PATH), { recursive: true });
  if (existed) {
    const stamp = new Date().toISOString().replace(/[:.]/g, "-");
    const backup = `${CONFIG_PATH}.bak-${stamp}`;
    copyFileSync(CONFIG_PATH, backup);
    console.log(`Backed up existing config → ${backup}`);
  }
  writeFileSync(CONFIG_PATH, output, "utf8");
  JSON.parse(readFileSync(CONFIG_PATH, "utf8")); // read-back validation
} catch (err) {
  console.error(`ERROR: could not write ${CONFIG_PATH} — ${err.message}`);
  process.exit(3);
}

console.log(`${before ? "Updated" : "Added"} "${SERVER_NAME}" → npx mcp-remote ${ANKI_URL}`);
console.log(`Wrote ${CONFIG_PATH}`);
console.log(`    Other MCP servers preserved: ${otherServers.length ? otherServers.join(", ") : "(none)"}`);
console.log(`    RESTART_REQUIRED: yes — fully quit and reopen Claude, then verify with a read-only Anki call.`);
