# Criteria: from a dataset card to the audit CSV columns

Shared by the fact-checkers and the Judge. For every rebuilt column: what it means, the card
fields that decide it, and the rule. Column meanings come from `release/README.md` (the release
codebook); card fields from `docs/schema.md`.

## Contents

1. The ground-truth principle
2. Settled policies (do not re-open)
3. Column rules, blocks A–F
4. Prose columns
5. Normalisation: when two values are "the same"

## 1. The ground-truth principle

The card (`datasets/<Name>.yaml`) is the ground truth, but a card mixes two kinds of statement:

- **Evidence**: a quoted passage of a source (with location), the verbatim `archive_page`, the
  top-level sizes, measured `empirical` values, and statements the card attributes to a named
  source it says it read. This is what the CSV must agree with.
- **The card's own inferences**: sentences without a quoted source, or marked "presumably",
  "likely", "probably", "can", "may", "our reconstruction", "not read", "unverified". They are
  the card author's reading, not established fact.

Under the paper's definitions some verdicts need *documented* facts (a Concern needs a
documented or data-verified shared source; Separated needs sources documented as different; a
constructed label needs a source saying who attached it). A card inference cannot by itself
raise a verdict to that level. The CSV may still carry the card's inference with an `[R]` tag.
Example: AllGestureWiimoteX's card says "the same ten people are in train and test" without
quoting any source, so the split stays Unclear, not Concern.

When the card's evidence decides a column, the card wins over the old CSV, whatever the old
CSV says. When the card holds nothing that bears on a column (typical for duplicate counts,
domain, family names), the column is **card-silent**: keep the old value. That is not an
inconsistency.

## 2. Settled policies (do not re-open)

The authors already decided these in the release pass (`crosscheck/HARD_CONFLICTS.md`). Apply
them as rules, and do not flag a row for following them.

- **Non-time indices.** A series indexed by frequency (power spectrum), phase (folded light
  curve), temperature (melt curve) or histogram bin is `ordered, non-temporal` (T1, the 72/48/8
  split).
- **Simulated time.** A simulator's process time (Trace) is `temporal` with `series_index: time`.
  Only a generator step with no physical clock is `synthetic`.
- **Subsetting a retrieval pool is task replacement.** MPEG-7 pairs such as BeetleFly and
  BirdChicken get `original_task: real task`, `source_target` "shape retrieval over 70 object
  classes …", `label_origin: redefined`, `label_attached_by: Curators` and `task replacement`
  (L1). ShapesAll, Car and Plane count the source's shape retrieval as a real task.
- **Survey annotations count as the source task.** When collectors annotated a
  deployment-relevant attribute (the appliance on each metered channel) without training a
  classifier, the label is still `source task` and `task_construction: pass`, with
  `label_attached_by: Collectors` and `label_evidence: S+R` (the electricians' appliance dropdown is
  quoted, Intertek Sec. 3.4; the mapping from dropdown entries to the archive's classes is inferred;
  amended 2026-11-04 by author ruling, was `R`) (L3, the five Household Electricity
  Survey datasets: Computers, LargeKitchenAppliances, RefrigerationDevices, ScreenType,
  SmallKitchenAppliances). ElectricDevices is not one of them: it comes from the GEO Visual
  Energy Trial, whose source study posed the 7-class task itself, so it follows its card
  (amended 2026-11-02 by author ruling).
- **Archive-framed strain labels.** Worms and WormsTwoClass: the source did unsupervised motif
  discovery, so `original_task: none`, `label_origin: metadata`, `label_attached_by: Curators`,
  `metadata as label` (L2).
- **Undocumented labels.** InlineSkate and NonInvasiveFetalECGThorax1/2: no source says what the
  classes mean. They get `original_task: undocumented`, `label_origin: undocumented`,
  `label_attached_by: Curators`, `task_construction: pass`, and overall verdict
  "label meaning undocumented (counted with the real tasks); …" (L4).
- **Separated by construction.** A Separated split where each series is a distinct physical
  event (a star, a lightning transient, a simulated transient) has `leakage_evidence`
  "source separation by construction (each series is …)" (S5).
- **Card overstatements of leakage** (S6): AllGestureWiimoteX/Y/Z, UWaveGestureLibraryAll/X/Y/Z,
  EOGHorizontalSignal/VerticalSignal and PhalangesOutlinesCorrect stay **Unclear**; their card
  sentences assert subject sharing without a source.

