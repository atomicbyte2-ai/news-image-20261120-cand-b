// news-image-20261120-cand-b: copies the pre-built entry.png to the output dir.
// The image itself was composed programmatically (PIL, flat vector-style
// drawings) from the verified 50-story list for Friday 20 November 2026;
// this script only copies it, after verifying its sha256 and size.
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const EXPECTED_SHA256 =
  "25c39a35f6778171981e46cc1d72dd827fd5f1f25a997d365c7a7a99bde4a57e";

const here = fileURLToPath(new URL(".", import.meta.url));
const sourcePath = join(here, "entry.png");
let bytes: Buffer;
try {
  bytes = readFileSync(sourcePath);
} catch {
  throw new Error(`cannot read entry.png at ${sourcePath}: file missing or unreadable`);
}
if (bytes.length === 0) {
  throw new Error(`entry.png is empty (0 bytes) at ${sourcePath}`);
}
if (bytes.length > 1048576) {
  throw new Error(
    `entry.png too large: ${bytes.length} bytes exceeds 1 MiB limit (1048576 bytes)`,
  );
}

const digest = createHash("sha256").update(bytes).digest("hex");
if (digest !== EXPECTED_SHA256) {
  throw new Error(
    `entry.png sha256 mismatch: got ${digest}, expected ${EXPECTED_SHA256}`,
  );
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "entry.png"), bytes);
console.log(`entry.png sha256 ${digest}`);
