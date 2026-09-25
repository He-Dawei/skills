---
name: chatcut
description: Create AI-edited videos via ChatCut from a prompt and a list of assets (URLs or local file paths). Use when the user asks to make/edit/generate a video, highlight reel, talking-head cut, social clip, promo, or similar — and provides or implies media to work from, whether that's links or files on their machine.
---

# ChatCut video creation

This skill creates an AI-edited video via the ChatCut Job API. The user describes what they want in natural language and supplies one or more media assets — either public URLs or absolute paths to files on their own machine. The CLI transcodes the assets locally with ffmpeg, uploads them, then ChatCut's agent assembles a timeline server-side and renders the final video in the cloud. The user gets back a signed URL to download.

## When to use

Use this skill when the user asks to:

- Make / edit / create / cut / generate a video
- Build a highlight reel, promo, talking-head cut, social clip, explainer, UGC ad
- Clean up or trim an existing clip via prompt ("remove the filler words", "tighten this up")

Do **not** use this skill if:

- The user is asking about ChatCut as a product (pricing, features, etc.) — answer from general knowledge instead
- The task clearly requires source media and the user has neither provided any (URLs or local file paths) nor indicated they have some they can share

## Prerequisites

The `chatcut` CLI must be installed and on PATH (end users install once via `npm i -g @chatcut/skill` — the package's postinstall step registers SKILL.md automatically). The first `chatcut submit` may briefly open a browser to sign in; everything after that is silent.

## Getting file paths from the user

Assets can be either public URLs or absolute paths to files on the user's machine (`/Users/...`, `~/Downloads/...`, `C:\Users\...`). Decide how to collect them:

- **If the user already pasted or dragged paths/URLs into chat** — use them directly. Terminals like iTerm, VS Code, and Terminal.app paste the absolute path when a file is dragged onto the prompt.

- **Otherwise, if the user implies they have files locally but hasn't shared paths** — run this yourself via the Bash tool to open a native OS file picker on their screen:

  ```bash
  chatcut pick
  ```

  **Run it with a Bash `timeout` of at least 300000ms (5 minutes)** — the command blocks until the user clicks through the dialog. The default 2-minute Bash timeout is too short if they're away from the keyboard.

  Announce the action first so the user knows to look for the dialog, e.g. _"Opening a file picker on your screen — select the files you want to use and click Open."_

  Output format: one `path:type` per line on stdout, ready to pass straight to `submit`:

  ```
  /Users/matt/Downloads/interview.mov:video
  /Users/matt/Pictures/logo.png:image
  ```

  Parse those lines and forward them to `chatcut submit --asset "..."` — one `--asset` per line, quoting each value.

  If `chatcut pick` exits non-zero:
  - Exit code + stderr `"Cancelled."` → the user dismissed the dialog. Ask what they'd like to do (retry, use URLs instead, give up).
  - Exit code + stderr about missing `zenity` or unsupported platform → fall back to asking the user to paste the absolute paths into chat directly, or drag the files onto the prompt.

- **If the user says "just use everything in my Downloads folder"** — don't glob the filesystem yourself; run `chatcut pick` so the user explicitly chooses. Bulk-selecting a whole directory blind is almost never what they actually want.

## Workflow

1. **Gather inputs from the user's message.**
   - **Use the user's own words as the prompt verbatim.** Pass their request through to `--prompt` unchanged. If they gave no editorial direction (e.g. _"render this"_, _"edit my video"_, _"can you put this together"_), do **not** invent one — either pass their words through as-is or ask one short clarifying question. Never paraphrase their request into a "highlight reel" / "best moments" / "engaging clips" prompt unless they actually used those words.

     > **Don't do this.** User says _"edit this video and render it out."_ Do not expand to `--prompt "Create a short edit keeping the most interesting moments"`. Pass `--prompt "edit this video and render it out"` or ask a one-line clarifying question. The user's literal words are always a valid prompt shape.

     The CLI automatically appends an export instruction matching the user's render preferences, so don't add one yourself.

   - Extract each asset and infer its type from the extension / context — pick from `video | audio | image | gif`. Assets may be URLs (`https://…`) or absolute local paths (`/Users/matt/clip.mp4`). Both are valid; pass them to `--asset` the same way. If the type is genuinely ambiguous, ask — don't guess.
   - If the user implies local files but hasn't shared paths, follow "Getting file paths from the user" above before continuing.
   - Extract optional render preferences if mentioned (e.g. "make it 720p", "audio only"). Pass them via the corresponding CLI flags (`--resolution`, `--format`, `--codec`). The same flags drive the auto-appended export clause and the cloud render.

   The render runs in the cloud — the CLI prints a signed download URL when it's done.

2. **Confirm before submitting — and make it a real gate when you synthesized the prompt.**
   - If `--prompt` is a direct quote of the user's words: briefly echo back the plan ("Submitting with your prompt, 3 video clips, 1080p…") and proceed unless they object.
   - If you altered the prompt at all — paraphrased, expanded, added editorial framing the user didn't request — **stop and ask** before submitting. Show them the exact `--prompt` string you plan to send and wait for an explicit OK. "Proceed unless objected" is not enough here; the user often won't notice the substitution in a brief echo. This is a paid operation; getting the prompt right beats moving fast.

3. **Run the full pipeline with a single Bash call.** `<asset>` can be either a URL or an absolute local path:

   ```bash
   chatcut submit \
     --prompt "<prompt>" \
     --asset "<asset1>:<type1>" \
     --asset "<asset2>:<type2>" \
     [--resolution 720p|1080p|480p] \
     [--format video|audio]
   ```

   Always quote each `--asset` value — paths and URLs can contain spaces or special characters.

   **`submit` does the entire pipeline end-to-end and blocks until done.** It transcodes the assets locally, uploads them, runs the agent edit loop, then waits for the cloud render to finish. Progress is streamed to stderr as human-readable lines. The final stdout line is JSON with the signed output URL.

   **Always run this with `timeout: 1800000` (30 minutes)** — a typical run is 3–10 minutes, but longer source clips can push agent + render time well past 10 minutes. On the very first invocation `submit` may also pause to open a browser sign-in (one-time, 5-minute internal timeout), so the 30-minute Bash timeout comfortably covers that too.

   Example streamed output (stderr) you'll see:

   ```
   Creating ChatCut project with 2 assets…
   Project created abc123
   Preparing 2 assets…
   All 2 assets ready.
   Submitting job to ChatCut agent…
   Job submitted def456
   Agent editing — step 1
   Agent editing — step 4
   Rendering — 25%
   Rendering — 60%
   Rendering — 95%
   Render complete → https://…/exports/def456.mp4
   ```

   Then a final stdout JSON line:

   ```json
   {
     "jobId": "def456",
     "projectId": "abc123",
     "outputUrl": "https://…/exports/def456.mp4"
   }
   ```

   Narrate the major transitions to the user (project created, agent thinking, rendering started, done).

   If `submit` exits non-zero, surface the stderr verbatim and stop. Common causes: agent run failed, malicious prompt detected, render error.

4. **On completion**, give the user the signed `outputUrl`. They can click it to download / view in their browser.

   You generally do **not** need `chatcut watch` — `submit` already runs to completion. `watch` is only useful for re-attaching to a job that was started externally.

## Login

`chatcut submit` triggers the browser sign-in flow inline if no API key is found — you don't normally need to run a separate login command. When this happens, `submit` prints `No API key found — opening browser to sign in…` to stderr, blocks while the user completes the flow, then continues with the job. Use the same `timeout: 1800000` (30 minutes) Bash timeout for `submit`; it covers both the browser flow and the run.

If you ever need to sign in explicitly (e.g. to switch accounts), run:

```bash
chatcut login
```

**Run `chatcut login` with a Bash `timeout` of at least 300000ms (5 minutes)** — the command blocks on a browser interaction. The CLI itself times out at 5 minutes.

Announce the action to the user before running it, e.g. _"Opening a browser so you can authenticate — this tab in the browser should be enough, no need to switch terminals."_

## Error handling

- **`No API key configured`** on `chatcut submit` — should rarely surface now that `submit` runs the browser sign-in inline. If you do see this, run `chatcut login` (see "Login" above), then retry once. If it fails again, stop and relay the error.
- **Asset ingestion failure** (e.g. a 404 URL) — surface the error. ChatCut may still be able to proceed with remaining assets, or may not. Don't retry automatically; let the user decide.
- **Agent run failure** — surface the error message from the response. Common causes: prompt misunderstood, malicious content flagged, or a genuine bug. Ask the user whether to retry with a tweaked prompt.
- **`error` at top level during polling** — stop polling immediately and relay the error verbatim.

## Examples of good invocations

The `--prompt` value is always the user's own words. The examples below pair each user-request shape with the matching CLI call. The CLI appends the export instruction automatically based on `--resolution` / `--format`, so prompts stay focused on whatever the user said.

**Minimal / pass-through prompt** — user gave no editorial direction. Their words are the prompt:

```bash
chatcut submit \
  --prompt "render this video" \
  --asset "/Users/matt/Downloads/interview.mov:video"
```

```bash
chatcut submit \
  --prompt "edit this and put something together" \
  --asset "/Users/matt/Downloads/footage1.mp4:video" \
  --asset "/Users/matt/Downloads/footage2.mp4:video"
```

**Editorial prompt** — user described the kind of edit they want; pass it through verbatim:

```bash
chatcut submit \
  --prompt "Make a 30-second highlight reel featuring the most engaging moments" \
  --asset "https://example.com/clip1.mp4:video" \
  --asset "https://example.com/clip2.mp4:video" \
  --asset "https://example.com/clip3.mp4:video" \
  --resolution 1080p
```

```bash
chatcut submit \
  --prompt "Trim filler words and long pauses, add a lower-third title 'Q3 all-hands'" \
  --asset "https://example.com/meeting.mp4:video"
```

**Mixed local + remote assets** — paths and URLs work identically:

```bash
chatcut submit \
  --prompt "Cut the best 60 seconds and add the logo image as a 3s intro card" \
  --asset "/Users/matt/Downloads/interview.mov:video" \
  --asset "/Users/matt/Pictures/logo.png:image" \
  --resolution 1080p
```

**Audio-only output:**

```bash
chatcut submit \
  --prompt "Podcast-style audio mix: intro bed under the first 10s, fade out over outro" \
  --asset "https://example.com/interview.mp3:audio" \
  --asset "/Users/matt/Music/bed.mp3:audio" \
  --format audio
```

## Output format for the user

When the job completes, report:

```
✓ Video ready
URL: <outputUrl>
```

Keep it brief. Give the user the signed download URL verbatim — don't paraphrase it, wrap it, or invent a different format. They can click or paste it into a browser.
