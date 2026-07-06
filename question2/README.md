# Question 2: Behavioral Deviation Analysis

## Deliverables

- `index.htm`: standalone interactive report with English/Chinese switching.
- `overview.htm`: fixed 1600 x 1200 summary board used for image export.
- `q2_data.js`: generated aggregate data loaded by the report.
- `build_data.py`: reproducible transformation from the source CSV.
- `q2_overview.jpg`: high-resolution overview for the VAST answer sheet.

The report has no external web dependencies. It can be opened directly after
`q2_data.js` has been generated.

## Rebuild the data

From the repository root:

```bash
python3 question2/build_data.py
```

The script reads `MC1_communications_flat.csv`, writes `question2/q2_data.js`,
and validates the source row count, round count, breach message, and headline
metrics used in the report.

## Phase definitions

| Phase | Records |
| --- | --- |
| Historical baseline | Rounds 1-13, before June 5 |
| Crisis build-up | Rounds 14-21, June 5 09:00-16:59 |
| Breach hour | Round 22, June 5 17:00-17:59 |
| Post-embargo | Round 23, June 5 18:00 onward |

Channel shares use each actor's message total within a phase as the
denominator. Public channels are `official_post`, `personal_post`, and
`anonymous_post`.

## Visual encodings

- Behavior fingerprint: position maps actor and channel; sequential lightness
  maps channel share; the alternate diverging scale maps percentage-point
  deviation around a meaningful zero.
- Behavioral drift timeline: horizontal position maps round, vertical position
  maps actor, circle area maps message count, and a redundant red ring marks
  public posting.
- Role allocation comparison: aligned process cards and actor-presence chips
  compare typical responsibilities with observed breach-hour behavior.

Interactions are limited to phase selection, share/deviation mode, language
switching, and linked actor/round evidence selection.
