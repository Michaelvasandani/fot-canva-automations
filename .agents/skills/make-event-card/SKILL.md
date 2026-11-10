---
name: make-event-card
description: Make a new Founders on Tap Event Card (the square Luma event cover) in Canva for a Speaker or a partner, by copying a Master Page and editing it through the Canva MCP. Use when asked to make, create or generate an FoT event card, Luma cover or Luma photo for a speaker, founder or partner event.
---

# Make an FoT Event Card

Read `GLOSSARY.md` first and use its terms (Event Card, Speaker, Master Page, Tagline, Polaroid Caption, Role Line, Credential Logo, Credential Line, City). Everything about the masters (design ID, page IDs, element IDs, positions) is in `assets/manifest.json` under `masters`. Re-read it every run; don't trust IDs from memory.

Cards are always made by copying a Master Page and editing the copy (`docs/adr/0001-copy-master-pages-not-compose.md`). Never edit the Masters design itself, and never build a card from the PNGs in `assets/`: the Canva MCP can't set the FoT fonts on new text.

## 1. Gather inputs

Ask for whatever is missing, in one message:

- **Speaker Card**: Speaker's name, LinkedIn URL or a short bio, a photo (local file or public URL), City (default `SF`), and the talk topic.
- **Partner Card**: partner name, the Tagline (usually the event name), and the partner logo (see step 3).

## 2. Draft the copy and pick the layout

Draft every text slot in the house voice (`references/voice.md` has the rules and the six real examples). Then show the user, in one message:

- the drafted Tagline, Polaroid Caption, Role Line, Speaker name and Credential Line, plus which part of the Credential Line is the lime highlight;
- for a Speaker Card, the two layouts to choose from:
  - **Logo layout** (`speaker_logo`, like `assets/luma_photo/01-speaker-daniel-ahmadizadeh.png`): large City, Role Line built as `<prefix> [Credential Logo] <suffix>` (e.g. "2X [YC] CEO"), two-colour Credential Line.
  - **Compact layout** (`speaker_compact`, like `assets/luma_photo/03-speaker-rob-snyder.png`): small City, text-only Role Line in caps, one-colour Credential Line.

Wait for the user to approve the copy and pick a layout. Apply their edits. Nothing touches Canva before this.

## 3. Logos (logo layout and Partner Cards only)

Ask whether the user has the logo. If they do, use their file. If not, find it online: prefer the organisation's own press or brand page, and a white or light version on a transparent background, because the card is dark (`#202020`). Show the user the logo and its source URL and wait for approval before using it.

- Not transparent: upload it and run Canva's `remove-background`, or ask the user for a better file.
- Dark logo: say so. Don't try to recolour it; the MCP can't recolour images.
- Save approved logos to `assets/logos/<org-slug>.png` and add an entry under `assets` in the manifest so the next run finds them.

The Y Combinator logo is already on the `speaker_logo` Master Page; don't re-upload it if the Credential Logo is YC.

## 4. Upload the photo and any new logo

Media IDs from the manifest can't be passed to `update_fill` (Canva answers "media bundle … not found"); always upload the file in this run and use the `mediaId` the upload returns.

- **Public URL**: `upload-asset-from-url`.
- **Local file**: `create-upload-url`, then POST the raw bytes:
  ```bash
  curl -sS -X POST -H "Content-Type: application/octet-stream" --data-binary @<file> '<uploadUrl>'
  ```
  The response is `{"mediaId": "..."}`. Each URL works once; get a new one per file.

## 5. Copy the Master Page

`copy-design` with the masters `canva_design_id` and `page_numbers: [<page_number>]` for the chosen layout. Then `read-design` on the new design with `open_transaction: true` and `fields: ["design_content", "thumbnails"]`. The copy has a **new page ID** but the **same element IDs**: build each locator as `<new_page_id>-<element_id from the manifest>`. If an element ID from the manifest isn't in the copy, stop and tell the user the Masters design has changed and the manifest needs updating.

## 6. Edit the copy

Send all edits for the page in one `edit-design` call with `finalize: "keep_open"` and `page_index: 1`. Start with `update_title` set to `FoT — <Speaker or partner name> — <City>`, then:

**Both Speaker layouts**

| Slot | Operation |
|---|---|
| `speaker_photo` | `update_fill` with the uploaded photo's mediaId. Put the whole photo in; don't crop. The user re-crops by hand if they want. |
| `tagline` | `replace_text`. It wraps by itself; a two-line Tagline is fine. |
| `city` | `replace_text` |
| `polaroid_caption` | `replace_text` |
| `speaker_name` | `replace_text`, then `format_text` with `link` set to the Speaker's LinkedIn URL (or `""`): the master's link survives `replace_text`. Font size: see "Fitting the name". |

**Logo layout only**

- `role_prefix` / `role_suffix`: `replace_text` (e.g. `"2X "`, `"CEO"`). If there's no prefix, `delete_element` it and `position_element` the logo to `left: 18.95`.
- `credential_logo`: if it isn't YC, `update_fill` with the uploaded logo, then `resize_element` with `preserve_aspect_ratio: true` and `height: 27.58`.
- After any change to the prefix or logo width, `position_element` the suffix to `left = logo.left + logo.width + 1` (keep its `top`). Read the new widths from the `document` the edit returns.
- `credential_line`: it has two text runs, a white lead-in and a lime highlight. Use two `find_and_replace_text` operations, one per run (`find_text` = the master's current run text, e.g. `"Instructor at "` and `"Columbia & Stanford"`), so each keeps its colour. Don't use `replace_text`: it collapses both runs into one colour.

**Compact layout only**

- `role_line`, `credential_line`: `replace_text`. The Role Line is in capitals with ` · ` between roles. In the master the Role Line is white and the Credential Line is lime; if the approved copy says otherwise, `format_text` the line's `color` (`#f7f7f7` or `#f4ffbc`).

**Partner Card**

- `tagline`: `replace_text`.
- `partner_logo`: `update_fill` with the uploaded logo, then `resize_element` with `preserve_aspect_ratio: true` and `width: 161.51`.
- `polaroid` and `polaroid_caption` stay as they are ("happy hour :)") unless the user asks otherwise.

### Fitting the name

The name slot is about 360px wide on the 480px canvas. The masters use 45.44 (short names, e.g. "Rob Snyder") and 37.55 (long names, e.g. "Daniel Ahmadizadeh"). Use 45 for names up to 12 characters and 37 for longer ones (`format_text` `font_size`; it only takes whole numbers). Never go below 37. If a name still overflows at 37, show the user the preview and ask; don't guess.

## 7. Check the preview

Look at the thumbnail the edit returns and compare it with the matching example in `assets/luma_photo/`. Check that:

- no text overflows the canvas or runs under the polaroid;
- the Role Line pieces don't overlap (logo layout);
- the name is on one line;
- the photo fills the polaroid window.

Fix what you can with one more `keep_open` call. If something still looks wrong, tell the user what it is rather than guessing a fix.

## 8. Approve, save, hand back

Show the user the preview and wait for an explicit yes. Then `edit-design` with `finalize: "commit"` and no operations. If they say no, apply their changes and preview again, or `finalize: "cancel"`.

Return the new design's Canva edit link. That's the deliverable; don't export a PNG unless asked.
