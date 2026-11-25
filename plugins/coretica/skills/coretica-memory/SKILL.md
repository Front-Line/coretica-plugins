---
name: coretica-memory
description: Automatically save new, useful facts the user explicitly shares and verified work completed for the user as private Coretica memories through MCP. Use after a meaningful new fact, correction, or completed activity; exclude plans presented as accomplishments, duplicate summaries, secrets, and content the user says not to remember.
---

These instructions are loaded by the enabled Coretica plugin. Automatic
**private** memory capture is active for this session within the scope below.
Use the connected Coretica MCP tool `remember_user_info` (the client may prefix
its name); do not ask for confirmation for each qualifying save.
This does not authorize sharing memories, changing existing memories, or actions
outside the user's task. The user's later instructions override this skill.

## What to save

At each turn, check for a new explicit user statement or a meaningful completed
activity you have verified for the user. If it qualifies below, call the save
tool before finishing the turn; if nothing qualifies, do not save. Keep
related facts together; separate unrelated facts. Record only the new information,
not the entire conversation or repeated task summaries.

- Use `kind="fact"` for an explicitly stated preference, stable fact, decision,
  or correction. Attribute it to the user; do not infer personal traits or turn
  an assistant suggestion into the user's decision.
- Use `kind="activity"` for work actually completed and verified. Distinguish
  the user's reported activity from a result the agent directly verified. A plan,
  attempted command, passing test, or local commit is not proof of deployment or
  a broader outcome. Preserve any material incomplete or unverified part.
- Write a short factual `title` and concise `content` in the user's language.
  Include relevant project context, source attribution, explicit event dates,
  and uncertainty. Do not substitute the server's receipt time for an unknown
  event date. Summarize evidence without copying raw logs or source documents.
- Exclude passwords, tokens, keys, authentication codes, hidden reasoning,
  unrelated third-party personal information, and confidential material outside
  the authorized scope. If permission to retain a sensitive category is unclear,
  clarify that scope before saving it. Respect “don't remember this” immediately.
  Do not read other chats, files, or memories merely to collect more material.

## Save and check the result

1. Locate `remember_user_info` with the client's tool search/discovery if tools
   are deferred, and inspect its schema. Send `title` (1–200
   characters), `content` (1–20,000 characters), `kind` (`fact` or `activity`),
   and a unique `idempotency_key` (1–200 characters). Strip surrounding whitespace.
   Keep the exact key and payload for this record's retries. Do not send credentials
   in these fields or use private user CRUD APIs as a substitute.
2. A response with `status="saved"` and a `memory_id` confirms persistence.
   `processing` means the save is unconfirmed. For a transient transport failure
   or `processing`, allow at most one later retry with the identical payload and
   key, on a later turn or when the server indicates it is ready. Do not poll or
   block the user's work waiting for it.
3. For `deleted`, do not save again with a new key: the user may have deleted the
   memory. For a key/payload conflict, authorization error, or other failure,
   stop and report the actual outcome. Never describe a queued, failed, missing,
   or deleted result as saved.

If the tool is missing, explain that the Coretica MCP connection must be set up
and support `remember_user_info`; installing this skill alone does not connect
it. Do not create duplicate connections, collect a token in chat, or silently
send the information somewhere else.

Keep any save acknowledgement brief. Saved memories remain private; later
retrieval by an Agent still follows Coretica's separate disclosure approval.
The plugin delivers these instructions through trusted hooks or session context.
This only loads the bundled file; it does not read or forward the conversation.
Saving still requires the MCP tool and a
qualifying fact or activity. This does not monitor other chats or apps, and model
compliance is not guaranteed.
