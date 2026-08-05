# Open Questions for Jack / Lynette

Date: 2026-07-23

## 1. Full-body portrait of Lynette (About page)

The About page now shows Lynette's **complete, uncropped portrait** on the right with her copy on the left (previously her body/shoulders were cropped off by a 4:5 cover crop). However, the source file `assets/.../lynette-wing-renewal-health.jpg` is only **599 x 757 px - a head-and-shoulders portrait**. A true head-to-toe / full-body image is not possible from this asset. If Jack wants a literal full-body photo, **Lynette needs to supply a new full-length photograph**. The current layout will drop that in cleanly (portrait frame on the right).

## 2. Pre-existing content mismatches in the source copy (not touched)

While consolidating services I noticed a few section headings that appear to be copy-paste artifacts from Lynette's original Squarespace content, unrelated to the naturopathic/homeopathic split, so I left them verbatim rather than change meaning on a YMYL page:

- **hormone-balance-support.html** contains a section titled "A Personalized Approach to Naturopathic Detox" (detox wording on a hormone page).
- **neurodivergent-support.html** ends with "Begin Supporting Your Body's Natural Detox Process" (detox wording on a neurodivergent page).
- **inflammation-support.html** opens with an empty "Gentle Root-Cause Detox Support" heading and carried a full "Homeopathic Detox" block.

These read as leftovers from templating. They were preserved to avoid altering Lynette's meaning. **Confirm with Lynette whether she wants these re-worded to match each page's topic.**

## 3. Provenance of the older assets/v2img/ image set

A set of 14 botanical images under `assets/v2img/` was staged in a prior session with **no attribution record**. This pass did not use them; the hero variety instead uses a freshly sourced, fully-attributed set in `assets/heroes/` (see IMAGE-LEDGER.md). The v2img files can be deleted, or their provenance confirmed if you want to keep them.

## 4. Contact page still has no working form

Carried over from earlier notes: the static contact page shows the contact copy and CTA but no form (the original Squarespace form is injected by JS on the live site). A real form is needed when this moves to a live platform.


## Added 2026-07-23 (batch 4)

**What should the Services Overview page actually say?**
`services.html` has carried the detox page's content since the original build, while the nav
labels it "Services Overview". In this batch it was made a byte-for-byte alias of
`naturopathic-detox.html` so no link breaks and no image is duplicated, but that is a holding
position. Lynette needs to decide whether "Services Overview" should be its own page (a short
hub introducing the seven service areas plus Programs and Packages) or whether the nav item
should simply point at one of the existing pages. New copy would be needed either way, so
nothing was invented here.

**`resources.html` is orphaned.** Nothing on the site links to it. It is a short teaser for the
root-cause blog post. Keep, redirect, or delete?


## Added 2026-07-27 (batch 5)

**Lynette's public email address is needed.** The rebuilt `contact-renewal-health.html` now has a
real contact panel and a working-looking contact form. There is no email address anywhere on the
site, so the info panel shows a placeholder `[add Lynette's email]` (also flagged as an HTML
comment on the page) and the form is UI only. **Please supply the public email** so it can go in
the info panel, and so the form can be wired to route submissions there when the site moves to a
live host. (The form is named `contact` with fields name/email/phone/message, ready to wire.)
