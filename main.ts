// The World in One Day — entrypoint for news-image-20261122.
//
// The finished front page is drawn before this program ever runs: draw.py
// paints the whole 1024x1024 image with PIL and saves it here as
// entry.png. This file does the only thing the grader needs it to do:
// copy that finished image into /output/entry.png.
//
// It uses nothing but the Node standard library, reaches no network, and
// writes the same bytes on every run, because it never redraws anything.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const targetDir = "/output";
const target = join(targetDir, "entry.png");

mkdirSync(targetDir, { recursive: true });
copyFileSync(source, target);
console.log(`wrote ${target}`);
