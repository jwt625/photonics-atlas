# DevLog-018: History stories video (MCVD hero, zoom out to the 4x4 grid)

| | |
|---|---|
| Date | 2026-11-12 |
| Status | v1 delivered after audit fixes: `cache/showcase_video/history_stories_grid.mp4` (45.0 s, 1350 frames, 1920x1080, 30 fps, H.264 yuv420p, faststart, no audio, 20 MB; 2x supersampled); soundtrack pending (owner) |
| Scope | One silent ~30 s video: the MCVD story auto-playing full frame with cursor hovers, then a zoom out to a 4x4 grid of all 16 history stories playing |
| Related | DevLog-017 (showcase runtime, Play pacing D996 / D1000), `app/scripts/showcase-thumbs.mjs` (capture pattern) |
| Decisions | D1120-D1139 reserved for this DevLog |

## Request (2026-11-12, Wentao)

Video: start on one story (MCVD), auto playthrough of the scroll animation with mouse hovers showing tooltips; same for all 16
stories. After 2/3 of the duration start zooming out; end when fully zoomed out to the 4x4 grid of all stories playing (loop).
Record each story first (lower res where the grid allows), then stitch with the zoom. Target ~30 s.

## Owner answers (2026-11-12)

1. 1920x1080, dark theme.
2. Each tile is the whole story stage (keyword, model, plot, side column, control bar), not the model pane only.
3. Most stories should show their complete playthrough; MCVD plays twice.
4. Hover pauses (playback holds while a tooltip is shown).
5. Chronological grid with a gap.
6. Silent (soundtrack later).

## Decisions

