# Image slots

The files here are **generated placeholder plates, not photographs.** They are
layered SVG scenes — dusk sky, haze, depth planes, grain — cut to the exact
aspect ratio of each slot, so the layout is final and real photography drops
straight in without anything reflowing.

Regenerate them with `python3 tools/make-plates.py`.

## Swapping in real photographs

```bash
# 1. add the file
cp ~/photos/rockville-teardown.jpg assets/img/photos/teardown.jpg

# 2. point the sources at it (pages/, never the built HTML at the repo root)
grep -rl 'photos/teardown.svg' pages/ | xargs sed -i 's|photos/teardown.svg|photos/teardown.jpg|g'

# 3. rebuild
./tools/build-pages.sh
```

Then **rewrite the `alt` text** to describe the photograph you actually used.
The current alt text describes the placeholder scene, and stale alt text is
worse than none.

Recommended: JPEG or WebP, ~1600px wide (2400px for `hero`), quality ~78,
under 300 KB each. The CSS crops with `object-fit: cover`, so a different
aspect ratio loses edges rather than distorting.

## The slots

| File | Ratio | Used on | Shoot |
| --- | --- | --- | --- |
| `hero.svg` | 2400×1250 | Home hero on tablet and desktop | A machine working a structure, dust in the air. Needs quiet space on the left third — the headline sits there. |
| `hero-portrait.svg` | 900×1300 | Home hero at 760px and below | The same job shot **portrait**. A landscape photo loses about 78% of its width to the crop in a phone-shaped frame, so shoot or crop a tall version rather than reusing the wide one. |
| `commercial.svg` | 4:3 | Home "Before" feature, Contact page head | A commercial or industrial building before or during demolition. |
| `cleared-lot.svg` | 4:3 | About "After" feature | A finished job: cleared, graded, stakes set, nothing left to trip over. |
| `teardown.svg` | 16:10 | Services page head | A house, garage or small commercial structure coming down. |
| `plant.svg` | 16:10 | Areas We Serve page head | Your machines and roll-offs staged on a site. |
| `site-wide.svg` | 2400×1000 | About page head | A wide establishing shot across a whole job. |

## Your own photos are better than stock

For a contractor, real job photos beat stock every time — they are proof of
work, and clients read them that way. Before/after pairs of the same site are
the most persuasive thing you can put on a page like this. Keep the client's
permission in mind before publishing a recognisable address.

If you do use stock, keep the licence record for each file alongside this
README so the provenance survives a handover.
