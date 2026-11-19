# AGENT.md — gta6-meme-x-01

Make a GTA 6 meme, post it on X, hand in the post.

1. Build the meme (`build-meme.py`, Python + PIL, deterministic). It must
   carry make.fun's ghost in the picture, be funny in one second, be about
   GTA 6 specifically (not a generic gaming joke), sell make.fun in its own
   voice, and read at a glance at 480 px. Our meme: "SAME SENTENCE" —
   Lucia did the time in her cell, the player did the waiting on his couch,
   both 4,811 days, same Vice City sunset; the ghost floats between them.
2. Post `meme.png` on X from the public account @wantorieta15. Post text
   must carry make.fun (link to the bounty page) and/or @makefunai, plus
   the entrant's play code, and pitch make.fun in the meme's voice.
   (Posting is done by the main agent / mas Wan — never by this build.)
3. Put the post's address in `POST.json` as
   `{"url": "https://x.com/<handle>/status/<id>"}`.
4. Test: `mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts`
   — `out/POST.json` must be byte-identical to `POST.json`.
5. Submit with the kit CLI (from the kit directory):
   `node cli/makefun.mjs check` then `submit --competition gta6-meme-x-01`.

Rules: Account 1 only (`~/.makefun/`). Free bounty, no fee. The repo must
be created after the bounty opened (2026-11-19T14:00:00Z). Keep the post
and the account public until results are out (result due 8 Dec 2026).
