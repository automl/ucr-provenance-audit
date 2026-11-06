Support the human verification of one or more drafted dataset records. The AI-drafted card
is the **claim under audit**, not the ground truth: your job is to re-derive the facts from
the references and cross-check the card against them, so the human can decide what to sign
off, correct, or challenge.

**Input:** dataset name(s) as in `datasets/<Name>.yaml`. With no argument, list the review
queue (records with status `drafted` in `audit/master_table.csv`) and ask which to review.

$ARGUMENTS

## Order of operations — references before discussion

Do **not** discuss, summarize, or defend the card until you have read the references. The
drafting agent may have confabulated, misquoted, or over-trusted the archive page; if you
start from the card you will inherit its framing. Per dataset:

1. Read `docs/schema.md` (the three layers, verdict decision rule, review-state
   conventions) and the record itself, noting — but not yet evaluating — its decisive
   claims.
2. **Fetch and read every entry in `references`** with WebFetch (and WebSearch when a
   citation has no URL). Also follow `archive_page.data_source_link` / `second_link` even
   if not listed. For papers, read the actual sections cited (e.g. "Sec. 7.4, p. 18"), not
   just the abstract. Dead links: try the Wayback CDX API before giving up.
3. If a reference is unreachable or paywalled, say so explicitly and mark every claim that
   rests on it as *unverifiable from here* — never fill the gap from memory of the field.

Only after step 2–3 do you engage in the discussion.

## Cross-check the card

Build a claim-by-claim check of the record's judgment fields (layers 1–3, verdict,
known_issues). For each decisive claim, report one of:

- **Confirmed** — you found the supporting text; give the location and quote.
- **Quote mismatch** — the card quotes or cites a source, but the quoted sentence, page,
  or number is not what the source says. Show both versions verbatim.
- **Not found** — the claim is plausible but you could not locate support in any
  consulted reference. Distinguish "source unreachable" from "source read, claim absent".
- **Contradicted** — a reference says otherwise; quote it.
- **Card is silent** — something load-bearing in the references that the card omits
  (an original task, a confound, a sibling dataset, a split rationale).

Additionally, and independently of the card's text:

- Re-derive the **verdict** from the layer-1/2 facts you verified, using the decision rule
  in `docs/schema.md`, and compare with the card's verdict. Flag any divergence.
- Sanity-check the identity stats and arithmetic (split sizes, class counts, series length
  vs. sampling claims) against the references and, where cheap, against the shipped data
  (`scripts/` has loaders; see the "Check the data, not just the documentation" section of
  `annotate-dataset.md` for one-line tests worth re-running).
- **Duplicate/leakage check** (always — it is cheap): load both splits, value-compare
  every series, and report the unique-series count, the duplicate-group histogram, how
  many test series are value-identical to a training series, and whether any duplicate
  group mixes labels. The archive ships datasets where a large fraction of the test set
  is byte-identical to training series (PowerCons: 67/180), and no card drafted before
  2026-08-26 was checked for this.
- Check `references` completeness: every decisive claim in the card must trace to a listed
  reference; sources you consulted that the card missed should be proposed as additions.

Present the cross-check compactly, ordered by severity (contradictions and quote
mismatches first, confirmations last and summarizable in one line). Then state your
overall assessment: ready to verify as-is, or what must change first.

## Label inference as inference

Everywhere in your output — the cross-check, the discussion, proposed wording — keep a
hard line between what a source *states* and what you (or the card) *infer*:

- A statement backed by a source gets its location (and, when decisive, a quote).
- Anything you derive, interpolate, or conclude yourself — arithmetic on reported numbers,
  "this is presumably the same cohort", reading between the lines of a methods section,
  domain knowledge not in the consulted references — must be explicitly marked, e.g.
  "**Inference:**" or "the source does not say this; I infer it from …", with the
  reasoning shown so the human can audit it.
- Never present an inference in the same breath as sourced facts in a way that lets it
  borrow their authority. If a paragraph mixes both, mark each part.
- Apply the same test to the card: a card sentence that is an inference dressed as a
  sourced fact is itself a finding (report it under **Not found** or as a mislabeled
  inference), even if the inference seems sound.

## Discussion mode

After the cross-check, this is a conversation, not an autonomous edit pass:

- Ground every answer in a reference you have read this session, cited by location. If
  the honest answer is "the sources don't say", say that.
- Argue against the card where the evidence warrants it — the human is here to catch the
  drafting agent's errors, and agreement is only useful when it is earned.
- Do **not** edit the record unless the human asks. When asked, apply exactly the agreed
  change; never reword adjacent text, never touch `archive_page`.
- **Never write the human's name into `checked_by` on your own initiative.** When the
  human explicitly declares the record verified, replace `AI (UNVERIFIED)` with the name
  they give, then run `.venv/bin/python scripts/build_table.py` (must exit clean) and
  `.venv/bin/python scripts/build_report.py`.
- If the review surfaces a new recurring trap, propose adding it to the heuristics list in
  `.claude/commands/annotate-dataset.md` in the same commit as the corrected record.
