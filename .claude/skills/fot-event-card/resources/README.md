# FoT resources

Local copy of the Drive folder **Founder's on Tap Advertising**
(https://drive.google.com/drive/folders/1cm61NcwkremUfqlhUd_9E-_PEVuIxvEN), pulled on 2026-11-10 through the
Google Drive MCP connector. Filenames drop the `-pdf-extracted` suffix used in Drive. All images were recovered from
Canva PDF exports, so they are export resolution, not upload originals.

```
resources/
├── shared/background-bar-photo.png        bar photo behind every card and slide (Canva MAHH5FfmCJQ)
├── luma-cards/                            the 480×480 square cards  (Drive: Luma photo cuts)
│   ├── 01-reusable-images/                speaker + happy-hour polaroid composites (frame/tape/photo baked in)
│   ├── 02-page-formats/                   all-pages contact sheet
│   ├── 03-page-exports/                   page-01…06 native PNGs + campaign-all-six-pages.pdf
│   └── 04-brand-notes/                    brand-and-layout-notes.md, resource-usage-inventory.csv
└── presentation/                          the 1920×1080 event deck  (Drive: presentations)
    ├── 01-reusable-images/                polaroid bases, portraits, event photos, screenshots
    ├── 02-page-formats/                   layout-01…06 references + all-slides contact sheet
    └── 04-brand-notes/                    brand-and-layout-notes.md, resource-usage-inventory.csv
```

## What the skill uses

| file | used for |
|---|---|
| `presentation/01-reusable-images/polaroid-base-with-original-portrait.png` | the real taped polaroid frame `scripts/make_polaroid.py` composites every new photo into |
| `luma-cards/03-page-exports/page-0N-*.png` | visual reference when checking a generated card against the originals |
| `luma-cards/04-brand-notes/brand-and-layout-notes.md` | colors, fonts, copy voice and past card copy |
| `presentation/02-page-formats/layout-05-speaker.png` | reference for the deck's speaker slide |

The logos, arrow and background already live in the Canva template, so card automation does not upload them again.

## Left in Drive (not copied)

These were skipped because the Drive connector returns small files inline, and they are not needed for automation
(each one is already in the Canva template or is deck-only). Fetch one with the Drive connector's
`download_file_content` and its file ID if needed.

| file | Drive file ID |
|---|---|
| logo-y-combinator (240×69) | `1t8C9sQYLfDEByCngRUyB00REOtqnulPa` |
| logo-every-partner (268×127) | `1n_BcPGTXso-di7YObeY24DDuiotWJmdD` |
| arrow-thin-curled-lime.svg / .png | `1EQDuCfL1QtCzMl69lhV0LF04g3uYkC5C` / `1E-FTUZlD_FTjVy_VVhOmqvaITWsWfbiV` |
| wordmark-founders-on-tap-rendered-crop | `1YlZdEpGQFP084NqYKUtDjAVkZrqOTjMx` |
| observed-color-palette (cards / deck) | `1RjgpmhNwEGeJwaH-CHNqT1j6qbE6nq4h` / `19U_Xzr1mrCRy69bD7qZaDd4900hU17pS` |
| font-and-color-evidence.json (cards / deck) | `1F6XDYRS8l_FHHTLjeExQGsGS1AuCsKh6` / `1wJqZ9UHXXDXq9jGkFQ7hWI4HrxDc5RuA` |
| format-square-480x480-* (4 files, identical to page exports) | in Drive › Luma photo cuts › 02 Page Formats |
| deck: event-card ×3, handdrawn arrow, QR codes ×3 | in Drive › presentations › 01 Reusable Images |
| START HERE docs (campaign + presentation inventory) | `11geivHRl47ildCOHo-WB5n8tTRPz-W5_JGYgdEXjDHY` / `17uiIuoE5NWphq5Y2u8N6i6r0H1eClGJsm-okzmfPYvk` |
