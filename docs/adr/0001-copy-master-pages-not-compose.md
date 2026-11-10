# Make Event Cards by copying a Master Page, not by composing from assets

New Event Cards are made by copying the matching Master Page (kept in a dedicated "FoT Event Card — Masters" Canva design) and editing its text and photo in place. We don't build cards from the PNGs in `assets/`. The Canva MCP can't set a font family on text it adds; it can only change the content of text that already exists, which keeps that text's font, size and spacing. Copying a Master Page is the only way to guarantee the cards match the existing designs.

## Considered Options

- **Compose from the extracted PNG assets plus new text.** Rejected: new text can't use the FoT fonts.
- **Canva Brand Template with autofill fields.** Rejected for now: it needs Canva Teams or Enterprise, and autofill doesn't adapt the layout (shrinking long names, choosing between layouts).

## Consequences

- The Master Pages are load-bearing. If one is edited by hand, every future card changes with it.
- Each Master Page's polaroid is rebuilt as a frame layer over a separate photo element, so swapping the Speaker's photo doesn't replace the frame.
