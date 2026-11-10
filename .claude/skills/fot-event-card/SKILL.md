---
name: fot-event-card
description: Create Founders on Tap (FoT) event cards in Canva from speaker or partner details. Use when asked to make, generate, or batch FoT / "Founders on Tap" / Luma event cards, speaker cards, partner cards, or social squares for an FoT event. Needs the official Canva connector.
---

# Founders on Tap event cards

Generates 480×480 Luma/social cards that match the FoT template. It copies a layout page
from the template design, swaps the text and the polaroid image, shows a preview, saves
once the user approves, and exports PNGs.

Everything goes through the **official Canva MCP connector**; no Canva API keys or browser
automation. The template has **no autofill fields**, so `autofill-design` does not work. Every card is
`copy-design` → `edit-design`. All element IDs live in `layouts.json` (same folder).

## Resources

`resources/` is a local copy of the team's Drive folder "Founder's on Tap Advertising" (see
`resources/README.md` for the full map and Drive IDs of anything left in Drive). Read these when relevant:

- `resources/luma-cards/04-brand-notes/brand-and-layout-notes.md` — colors, fonts, copy voice, and the copy of
  every past card. Read it before drafting copy.
- `resources/luma-cards/03-page-exports/page-0N-*.png` — the original cards. Compare against them when verifying.
- `resources/presentation/01-reusable-images/polaroid-base-with-original-portrait.png` — the real taped
  polaroid frame. `scripts/make_polaroid.py` uses it; don't edit or move it.
- `resources/presentation/` — the 1920×1080 event deck's assets and notes, for deck work.

Brand at a glance: charcoal `#202020` base under the darkened bar photo; off-white `#F7F7F7` titles and names;
white `#FFFFFF` small copy; pale lime `#F4FFBC` highlights; lime `#E7F5A2` arrow; black italic polaroid captions.
Fonts: Exposure (title, names), Schoolbell (handwritten hook), TT Interphases (credentials), Inter SemiBold
Italic (captions). Never introduce other colors or fonts; edit the template's existing text boxes so styling carries over.

## Layouts

| layout | use for | fields |
|---|---|---|
| `speaker-badge` | speaker with a "2X [YC logo] CEO" badge row | hook, city, photo, caption, badge_prefix, badge_suffix, name, linkedin, credential_lead, credential_highlight |
| `speaker` | speaker with a plain uppercase eyebrow | hook, city, photo, caption, eyebrow, name, linkedin, credential |
| `partner` | sponsor or partner announcement | hook, photo, caption, partner_logo |
| `photo` | photo-only teaser | photo, caption |

Use `speaker` by default. Use `speaker-badge` only when the person is a YC founder and the
user wants the YC badge.

Copy-writing conventions (from the existing cards; past examples in the brand notes):
- **hook**: the talk topic in a casual voice, 2–4 words per line, at most 2 lines ("Why customers\nactually buy").
- **caption**: a punchy 2–4 word takeaway handwritten on the polaroid ("From push to pull", "Start with one"). Keep it under 18 characters.
- **eyebrow**: UPPERCASE role with ` · ` separators ("FOUNDER · PMF ADVISOR").
- **credential**: one short credibility line ("Author of The Power of PULL").
- **city**: 2–3 letter code (SF, NYC, LA).

If the user gives only a name and a topic, draft the hook, caption, eyebrow and credential
yourself, show the drafts, and then build.

## Workflow (per card)

Every Canva tool lives on the Canva MCP server. Load them with ToolSearch first:
`copy-design, read-design, edit-design, create-upload-url, upload-asset-from-url, export-design, get-export-formats`.

