// gta6-meme-x-01 entry program (Node 22, standard library only).
//
// The entry itself is the X post: the meme image was made by the agent,
// posted on X from a public account with make.fun and the entrant's play
// code in its text, and POST.json at this repository's root names that
// post. All this program has to do is hand POST.json to the grader by
// copying it into /output, where the gate reads it.
//
// The house reads the post from X itself (first picture, then text) and
// the judge scores the post, not anything this program writes.
//
// Run locally the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
// out/POST.json is then byte for byte this directory's POST.json.

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

// Fail fast on a placeholder or broken POST.json instead of handing in
// a file the gate would refuse: it must name a real X post address.
const postPath = join(botDir, "POST.json");
const post = JSON.parse(readFileSync(postPath, "utf8")) as { url?: unknown };
if (typeof post.url !== "string" || !/^https:\/\/(www\.|mobile\.)?(x|twitter)\.com\/[^/]+\/status\/\d+/.test(post.url)) {
  console.error(`POST.json does not name a post yet: ${JSON.stringify(post)}`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(postPath, join(outDir, "POST.json"));
console.log(`POST.json handed in: ${post.url}`);
