# Renewal Health site-v2 Redesign Notes

Date: 2026-07-22

## What changed
- All 20 content pages were rebuilt from the Squarespace mirror into clean, hand-rolled static HTML using a shared design system. Every word of copy, every heading, every image, and all internal links were extracted verbatim from the originals (site-mirror on :3006 is the untouched reference).
- New shared stylesheet `assets/v2.css` and interactions `assets/v2.js` are linked into every page. No CDN dependencies; everything is local.
- Home page (`index.html` / `home.html`, identical files) got a custom Digital Gravity inspired layout:
  - Full-bleed dragonfly photo hero with plum gradient veil, oversized serif headline, italic serif lede, dual CTAs, parallax on scroll, animated line-art dragonflies (drifting + wing flutter), scroll hint.
  - Scrolling word band ("Emerge / Align / Live Fully / Renewal Health", all existing copy).
  - Alternating split sections, symptoms checklist card, 7-service icon card grid, numbered 4-step process, plum CTA panel.
- Interior pages share the system: plum gradient page hero with floating dragonflies, alternating cream/white/sage sections, checkmark lists, framed images, closing "Start Your Renewal" CTA panel, reveal-on-scroll animations.
- Header: sticky frosted-glass bar, logo, dropdowns for Services (8 links) and About (3 links), Contact CTA pill, mobile hamburger nav.
- Footer: dark plum, logo card, tagline, three link columns.
- Testimonial quote paragraphs styled as quote cards.
- SEO: original titles and meta descriptions preserved on every page; one H1 per page; heading hierarchy preserved in original order.

## Design tokens (assets/v2.css)
- Colors: plum #4b2e5a / deep #372145 / ink #2d1b38, lilac #b79cc9 (+#e9e1f0), sage #8fae85 / deep #6d8f63 (+tint #eef3ea), cream #faf7f2, text #3a3141.
- Type: serif headings (Cormorant Garamond > Playfair > Georgia stack, system fallback only, no webfont files), Segoe UI body. Hero H1 clamps to 5.6rem.
- Motion: `.reveal` IntersectionObserver fade-ups, dragonfly drift/flutter keyframes, marquee word band, hero parallax. All disabled under prefers-reduced-motion.

## Regeneration
The whole build is scripted: it re-extracts copy from `../site-mirror` and rewrites site-v2 pages. Script kept in the session scratchpad (`build_v2.py`); copy it here if you want to re-run after mirror updates. Note: testimonials quote-card styling is a small post-processing regex on `<p>&quot;` paragraphs.