1. **Make the polaroid image.** The template polaroid is a single flattened image of the frame,
   tape and photo, so each new photo is composited locally into the team's real frame art:
   ```bash
   python3 .claude/skills/fot-event-card/scripts/make_polaroid.py PHOTO_PATH_OR_URL /path/to/scratchpad/polaroid.png --focus-y 0.3
   ```
   The photo can be a local path, a URL, or a Drive file downloaded with the Drive connector.
   `--focus-y` sets the vertical crop (0 = top, 1 = bottom). Faces usually work at 0.25–0.35.
   Open the PNG to check the face is not cut off by the tape. The `photo` layout skips this step only when
   the user supplies a ready-made polaroid; the composites in `resources/luma-cards/01-reusable-images/` are
   ready-made polaroids of past speakers.
2. **Upload it.** Call `create-upload-url`, then:
   `curl -sS -X POST -H "Content-Type: application/octet-stream" --data-binary @polaroid.png "<uploadUrl>"`
   The response has a `mediaId`. Each upload URL works once. A partner logo at a public URL
   can go through `upload-asset-from-url` instead.
3. **Copy the layout page.** Call `copy-design` with `design_id` = `template_design_id` and
   `page_numbers` = `[source_page]`. This makes a new single-page design and leaves the template untouched.
4. **Open a transaction.** Call `read-design` on the new design with `open_transaction: true` and
   `filter.fields: ["design_content","thumbnails"]`. Element IDs survive the copy but the page
   ID changes, so each **locator is `<new page id>-<element id>`**.
5. **Apply edits** in one `edit-design` call (`page_index: 1`, `finalize: "keep_open"`):
   - Polaroid: `update_fill` (`asset_type: image`, the new `mediaId`, alt text "<Name> polaroid"),
     **then `crop_media` with `top: 0, left: 0` and the slot's `box` width/height**. Without the
     crop, Canva zooms the image in and the polaroid edges get clipped.
   - Single-style text (hook, city, caption, eyebrow, credential on `speaker`): `replace_text`.
     Formatting is preserved.
   - Name: `replace_text`, then `format_text` with `link` set to the LinkedIn URL (or `""` to
     clear it). Always reset the link, because the template's link belongs to the previous speaker.
   - Two-tone credential (`speaker-badge`): one `find_and_replace_text` per region, using the
     `two_tone` strings in `layouts.json` as `find_text`. This keeps white text + accent.
   - No YC badge on `speaker-badge`: `delete_element` the badge_prefix and badge_logo, then
     `replace_text` the badge_suffix and `position_element` it to `left: 18.95`.
   - Rename the design with `update_title`: `FoT <City> – <Name>` (or `FoT – <Partner> partner`).
6. **Verify.** Look at the returned thumbnail. Check that:
   - no name wraps onto a second line or runs past the left column (~350px);
   - the hook does not collide with the squiggle arrow;
   - the caption fits on the white strip;
   - it reads like the originals in `resources/luma-cards/03-page-exports/` (same polaroid placement and type scale).
   On overflow, shrink with `format_text` `font_size` (roughly 10% at a time) rather than rewording, unless the user
   prefers shorter copy. Known fit: the `speaker` caption holds ~17 characters at its default 27px; at 18–20
   characters set it to 23px (the original Trevor card uses ~24px for "Agents for founders").
7. **Get approval.** Show the user the thumbnail and ask before saving. Only after a yes, call
   `edit-design` with `finalize: "commit"`. If the user says no, use `"cancel"` and delete nothing.
8. **Export.** Call `get-export-formats`, then `export-design` as `png` (`export_quality: "pro"`,
   `width: 1080`). Give the user the edit link and the PNG URL.

For a batch (a CSV or a list of speakers), run steps 1–6 for every card first. Then show all
thumbnails together and ask for one approval covering the batch, commit each card, and export.

## Gotchas

- The three `LOADING` text boxes sit off-canvas below the page (top ≈ 478). They are leftovers;
  leave them alone.
- Never edit the template design `DAHafwGwXgg` itself. Always copy it first.
- If `layouts.json` IDs stop matching (someone edited the template), re-run `read-design` with
  `open_transaction: true` on the template, re-map the slots by text and position, update
  `layouts.json`, and **cancel** that transaction.