## 3. Column rules

`card:` lists the fields to read. `rule:` says how to decide. Use the CSV's vocabulary exactly
(the enums below are checked by `fc.py check`).

### A. Identity

| column | card | rule |
|---|---|---|
| `archive_type` | `archive_type_tag` | Upper-case it (`Image` → `IMAGE`). |
| `n_train`, `n_test`, `series_length`, `n_classes` | top-level fields; `known_issues` | Top-level value, unless a `known_issue` documents that the shipped files differ (Chinatown: "shipped data files have 343 test cases"). Then use the shipped number and cite the known_issue. `series_length` may be `variable`. |

### B. Stage 1: the source study (field ii)

| column | card | rule |
|---|---|---|
| `original_task` | `original_problem.description`, `.prediction_target`, `.task_family`, `.stakeholder_and_use`, `.source`; `benchmark_task.is_same_as_original` | `real task`: the collectors posed a prediction target that a stakeholder outside the paper needed. `toy task`: data staged or generated to demonstrate a method (`task_family: synthetic-demo`, `is_same_as_original: no-original-exists`, stakeholder "none (synthetic demo)"). `none`: the source collected data but posed no classification target. `undocumented`: no source says (policy L4). |
| `source_target` | `original_problem.prediction_target` (and `.description` when the source posed no target) | What the source predicted, or its purpose when it posed none. Compare in substance, not wording. |

### C. Stage 2: the archive task (fields iii–iv)

