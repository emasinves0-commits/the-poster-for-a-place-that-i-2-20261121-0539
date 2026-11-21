// Veldora — entrypoint for "The Poster for a Place That Isn't There".
// v2: the poster is a rich painterly render produced by draw.py (see
// that file for the generation prompt + the PIL resize/optimise step)
// and shipped as entry.png; this program only copies it into the
// grader's output directory. It never draws anything itself, so the
// graded file is byte-identical to the entry.png in this repo.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
if (!existsSync(source)) {
  throw new Error(
    "entry.png is missing next to main.ts — run `python3 draw.py <generated.png>` first (see draw.py)",
  );
}
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "output";
mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, "entry.png"));