## Untouched / unfinished
- `cart.html` left as original (Squarespace JS cart, non-functional in a static mirror anyway).
- `blog/category/*` and `blog/tag/*` listing pages left as original mirror pages (linked only from the blog post's category chips).
- `sitemap.xml` unchanged.
- Contact page has no form: the original static mirror never captured the Squarespace form (it is injected by JS on the live site), so the page shows the contact copy + CTA. When this moves to a real platform, add a working form there.
- Original copy contains em dashes; copy was preserved byte-for-byte per "change zero wording", so they remain.
- Step cards on the home page show both a decorative number (01) and the original "1. ..." heading text, kept because wording is preserved verbatim.

## Polish pass (2026-07-23)

Goal: better looking and more compact, with zero content removal. No copy was reworded, cut, or added anywhere.

### Measured result (headless Edge, 1280px wide, document scrollHeight)

| page | before | after | delta |
|---|---|---|---|
| index.html / home.html | 6210 | 4234 | -32% |
| services.html | 8925 | 6756 | -24% |
| neurodivergent-support.html | 9972 | 7042 | -29% |
| gut-health-support.html | 9273 | 7216 | -22% |
| programs-packages.html | 7045 | 5085 | -28% |
| about.html (and about-lynette...) | 6273 | 4895 | -22% |
| why-a-dragonfly-renewal-health.html | 4133 | 3657 | -12% |
| testimonials.html | 3334 | 2466 | -26% |
| blog.html | 1894 | 1557 | -18% |
| contact-renewal-health.html | 1706 | 1276 | -25% |

Homepage section breakdown, before to after: hero 662 to 475, word band 72 to 50, intro 761 to 545, root cause 773 to 520, services 1505 to 700, process 1059 to 760, CTA 767 to 580, footer 534 to 379, header 79 to 61.

### Design system changes (assets/v2.css)
- Real spacing scale as custom properties (`--s-1` through `--s-10`, `--gutter`, `--section-y`, `--wrap`). Section padding is now a single fluid token, `clamp(2.75rem, 4.6vw, 4rem)`, down from a flat 5.5rem.
- Fluid type scale on every level with `clamp()`. Body 17px to 16.5px, line height 1.75 to 1.68, paragraph rhythm tightened. Headings got `text-wrap: balance`, tighter letter spacing and line height. Default measure capped at 68ch for readability.
- Radius scale (`--r-xs` 8 through `--r-lg` 22) replaces the single 22px radius, so small elements no longer look over rounded. Softer, less blurry shadow tokens plus a dedicated hover lift token.
- Header is slimmer (logo 56px to 46px, tighter padding) and nav links gained an animated sage underline. Dropdowns are smaller with a hairline border.
- Cards rebuilt: flex grid so the 7 service cards sit 4 across with the trailing 3 centred, instead of an uneven 3 across block. Smaller icons, tighter padding, hover lift with a sage border tint.
- Step cards: fixed 4 across on desktop, a sage to lilac top bar that wipes in on hover, smaller decorative numeral.
- Buttons, links and all interactive elements now have a visible `:focus-visible` ring in sage.
- Testimonial and quote cards restyled as left rule cards rather than heavy padded blocks.
- Footer compacted from 4.5rem to 2.6rem padding with tighter columns. Every link is still there.
- Sage green darkened to #5f8155 for AA contrast on cream, and emphasis text on the plum panels now inherits light colour instead of the dark body grey (that italic line in the CTA was previously low contrast).
- Motion kept and refined: shorter reveal distance and duration, slower dragonfly drift and wing flutter, slower word band. `prefers-reduced-motion` now also kills the scroll hint and clamps all transitions.
- Fixed a pre-existing horizontal overflow: the off canvas mobile nav made the document scroll sideways. `overflow-x: hidden` on `html` clips it. Verified `documentElement.scrollWidth` is now inside the viewport at 492, 744, 1024 and 1280.
- Mobile: card and step grids collapse cleanly, footer goes 2 columns then 1, nav panel restyled, type scales down at 640.

### Structural change on interior pages
The generator emitted every content chunk as its own full padded band with alternating cream, white and sage backgrounds. On a page like neurodivergent-support that meant 11 bands, roughly 1900px of pure padding, and a stripey choppy read.

Those runs are now merged into one continuous `.section.article` editorial column. This is a pure structural merge: the inner HTML of every merged band is preserved verbatim and in order, only the wrapper `</div></section><section ...><div ...>` seams were removed. Rhythm inside the article now comes from typography instead of background stripes: a hairline rule and short sage marker above each `h2` that follows body content.

Also on article pages:
- `ul.checks` lists render as a white bordered panel in 2 columns on desktop, 1 on narrow screens. Big saving on the service pages, which are full of symptom lists.
- In article figures are capped to a 2:1 band (lead figure 16:6) rather than running at natural height. Nothing is cropped out of the layout, the images are just framed as editorial bands.

### Verification
- Text diff: visible text extracted from all 19 rebuilt pages plus the blog post, word by word, before and after. 0 pages differ, 14232 words on the top level pages and 1633 on the blog post, identical sets and order.
- Link and asset sweep: 2138 local href and src references across every HTML file resolve to a file on disk. 0 broken. The only external hosts referenced are inside the untouched mirror pages (`blog/category/*`, `blog/tag/*`) and `cart.html`, exactly as before. The 20 rebuilt pages are fully offline safe.
- SEO: every `<title>` and `<meta name="description">` byte identical to the pre pass version, and every page has exactly 1 `<h1>`.
- Visual: full page headless screenshots at 1280 and at 492 (Edge headless clamps its minimum window width to 492, so a true 390 capture was not possible; the 640 and 430 breakpoint logic was reviewed by hand and the 492 render is correct).

### Left undone
- `cart.html`, `blog/category/*` and `blog/tag/*` are still raw mirror pages and were not touched, same as before.
- The contact page still has no form. It needs one when this moves to a real platform.
- Testimonials are still a single column stack. A 2 across grid would compact further but the heading, subheading and quote are flat siblings, so it needs a markup regroup rather than a CSS change.
- `why-a-dragonfly` only came down 12% because it is mostly one long image plus short copy.
- `build_v2.py` was not updated. If it is re run it will regenerate the old one band per chunk markup, so re run `merge_sections` style post processing after any rebuild.

## Feel and motion pass (2026-07-23)

Goal from Jack (voice brief): kill the templated sameness, calm the motion, make the hero premium and immersive, consolidate the nav, tidy the data, and fix Lynette's photo. Zero copy removed or reworded anywhere. All changes are layout, markup structure, CSS and JS. Applied through `apply_redesign.py` (idempotent per-page transform) plus edits to `assets/v2.css` and `assets/v2.js`.

1. Layout variety (no more identical section treatment). A small vocabulary of distinct treatments is now distributed so consecutive sections differ and pages lead differently. Home already alternates split-image-left / split-image-right / centered card grid / split + staggered step cards / plum CTA panel. Interior pages get one of four hero treatments (centered plum, left-aligned editorial `ph-left`, softer statement `ph-quiet`, lilac side-band `ph-band`) plus one of three article lead treatments (`av-band` wide cinematic, `av-panel` bordered/framed, `av-offset` floated lead image with the opening prose wrapping beside it), and alternate cream vs white article backgrounds (`art-white`). The hero/article variant per file is a fixed map in `apply_redesign.py` so the rotation is deterministic and cohesive.
2. Scroll reveal reworked. The old ongoing per-section IntersectionObserver fade-up is gone. Only the FIRST content section per page animates in now, once, on load. That section is tagged `.intro-reveal` (added to the first `.section` after the hero); its `.reveal` children lift into place. Everything below is already in place with no scroll animation (`.reveal` now defaults to fully visible). `v2.js` adds `.in` to the single intro section on load. Under `prefers-reduced-motion` the intro section is forced visible immediately.
3. Services + Programs consolidated in the nav. The standalone top-level "Programs & Packages" item was removed; it now lives inside the Services dropdown below a hairline divider (`li.drop-sep`). No page or content deleted: `programs-packages.html` is unchanged and still reachable from the dropdown and the footer Explore column. Top-level nav went from 6 items to 5.
4. Data simplified by layout only. The article lead treatments and the reworked Lynette block tighten hierarchy and reduce clutter; no copy changed. (Prior polish pass already merged the stripey per-chunk bands into one editorial column and put symptom lists into bordered 2-column panels.)
5. All floating/drifting dragonflies removed. Every `<svg class="hero-dragonfly">` (hero backgrounds and CTA panels, 3 to 5 per page) was stripped site-wide.
6. New home hero entrance. A single tasteful line-art dragonfly (`.df-entrance`) flies in from the bottom-left to the top-right corner once on first load (`df-fly`, `forwards`, no loop) and the hero content fades up behind it (`hero-open`). After it completes the hero sits calm. Under `prefers-reduced-motion` the final state (dragonfly resting top-right, content visible) shows immediately with no flight.
7. Immersive over-hero header. On every page (`body.has-hero`) the header is now `position:fixed` and transparent at the top, so the hero background extends behind it (nav text and hamburger go light, logo gets a soft white chip). Once the user scrolls past the hero it transitions to the solid frosted style (`.scrolled`, toggled by `v2.js` at hero height minus 64px). `scroll-padding-top` and extra `.page-hero` top padding keep content clear of the fixed bar.
8. Scrolling word band deleted site-wide. The "Emerge / Align / Live Fully / Renewal Health" marquee under the home hero is gone. (Text diff shows home/index dropping exactly 12 words = the two duplicated marquee runs; every one of those words still exists in the hero H1 "Emerge. Align. Live Fully." and the footer tagline, so no unique copy was lost.)
9. Lynette's photo fixed. Her portrait was being cropped to a 16:8 band that cut off her face. It is now a smaller 4:5 portrait with `object-position:50% 18%` so her full face shows, laid out as a clean two-column `.bio-block`: her content on the LEFT (the opening heading plus first two paragraphs), her photo on the RIGHT, with a sage offset frame. On mobile the portrait stacks above the copy. Applies to `about.html` and `about-lynette-wing-renewal-health.html`.

### Verification (2026-07-23)
- Text diff, visible text every page before vs after: 20 pages, 15845 -> 15821 words. The ONLY delta is home/index -12 words, the deleted decorative marquee (item 8); all other 18 pages are word-for-word identical, same order. 0 loss of her copy.
- Titles and meta descriptions: byte-identical on all 20 pages. Exactly one H1 per page.
- Link/asset sweep: 919 local href/src references across all rebuilt pages plus the blog post resolve on disk. 0 broken. Only external hosts referenced are inside untouched mirror pages.
- Headless Edge screenshots in `qa-shots/` at 1280 and ~492 wide (Edge headless clamps min width to 492, so a true 430 render was not possible; mobile breakpoints reviewed at 492): home (full length), about, programs-packages, services, gut-health, plus a `--force-prefers-reduced-motion` home capture. Eyeball confirms: no floating dragonflies, hero covers the header, word band gone, first-section-only reveal, Lynette's face visible with photo right / content left, and visibly varied hero + section treatments across pages.

### Left as-is
- `cart.html`, `blog/category/*`, `blog/tag/*` untouched (raw mirror), same as before.
- Contact page still has no form (needs one on a real platform).
- `services.html` remains the detox content that "Services Overview" links to (a pre-existing quirk of the original build); not a content change, left alone.
- `apply_redesign.py` is idempotent but assumes the current markup; re-run `merge_sections.py` first if `build_v2.py` is ever re-run.

## [2026-07-23] Hotfix (main session QA)
- Hero content (H1 "Emerge. Align. Live Fully.", lede, CTAs) was invisible for the first 1.2s on load: `.home-hero.opened .home-hero-content` used `hero-open 1.1s ... 1.2s both`, so `both` fill held the from-state (opacity 0) through the 1.2s delay. Visitors saw an empty hero. Shortened to `.9s ... .3s both`. Verified settled render via Edge headless --virtual-time-budget: H1, lede, both CTAs, immersive over-hero header, dragonfly resting top-right, no word band, first-section split all correct.

## Immersive hero, hero variety, service merge, blog build (2026-07-23, batch 2)

Six-area front-end batch. Zero of Lynette's copy was reworded or deleted; the only content-affecting change is the service heading merge (item 3, proven in SERVICES-MERGE-LOG.md) and the blog formatting. No em dashes were introduced. All assets local; prefers-reduced-motion and focus states preserved.

1. HOME HERO - full-screen immersive. `.home-hero` is now `min-height:100vh` (full viewport on open, header transparent over it via the existing has-hero behavior). The white line-art `.df-entrance` SVG was replaced by a REALISTIC dragonfly: a free Pexels photo (id 18151389, dragonfly in mid-flight, Petr Ganaj) was cut out with rembg into `assets/dragonfly-flight-cutout.png` (transparent, alpha-cropped, 900px). New `.df-flight` element flies once from bottom-left (translate -14vw,96vh) across the whole viewport to rest near top-right (74vw,7vh), non-looping (`forwards`), tasteful eased path with subtle scale/rotation. Hero H1/lede/CTAs kept and settle in at .3s (unchanged). Under prefers-reduced-motion the dragonfly shows at rest and content is visible immediately, no flight. The liked service-card hover motion and first-section-only reveal are untouched.
   Note: Edge headless `--virtual-time-budget` does NOT advance CSS animations (it captures the initial keyframe), so the settled hero was QA'd with `--force-prefers-reduced-motion`, which renders the identical final state. Real browsers run the flight normally.

2. HERO IMAGE VARIETY - the dragonfly-on-grass photo (pexels-depthofraw-10722719) is now the HOME hero only. It was removed as the repeated inline figure on every interior page. 14 fresh, fully-attributed calming nature/botanical images were sourced from Pexels into `assets/heroes/` (each unique per page) and wired as photo-backed heroes (`.page-hero.has-photo` = image + plum veil). No two pages share a hero image. Full mapping + sources in IMAGE-LEDGER.md.

3. SERVICES CONSOLIDATION - merged the naturopathic-vs-homeopathic split framing into one unified presentation. Only three pages actually had the hard split (detox, its services.html mirror, and inflammation's stray block); the other service pages already introduced both together in a single heading. The merge changed ONLY split-framing heading labels; every body paragraph, list, symptom, mechanism and instruction is preserved verbatim. Word deltas: detox +1, services +1, inflammation +2 (heading tokens only). Full point-by-point preservation proof in SERVICES-MERGE-LOG.md.

4. ABOUT - the flat purple banner is now a soft water-lily texture under a layered plum overlay (elegant, readable). Lynette's portrait renders fully uncropped (object-fit:contain, aspect 599/757) on the right with her copy on the left. Source is only a 599x757 head-and-shoulders image, so a true full-body shot needs a new photo from Lynette (logged in OPEN-QUESTIONS.md).

5. TESTIMONIALS - top photo removed. The page now leads loud with the three testimonials as large cards (first full-width, then a 2-up grid) headed "Real Results from Root-Cause Health Support". Every testimonial and attribution kept (only the 3 decorative " | " separators between quote and name were dropped). The reflective narrative follows below.

6. BLOG - blog.html is now a real index: 4 cards (the 3 new posts + the existing root-cause post) with thumbnail, category, date, title and excerpt, plain plum-on-white for AA contrast (fixes the purple-on-purple). The 3 ready drafts were built as real pages under `blog/` using the site shell (shared nav/footer, one H1 = post title, title/meta from frontmatter, Article + FAQ JSON-LD carried over, images copied to `assets/blog/<slug>/`, site-internal absolute links rewritten to local, external citations kept). Post wording unchanged. The pre-existing root-cause post was modernized to the current nav/footer, its floating dragonflies removed, and given a photo hero + back-link. Every post links back to the index.

### Verification (batch 2)
- Text diff (visible words, before vs after, 20 top-level pages + root-cause post): 13 non-restructured pages are 0-word identical. Restructured deltas are all accounted for: detox/services +1, inflammation +2 (heading-label tokens only, body intact); testimonials -1 (3 "|" removed, "Patient Stories" eyebrow added, all quotes+names intact); blog.html rebuilt (meta description filled from empty); root-cause +5 ("Back to the blog"). No page title changed; every page has exactly one H1.
- Blog posts vs drafts: each built post contains 100% of its draft article prose (only the title + byline moved into the hero).
- Link/asset sweep: 2475 local href/src refs across 41 HTML files (incl. the 3 new posts) resolve on disk; 0 broken. External hosts are the blog citations (Cleveland Clinic, NCBI, Harvard Health, Poetry Foundation, BibleGateway) and the untouched mirror pages.
- Headless Edge screenshots in qa-shots/ at 1280 and ~492: home hero (settled, reduced-motion), home full, detox (consolidated), about, testimonials, blog index, and the vagal-tone post. Eyeballed: full-viewport immersive hero + realistic dragonfly at rest top-right, distinct hero photo per page, seamless consolidated detox, richer About banner + full uncropped portrait right / copy left, testimonials leading loud with no top photo, blog index real with readable contrast and working post pages.

### Deliverables added
IMAGE-LEDGER.md, SERVICES-MERGE-LOG.md, OPEN-QUESTIONS.md, assets/heroes/ (14 images + _ledger.json), assets/dragonfly-flight-cutout.png, assets/blog/<slug>/ images, blog/<slug>.html x3. Helper scripts: _apply_heroes.py, _build_blog.py, _check_text.py.

## Dragonfly curtain reveal, service card grids, About portrait, testimonials legibility (2026-07-23, batch 3)

Front-end batch from Jack's voice feedback. No copy of Lynette's was reworded or deleted except
the directed detox retitle and the de-duplication proven point by point in SERVICES-MERGE-LOG.md.
No em dashes introduced. All assets local, no external runtime requests added.
prefers-reduced-motion, AA contrast and visible focus states preserved throughout.

### 1. Home hero: the dragonfly opens the page

Replaced the previous photo-cutout dragonfly (too photorealistic, too small, and it stayed
pinned to the viewport while scrolling) with a purpose-built cinematic entrance.

- **Solid plum curtain.** `.hero-curtain` is a `position:fixed` full-viewport panel at
  `z-index:120` (above the fixed header) filled with a solid deep brand plum:
  `var(--plum-ink)` #2d1b38 base under a barely-there deep plum gradient
  (#3d2450 to #2d1b38 to #2a1734) plus one soft plum radial. It is opaque, not a translucent
  veil over the photo, so the page genuinely starts as rich purple.
- **Large stylised dragonfly.** `.df-reveal` is hand-drawn inline SVG (no photo, no raster
  asset, nothing to download): a 640x360 viewBox with a tapered segmented abdomen, thorax,
  compound eyes, legs, and two pairs of long swept wings filled with white-to-lilac gradients
  at partial opacity, hairline vein work, pterostigma marks and a soft plum aura so the
  silhouette holds against the curtain. It renders at `min(54vw,74vh)` on desktop and
  `min(88vw,54vh)` on narrow screens, roughly half the viewport as it crosses. The two wing
  pairs beat on offset `df-beat` cycles and a `df-glint` gradient band sweeps along the wings
  for shimmer, clipped to the wing shapes.
- **The dragonfly opens the curtain.** `df-cross` flies it from off-screen left
  (`translate(-62%, 7vh)`) to off-screen right (`translate(132vw, -8vh)`) with a gentle arc and
  rotation. `curtain-wipe` animates the curtain's `clip-path` polygon from
  `-34% / -48%` to `148% / 134%`, a slanted trailing edge that tracks the dragonfly's x
  position. Both use the identical duration, delay and easing
  (2.45s, 0.15s delay, `cubic-bezier(.44,.06,.34,1)`) so the reveal edge stays locked to the
  flight and the hero photo, H1, lede and CTAs are uncovered along its path.
- **Timing.** 0.15s delay + 2.45s flight, with the hero content fading up at 0.55s over 0.9s.
  Total entrance ~2.95s, and hero content is fully visible well before the end.
- **The dragonfly is removed, guaranteed.** It fades to `opacity:0` over the last 16% of the
  flight, and `v2.js` listens for `animationend` on `df-cross` and calls `removeEntrance()`,
  which `removeChild`s BOTH the curtain and the SVG and stamps
  `documentElement[data-entrance="done"]`. A `setTimeout(finish, 3200)` fallback covers any
  browser that misses the event, and the handler is idempotent. Nothing can linger or follow
  the reader while scrolling because the nodes no longer exist.
  Asserted in QA with `--dump-dom`: after the entrance, `class="df-reveal"` and
  `class="hero-curtain"` are both absent from the DOM and `data-entrance="done"` is present,
  in normal motion AND under `--force-prefers-reduced-motion`.
- **prefers-reduced-motion.** CSS sets `display:none !important` on both, and `v2.js` removes
  them immediately without running anything, so reduced-motion users get the finished hero at
  once with no curtain and no dragonfly.
- **QA hook.** `index.html?stage=flight` adds `html.df-freeze`, which applies
  `animation-delay:-1.05s; animation-play-state:paused` to the curtain and the dragonfly and
  pauses the wing beat, seeking the entrance to t=1.05s and holding it. This exists because
  Edge headless `--virtual-time-budget` does not advance CSS animations; it is how the
  mid-flight screenshots were captured. Nothing is removed while frozen.
- Kept untouched: service-card hover motion, first-section-only scroll reveal, immersive
  transparent over-hero header.
- The old `assets/dragonfly-flight-cutout.png` is no longer referenced by any page. It is left
  on disk and marked retired in IMAGE-LEDGER.md.

### 2. Service pages: retitled, de-duplicated, reformatted as card grids

Full point-by-point proof in SERVICES-MERGE-LOG.md. Summary:

- Detox retitled to **"Naturopathic Detox"** in the H1 and the `<title>` (the only title change
  on the site); its in-body "Is Naturopathic and Homeopathic Detox Right for You?" heading
  became "Is Naturopathic Detox Right for You?". Filename unchanged, all links still work.
- De-duplication: 2 duplicate subtitles on detox/services, 1 verbatim duplicate heading on
  weight, and on inflammation a 253-word block that was a byte-for-byte copy of the detox
  page's central detox section. Word deltas: detox -17, services -17, weight -6,
  inflammation -253, and 0 on gut, hormones, emotional overwhelm, neurodivergent and programs.
- Reformat (zero words moved or lost): stacked double H2s became eyebrow kickers, orphan
  heading-like paragraphs became real H3s, runs of sibling H3 sections became `.svc-cards`
  grids in the home-page card language, and the three programs became `.pkg-cards`.
- New CSS: `.svc-cards` / `.svc-card` (auto-fit grid, hairline border, sage-to-lilac hover bar,
  hover lift, sage rule under each heading, nested `ul.checks` de-panelled),
  `.pkg-cards` / `.pkg-card` (three-up, plum top rule, display numeral). Both grids break
  gently out of the narrow reading measure above 860px so the cards get real width while the
  prose keeps its comfortable line length; they collapse to one column under 560px.
- The purple page-hero backgrounds and each page's distinct hero image are untouched, as asked.

### 3. About: Lynette's portrait rendered whole

The generic in-article rule `.article .flow figure img{aspect-ratio:16/8;object-fit:cover}` was
out-specifying the old `.bio-portrait img` rule and cropping her portrait to a 16:8 band, which
is why only her head showed. New higher-specificity rules
(`.article .flow .bio-portrait figure img`) reset `aspect-ratio:auto`, drop the crop and render
the source at its natural 599x757 proportions, `width:100%; height:auto`, so nothing is cut off.
The frame is bigger (430px, up from 360px) and sits in a soft white-to-cream mat with a hairline
border, rounded corners, soft shadow and an offset sage rule behind the lower-right corner, with
the copy on the left in a `1.05fr / .95fr` grid, vertically centred. Under 760px it stacks and
centres at 340px. A true head-to-toe shot is impossible from a 599x757 head-and-shoulders source;
that still needs a new photo from Lynette (already logged in OPEN-QUESTIONS.md). Nothing else on
the About page was changed and its visible text is a 0-word diff.

### 4. Testimonials: same layout, easier to read

CSS only, every testimonial, attribution and word untouched (0-word diff).

- Quote size up to `clamp(1.08rem, 1.25vw, 1.19rem)`, line-height 1.6 to **1.78**, colour moved
  from the soft grey to full `--ink` for stronger contrast.
- Measure capped at **60ch** so a quote is never a 1100px line.
- The lead (full-width) testimonial now puts its category and "The Shift" line in a left column
  and the quote in a comfortable right column above 880px, instead of running the quote across
  the whole card.
- Card padding up to `clamp(1.7rem, 3vw, 2.8rem)`, grid gap up to `clamp(1.4rem, 3vw, 2.4rem)`.
- The attribution is now plum, bolder, larger, and separated by a hairline rule above it.
- The "Patient Stories" eyebrow is centred to match the centred heading.
- The decorative quote glyph was softened so it never competes with the text.

### 5. Blog

Untouched, as instructed. Blog index and all post pages are 0-word diffs.

### Verification (batch 3)

- **Link and asset sweep:** 2378 local href/src references across 38 HTML files all resolve on
  disk. **0 broken.** External hosts are unchanged: the blog's citations (Cleveland Clinic,
  NCBI, Harvard Health, Poetry Foundation, BibleGateway) and the untouched raw mirror pages
  (`cart.html`, `blog/category/*`, `blog/tag/*`).
- **Content preservation:** visible text extracted word by word before and after on all 25
  pages. **14 of 14 non-service pages are 0-word identical**, including every About,
  testimonials and blog page. The only deltas are the 4 service pages listed above, each
  justified line by line in SERVICES-MERGE-LOG.md.
- **Headings:** 37 of 38 pages have exactly one H1. The exception is `cart.html`, an untouched
  raw Squarespace mirror page with no H1, exactly as before.
- **Titles:** one intentional change, the detox page (and its `services.html` mirror), from
  "Naturopathic Detox &amp; Homeopathic Detox | ..." to "Naturopathic Detox | ...". Every other
  `<title>` and every `<meta name="description">` on the site is byte-identical.
- **Entrance removal:** asserted with `--dump-dom` that `.df-reveal` and `.hero-curtain` are
  absent from the DOM and `data-entrance="done"` is set once the entrance finishes, in both
  normal motion and forced reduced motion. Nothing overlays content while scrolling.
- **No horizontal overflow:** `documentElement.scrollWidth === clientWidth` on 12 pages
  measured at 1280, 1024, 744 and 492 viewport widths.
- **Screenshots** in `qa-shots/` at 1280 and 492: `home-entrance-start-*` (purple curtain plus
  the large stylised dragonfly mid-flight), `home-settled-*`, `detox-condensed-*`,
  `about-full-portrait-*`, `testimonials-*`, plus `gut-health-cards-1280`,
  `programs-cards-1280`, `inflammation-1280` and `home-full-1280`.
  Capture method, since Edge headless `--virtual-time-budget` does not advance CSS animations:
  the mid-flight frames use the `?stage=flight` freeze hook described above (negative
  animation-delay plus `animation-play-state:paused`), and every settled frame uses
  `--force-prefers-reduced-motion`, which renders the identical finished state.

### Helper scripts added

`_hero_entrance.part` (the entrance markup, injected by `_inject_hero.py` into index.html and
home.html, idempotent), `_service_cards.py` (the service-page restructure, with the explicit
de-duplication tables), `_text_snap.py` (visible-text snapshot and diff), `_qa_sweep.py`
(link/asset sweep, H1 and title report), `_qa_shots.sh` (screenshot run).

### Follow-up within batch 3

Card grouping initially swallowed the concluding paragraph of a parent H2 section into the last
card of the grid below it (for example "Together, this creates a more stable environment where
your gut can heal and regulate." on the gut page). `_card_tails.py` pulls those surplus trailing
paragraphs back out, after the grid, on gut, hormones, inflammation, emotional overwhelm and
neurodivergent. Verified as a pure move: word-for-word text diff before and after the fix is
0 across all 25 pages.

Stale batch-2 captures (about-1280/492, detox-1280, home-hero-1280/492) were removed from
qa-shots/ since batch-3 captures supersede them. The blog captures were kept, since the blog was
deliberately untouched.


## Hero entrance v3, image de-duplication, slug cleanup, testimonial restyle (2026-07-23, batch 4)

Front-end batch from Jack's voice feedback. **Zero words of Lynette's copy were reworded,
added or removed anywhere: the visible-text diff is 0 differences on all 24 pages.** Titles
and meta descriptions untouched, one H1 per page. No em dashes introduced. No CDN or external
runtime request added; every asset is local. prefers-reduced-motion, AA contrast and visible
focus states preserved (and the reduced-motion hero was actually fixed, see below).

### 1. Hero entrance v3

**Faster.** Total entrance is now **1.75s** (0.10s delay + 1.65s flight), down from 2.95s.
Hero content settles at **0.96s**, well before the end, so the H1, lede and both CTAs are
fully visible while the dragonfly is still finishing its exit. Wing beat sped up from 0.26s
to 0.17s. The v2.js hard-removal fallback moved from 3200ms to 2100ms to match.

**Diagonal, bottom-left to top-right.** df-cross now flies the whole diagonal, from
translate(-58%, 58vh) at the bottom-left corner to translate(132vw, -60vh) past the
top-right corner, nose pitched up through the arc. curtain-wipe animates the curtain's
clip-path along a slanted trailing edge that slides up and to the right on the same
duration, delay and easing, so the reveal edge tracks the flight. The polygon runs from
(-80% -20%, 250% -20%, 250% 220%, 40% 220%) to
(118% -20%, 250% -20%, 250% 220%, 238% 220%); both end points were solved so that at t=0
every viewport corner is inside the curtain and at t=1 every viewport corner is outside it.
No wedge of curtain can be left behind anywhere. Verified visually at 1280 and 492 at four
points along the flight.

**Curtain colour, derived from the hero photograph.** The hero photo
(pexels-depthofraw-10722719.jpg) was sampled with Pillow: an 8-colour median-cut quantise
plus a 1x1 average. Its dominant colour is **#032644**, a deep blue at hue 208 (the average
is #0e2133, same hue family). That hue was blended 35% into brand plum-ink #2d1b38 (hue 277)
and lifted 6 points of lightness in HLS, landing on **#291e52**: hue 253 blue-violet,
lightness 0.22 against plum-ink's 0.16. The curtain is that colour, fully opaque, with a
linear-gradient(148deg, #392970, #291e52 46%, #241a47) and one soft rgba(96,72,153,.34)
radial. It is not a translucent veil. The handoff into the dark blue-violet hero photo now
reads as the same world.

**A far more realistic dragonfly.** The flat hand-drawn SVG was replaced by a generated
naturalistic one, still pure vector, still inline, still no raster asset and no download.
It is authored by _make_dragonfly.py, which computes the geometry mathematically:

- Each of the four wings is a quadratic spine plus a width profile, giving a properly
  tapered anisopteran blade: narrow at the articulation, broadest just past mid-wing,
  rounded apex, straighter leading edge than trailing edge.
- **Dense venation.** Nine longitudinal veins per wing plus a staggered cross-vein mesh
  (roughly 280 cross veins per wing) clipped to the wing outline, so it reads as real
  wing cells rather than a few decorative lines. The costal leading-edge vein is drawn
  thicker, as on a real wing.
- **Pterostigma** drawn as a real opaque cell near each apex, not a smudge.
- **Iridescence.** A blue-violet to teal to violet gradient washes over each membrane at
  low opacity for the oil-slick sheen; membranes are translucent white to lilac.
- **Motion blur.** A blurred, lagging ghost copy of the beating forewing pair
  (feGaussianBlur, offset, on its own beat phase) sells the speed.
- **Body.** Ten-segment abdomen computed with the real S6 pinch and S8 club, a lit dorsal
  ridge, cerci, a shaded thorax with a shoulder cap over the wing articulation, five
  delicate spined legs folded forward, and two large faceted compound eyes with a
  specular highlight.

It renders at min(52vw,72vh) desktop and min(92vw,56vh) narrow, still roughly half the
screen. Deliberately NOT a photo cutout, which Jack rejected.

**Kept:** removal of both nodes on completion with the timeout fallback, prefers-reduced-motion
skipping to the finished hero, service-card hover motion, first-section-only reveal,
immersive over-hero header.

**Bug fixed along the way.** Under prefers-reduced-motion the hero content was still invisible:
.home-hero.opened .home-hero-content (specificity 0,3,0) was out-specifying the reduced-motion
override (0,2,0), so reduced-motion users got the delayed fade rather than the finished hero.
The override is now explicit and uses !important. Confirmed by capture.

**QA hook extended:** ?stage=flight still freezes the entrance (default t=0.75s) and now also
accepts &t=<seconds> to seek any frame, which is how the flight was checked end to end.

### 2. Image de-duplication (site-wide)

14 images were used in more than one place, across 34 reference sites. All repeats are gone;
23 fresh free-to-use photographs were downloaded locally into assets/figures/. The white
lattice/web picture Jack called out (interconnected-holistic-health.jpg) was the article lead
on 11 pages plus the home intro and is now referenced by zero pages. Full before/after map,
provenance and the 53-row uniqueness table are in IMAGE-LEDGER.md.

### 3. Service page slugs

| old | new | why |
|---|---|---|
| naturopathic-homeopathic-detox.html | **naturopathic-detox.html** | the page was retitled "Naturopathic Detox" in batch 3; the filename still carried the dropped dual naming |

120 references were rewritten across 49 files: nav, the Services dropdown, footers, in-page
links, blog post links, the raw mirror pages under blog/category and blog/tag, cart.html
and sitemap.xml. A grep for the old slug returns 0 hits in any .html, .xml or .md file
(the only matches left are inside _batch4_verify.py, which reverts the rename on purpose to
prove the text diff).

Every other service filename was reviewed and left alone: gut-health-support,
hormone-balance-support, inflammation-support, neurodivergent-support,
weight-metabolic-health and emotional-overwhelm-nervous-system all match their titles, and
naturopathy-homeopathy-holistic-healing is genuinely about both modalities (H1 "Naturopathy
and Homeopathy"), so its dual naming is accurate rather than stale.

**services.html** is now a byte-for-byte alias of naturopathic-detox.html. It has always
carried the detox content (a quirk inherited from the original build) while the nav labels it
"Services Overview". Making it a true alias keeps every existing link working, keeps its
visible text identical, and removes the last source of duplicate imagery. What a real Services
Overview page should actually SAY is a copy decision for Lynette, so it is logged in
OPEN-QUESTIONS.md rather than invented here.

### 4. Testimonials restyle

CSS only. Every testimonial, attribution, word and order untouched (0-word diff), and nothing
was shrunk or crowded.

- The section now sits on its own ground: a soft lilac-to-sage-to-cream gradient wash instead
  of flat cream, so the white cards read as objects on a surface.
- A short sage-to-lilac rule under the section heading.
- Cards: crisper 1px plum-tinted border, 20px radius, a two-layer shadow (hairline ring plus a
  deep soft drop), a permanent sage-to-lilac accent bar across the top edge, and a gentle hover
  lift. Grid gap opened to clamp(1.6rem, 3.2vw, 2.6rem) and padding to
  clamp(2rem, 3.4vw, 3.1rem), so the separation between cards is unmistakable.
- The quote mark is now a deliberate design element: a solid plum disc set into the top edge of
  each card carrying a lilac open-quote glyph, replacing the giant washed-out glyph that used
  to float in the corner.
- Quote typography moved into the brand serif at clamp(1.24rem, 1.55vw, 1.44rem) with 1.62
  leading and a 56ch measure. That is larger than before, not smaller.
- The category is now a sage pill; the "The Shift" line is larger italic serif plum.
- Attribution is prominent: uppercase, letterspaced, bold plum, preceded by a short
  sage-to-lilac rule instead of the old em dash glyph.
- Lead testimonial keeps its two-column layout above 880px and gains a hairline divider
  between the meta column and the quote.

### Verification (batch 4)

- **Link and asset sweep:** 2378 local href/src references across 38 HTML files all resolve on
  disk. **0 broken.** External hosts unchanged (blog citations plus the untouched raw mirror
  pages). 0 orphaned references to the old detox slug in any .html, .xml or .md.
- **Visible text:** a "before" tree was rebuilt by mechanically inverting every HTML change in
  this batch and diffed page by page (_batch4_verify.py). **24 pages compared, 0 with any
  visible-text difference.** Note that the extractor reads main with tags stripped, so image
  src/alt swaps and href rewrites cannot register; the entrance block sits outside main and is
  aria-hidden. The one genuine content-shaped change, aliasing services.html, is safe because a
  direct diff of the two files before the alias showed their only differences were image src
  values and CSS class names, with identical text.
- **Headings and metadata:** 37 of 38 pages have exactly one H1 (the exception remains
  cart.html, an untouched raw mirror page with none). No title or meta description changed.
- **Image uniqueness:** 53 images, **0 duplicates** outside the four documented exception
  classes. Table in IMAGE-LEDGER.md.
- **Entrance removal:** asserted with --dump-dom --virtual-time-budget=6000 that
  class="df-reveal" and class="hero-curtain" are both absent from the DOM and
  data-entrance="done" is set, with the hero H1 present, in normal motion AND under
  --force-prefers-reduced-motion. The post-entrance DOM is 15.6 kB; the 110 kB inline SVG is
  genuinely gone.
- **Measured entrance duration from the CSS:** 0.10s delay + 1.65s flight = **1.75s** total,
  hero content settled at 0.96s.
- **Screenshots** in qa-shots/, prefix b4-, at 1280 and 492:
  b4-home-entrance-flight-* (mid-flight, new dragonfly on the diagonal against the lighter
  blue-violet curtain), b4-home-settled-*, b4-testimonials-*, b4-detox-slug-* (the renamed
  page). Capture method: a local python -m http.server on 127.0.0.1:8791 serving site-v2,
  driven by Edge headless (--headless=new --screenshot). Because Edge headless does not
  advance CSS animations, mid-flight frames use the ?stage=flight freeze hook (negative
  animation-delay plus animation-play-state:paused) and settled frames use
  --force-prefers-reduced-motion, which renders the identical finished state.

### Helper scripts added

_make_dragonfly.py (generates the dragonfly and writes _hero_entrance.part),
_fetch_figures.py (Pexels sourcing with photo-ID de-duplication, writes
assets/figures/_ledger.json), _apply_figures.py (the image swap table and the services
alias), _img_audit.py (site-wide image usage map), _batch4_verify.py (before/after
visible-text proof).

## [2026-07-23] Batch 5 - approved entrance ported to the live homepage
- Replaced the naturalistic-vector entrance with the preview-approved "unzip" reveal.
- Two full-viewport triangles (.hero-curtain.hc-top / .hc-bot) tile the screen exactly along the bottom-left to top-right seam, so at rest coverage is 100% with no corner gaps. They slide apart perpendicular to the seam in one continuous glide (part-top / part-bot, 1.6s).
- Curtain is layered, not flat: two lilac/blue glow blooms plus five faint sparkles over a blue-violet gradient (#3c336e -> #20264a) pulled toward the hero photo tones.
- Pearl-white dragonfly with violet-blue falloff rides exactly on the seam (df-cross, 1.6s, bottom-left to top-right). Four wings beat independently at .12s, body undulates, wing shimmer.
- v2.js updated to track BOTH curtain halves (querySelectorAll) and remove all three nodes on animationend, fallback 2000ms. Verified: after the entrance, 0 curtains, 0 flyer, data-entrance=done, hero opacity 1.
- Reduced motion still skips the entrance entirely.
- Added ?v=5 cache-busting stamps to assets/v2.css and assets/v2.js across 23 pages (stale cached JS was masking edits during preview).
- Homepage layout/content otherwise unchanged, per Jack.

## [2026-07-23] Entrance slowed + image duplication audit
- Entrance slowed from 1.6s to 2.4s (curtain part-top/part-bot and df-cross share the same 2.4s clock and easing so the reveal stays locked to the flight). Wing beat eased .12s -> .16s, body undulation 1.1s -> 1.5s, so the dragonfly reads calmer at the slower pace. v2.js removal fallback 2000ms -> 2800ms.
- Image audit across all 20 content pages: 53 distinct images, 0 within-page repeats, 0 genuine cross-page duplicates. The 14 flagged pairs are all legitimate: 3 alias pages that are byte-identical copies (index/home, about-lynette-wing/about, naturopathic-detox/services), blog thumbnail-plus-own-post-hero pairs, and Lynette portrait used on About plus as the author image on one post.
- NOTE for Jack: services.html is still a byte-identical copy of naturopathic-detox.html (pre-existing, from the original Squarespace site). A real Services Overview page is still needed.
- Cache stamps bumped to ?v=6 across 23 pages; alias pages resynced after the edit.

## [2026-07-23] Wing geometry: perpendicular, natural flap
- Jack: wings should stick out to the SIDES, perpendicular to the body, like the dragonfly in the hero photo, not swept back over the abdomen.
- Root cause: the four wing paths were all drawn extending back-left from the thorax, and all four rotated around one shared origin near the body centre, so the beat read like windshield wipers.
- Rebuilt all four wing paths programmatically (scratchpad/wings.py) as blades extending perpendicular to the body axis with a slight backward lean: forewings rooted at x116, hindwings at x97, length 58 (hind 53), measured bbox ratios now about 1:4 (was 1:2, which read as flower petals).
- Each wing now pivots from its OWN root (per-wing transform-origin) and the beat is mostly vertical compression toward that root with only a couple of degrees of rotation, so it reads as a real flap. Wing pairs beat together; the rear pair counter-strokes on a half-cycle offset.
- Same visual language kept: pearl-to-violet gradients, longitudinal plus cross veining, pterostigma near each tip.
- Verified via SVG getBBox rather than eyeballing. Link sweep 2378 refs, 0 broken. Entrance still fully removes itself (0 curtains, 0 flyer, data-entrance=done, hero opacity 1).

## [2026-07-23] Wing placement relative to the torso + 4s entrance
- Wing roots were at x116/x97: the forewings attached under the HEAD (circle cx124) and the hindwings at the very back edge of the thorax. Moved both pairs onto the thorax proper (ellipse cx108 rx12, spans x96-120): forewings x113, hindwings x102, up y49 / down y59.
- Render order fixed: the wings were drawn BEFORE the abdomen and thorax, so the torso painted over them and the wing roots disappeared. Wings now draw AFTER the abdomen and thorax (so they sit on top, as they do on a real dragonfly viewed from above) and BEFORE the head, eyes and legs, which stay in front.
- Per-wing transform-origins updated to the new roots so the flap still pivots correctly.
- Entrance slowed another second: 3s -> 4s (curtain and flight share the clock), body undulation 1.7s -> 2s, JS removal fallback 3400ms -> 4400ms.

## [2026-07-23] Typographic orphans + a real image overflow bug
- Jack spotted "on." stranded alone on the last line of the home CTA paragraph. Added text-wrap:pretty to p/li/blockquote/figcaption, which was NOT enough on its own (43 orphans remained), so a build pass binds the last two words of every text block with a non-breaking space: 1345 blocks across 23 files. Whitespace only, no wording altered (verified by normalised text comparison).
- Built site-v2\_audit.html, a harness that iframes all 20 pages at 1280 and reports orphans, viewport overflow, clipped elements, empty blocks and broken images. Orphans went 43 -> 18, and the remaining 18 are two-word last lines, which is normal typography rather than a stranded word.
- REAL BUG found by the audit: .flow>*{max-width:none} (intended to let text blocks span the column) also unconstrained any image placed directly in a flow rather than inside a figure. On the vagal-tone post a 1600x1067 image rendered at full size and pushed 558px past the viewport. Added .flow img/svg/video{max-width:100
## [2026-07-23] Typographic orphans + a real image overflow bug
- Jack spotted "on." stranded alone on the last line of the home CTA paragraph.
  Added text-wrap:pretty to p/li/blockquote/figcaption, which was NOT enough on its
  own (43 orphans remained), so a build pass binds the last two words of every text
  block with a non-breaking space: 1345 blocks across 23 files. Whitespace only, no
  wording altered (verified by normalised text comparison).
- Built site-v2/_audit.html, a harness that iframes all 20 pages at 1280 wide and
  reports orphans, viewport overflow, clipped elements, empty blocks and broken
  images. Orphans went 43 -> 18, and the remaining 18 are two-word last lines,
  which is normal typography rather than a stranded word.
- REAL BUG found by the audit: `.flow>*{max-width:none}` (intended to let text
  blocks span the column) also unconstrained any image placed directly in a flow
  rather than inside a figure. On the vagal-tone post a 1600x1067 image rendered at
  full size and pushed 558px past the viewport. Added
  `.flow img,.flow svg,.flow video{max-width:100%;height:auto}` plus an
  `.article .flow>img` editorial treatment so a bare in-flow image matches
  figure-wrapped ones. That image now renders 790px inside its column, and page
  scrollWidth is 1265 at a 1280 viewport.
- Remaining CLIPPED flags are benign: the hero-curtain mid-animation (removed when
  the entrance ends) and the hero background image, which overscans by design at
  scale(1.04) and is contained by overflow-x:hidden.

## [2026-07-23] Proportion, image sizing and grid balance pass (batch 6)

Jack's brief: every image sized sensibly for its role, every box grid an even
distribution with nothing dangling, everything looking equivalent and natural at
every width. Layout, sizing, styling and image files only. **Visible text diff:
37 pages compared, 0 with any difference.** Titles and meta descriptions
untouched, one H1 per page (cart.html still has none, as before). No em dashes
introduced, no external requests added, prefers-reduced-motion / AA contrast /
focus states preserved. The hero entrance was not touched.

### 1. Page heroes now occupy one consistent band

Interior hero height was driven entirely by the length of the H1, so the same
component rendered 248px tall on the detox page and 414px on inflammation and
601px on contact. `.page-hero` now has `min-height:clamp(300px,30vw,420px)` and
centres its content vertically. Measured at 1280 the hero photo band is now
384-402px on every page (blog posts 448 because they also carry an eyebrow and a
byline; contact is still 584 because it carries three lede paragraphs, which are
Lynette's copy and were not touched).

Three more hero fixes:
- `.page-hero .ph-bg img` no longer carries `transform:scale(1.03)`. It bought
  nothing and pushed the image 23px past the viewport edge at 1280.
- `.ph-left` and `.ph-band` heroes used `margin:0` on their inner wrapper, so a
  left-aligned H1 sat hard against the viewport edge instead of on the same
  column as the header logo and the footer. Now `margin:0 auto`.
- A linked hero H1 (resources.html) was inheriting the plum link colour and an
  underline, rendering dark purple on dark purple. `.page-hero h1 a` now inherits
  white with a hover/focus underline.

### 2. Every image role has one aspect ratio

| role | ratio | rendered at 1280 | source |
|---|---|---|---|
| home hero background | full-bleed cover | 1316x936 | 2000x1334 |
| page hero background | full-bleed cover | 1265x384 (402 on band heroes) | 1400-1600 wide |
| in-article LEAD figure | 16/7 | 790x346 (766x335 inside the av-panel mat) | 1100-1600 wide |
| in-article band figure | 16/8 | 790x395 | 1500-1600 wide |
| split-section media | 4/3 | 568x426 | 1600x1067 |
| blog card thumbnail | 16/10 | 573x358 | 1100-1600 wide |
| Lynette portrait (About) | 599/757 natural | 321x406 | 599x757 |
| author portrait (blog post) | 599/757 natural | 168x212 | 599x757 |
| logo | natural | 108x46 header, 99x42 footer | 240x102 |

Changes made to get there:
- The `av-band` lead was 16/6 and the `av-panel` lead 16/7; both are 16/7 now.
- The `av-offset` variant floated the lead figure to one side at 44% width so the
  opening prose could wrap beside it. On all three pages carrying that variant
  (hormone, neurodivergent, naturopathy) the lead figure is followed by an
  eyebrow, an H2 and a card grid rather than by prose, so nothing ever wrapped
  and the float left a dead gutter beside a small image. Those leads are now the
  same 16/7 band as every other page. Page-to-page variety still comes from the
  four hero treatments and the alternating article backgrounds.
- **Author portrait bug on the root-cause blog post.** Lynette's 599x757
  head-and-shoulders photo was being caught by the generic in-article band rule
  and rendered at 790x395: upscaled 1.3x AND cropped straight through her face.
  It now has its own `figure.post-author` role, floated at 120-168px, natural
  aspect ratio, face visible, with the byline set beside it. `.post-back` became
  a block-level flex so the back link keeps its own line above the portrait.

### 3. Images re-encoded (same filenames, same visual quality)

| file | was | now | bytes |
|---|---|---|---|
| unsplash-image-d1eaoAabeXs.jpg | 2500x1667 | 1600x1067 | 706 KB -> 286 KB |
| unsplash-image-XDoGdUtTm-U.jpg | 2500x1875 | 1600x1200 | 750 KB -> 372 KB |
| gut-brain-connection.jpg | 2500x2500 | 1600x1600 | 499 KB -> 243 KB |
| hormonal-balance-1.jpg | 2500x1667 | 1600x1067 | 492 KB -> 210 KB |
| vitruvian.jpg | 2500x1049 | 1600x671 | 251 KB -> 88 KB |
| pexels-depthofraw-10722719.jpg (home hero) | 2500x1667 | 2000x1334 | 235 KB -> 145 KB |
| renewalhealth2stack.jpg (logo, 2 copies) | 507x216 | 240x102 | 35 KB -> 7 KB each |
| fig-hormone-wildflowers, fig-neuro-forest-path, fig-naturopathy-mortar | 1600 wide | 1100 wide | 620 KB -> 361 KB total |

**Total 3628 KB -> 1725 KB, 1903 KB saved.** Every one of those was rendering at
3x to 5x its displayed size. Nothing renders above its natural resolution now
except the spiritual-growth blog hero (oak-tree-straining-in-wind.jpg, 1100 wide
rendered at 1265, a 1.15x stretch): that is the only source available for that
post and replacing it needs a new photograph, so it is logged rather than faked
with an upsample.

### 4. Grids: every row filled, nothing dangling

Measured with a scripted harness that reads every grid's child rectangles at
1280 / 1024 / 768 / 430 and reports whether the last row reaches the grid's right
edge. **Before: 14 ragged last rows. After: 0.**

| page | grid | cards | 1280 | 1024 | 768 | 430 |
|---|---|---|---|---|---|---|
| home / index | services `.card-grid` | 7 | 4 + 3 | 3 + 2 + 2 | 2 + 2 + 2 + 1 wide | 1-up |
| home / index | process `.steps` | 4 | 4 | 2 + 2 | 2 + 2 | 1-up |
| blog | `.blog-grid` | 4 | 2 + 2 | 2 + 2 | 2 + 2 | 1-up |
| testimonials | `.testi-grid` | 3 | 1 full + 2 | 1 full + 2 | 1 full + 2 | 1-up |
| programs-packages | `.pkg-cards` | 3 | 3 | 3 | 1-up | 1-up |
| detox / services | `.svc-cards` x3 | 2, 2, 4 | 2 / 2 / 4 | same | 2 / 2 / 2+2 | 1-up |
| gut-health | `.svc-cards` x2 | 3, 4 | 3 / 4 | same | 2+1 wide / 2+2 | 1-up |
| weight-metabolic | `.svc-cards` x2 | 2, 3 | 2 / 3 | same | 2 / 2+1 wide | 1-up |
| hormone-balance | `.svc-cards` x2 | 5, 4 | 3+2 / 4 | same | 2+2+1 wide / 2+2 | 1-up |
| inflammation | `.svc-cards` x2 | 3, 5 | 3 / 3+2 | same | 2+1 wide / 2+2+1 wide | 1-up |
| emotional-overwhelm | `.svc-cards` x2 | 3, 4 | 3 / 4 | same | 2+1 wide / 2+2 | 1-up |
| neurodivergent | `.svc-cards` x2 | 4, 4 | 2+2 / 4 | same | 2+2 / 2+2 | 1-up |

("wide" above means the odd final card stretches across the whole row, so the row
is still full.)

How each was fixed:
- **Home, 7 services.** Was a flex grid capped at 25%, so it read 4 across with
  three cards stopping 150px short of the right edge, and it degraded to 3+3+1
  and 2+2+2+1 with a single orphan at smaller widths. It is now a 12-column grid
  where the first four cards span 3 and the last three span 4, so both rows run
  edge to edge; 3+2+2 on a 6-column grid at 901-1080; 2+2+2 with the seventh card
  spanning the row below 900; 1-up below 640. No service was removed or merged.
- **Service card grids.** `auto-fit` was leaving holes: four wide cards became
  3 + 1 with a 680px gap, five became 3 + 2 with a 340px gap. Column counts are
  now explicit per card count (`n2`..`n5` classes written into the markup from
  the actual child counts). Four wide cards are a 2 x 2 block; five are a
  6-column grid with the first three spanning 2 and the last two spanning 3.
  Below 860 all of them go 2-across with an odd final card spanning the full row.
- **Blog index, 4 posts.** Was 3 across with a lone fourth card underneath. Now
  2 across, which divides evenly, fills both rows and gives each thumbnail 573px
  instead of 371px.
- **Equal heights.** `grid-auto-rows:1fr` on the home service card grid, the step
  grid and the blog grid, so every card in those grids is exactly the same height
  rather than one row being 22px taller than another. The long-form `.svc-cards`
  keep per-row equal heights (content lengths vary too much between rows for a
  single height across the whole grid to look right).

### 5. Consistency fixes

- testimonials.html and resources.html were the only two pages whose hero had no
  photograph behind the plum veil. Both now have one, sourced from the unused
  local `assets/v2img/` set, resaved into the hero library's format and checked
  against every other image on the site for duplication (closest perceptual-hash
  distance 54 and 66 out of 256, i.e. clearly different photographs):
  `hero-testimonials-lake-reflection.jpg`, `hero-resources-water-lily.jpg`.
- Section padding, heading scale, eyebrow styling, button sizes, card radius,
  border and shadow treatment were already single-sourced from the design tokens
  and were left alone.

### Verification (batch 6)

- **Visible text:** a "before" tree was rebuilt by mechanically inverting every
  HTML edit in this batch (the `nN` grid classes, the two hero photo blocks, the
  `post-author` class, the cache stamp) and diffed word by word against the
  shipped tree. **37 pages compared, 0 with any visible-text difference,
  19183 words.** Non-breaking spaces compare equal to normal spaces. Titles and
  meta descriptions byte-identical.
- **Links and assets:** 2380 local href/src references across 38 HTML files all
  resolve on disk. **0 broken.** External hosts unchanged (the blog's citations
  plus the untouched raw mirror pages).
- **Images:** every image on every page reports `naturalWidth > 0` at all four
  widths. 0 IMG404.
- **Overflow:** `documentElement.scrollWidth` is inside the viewport on all 23
  pages at 1280, 1024, 768 and 430, and no element's right edge crosses the
  viewport. The one remaining flagged element is the home hero photograph, which
  is deliberately scaled 1.04 for the parallax and is clipped by the hero's own
  `overflow:hidden`.
- **Grids:** 0 ragged last rows across all grids at all four widths (was 14).
- **Aliases re-synced:** index/home, about-lynette-wing/about and
  naturopathic-detox/services are byte-identical again.
- Cache stamps bumped to `?v=15` on `assets/v2.css` and `assets/v2.js` across all
  23 pages.
- Capture method: a local `python http.server` on 127.0.0.1:8842 serving site-v2,
  driven by Edge headless with `--force-prefers-reduced-motion` for settled
  frames. Measurements were taken by a harness page that iframes every page at
  each width and reports rectangles into the DOM, read back with `--dump-dom`.
  The measurement and screenshot harnesses and the inherited `_audit.html` were
  all deleted after the pass, as asked.

### Left as-is

- contact-renewal-health.html has the tallest hero (584px vs 384-448 elsewhere)
  because its hero carries three of Lynette's lede paragraphs. Shortening it
  would mean cutting her copy.
- `blog/spiritual-growth-through-hardship` renders its 1100px-wide hero source at
  1265px, a 1.15x stretch. It needs a wider source photograph.
- The fourth blog card ("Why Your Body Needs a Master Builder") has no date in
  its meta line while the other three do. That is missing content, not layout.
- `assets/v2img/` still holds 12 unused photographs and
  `assets/dragonfly-flight-cutout.png` is still retired-but-present; both are
  dead weight on disk and are referenced by no page.
- cart.html, blog/category/* and blog/tag/* remain untouched raw mirror pages.

## [2026-07-24] Event promo card (Woman at the Wellness Conference)
- Jack supplied the conference flyer. Added a dismissible promo card fixed to the
  bottom right of EVERY page, injected by v2.js so there is one place to edit and
  no markup duplicated across 23 files. Styles live in v2.css (.promo-card).
- Content is taken verbatim from the flyer, nothing invented: Woman at the Wellness
  Conference, Saturday August 8 2026, 9:00am to 5:00pm, The Sims Barn (S Bar 8 Land
  and Cattle Co., 21400 FM 2590, Canyon, Texas 79015), $120 per person with lunch
  provided, register by August 4. Lynette's talk is "Nothing Missing, Nothing
  Broken", which is also her book title. CTA points to aroundthetable.life/events.
- SELF EXPIRING: the card checks the date and stops rendering after 2026-08-09, so
  the site can never advertise a conference that has already happened. This matters
  because nobody will remember to take it down.
- Dismissal is remembered per visitor in localStorage and persists across pages
  (verified). Escape key closes it. Timed to appear after the hero entrance
  finishes: 5.2s on the home page, 2.2s elsewhere, 0.8s under reduced motion.
- z-index 90, deliberately below the hero entrance layer (120+) so it can never
  cover the dragonfly reveal.
- QA hook: append ?promo=now to any URL to show it instantly and bypass dismissal.
- NOTE for the intake file: the flyer gives Lynette's credentials as RN, HHP, which
  is more specific than what business-context.md had. Updated there.
- The flyer artwork itself is NOT embedded (the images were pasted into chat, not
  saved to disk). If Jack wants the actual flyer graphic in the card, drop the files
  in assets/events/ and it can be swapped in.

## [2026-07-27] Batch 5 (Jack's change list: header, CTAs, contact page, testimonials, hormone image)

Asset cache stamp bumped v18 -> v19 on assets/v2.css and assets/v2.js across all 25 HTML files (root + blog/). No em dashes used in any copy written this pass.

1. HEADER - scrolled state inverted to PURPLE. Previously the scrolled header was frosted cream with dark nav. Now `.v2-header.scrolled` (and `body.has-hero .v2-header.scrolled`) is a solid plum->plum-deep gradient with blur+shadow kept. Scrolled nav links + hover underline go WHITE, carets light lilac, mobile toggle bars white, logo sits on a white rounded chip, and the nav Contact button inverts to white ground / plum text (`.v2-header.scrolled .v2-nav a.nav-cta`). Top (not-scrolled) states unchanged. Added a mobile-panel guard inside the 960px media query so the white-link treatment never washes out on the cream slide-in menu (links stay plum there). AA holds: white on #4b2e5a ~8.9:1; plum-on-white button ~8.9:1. prefers-reduced-motion untouched.

2. CTA WORDING - every "Contact Me to Schedule Your Consultation!" -> "Contact Lynette to Schedule Your Consultation!" (25 replacements, one per file). The short nav "Contact" button is unchanged.

3. CONTACT PAGE rebuilt - contact-renewal-health.html. Kept the existing hero (chamomile photo, dedicated to this page and used nowhere else as a hero) and Lynette's three intro lede paragraphs verbatim. Replaced the self-referential cta-panel with a real two-column layout: an info panel (phone 580.461.1686 as a tel: link, hours Mon-Fri 9am-5pm + weekends by appointment, and a clearly-labelled `[add Lynette's email]` placeholder + HTML comment) and a working-looking contact form (Name/Email/Phone optional/Message + a .btn-primary submit). Form is named `contact` with an HTML TODO to wire it at hosting time. Title/meta kept. One H1. New CSS: `.contact-grid/.contact-info/.contact-list/.contact-form`. Logged the missing email in OPEN-QUESTIONS.md.

4. DE-DUPLICATED stacked closing CTAs. On every page that had an in-article closing CTA block immediately followed by the global .cta-panel, the in-article block (closing heading + summary paragraph(s) + repeated italic invite + in-article button) was removed so ONLY the .cta-panel remains. Pages changed and what was removed (heading of the removed block):
   - naturopathic-detox.html + services.html alias: "Begin Supporting Your Body's Natural Detox Process" block
   - gut-health-support.html: "Begin Restoring Your Gut Health and Whole-Body Balance" block
   - weight-metabolic-health.html: "Restoring Balance to Your Metabolism and Weight" block
   - inflammation-support.html: "Begin Reducing Inflammation and Restoring Balance" block
   - emotional-overwhelm-nervous-system.html: "Begin Restoring Calm, Clarity, and Nervous System Balance" block
   - neurodivergent-support.html: "Begin Supporting Your Body's Natural Detox Process" block
   - programs-packages.html: "Begin Your Personalized Path Forward" block (kept the substantive "Choosing the Right Place To Begin" section above it)
   - naturopathy-homeopathy-holistic-healing.html: the "Begin Your Path to Whole-Body Healing" promo line + follow-on paragraph + italic invite + button
   - hormone-balance-support.html: "Begin Restoring Your Hormone Balance Naturally" block
   - about-lynette-wing-renewal-health.html + about.html alias: removed the in-content "A simple first conversation..." H3 invite + "Contact me today to schedule your conversation!" button (the redundant one), kept "Your renewal begins here." and the cta-panel.
   Hard scan confirms no page now has two stacked contact CTAs; each content page has exactly one closing cta-panel (plus the persistent header nav button, which is expected).

5. HORMONE lead image swapped. The first in-article figure was fig-hormone-wildflowers.jpg (a purple meadow that echoed the lavender-field hero). Replaced with a freshly sourced fig-hormone-eucalyptus.jpg (soft sage eucalyptus branch on a muted plum-toned ground, Pexels 6168147 Vie Studio, saved locally, added to IMAGE-LEDGER, meaningful alt). Clearly distinct from the hero. The mid-page hormonal-balance-1.jpg (balanced stone cairn by the sea) is high quality and on-brand, left in place. Hero background untouched.

6. TESTIMONIALS on HOME + ABOUT. Added a compact 3-up testimonials section (eyebrow "Patient Stories" + heading + the three verbatim cards from testimonials.html: Marilyn B / Taylor W / Stella I + a "Read more stories" link to testimonials.html). On the home page it sits after the "How Your Renewal Unfolds" process section and before the final cta-panel; on the About page it sits before the final cta-panel. New CSS `.testi-3up` reuses the existing testi-card styling as a 3-across row that stacks on mobile (neutralising the standalone page's full-width lead-card rules). Standalone testimonials.html left as-is.

Alias pairs re-synced by copying canonical -> alias (index->home, about-lynette->about, naturopathic-detox->services); cmp confirms byte-identical.

QA (Edge headless, python ThreadingHTTPServer on 127.0.0.1:8791, screenshots in qa-shots/batch5-*.png):
- Link/asset sweep: 1021 local refs across all pages, 0 missing.
- No page has two stacked contact CTAs (verified: 0 in-article `btn btn-primary reveal` contact buttons remain).
- One H1 per page (cart.html is the untouched raw mirror, 0 H1, out of scope).
- Screenshots verified: scrolled purple header (white nav + inverted white Contact button + logo chip), home testimonials 3-up, about testimonials 3-up + single CTA, rebuilt contact page (info panel + form), hormone top (new eucalyptus lead, distinct from lavender hero), hormone bottom (single cta-panel).
- Temp QA pages deleted. site-mirror/ and _deploy/ not touched.

## [2026-08-03] Batch 6 (Detox rename, Services overview rebuild, Neuro fix, Programs "Renewal Path")

Asset cache stamp bumped v22 -> v23 on assets/v2.css and assets/v2.js across all 23 root+blog HTML files. No em dashes in any new copy (ranges written as "$950 to $1,250"; all "provided" copy converted). The only remaining em dashes on edited pages are inside the site-wide <title> branding convention (" — Renewal Health with Lynette Wing"), left untouched for consistency across all pages.

1. DETOX RENAME (site-wide "Naturopathic Detox" -> "Detox"):
   - Page file renamed: naturopathic-detox.html -> detox.html (copied, then edited). Old filename kept as a redirect stub (meta refresh + rel=canonical to detox.html + JS location.replace + noindex,follow), so old inbound links still resolve.
   - Every internal href updated naturopathic-detox.html -> detox.html across all root + blog HTML (nav dropdowns, footers, cards, cross-links) plus sitemap.xml (loc /naturopathic-detox -> /detox). cart.html (raw mirror, out of scope) left as-is; its links still resolve via the stub. Link sweep: 0 broken refs.
   - Copy on detox.html: <title>, meta stays modality-accurate, <h1> "Naturopathic Detox" -> "Detox"; "A Naturopathic detox approach" -> "A detox approach"; "benefit from Naturopathic detox support" -> "benefit from detox support"; "Is Naturopathic Detox Right for You?" -> "Is Detox Right for You?". Kept the modality pairings "Naturopathic and Homeopathic detox/medicine" (they describe her actual practice, not the service name).
   - Also caught a stray service-name on hormone-balance-support.html: "A Personalized Approach to Naturopathic Detox" -> "A Personalized Approach to Detox".

2. SERVICES OVERVIEW (services.html) rebuilt from scratch. It was previously a byte-identical duplicate of the detox page. Now: centered photo hero (hero-services-eucalyptus.jpg), eyebrow + one H1 ("Services") + intro, then a 7-card svc-cards grid (Detox, Gut Health Support, Weight Loss & Metabolic Health, Hormone Balance, Inflammation Support, Emotional Overwhelm & Nervous System Support, Neurodivergent Support). Each card has a one-line description pulled from that service page's own intro (her words), plus a "Learn more" link to the service page. New CSS: .svc-card .svc-more link style. Overview-appropriate title/meta. Confirmed services.html != detox.html.

3. NEURODIVERGENT (neurodivergent-support.html) - the "Signs Additional Support May Be Helpful" card had its lead-in line ("You or your child may benefit from this approach if you notice:") marked up as a checkmarked <li>. Moved it out of the <ul> into a plain <p> lead-in (same treatment as the neighboring card intro), so the checklist below is the checked items and this line is the explainer. Wording unchanged (note: text contains non-breaking spaces, handled in the edit).

4. PROGRAMS & PACKAGES (programs-packages.html):
   4a. Hero centered: removed the ph-left modifier from the page-hero so the heading + background render centered on open.
   4b. Replaced the old package trio (Bio-Intake/Bio-Terrain/Alchemy Protocol) with the new "The Renewal Path" content (verbatim, em dashes converted). Section intro "The Renewal Path" + "Three ways to work together, matched to how deep you are ready to go." Three stacked tiers (pkg-cards.pkg-stack) numbered 01/02/03, each with number, title, subtitle, intro paragraph, a lilac "Best for:" callout, the deeper paragraph, an "Included" checklist, an Investment line, and a Contact CTA button. Tier 01 carries the requested non-visible HTML comment about confirming deposit language. Kept the existing hero image and the "Choosing the Right Place To Begin" closer. New CSS: .pkg-cards.pkg-stack (single-column, max 820px), .pkg-best callout, .pkg-invest, .pkg-cta, article h4 heading style.

ALIASES re-synced byte-identical after edits: index.html==home.html, about-lynette-wing-renewal-health.html==about.html (cmp confirmed).

QA (Edge headless, python http.server, screenshots in qa-shots/batch6-*.png):
- Link/asset sweep across all root+blog HTML: 2381 local refs, 0 missing (incl. renamed detox.html and the old-file stub).
- One H1 per page. Only non-1: cart.html (raw mirror, out of scope) and naturopathic-detox.html (redirect stub, intentionally no H1).
- services.html verified NOT a duplicate of the detox page.
- Screenshots verified by eye: batch6-services-overview.png (7-card overview, Detox in nav+footer), batch6-neuro-fixed.png (lead-in now a paragraph, checklist below), batch6-programs-hero.png (hero centered) and batch6-programs-full.png (The Renewal Path + tiers 01/02/03 with Best-for callouts, lists, investment, CTAs).
- Headless note: this site's content sits inside .intro-reveal (opacity 0 until JS adds .in on scroll); the programs full-page shot was taken against a temp copy with reveal forced visible, then the temp deleted. Live pages behave normally in a real browser.

REMAINING standalone "naturopathic" occurrences for Jack's review (all legitimate practice/modality descriptors, NOT the detox service name; kept per scope):
- about-lynette-wing-renewal-health.html / about.html: "Naturopathic and Homeopathic signaling", heading "My Approach to Functional, Naturopathic, and Homeopathic Health", "Naturopathic and Homeopathic support", footer "Personalized naturopathic & homeopathic care".
- detox.html: "Naturopathic and Homeopathic detox" (meta), "A Naturopathic and Homeopathic detox approach", "In Naturopathic and Homeopathic medicine", footer descriptor.
- home.html / index.html: "personalized naturopathic and homeopathic care", eyebrow "Naturopathic & Homeopathic Care", "Through Naturopathic and Homeopathic support", footer descriptor.
- services.html: title "Naturopathic & Homeopathic Root-Cause Care", meta "naturopathic and homeopathic services", eyebrow "Naturopathic & Homeopathic Root-Cause Care", footer descriptor.
- gut-health-support.html: title + eyebrow "Naturopathic & Functional Digestive Health", "How Naturopathic and Homeopathic Care Support...", footer descriptor.
- emotional-overwhelm-nervous-system.html, hormone-balance-support.html, inflammation-support.html, weight-metabolic-health.html, neurodivergent-support.html, programs-packages.html: each has a "How/A ... Naturopathic and Homeopathic ..." section heading and/or meta, plus the footer descriptor.
- naturopathy-homeopathy-holistic-healing.html, why-a-dragonfly-renewal-health.html, resources.html, testimonials.html, blog.html, contact-renewal-health.html: footer descriptor "Personalized naturopathic & homeopathic care" (contact page also body "learn more about naturopathic care, homeopathy...").
- cart.html: raw Squarespace mirror, out of scope (footer descriptor x1).
Every remaining occurrence is a "naturopathy/naturopathic + homeopathy" practice descriptor or the footer tagline; none names the Detox service.
