# PROMPT (copy everything below this line into ChatGPT)

You are a senior motion-graphics engineer. I will attach: (1) my SCRIPT (.md), (2) my VOICEOVER (.mp3, one chapter at a time), (3) three reference code files (`lib.py`, `scenes.py`, `seg.py`) from an already-working project. Build a finished explainer video from my voiceover in the EXACT visual style below, entirely with code (no stock footage, no AI image generation). The video must be RENDERED ON GITHUB ACTIONS, not on my computer.

## 1. Deliverables
1. A GitHub repo layout (files + full contents).
2. `.github/workflows/render.yml` that renders the video and uploads it as a downloadable artifact (also attach to a GitHub Release if a tag is given).
3. Python code that draws every scene and renders the frames.
4. A short README: how to drop in a new voiceover + script and run the workflow.

Reuse the attached `lib.py` / `scenes.py` / `seg.py` as the base. Keep their drawing helpers and animation engine. Only replace scene content for my new script. Fix font paths (see section 8).

## 2. Video format
- 1920x1080, 30 fps, H.264 (libx264, crf 17-18, yuv420p), AAC 192k audio = my voiceover mp3 only. `-movflags +faststart`.
- Video length = voiceover length exactly. Last 0.35 s fades to black.
- No captions, no stock music, no logos watermark. On-screen text is only short hand-drawn labels.
- First scene shows a small chapter tag top-left ("CHAPTER N | TITLE", size 34, light grey-blue) that fades in at 0.1 s and out at about 3.2 s.

## 3. Visual style (must match exactly)
Flat 2D cartoon explainer, same look as the "Biggest Hack in History" style channels:
- **Outlines:** thick black ink `(17,17,17)`, 6-7 px at 1080p on every shape, rounded joins and round line caps. Everything flat colored, no gradients on objects.
- **Antialiasing:** draw every sprite at 2x supersampling (SS=2) on a transparent RGBA canvas, then downscale with LANCZOS.
- **Characters:** round WHITE head `(244,244,240)` with a grey crescent shade `(190,192,196)` lower-right, two small black dot eyes, simple mouth (moods: neutral, happy, worried, think, surprised, sad), rounded-rectangle colored body, stick arms with small white round hands, stick legs with black oval feet. No fingers, no noses, no hair. Body colors vary per character (blue `(70,120,200)`, red `(200,90,80)`, purple, grey).
- **Props:** simple flat icons (calendar, TV, teddy bear, gift, Christmas tree, grocery bag, shopping cart, phone with app UI, browser window, laptop, money sack, clock, megaphone, location pin, warning triangle, store building, magnifier, X mark, question mark). Real brand marks are drawn as simple approximations (blue sign with yellow six-petal spark for Walmart, black "amazon" text with orange smile, red bullseye for Target).
- **Backgrounds:** solid dark color + one soft blurred spotlight ellipse (GaussianBlur ~90) in a lighter shade of the same hue, sometimes a darker floor band. Palette rotates per scene:
  - Navy `(28,34,48)` + spot `(52,62,86)`
  - Sage `(168,190,190)` + spot `(196,214,212)` (light scenes)
  - Warm brown `(60,44,44)` + spot `(98,72,64)`
  - Charcoal `(36,36,42)` + spot `(62,64,74)`
  - Royal blue `(26,66,124)` + spot `(48,100,176)`
  - Peach `(222,200,172)` + spot `(240,224,200)`
  - Slate `(46,58,80)` + spot `(74,90,120)`
  - Danger/alert scene: deep red `(58,26,30)` + spot `(110,44,50)`
  - Accent colors: red `(219,56,52)`, gold `(236,184,64)`, green `(62,160,90)`, brand blue `(0,113,206)`, brand yellow `(255,194,32)`.
- **Fonts:** hand-drawn look = **Comic Relief Bold** for all labels/words; **Poppins Bold** for logos and UI. White text on dark scenes, near-black `(17,17,17)` on light scenes, gold for emphasis, red for negative words.
- **Composition:** big close-up props (a prop is often 400-900 px tall). One clear idea per scene, 2-5 items per scene, lots of empty space, a short label (3-5 words, ALL CAPS, 60-110 px) that appears after the visual.

## 4. Animation rules
Build a tiny sprite engine (class `Item`) with these animations, all time-based:
- `pop`: scale 0 to 1 with ease-out-back overshoot (0.4 s)
- `fade`: alpha 0 to 1
- `slide`: slide in from an offset with ease-out cubic
- `wipe`: left-to-right reveal (for timelines, bars, arrows)
- extras: `bob` (slow vertical sine float), `sway` (small rotation shake), `path` (piecewise smoothstep movement for walking characters), `end` (fade out), `amax` (max alpha, for ghost items).
- **Camera:** every scene has a slow push-in (zoom 1.00 to 1.05/1.06) toward a focus point, done by cropping the composed frame and resizing with cv2 `INTER_LINEAR`. Skip zoom on scenes that fill the full width.
- **Transitions:** hard cut with a 0.14 s cross-dissolve between scenes.
- Elements appear exactly when the narrator says the matching word/phrase (see section 5).