| column | card | rule |
|---|---|---|
| `data_origin` | `translation.what_the_x_axis_is`, `.sampling`, `verdict`, `original_problem.task_family` | `temporal` when the index is physical (or simulated process) time. `synthetic` when a generator made the series (`task_family: synthetic-demo` and the index is a generator step). Otherwise `ordered, non-temporal`: arc-length, wavelength, position, frequency, phase, temperature, histogram bin, entity index. The card's `verdict` must not contradict the choice. If `verdict` says `ordered-not-temporal` while the CSV says `temporal`, read `sampling` and decide. |
| `series_index` | `translation.what_the_x_axis_is`, `.sampling` | One of: `time`, `time (three axes concatenated)`, `contour arc-length`, `wavelength or wavenumber`, `frequency (power spectrum)`, `phase (folded light curve)`, `temperature (melt curve)`, `histogram bin (intensity histogram)`, `spatial position`, `entity index (network node)`, `generator step`. |
| `benchmark_target` | `benchmark_task.description`, `archive_page.description`, `translation.label_semantics_changed` | What the archive's class means. When the label semantics changed, it differs from `source_target`. |
| `label_origin` | `translation.label_semantics_changed`, `benchmark_task.is_same_as_original`, `original_problem.task_family`, `known_issues`, `archive_page.description` | `source task`: the source's own target, possibly coarsened. `metadata`: a recording attribute (date, season, lead, device, strain). `instance identity`: which subject, sensor, animal or actor produced the series (often `task_family: biometric-identification`). `redefined`: the archive defined the target where the source posed none or a different one. `undocumented`: policy L4. A toy source whose own classes are kept is `source task` (with `original_task: toy task`). |
| `label_attached_by` | `archive_page.description`, `original_problem.source`, `known_issues` | Who attached the class: `Source study` (the source's analysis used this target), `Collectors` (the people who recorded the data annotated it, without posing a classifier), `Collectors (= curators)` (the archive curators recorded the data themselves), `Curators` (the archive assigned it), `Generator` (synthetic), `Unknown`. |
| `label_evidence` | where the label claim comes from | `S` when a quoted source states it, `R` when it is inferred, `I` for a deployment inference. Combine with `+`. Under-tagging (a quoted source but `R`) is an inconsistency. Over-tagging (`S` for something the card marks unverified) is one too. |
| `task_construction` | derived | `fail` if `original_task` ∈ {toy task, none} or `label_origin` ∈ {metadata, instance identity, redefined}; else `pass`. |
| `task_construction_mechanisms` | derived from the above | Empty when `pass`. Otherwise one or two of `metadata as label`, `instance identity as label`, `task replacement`, `toy source task`, joined with `; `. A toy source plus a label mechanism lists both. |
| `task_construction_primary_mechanism` | derived | The label mechanism when there are two; otherwise the single one; empty when `pass`. |

### D. Stage 3: split and leakage (fields v–vi)

| column | card | rule |
|---|---|---|
| `split_verdict` | `known_issues`, `archive_page.description`, `original_problem.source`, `empirical`, sibling cards | `Concern`: a documented or data-verified shared source across the split (same subject, animal, recording or specimen on both sides, stated by a quoted source or measured), or test series value-identical to training series. `Separated`: the relevant sources are documented as different. `Related periods`: different days or windows of one ongoing process. `Generated`: generated data. `Unclear`: anything else, including a card that *suspects* sharing without a source (principle 1). |
| `leakage` | derived | Concern→`fail`, Unclear→`unknown`, Separated→`pass`, Related periods→`pass (related periods)`, Generated→`n/a (generated)`. |
| `relevant_new_case` | `original_problem.stakeholder_and_use`, `known_issues` | The deployment unit a new case means (new patients, new people, new recording occasions, new physical samples …). Inconsistent only if the card names a different deployment unit, not over phrasing. |
| `leakage_evidence` | derived plus evidence | Concern: `exact cross-split matches (n of N test series[, k duplicate groups with conflicting labels])` and/or `documented or data-verified shared source`, joined with ` + `. Unclear: `source separation undocumented`. Separated: `source separation documented` or the S5 wording. Related periods: `different periods of one ongoing process`. Generated: `not assessed (generated data)`. |
| `n_test_identical_to_train`, `pct_test_identical_to_train`, `n_duplicate_groups_with_conflicting_labels` | `known_issues`, `empirical` (usually silent) | Measured on the shipped files. Card-silent unless the card states a count. `pct` = 100·n/n_test, one decimal. |
| `split_evidence` | as `label_evidence` | Tags behind the split verdict: `D` for measured duplicates, `S` for a quoted split rule, `R`/`I` for inferences. |

### E. Section-4 questions

| column | card | rule |
|---|---|---|
| `multivariate_source` | `translation.transformation` (`channel-selection`), `.information_lost_or_added`, `original_problem.input_as_originally_posed` | `yes` when the series is one channel or quantity cut from a recording that measured several (one axis of an accelerometer, one of six electrical quantities). |
| `sibling_family`, `family_members` | `known_issues`, `references`, sibling cards | Card-silent for the family *name*. `family_members` is inconsistent if the card names a sibling that is missing, or denies a relation the CSV asserts. |
| `archive_transformation` | `translation.transformation` | The card's list, comma-joined, same vocabulary. |

### F. Overall

| column | rule |
|---|---|
| `overall_verdict` | Derived from `task_construction`, `leakage` and `original_task`: `fails task construction and leakage`; `fails task construction` with ` (leakage unknown)` or ` (generated data)` when those apply; `fails leakage`; `real task; leakage unknown`; `real task; split tests related periods`; `real task with a documented split`; undocumented labels: `label meaning undocumented (counted with the real tasks); fails leakage` or `…; leakage unknown`. |

## 4. Prose columns

`data_description`, `benchmark_task`, `source_publication`, `stakeholder_and_use`,
`original_task_reasoning`, `data_origin_note`, `task_construction_reasoning`,
`split_provenance`, `split_reasoning`, `multivariate_source_note`, `family_relation`,
`assumptions_and_inferences`, `open_questions`.

These are not rebuilt. File a prose issue only when the text states something the card
contradicts or does not support, as a fact. Examples: a source named that the card says was
not read; a split rule given as documented that the card marks as inferred; a number that
disagrees with the identity columns; reasoning that no longer fits a rebuilt verdict column.
Do not file style, tone or completeness. When a rebuilt column changes, also check the prose
columns that explain it (`split_reasoning` for `split_verdict`, `task_construction_reasoning`
for the label columns, `data_origin_note` for `data_origin`).

## 5. Normalisation: when two values are "the same"

`fc.py compare` marks `differs` mechanically. It ignores case and spacing, the order of `+`
tags and of `;`/`,` lists, and number formatting. Beyond that, two values are the same when
a reader of the paper would draw the same conclusion from either. "appliance category (10
classes)" and "appliance category (10 classes of household device)" are the same; "gesture" and
"user identity" are not. A difference that changes a verdict, a count, a table membership or
an attribution is never just wording.