| ID | Decision | Source |
|---|---|---|
| D1120 | Every story is one complete playthrough time-scaled to the same loop T = 15 s (450 frames at 30 fps); MCVD plays it twice (0-15 s, 15-30 s) = 30 s total; zoom out from 20 s (2/3) to 30 s; the 15 other tiles loop in phase with MCVD, so all 16 reach p = 1 on the last frame. Native Play is 28.6-39.4 s per story (MCVD 35.8 s), so the playthrough runs at about 2.4x Play speed. T is one parameter | owner Q3 + coordinator |
| D1121 | Pacing follows the runtime's own Play plan (`playPlan`, near-linear move per chapter, 80 ms dwell) scaled to fit T minus the hover pauses | coordinator |
| D1122 | Deterministic frame capture, not real-time recording: per frame set the scroll position for p(t), move the real pointer, wait two animation frames, screenshot the stage. frame(p) is pure in the runtime (README "Plot hook"), so frames are exact | coordinator |
| D1123 | Viewport 1920x1100, history menu bar unpinned (`history.barPinned` = false), so the sticky stage is exactly 1920x1080 above the 20 px site footer; the screenshot clips the stage | probe |
| D1124 | Hovers: 2 per story (a 3D part around 35 % of the chapters; a plot point at the end of the first plot chapter, or a second part if the story has no plot), 3 for MCVD (plus the process step chip). Pause 0.8 s each; the cursor glides 0.6 s to each target and rests on the control bar between hovers. Targets are found by scanning the pointer over the model pane and reading the tooltip (no guessed positions). Cursor: plain white arrow with black outline drawn in the page; the real pointer follows it | owner Q4 + coordinator |
| D1125 | MCVD captured at 1920x1080; the other 15 at 960x540 (the screenshot's clip scale 0.5 of a full-res render). A neighbour tile is fully in view only below about 2x its grid size | coordinator |
| D1126 | Grid: chronological reading order (colladon1842 ... wang2018b), MCVD lands at row 2, column 3; 16:9 tiles, 4 px gap, background #0d0d0d. Zoom: one scale about the fixed point of the MCVD-tile-to-frame map, log-scale interpolation with ease-in-out, ends exactly on the grid (no hold) | owner Q5 + coordinator |
| D1127 | Output H.264 yuv420p, 30 fps, `+faststart`, no audio track. Frames and per-story clips under `cache/showcase_video/` (gitignored); script `app/scripts/showcase-video.mjs`, compositor `scripts/showcase_video_grid.py` | owner Q6 + coordinator |
| D1128 | Zoom ease: sine ease-in-out on log scale (cubic left the first 2 s nearly static) | coordinator |
| D1129 | Audit round: scan accepts only tooltips created by that move (energy-level diagrams clear on pointerleave only; the gordon1954 plot hover had no tooltip); real pointer on the target only during holds, parked on the footer otherwise (no stray tooltips while the scene moves; drawn cursor still glides); cursor rests 48 px above the control bar (was 4 px visible); return glide ends by T (papuchon1975 cursor stuck mid-glide on the last frame); gap colour #383835 (D997 rule colour) so the 4 px gaps read against the tiles' #0d0d0d | audit + coordinator |
| D1130 | (owner 2026-11-12: "start zooming out at 1/2 duration so other videos are more visible to more complete duration") Zoom 15-30 s (frames 450-899), compositor default `--zoom-start 0.5`; supersedes the 2/3 start in D1120. The zoom now begins with MCVD's second play, and the other tiles are on screen for most of their loop | owner request |
| D1131 | (owner 2026-11-12: "add 10 or 15 s more at the end after zoom complete so all are in view and viewer can watch") 15 s hold on the full grid after the zoom (frames 900-1349), every tile still looping: one complete loop of each story (all restart together at 30 s and end at p = 1 on the last frame). Total 45 s. Compositor `--hold 15` | owner request |
| D1132 | (owner 2026-11-12: "improve on anti aliasing, details look horrible") Cause: the 0.5 CDP clip scale rasterized non-hero stories at half size (no supersampling, canvas shrunk bilinear); the hero had only 4x MSAA at 1x. Now every story renders at deviceScaleFactor 2 (WebGL at pixel ratio 2 with MSAA, text at 2x), screenshot 3840x2160 (CDP clip scale is per CSS px, so scale = 2), box-filtered down by an integer factor (hero 2, tiles 4) in `scripts/showcase_video_downsample.py`, which takes each 4K JPEG from a temp file and deletes it at once (disk had 4.4 GiB free). Hover targets reused from the earlier scan (`--reuse-hovers`; CSS px). 159-175 ms/frame | owner request |
| D1133 | (owner 2026-11-12: "when you pause for the tooltip showcases, make it quick slow down, and then speed back up (e.g. 0.3 s each), instead of hard start stop") Each hold is entered and left through 0.3 s cosine playback-rate ramps (1 -> 0, hold 0.8 s unchanged, 0 -> 1); each ramp costs 0.15 s of play time, absorbed in the loop scale k so T stays 15 s; the hold still starts exactly at the hover chapter's end | owner request |

## TODO

- [x] Capture script: timeline (Play plan + pauses), hover target scan, cursor overlay, frame loop, resumable per story
- [x] Benchmark one frame by stage; pilot MCVD full-res
- [x] Capture all 16 (parallel workers)
- [x] Compositor: zoom + grid, encode
- [x] Verify: ffprobe, contact sheet of key frames, first / zoom / last frames
- [x] Fresh-context audit (fixes applied, re-captured, re-encoded)
- [ ] Soundtrack (owner, later)

## Progress log

- 2026-11-12: probe on a private vite dev server (port 47877, tmux `showcase-video-dev`); stage 1920x1060 at 1920x1080, footer 20 px -> D1123.
- 2026-11-12: capture script `app/scripts/showcase-video.mjs` written. Benchmark (MCVD, full res): 114-126 ms/frame, 450 frames in about 57 s; hover-target scan about 97 s per story (pane grid 40 px, plot grid 12 px). Pilot fixes:
  - stage rect measured after the stage is sticky (first measure gave y = 104).
  - pointer moves after the story drew the frame's p (a pointer that arrives before the plot exists gets no tooltip).
  - plot hover prefers drawn markers, else the series with most hits (first pick was the dashed lambda^-4 guide).
  - data-tip tooltips (process step chip) hide on scroll and re-arm only on pointerover: the pointer re-enters the target at the start of each hold.
  MCVD hovers: threaded feed member (ch 4), process step chip with the US 4,217,027 parameters (ch 6), measured loss curve point (ch 9). Key frames checked visually.
- 2026-11-12: full capture of 16 stories started (4 workers, tmux `showcase-video-cap`); compositor `scripts/showcase_video_grid.py` written (fixed-point log-scale zoom, float source boxes, LANCZOS; ease see D1128).
- 2026-11-12: all 16 captured (4 workers, about 10 min; 123-128 ms/frame; 376 MB of frames). Hovers per story (log `cache/showcase_video/capture-*.log`, targets `cache/showcase_video/hovers/<id>.json`): colladon1842 Basin, Water (no plot); gordon1954 focusing electrodes, inversion-level split; maiman1960 helical flash lamp, R1 line; hall1962 GaAs diode cube, light output; tien1969 glass substrate, TE observed; hayashi1970 graphite solution holder, pulsed points; macchesney1974 threaded feed member, process step chip, measured loss; papuchon1975 straight guide, delta-beta = 0 curve; mears1987 Er-doped fibre, Pabs = 100 mW; smit1988 phased array, Eq. (4) curve; knight1996 stack, air holes; waldhausl1997 PMMA-copolymer film, measured; liu2004 oxide, 8.0 mm measured; delhaye2007 silica disk, spectrum; herr2014 MgF2 microresonator, transmission; wang2018b T-rail segments, 20 mm device.
- 2026-11-12: composite + encode 20 s. Zoom ease changed from cubic to sine ease-in-out (D1128): cubic changed scale by 0.1 % in the first 0.7 s, so the zoom read as starting about 2 s late. Checked: ffprobe (30.000 s, 900 frames), moov before mdat, contact sheets of hover frames, zoom 605 / 630 / 660 and the final grid frame. Known: hard cut at 15 s where MCVD restarts from p = 0 (two plays); the cursor's glide back to rest can pass over a part and show its tooltip briefly (real pointer behaviour).
- 2026-11-12: fresh-context audit (subagent): timeline, encode, grid order and gaps, zoom continuity, pause holds (24 identical frames each) all verified; 32 of 33 hovers correct; fixes in D1129. Re-captured all 16 (signature v2), re-encoded; hover frames of gordon1954 (level split, 23 870 Mc/sec), maiman1960 (4F2 band), papuchon1975, macchesney1974 and the last frame checked. Intermediate check / audit images removed; frames, hover targets and capture logs kept under `cache/showcase_video/` for re-renders. Dev server (port 47877) and tmux sessions stopped.

## Handoff

- Rebuild: start a server (`cd app && ./node_modules/.bin/vite dev --host 127.0.0.1 --port <free port> --strictPort`), then `node scripts/showcase-video.mjs http://127.0.0.1:<port> --workers=4` (skips stories with a matching done.json; `--force` re-renders), then from the repo root `uv run scripts/showcase_video_grid.py`.
- Knobs: `--T` (loop length, s), `--hero`, `--small-scale`; compositor `--loops`, `--zoom-start`, `--gap`. Changing T means a re-capture (about 10 min at 4 workers).
- Soundtrack: the edit has no beat grid yet; to cut against a track, pick T so that 2 T matches whole bars.
- 2026-11-12: D1130 applied: re-composited from the existing frames (no re-capture); ffprobe 30.000 s, 900 frames, 15.7 MB; frames 449 / 480 / 560 / 660 / 780 / 899 checked (full-frame MCVD to 449, zoom from 450, grid at 899).
- 2026-11-12: D1131 + D1132 applied. Re-captured all 16 at 2x (about 5 min, 4 workers, no failures, temp folder empty after), re-composited: ffprobe 45.000 s, 1350 frames, 20.4 MB. Checked at 100 %: hero rail and burner edges and tile text no longer stair-stepped; hold frames 899 / 900 / 1100 / 1349. Dev server and tmux sessions stopped; check images removed.
- 2026-11-12: D1133 applied. Dry check of the timeline (MCVD: smooth p taper into and out of each hold, last frame p = 1); re-captured all 16 (2x, reused targets, no failures), re-composited: 45.000 s, 1350 frames, 20.2 MB. Measured on the MCVD frames around the first hold: mean frame difference 3.8 -> 3.2 -> 1.6 -> 0.7 -> 0.25 -> 0 into the hold, ramping back up after it.
