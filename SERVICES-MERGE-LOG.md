# Services Consolidation - Merge Log

Date: 2026-07-23

Jack's directive: stop splitting service content into "naturopathic" vs "homeopathic" framings; present each service as ONE unified story. HARD rule: preserve every substantive point; only merge/dedupe the naturopathic-vs-homeopathic terminology and collapse duplicated framing. This is a YMYL health site, so no claim was invented, removed, or changed in meaning.

## Method

The only change made is to a small number of **section heading labels** that carried the "Naturopathic X" vs "Homeopathic X" split framing. Every body paragraph, list item, benefit, symptom, mechanism, and instruction is preserved **verbatim and in original order**. No sentence of Lynette's copy was reworded or deleted. Because only heading label words changed, the visible-text word delta per page is tiny (see REDESIGN-NOTES verification), and each original content point still lives exactly where it did.

## Audit of the split across all service pages

Reviewing every service subpage, only three pages actually presented the hard "Naturopathic section THEN Homeopathic section" split. The other service pages already introduced naturopathic and homeopathic care together in a single unified heading (e.g. "How Naturopathic and Homeopathic Care Support Gut Health"), so there was no split to collapse there - those pages received only the visual/compacting polish (photo hero, distinct imagery), not a content merge.

| Page | Had the naturopathic-vs-homeopathic split? | Action |
|---|---|---|
| naturopathic-detox.html | YES - "What Is Naturopathic Detox?" + "What Is Homeopathic Detox?" as parallel sections | Headings unified (below) |
| services.html (the detox-content page) | YES - identical detox content | Headings unified (same as detox) |
| inflammation-support.html | Partial - a stray "What Is Homeopathic Detox?" section label | Heading unified |
| gut-health-support.html | No - already "How Naturopathic and Homeopathic Care Support Gut Health" | Polish only |
| hormone-balance-support.html | No - already "How Naturopathic and Homeopathic Care Support Hormone Balance" | Polish only |
| weight-metabolic-health.html | No - already "A Sustainable, Naturopathic and Homeopathic Approach to Weight Balance" | Polish only |
| emotional-overwhelm-nervous-system.html | No - already "How Naturopathic and Homeopathic Care Support Nervous System Regulation" | Polish only |
| neurodivergent-support.html | No - already "How Naturopathic and Homeopathic Care Support Neurodivergent Individuals" | Polish only |

## Heading changes (the only edits)

### Detox (naturopathic-detox.html AND services.html)

1. `What Is Naturopathic Detox?` → `What Detox Really Means`
2. `What Is Homeopathic Detox?` → `How Gentle, System-Wide Detox Support Works`
3. `A Personalized Approach to Naturopathic Detox` → `A Personalized Approach to Detox`

The page title (`<title>`) and meta description are unchanged (they still read "Naturopathic Detox & Homeopathic Detox"), so search intent is preserved; only the on-page section framing now reads as one seamless detox story.

### Inflammation (inflammation-support.html)

4. `What Is Homeopathic Detox?` → `How Gentle, System-Wide Detox Support Works`

## Content-point preservation checklist (detox page)

Every original point below is confirmed still present, in order, under the unified headings:

- Detox misconception (cleanses/quick fixes); body detoxes every day - PRESENT (opening of "What Detox Really Means")
- Naturopathic detox supports natural systems, not forcing them - PRESENT (verbatim body)
- Sluggish/inflamed = pathways need support not stress - PRESENT
- How the body detoxifies: Liver, Lymphatic, Digestive, Kidneys, Skin (5-item list) - PRESENT
- Systems functioning well = efficient continuous detox; overwhelmed = symptoms - PRESENT
- Signs detox pathways need support (8-item symptom list) - PRESENT
- Homeopathic detox = targeted signaling remedies, gentle stimulation - PRESENT (under "How Gentle, System-Wide Detox Support Works")
- Body can: activate pathways / release gradually / maintain balance / avoid overwhelm (4-item list) - PRESENT
- Homeopathy works system-wide, restoring function not just removing toxins - PRESENT
- Why gentle > aggressive; aggressive risks (4-item list) - PRESENT
- Naturopathic AND Homeopathic approach = capacity first (3-item list) - PRESENT
- Drainage/flow concept; supporting flow (4-item list) - PRESENT
- How detox supports gut/hormones/inflammation/energy (4 subsections) - PRESENT (unchanged)
- Personalized approach guided by 4 factors - PRESENT (under "A Personalized Approach to Detox")
- Detox without extremes; 3-item "it's about" list; goal statements - PRESENT
- "Is Naturopathic and Homeopathic Detox Right for You?" 4-item list - PRESENT (retained verbatim, including the phrase in the body)
- Closing "Begin Supporting Your Body's Natural Detox Process" + CTA - PRESENT

