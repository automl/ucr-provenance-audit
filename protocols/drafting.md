Draft the audit record for one or more scaffolded UCR/UEA datasets: research the original
problem, fill the three schema layers, set a verdict — honestly labelled as AI-drafted and
awaiting human verification.

**Input:** dataset name(s) as in `datasets/<Name>.yaml`, or `--batch N` to take the first N
scaffolded records (status column of `audit/master_table.csv`).

$ARGUMENTS

## Before drafting

1. Read `docs/schema.md` in full — the three layers, the controlled vocabularies, the
   verdict decision rule, and the review-state conventions. The `task_family` enum is the
   curation taxonomy; extend it only deliberately, in the same commit that first uses a new
   value, and update `scripts/build_table.py`'s vocabulary sets to match.
2. Read the target record(s). The `archive_page` block holds the scraped
   timeseriesclassification.com text — the starting point, not the finish: it usually
   describes the *data*, and often not *why it was collected*.

## Research, per dataset

* Follow `archive_page.data_source_link` / `second_link`; find the original paper, thesis,
  or competition. The UCR briefing document (Dau et al. 2019) and UEA archive paper
  (Bagnall et al. 2018) cover many datasets.
* **Cite by location, never from memory.** Any decisive claim needs the source named and,
  where possible, the load-bearing sentence quoted with its location. You must have read
  that text — not the title, not your recollection of the field. If the source is
  unreachable or paywalled, say so and set `provenance_confidence` accordingly; do not
  paraphrase an abstract as if you had read the paper.
* **Never invent provenance.** `provenance_confidence: low` plus a note on what is missing
  beats a fluent backstory. `unclear` is a legitimate verdict.
* Scope by the **original** task, not the archive's framing: the type tag can mislead
  (PenDigits is tagged Motion but its constant-arc-length resampling removed the temporal
  dimension → `translated-modality`).

## Recurring patterns (heuristics — the dataset wins over the pattern)

* Image/outline data (`IMAGE` tag, contour-unrolling) → x-axis is arc-length →
  `translated-modality`.
* Spectra (`SPECTRO`) → x-axis is wavelength → `ordered-not-temporal` (task may still be
  the original one).
* `SIMULATED` → `synthetic-demo` → `synthetic`.
* Labels derived by curators from metadata (season from timestamp, identity of segment) →
  note in `label_semantics_changed` + `known_issues`; the verdict can still be
  `native-tsc`.
* Windowed slices of one long recording → known issue: train/test independence is
  questionable.
* Few subjects/actors/devices → known issue: identity shortcut.

Extend this list in this file when a new trap is found — in the same commit as the record
that surfaced it.

### Check the data, not just the documentation

The archive's own prose is wrong often enough that a one-line check on the shipped values
is worth more than another hour of searching.

* **The stated transform may be false.** UEA's "each dimension is a frequency band" is
  copy-pasted boilerplate; StandWalkJump is a raw signed waveform (52% negative values).
  Sign of the values separates a waveform from a spectral magnitude in one line.
* **A temporal-sounding name may hide a spectrum.** InsectWingbeat*Sound* and the SemgHand*
  sets ship power spectra. Test: non-negative values + low lag-1 autocorrelation + a
  decaying/harmonic-peaked profile ⇒ spectrum, so the axis is `frequency`.
* **Reconcile window × sampling-rate arithmetic against the shipped channel count** for
  spectrogram-derived data; it settles which axis is time and which is frequency without
  guessing (PhonemeSpectra, Heartbeat, DuckDuckGeese).
* **If `series_length` equals a count of *entities* in the source** (nodes, sensors, leads),
  suspect the archive copy is a **transpose** and the axis is entity index
  (ChlorineConcentration: length 166 = the EPANET node count).
* **A missing timestamp channel is verdict-changing.** For irregularly-sampled sources,
  check whether time survived the conversion at all (LSST: it did not).
* **Instance-count arithmetic is a cheap duplicate detector.** FaceAll ≡ FacesUCR (2250),
  FiftyWords ≡ WordSynonyms (905, mirrored "so that it would not be recognized"),
  PhalangesOutlinesCorrect = the row-wise union of its three siblings.

### Traps in the labels

* **Class = recording channel / lead / session / date.** If the class count equals the number
  of channels, sessions or dates in the source recording, the label is an acquisition
  artifact and any drift solves the task (ECGFiveDays, TwoLeadECG, MoteStrain).
* **The curator replaced a *documented* task with identity.** Always look for the source's
  own prediction target before accepting the archive's (Pig×3 discarded a published
  internal-bleeding task; CinCECGTorso discarded infarct localization).
* **Retrieval benchmarks re-posed as classification** → `different-task` even though the
  labels look preserved (MPEG-7 bulls-eye, Rath & Manmatha word matching).
* **Acted or mimicked classes**: ToeSegmentation's "abnormal" gait is able-bodied actors
  miming a limp; Epilepsy's seizures are mimicked. The label is a performance.
* **No documented label semantics at all** is a first-class known issue and now triggers
  verdict rule 5 (`unclear`), even when the data's *origin* is well documented.
* **Padding conventions can leak the label**: the phalanx series encode "no epiphysis" as 30
  trailing zeros, and epiphyseal fusion is itself the maturity cue — the encoding, not the
  shape, may carry the signal. NaN-padding of variable-length series makes *length* a feature.

### Traps in the splits and siblings

* **Sibling datasets cut from one study.** Six datasets come from one UK household survey,
  three from one pig experiment, three from one Dodgers loop recording. Cross-note the family
  in every member; archive-wide averages multiply-count these.
* **Same data, two train sizes** (Freezer*, InsectEPG*, MixedShapes*) — cross-note in both.
* **Deliberate train/test distribution shift can be the dataset's whole point** (FordB);
  merging and re-splitting destroys it. Check any "A/B" pair before assuming they are variants.
* **Check whether the provided split controls a documented confound**: EthanolLevel's is
  bottle-disjoint, EthanolConcentration's default 50/50 is not.
* **z-normalization can delete the phenomenon**: absolute power *is* the appliance signature;
  DiatomSizeReduction normalizes away the size it is named for.

### Research technique

* **Dead donor URLs are often recoverable from the Wayback CDX API** — this turned FordA/B
  from `low` to `high`. Try it before settling for `low`.
* **A broken or wrong `data_source_link` is itself evidence** for `provenance_confidence: low`
  (ECGFiveDays' link points at pamap.org, an unrelated activity dataset; Cricket's points at a
  different cricket dataset).
* **A `SIMULATED` tag does not imply `synthetic-demo`.** Physics simulators of real, stakeheld
  systems (EPANET) produce simulated data for a real domain — do not apply rule 1 reflexively.
* **Type tags mislead in both directions**: Crop (IMAGE) is satellite phenology and genuinely
  temporal; Car and Plane (SENSOR) are image outlines; Symbols (IMAGE) is recorded hand motion.


## Write the record

* Replace every `TODO(verify)`; leave none (a record with TODOs cannot be drafted — the
  build enforces it).
* Keep `archive_page` untouched. Add every source consulted to `references`.
* Set `checked_by: [AI (UNVERIFIED)]`. Never write a human's name yourself; verification
  is theirs. Never remove or reword existing human notes — add counter-arguments
  separately and leave the final call to the human.

## Validate and report

1. Run `.venv/bin/python scripts/build_table.py` — must exit clean —
   then `.venv/bin/python scripts/build_report.py`.
2. Report per dataset: verdict + one-line rationale, `provenance_confidence` with what
   would raise it, and anything a human must specifically check during verification.
   Substance over volume.
