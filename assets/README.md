# FoT event card assets

These are the reusable pieces of the Founders on Tap Luma event card ([Canva source](https://www.canva.com/design/DAHafwGwXgg/58EH6S69-axVFE3vYW1z8A/edit)). Every PNG is exported at 2400px, 5x the 480px Canva canvas. All of them except the background and the template have transparent backgrounds and are trimmed to their content.

| Folder | File | What it is |
|---|---|---|
| `backgrounds/` | `bg-dark-bar-texture.png` | `#202020` plus a faded B&W bar photo (22% opacity). Used on every card |
| `backgrounds/` | `bg-source-bar-photo.png` | The unedited bar photo the background is made from. `manifest.json` explains how it's edited |
| `templates/` | `base-card-blank.png` | The background with the wordmark and squiggle already in place. Start new cards here |
| `brand/` | `founders-on-tap-wordmark.png` | "Founders on Tap" wordmark |
| `decor/` | `squiggle-arrow-lime.png` | Lime (`#e7f5a2`) curled arrow. Rotate ~15° clockwise to place it |
| `photos/` | `polaroid-happy-hour.png` | Taped polaroid with a happy-hour photo, for non-speaker cards |
| `logos/` | `y-combinator.png`, `partner-every.png` | Credential and partner logos |

`luma_photo/` holds the six finished cards from the source design (four speaker cards, the Every partner card and the photo-only happy-hour card), exported at 2400px. Use them as reference examples when checking generated cards.

`manifest.json` has the details the automation needs:

- the Canva media ID for each asset, so it can be reused inside Canva
- the colour palette and Canva font refs
- each text slot (tagline, city, polaroid caption, role, name, credential) with its exact position on the 480px canvas
- the six page variants

Each speaker's polaroid has their photo already inside the frame, so those images can't be reused. Their media IDs are listed in the manifest for reference.