Nothing substantive was dropped. The words removed are only the heading tokens "Naturopathic" / "Homeopathic" / "Is" / "What" where they served purely as the split-framing label; those same terms still appear throughout the preserved body copy and in the page title/meta.

---

## 2026-07-23 (batch 3): retitle, de-duplicate, card-grid reformat

Scope: every service page plus `services.html` and `programs-packages.html`.
Rule applied: **condensing means removing genuine duplication only**. Restructuring
prose into cards moves markup, never words. Every removal below is listed with the
exact text removed and where that information still lives.

### Word deltas (visible text, before to after)

| page | before | after | delta | cause |
|---|---|---|---|---|
| services.html | 856 | 839 | -17 | detox retitle + 2 duplicate subtitles |
| naturopathic-detox.html | 856 | 839 | -17 | detox retitle + 2 duplicate subtitles |
| gut-health-support.html | 810 | 810 | 0 | reformat only |
| weight-metabolic-health.html | 822 | 816 | -6 | 1 verbatim duplicate heading |
| hormone-balance-support.html | 806 | 806 | 0 | reformat only |
| inflammation-support.html | 1106 | 853 | -253 | detox section duplicated verbatim from the detox page |
| emotional-overwhelm-nervous-system.html | 855 | 855 | 0 | reformat only |
| neurodivergent-support.html | 891 | 891 | 0 | reformat only |
| programs-packages.html | 921 | 921 | 0 | reformat only |

### 1. Retitle: dual naturopathic/homeopathic naming dropped

Only one page carried dual naming in its title and H1.

- `naturopathic-detox.html` and `services.html`
  - H1 "Naturopathic Detox &amp; Homeopathic Detox" becomes **"Naturopathic Detox"**
  - `<title>` "Naturopathic Detox &amp; Homeopathic Detox | Gentle Root-Cause Detox Support ..." becomes **"Naturopathic Detox | Gentle Root-Cause Detox Support ..."**. This is the only `<title>` change made anywhere on the site.
  - in-body heading "Is Naturopathic and Homeopathic Detox Right for You?" becomes **"Is Naturopathic Detox Right for You?"**
  - `<meta name="description">` left byte-identical: it is descriptive prose ("personalized Naturopathic and Homeopathic detox"), not a dual page name.
  - Filename unchanged (`naturopathic-detox.html`) so every internal link and the sitemap keep working.
- No other page had a naturopathic-vs-homeopathic split in a title or H1. Phrases such as
  "A Naturopathic and Homeopathic Approach To Reducing Inflammation Naturally" are Lynette's
  own descriptive prose about her combined method, not a dual naming of the same service, so
  they were left exactly as written.

### 2. De-duplication, point by point

**naturopathic-detox.html and services.html** (identical content)

| removed | why it is a duplicate | where the information still is |
|---|---|---|
| paragraph "A Gentle, Root-Cause Approach to Detoxification" | restates the page kicker "Gentle Root-Cause Detox Support" sitting a few lines above it, and the `<title>` | the kicker "Gentle Root-Cause Detox Support" (now the eyebrow above "What Detox Really Means") and the `<title>` |
| paragraph "Supporting Detox at a System-Wide Level" | restates the H2 directly above it, "How Gentle, System-Wide Detox Support Works" | that H2, unchanged |

Every other paragraph, list item, symptom, mechanism and instruction on both pages is present
verbatim and in the original order.

**weight-metabolic-health.html**

| removed | why | where |
|---|---|---|
| the SECOND `<h3>How Hormones Affect Weight and Metabolism</h3>` | the exact same heading string appeared twice in a row in the source; the two bodies underneath are different (hormones, then gut) but the label was copy-pasted | the first H3 of that name is kept; BOTH bodies are kept in full, in order, and now sit together under that single heading |

No sentence, list item or claim was removed. Word delta -6 equals the six words of the repeated label.

**inflammation-support.html** (the large one)

Two blocks on this page were byte-for-byte copies of the detox page that had been pasted onto
the inflammation page during the original build. They are about detox, not inflammation, and
the inflammation page already covers clearing in its own words under
"Detox Pathways and Inflammation: Why Clearing Matters".

