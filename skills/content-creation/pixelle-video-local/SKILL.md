---
name: pixelle-video-local
description: Route video-generation requests through the user's local Pixelle-Video service. Use whenever the user asks to create, generate, render, or make a video. Before selecting any video backend, ask whether to use local Pixelle-Video at http://localhost:8000; an explicit Pixelle selection counts as yes. If yes, start or verify the API, submit the asynchronous video request, and poll it to completion. If no, hand off to the appropriate non-Pixelle video skill.
---

# Local Pixelle Video

Use the local project at `C:\Users\44527\Pixelle-Video` as an opt-in video backend.

## Backend Choice

Before generating a video, ask exactly:

`是否用本地的 Pixelle-Video (http://localhost:8000) 生成？`

Do not start generation until the user answers. Treat an explicit request to use Pixelle-Video as an affirmative answer. If the answer is no, route to the appropriate existing video skill without invoking Pixelle.

## Verify the Local Service

1. Confirm the project and template exist:
   - `C:\Users\44527\Pixelle-Video\api\app.py`
   - `C:\Users\44527\Pixelle-Video\templates\1080x1920\image_default.html`
2. Run `scripts/start_api.ps1` in a long-running shell cell if `GET http://localhost:8000/health` is unavailable. Keep the returned cell active while generating, then stop it after delivery unless the user asks to keep the API running.
3. Verify `GET http://localhost:8000/openapi.json` before submission.
4. Check `C:\Users\44527\Pixelle-Video\config.yaml`. If it is missing or required provider credentials/workflows are blank, state that the API can start with defaults but generation is not proven ready. Do not expose secret values.

The current checked project exposes `POST /api/video/generate/async`, not `POST /api/video`. Prefer the live OpenAPI schema if a future project version changes the route.

## Generate

Run:

```powershell
python scripts/generate_video.py --text "<视频文案>"
```

The client submits this payload to `POST http://localhost:8000/api/video/generate/async`:

```json
{
  "text": "<视频文案>",
  "mode": "generate",
  "n_scenes": 5,
  "frame_template": "1080x1920/image_default.html",
  "video_fps": 30,
  "bgm_volume": 0.3
}
```

Poll `GET /api/tasks/{task_id}` every 5 seconds. Stop successfully only at `status=completed`; report `result.video_url` when present. Stop with the returned error at `failed` or `cancelled`. Default total timeout is 600 seconds.

Do not silently switch to synchronous generation or another provider after an error. Diagnose the failure and ask for any missing configuration or authority.

## Optional Web UI

Start the Streamlit UI only when the user asks to open or use it:

```powershell
Set-Location 'C:\Users\44527\Pixelle-Video'
uv run streamlit run web/app.py
```
