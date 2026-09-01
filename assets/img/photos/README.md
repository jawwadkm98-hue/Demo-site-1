# Image slots

These are the client's photographs, cropped and compressed into the site's
slots by `python3 tools/prepare-photos.py`. The full-resolution originals live
in `assets/brand/photo-originals/` and are held back from the deploy bundle by
`firebase.json`.

Do not edit the files here by hand — they are build output. Change the crop,
the bias or the width in `tools/prepare-photos.py` and re-run it.

## The slots

| File | Delivered | Used on |
| --- | --- | --- |
| `hero.jpg` | 1510×786 | Home hero, tablet and desktop. Machine right, quiet left third under the headline |
| `hero-portrait.jpg` | 900×1300 | Home hero on phones, via `<picture>` below 760px |
| `site-wide.jpg` | 1600×667 | About page head, full bleed |
| `commercial.jpg` | 1200×900 | Home "before" feature |
| `commercial-wide.jpg` | 1400×875 | Contact head — the same building, cropped to its other end |
| `cleared-lot.jpg` | 1200×900 | About "after" feature |
| `teardown.jpg` | 1400×875 | Services head, full bleed |
| `plant.jpg` | 1294×809 | Areas We Serve head, full bleed |
| `../service-area-map.jpg` | 1400×933 | Service-area figure on Home and Areas We Serve |

Width is set by how large each slot ever renders, not by the source file. A
half-column figure never needs more than about 1200px even on a 2x display,
and every pixel past that is bytes a visitor pays for.

## Two photographs do double duty

There are seven slots and six photographs, so `fleet-wide.png` serves both the
About head and the Areas We Serve head, and `commercial.png` serves both the
Home "before" feature and the Contact head. Each pair is cropped to a
different part of the frame and a different ratio so they do not read as the
same picture twice — that is what the `bias` column in `prepare-photos.py` is
doing. A seventh photograph would let those crops be dropped.

## If you replace one

1. Drop the new file into `assets/brand/photo-originals/` under the same name.
2. Re-run `python3 tools/prepare-photos.py`.
3. Check the `bias` still keeps the right part of the new frame.
4. **Rewrite the `alt` text** in `pages/` to describe the new photograph.
   Stale alt text is worse than none. The decorative page-head bands
   correctly carry `alt=""` — they sit behind headings and add nothing a
   screen reader needs.
5. Rebuild with `./tools/build-pages.sh`.

Keep the licence or provenance record for each photograph alongside this file
so it survives a handover.