## 5. Timing from the voiceover (very important)
1. Run `ffmpeg -af silencedetect=noise=-35dB:d=0.28` on the mp3 to get pauses.
2. Map script sentences to speech segments: paragraph breaks = pauses of about 0.55 s or more, commas = shorter pauses. Use word counts (about 3.3 words/sec) to verify which pause belongs to which sentence.
3. Each sentence or short group of sentences = one scene. Inside a scene, every item's `t0` is the start of the phrase it illustrates (e.g. in a list "TV in November, toy deal, decorations, groceries", each icon pops at its own phrase).
4. The chapter's final question is shown as large on-screen text typed in word-by-word (fade 0.18 s per word) across the narration of that sentence, key words highlighted (brand name gold, "competing/risk" words in soft red), plus a glowing "?" at the end.
5. Print the computed scene table (start, end, sentence) in the build log so I can adjust times.

Scene vocabulary that worked (reuse the idea, not the exact content):
- one thing / one chance: calendar -> arrow -> money sack
- long period: wide segmented bar wiping in, pin marking one day
- thinking about habits: big character + thought bubble with icons
- negation: ghost (35% alpha) items with a big red X
- stages over time: horizontal timeline with colored nodes, icons above, two-line labels below, mini character walking along it
- list of events: row of colored chevron blocks with icons above
- series vs one big moment: row of small circles vs one giant red circle with X
- competitor options: logo tiles + browser window comparing prices
- warning: red triangle with shake + worried character
- ending: question text typed on dark navy

## 6. Quality rules
- Everything programmatic, deterministic, no network calls at render time except installing tools.
- Never place text outside the safe area (keep 120 px margins); check no overlaps (I had to shrink timeline labels to 34-38 px so four labels fit side by side).
- Before the full render, generate a contact-sheet preview PNG (about 9 key frames) and upload it as an artifact too.
- Render in segments of about 660 frames to separate mp4s, then `ffmpeg -f concat`, then mux audio with `-t <voiceover duration>`.
- Add `workflow_dispatch` inputs: `voiceover` path, `script` path, `chapter_title`.

## 7. GitHub Actions requirements
```yaml
name: render-video
on:
  workflow_dispatch:
    inputs:
      voiceover: { description: "path to mp3", default: "assets/ch-1.mp3" }
      chapter_title: { description: "chapter tag text", default: "CHAPTER 1 | TITLE" }
jobs:
  render:
    runs-on: ubuntu-latest
    timeout-minutes: 60
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: sudo apt-get update && sudo apt-get install -y ffmpeg
      - run: pip install pillow numpy opencv-python-headless
      - name: Download fonts
        run: |
          mkdir -p fonts
          curl -L -o fonts/ComicRelief-Bold.ttf https://github.com/google/fonts/raw/main/ofl/comicrelief/ComicRelief-Bold.ttf
          curl -L -o fonts/Poppins-Bold.ttf https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf
      - name: Preview contact sheet
        run: python preview.py out/preview.jpg
      - name: Render segments
        run: python render_all.py "${{ inputs.voiceover }}" out/final.mp4
      - uses: actions/upload-artifact@v4
        with: { name: video, path: out/final.mp4 }
      - uses: actions/upload-artifact@v4
        with: { name: preview, path: out/preview.jpg }
```
Adapt this template as needed. `render_all.py` must detect the mp3 duration with `ffprobe`, loop segments, concat and mux. Do NOT depend on local paths like `/usr/share/fonts/...` or `/mnt/...`; read fonts from `./fonts/` and files from `./assets/`.

## 8. Known gotchas (already solved in my attached code, keep the fixes)
- Long single background process gets killed, so render in segments.
- Multi-line text with `\n` in PIL aligns left; draw each line as a separate centered text call.
- X marks drawn over text hide it; put the label outside the shape.
- Third character at the far right gets cropped by the camera zoom; keep x below 1700 when zoom is above 1.0.
- Glows that appear before their object look like blobs; fade them in at the same time as the object.

## 9. How I will use you
I will attach script + voiceover for each chapter. For each one: (a) show me the scene table first, (b) then output only the changed/new files, (c) tell me which GitHub workflow inputs to set. Keep replies short. Do not ask me questions unless the voiceover and script clearly do not match.

Now confirm you understood, list the files you will create, and wait for my attachments.