| removed | why | where the exact same words still are |
|---|---|---|
| H2 "Gentle Root-Cause Detox Support" (orphan kicker, no content under it) | verbatim copy of the detox page's kicker; it announced "detox support" at the top of the inflammation page | `naturopathic-detox.html`, as the eyebrow above "What Detox Really Means" |
| H2 "How Gentle, System-Wide Detox Support Works" plus the three sections under it, "Supporting Detox at a System-Wide Level", "Why Gentle Detox Is More Effective Than Aggressive Cleanses", "Detox and Drainage Pathways: Why Flow Matters for Your Health" (249 words) | verbatim copy of the detox page's central section, including the identical lists | `naturopathic-detox.html` under "How Gentle, System-Wide Detox Support Works", reachable from the inflammation page via the Services dropdown and the footer |

Verified mechanically: of every word removed from `inflammation-support.html`, the only two not
also present on the current detox page are "at" and "Level", from the removed duplicate
subtitle "Supporting Detox at a System-Wide Level", whose meaning is carried by the H2
"How Gentle, System-Wide Detox Support Works" directly above it on the detox page.

Everything genuinely about inflammation was kept: "What Is Inflammation?", acute vs chronic,
the symptom list, causes, "How Inflammation Affects Your Whole-Body Health" (which now sits
directly under "What Is Inflammation?" since its old parent heading was the duplicated one),
the whole "A Naturopathic and Homeopathic Approach To Reducing Inflammation Naturally"
section with all five sub-sections, the personalised approach, what it feels like, and the CTA.

### 3. Structural changes that removed ZERO words

Applied across all nine pages and verified by word-for-word diff. Five of the nine pages show a
0-word delta, which is only possible because these moves preserve every token.

1. **Stacked double H2** at the top of each page (an orphan kicker H2 immediately followed by
   the real first H2) is now an `.eyebrow` kicker above that heading. Same words, one H2
   instead of two stacked. Applied to: detox and services ("Gentle Root-Cause Detox Support"),
   gut ("Naturopathic &amp; Functional Digestive Health"), weight ("Root-Cause Functional Care"),
   hormones ("Natural &amp; Functional Hormone Health"), emotional overwhelm ("Natural Stress
   Relief"), neurodivergent ("ADHD, Autism, Dyslexia, Learning Differences &amp; Nervous System
   Balance").
2. **Orphan heading-like paragraphs promoted to real H3** (identical words except the detox
   retitle noted above): "Is This Gut Health Approach Right for You?",
   "This Weight and Metabolic Approach Right for You?",
   "Is This Hormone Balance Approach Right for You?",
   "Is This Inflammation Support Approach Right for You?",
   "Is Emotional Overwhelm Support Right for You?",
   "Is Neurodivergent Support Approach Right for You?".
3. **Runs of sibling H3 sections became card grids** (`.svc-cards`), matching the card style
   used by the home page service boxes: heading, sage rule, supporting text, hover lift.
   - detox and services: "How Your Body Detoxifies Naturally" + "Signs Your Detox Pathways May
     Need Support"; "Why Gentle Detox Is More Effective..." + "Detox and Drainage Pathways...";
     and the 4-up compact grid "Gut Health / Hormone Balance / Inflammation / Energy and Clarity".
   - gut: the 3-up "What Is Gut Health?" run, and the 4-up "Functional Digestive Support /
     Homeopathic Regulation / Nervous System Support / Detox and Drainage Support".
   - weight: the 2-up root-cause run, and the 3-up hormones / stress / quick-fix run.
   - hormones: the 5-up "What Is Hormone Balance?" run, and the 4-up care run.
   - inflammation: the 3-up "What Is Inflammation?" run, and the 5-up approach run.
   - emotional overwhelm: the 3-up dysregulation run, and the 4-up care run.
   - neurodivergent: the 4-up "What Is Neurodivergent Support?" run, and the 4-up care run.
4. **programs-packages.html**: the three offerings (01 The Bio-Intake &amp; Vitality Audit,
   02 The Bio-Terrain, 03 The Alchemy Protocol) are now three side-by-side package cards with
   the number as a display numeral, the sub-headings, the full description, the full
   deliverables list and the investment line, all verbatim. 0-word delta.

### 4. What was deliberately NOT touched

- Purple page-hero backgrounds and each page's distinct hero image: unchanged.
- Headings that carry another page's topic but head unique content, for example
  "A Personalized Approach to Naturopathic Detox" on the hormone page and
  "Begin Supporting Your Body's Natural Detox Process" on the neurodivergent page.
  Rewriting them would mean inventing wording on a YMYL health page, so they stand as written.
- Every `<meta name="description">` on every page.
