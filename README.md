# Coretica plugins

Connect your Agent to [Coretica](https://coretica.frontli.ne.kr) and keep newly learned
facts, preferences, decisions, and verified completed activities as **private memories**.
These packages combine MCP connection settings with instructions for the Agent.
They do not run a separate conversation uploader or background monitor.

This repository contains only distribution files. No credentials or Coretica application
source are included. The marketplace is maintained by Front-Line; adding it does not
mean the plugin has been reviewed or listed in an Agent vendor's official directory.

## Before connecting

1. In Coretica, configure a default information extraction model and consent to its
   processing. The server must support the `remember_user_info` MCP tool.
2. Create a dedicated Agent connection in **Agent connections → Manual**. Set its
   token as `CORETICA_AGENT_TOKEN` in the client's secure runtime environment, including
   the environment of an existing background service. Never paste the token into a
   chat, repository, command example, or plugin file.
3. Review the plugin files and the client's normal installation, hook, and tool prompts.
   Preserve existing connections and unrelated settings. Start a new session after setup.

The default MCP endpoint is `https://coretica.frontli.ne.kr/mcp/`. For another Coretica
deployment, update only the endpoint while retaining the environment-variable reference.
Installing a plugin does not deploy or upgrade your Coretica server.

## Codex

Add this marketplace in the plugin manager, then install Coretica:

```sh
codex plugin marketplace add Front-Line/coretica-plugins
codex plugin add coretica@coretica
```

Restart Codex. In `/hooks`, review, trust, and enable Coretica's hooks, which read only
the bundled `skills/coretica-memory/SKILL.md`. Confirm the MCP connection separately.
The MCP configuration is `plugins/coretica/mcp.codex.json` and uses
`bearer_token_env_var`. Tested with Codex 0.168.0 on macOS.

## Claude Code

```sh
claude plugin marketplace add Front-Line/coretica-plugins
claude plugin install coretica@coretica
```

Use `/plugin` to manage the installed Coretica plugin and start a new session. Its
MCP configuration is `plugins/coretica/.mcp.json`; keep the `CORETICA_AGENT_TOKEN`
reference in the Authorization header. Tested with Claude Code 2.1.220 on macOS.
ChatGPT and Claude web do not install these desktop/CLI packages.

## Hermes

Install both components together through Hermes's plugin manager. The pack pins both
components to the same reviewed public commit and uses Hermes's normal review prompts:

```sh
hermes plugins pack install https://raw.githubusercontent.com/Front-Line/coretica-plugins/main/hermes-pack.yaml
```

Alternatively, choose a reviewed full commit SHA from this repository's history and
install both components individually using the same SHA:

```sh
hermes plugins install https://github.com/Front-Line/coretica-plugins#hermes/coretica --ref <full-commit-sha>
hermes plugins install https://github.com/Front-Line/coretica-plugins#hermes/coretica-memory-rules --ref <full-commit-sha>
hermes plugins enable coretica
hermes plugins enable coretica-memory-rules
hermes plugins list --plain --no-bundled
```

`coretica` provides the native client's MCP connection and skill. The native
`coretica-memory-rules` component adds the bundled static instructions to a new
session's system prompt. Both are required for automatic capture guidance;
`requires_plugins` does not install dependencies. A portable plugin alone does not
run Claude hooks in Hermes. Start a new session after enabling or disabling the rules.
The MCP endpoint is in `hermes/coretica/mcp.json`. Tested against Hermes commit `8d70b88`.

## OpenClaw

OpenClaw 2026.11.10 or newer is required. The package uses the native plugin API,
native HTTP MCP, and `before_prompt_build`. Its Node requirement matches that runtime:
`>=24.22.1 <25 || >=26.12.1`. Registry availability is separate from source availability.
Until a ClawHub release is available, download or clone this repository and install
the reviewed `openclaw` directory through the plugin manager:

```sh
openclaw plugins install <downloaded-repository>/openclaw
openclaw plugins enable coretica
```

Follow source and capability confirmations. Review the static instruction hook, then
merge these two permissions into `plugins.entries.coretica.hooks` in your active
OpenClaw configuration, preserving existing options:

```json
{ "allowConversationAccess": true, "allowPromptModification": true }
```

OpenClaw requires these plugin-specific permissions even though the hook does not read
conversation events. For another Coretica deployment, add or update
`mcp.servers.coretica` in your active profile (`~/.openclaw/openclaw.json` by default):

```json
{
  "url": "https://coretica.frontli.ne.kr/mcp/",
  "transport": "streamable-http",
  "headers": { "Authorization": "Bearer ${CORETICA_AGENT_TOKEN}" },
  "requestTimeoutMs": 120000
}
```

This user configuration overrides the packaged endpoint. Restart your existing Gateway
service after configuration changes; do not start a second Gateway. Inspect loading with
`openclaw plugins inspect coretica --runtime --json` and check actual MCP connectivity.

## What is sent and stored

The instruction components only load their bundled local instructions. The Agent
chooses meaningful new information and calls `remember_user_info` through its native
MCP client. Only a `saved` receipt confirms a write. The client may require permission
for this write tool; allow only the intended scope through its normal controls.
Automatic tool selection depends on the model and is not guaranteed for every model.

The server uses the user's configured extraction model and processing consent.
It appends private memories without granting permission to edit or delete existing
memories. Sharing or retrieval by another Agent still needs separate Coretica approval.
Do not send secrets, full transcripts, hidden reasoning, invented facts, or information
the user asked not to remember. Installation never authorizes unrelated tool use.

Disable or uninstall Coretica through the client's plugin manager and start a new
session to stop its instructions. Disable both Hermes components. Revoking the Agent
connection in Coretica blocks subsequent MCP access, including from an existing session.
These actions do not delete previously saved memories; manage those in Coretica.

## Verification and support

Codex's normal hook trust and tool permission flow was tested with a real private-memory
write from a natural preference statement. Claude Code installation and MCP connectivity
were checked; automatic selection by a logged-in Claude model remains unverified.
Hermes and OpenClaw were tested for package installation, complete instruction loading,
native MCP writes, and owner isolation. Their automatic selection from a natural utterance
was not verified with the final instructions. A small local model sometimes omitted calls.
Windows and mobile installation are not verified. Codex/Claude hooks require a compatible
shell and `cat` (for example the client's supported Git Bash setup on Windows).

For problems, use this repository's issues without tokens, memory contents, or private
conversation logs. Report the client version, plugin version, and a redacted error.
