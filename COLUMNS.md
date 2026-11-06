# Columns of `ucr_provenance_audit.csv`

Evidence tags: `S` = quoted source, `D` = measured duplicates, `R` = inference from the record,
`I` = inference about use in practice. Tags joined by `+` indicate combined evidence.

### Identity and description

| Column | Meaning |
|---|---|
| `dataset` | Archive name. |
| `archive_type` | The archive's own type tag (IMAGE, HAR, SENSOR, DEVICE, SPECTRO, ECG, ...). |
| `domain` | Application area of the source study, one of 13 values (Physiological signals; Medical imaging; Human motion & gesture; Handwriting & documents; Audio & speech; Energy & appliances; Traffic & pedestrians; Industrial, sensors & robotics; Spectroscopy & chemistry; Biology & ecology; Shapes & object images; Earth & space science; Simulated). |
| `n_train`, `n_test`, `series_length`, `n_classes` | Default split sizes, series length (`variable` where applicable), number of classes. |
| `data_description` | What the data are and why they were collected (from the audit record). |
| `benchmark_task` | What the archive asks of them. |
| `source_publication` | The paper, thesis, competition or data release the series come from, with what was read. |
| `stakeholder_and_use` | Who would use such a model in practice, if anyone. |

### Source study

| Column | Meaning |
|---|---|
| `original_task` | `real task` (a stakeholder outside the paper needed the prediction), `toy task` (data staged or generated to demonstrate a method), `none` (the source collected data but posed no classification target), `undocumented` (no source says; four datasets). |
| `source_target` | What the source study predicted, or its purpose when it posed no target. |
| `original_task_reasoning` | Why `original_task` has that value. |

### Archive task

| Column | Meaning |
|---|---|
| `data_origin` | `temporal` (sampled over physical time), `ordered, non-temporal` (wavelength, contour arc-length, spatial position, entity index), `synthetic` (a generator's step). Series indexed by frequency, phase, temperature or histogram bin (seven datasets) are `ordered, non-temporal`; `series_index` says which. |
| `series_index` | What the ordered axis is: `time`; `contour arc-length`; `generator step`; `wavelength or wavenumber`; `frequency (power spectrum)`; `spatial position`; `entity index (network node)`; `temperature (melt curve)`; `histogram bin (intensity histogram)`; `phase (folded light curve)`; `time (three axes concatenated)` (UWaveGestureLibraryAll, filed as `ordered, non-temporal`). |
| `data_origin_note` | Populated for 13 datasets: unusual index cases plus Trace (simulated time). Empty for contour arc-length, wavelength or wavenumber, and generator-step series. |
| `benchmark_target` | What the archive's class means. |
| `label_origin` | `source task` (the same target, possibly coarsened), `metadata` (a recording attribute such as season, date, lead or device), `instance identity` (which subject, sensor or actor produced the series), `redefined` (a target the archive defined where the source posed none or a different one), `undocumented`. |
| `label_attached_by` | Who attached the benchmark label: `Source study`, `Collectors`, `Collectors (= curators)`, `Curators`, `Generator`, `Unknown`. |
| `label_evidence` | Evidence tag(s) behind `label_origin`: `S`, `S+R`, `R`. |
| `task_construction` | `pass` / `fail`. Fails when `original_task` is `toy task` or `none`, or `label_origin` is `metadata`, `instance identity` or `redefined`. The four datasets with `original_task = undocumented` are counted with the real tasks (see `open_questions`). `label_origin = undocumented` occurs in the same four datasets. |
| `task_construction_mechanisms` | Reasons for a task-construction failure: `metadata as label`, `instance identity as label`, `task replacement`, `toy source task`; five datasets have multiple reasons. |
| `task_construction_primary_mechanism` | The reason used to group the dataset in counts; when a toy source also has a changed label, the label change takes priority. |
| `task_construction_reasoning` | Benchmark target, source target, who attached the label, and the mechanism definition. |

### Evaluation split

| Column | Meaning |
|---|---|
| `split_verdict` | Split assessment: `Concern` (a documented or data-verified shared source, or at least one test series value-identical to a training series), `Unclear` (the information needed to check separation is missing), `Separated` (the relevant sources differ, as documented or by construction when each series is a distinct event or object with no known grouping above that unit), `Related periods` (different days or windows of the same ongoing process), `Generated` (not assessed by source separation). |
| `leakage` | The split assessment encoded as: `fail` (Concern), `unknown` (Unclear), `pass` (Separated), `pass (related periods)`, `n/a (generated)`. |
| `relevant_new_case` | The assumed evaluation setting: what a new case means for this task (a new patient, a new physical sample, a fresh recording of a familiar person, ...). Each verdict applies to this setting. |
| `leakage_evidence` | What the verdict rests on: exact cross-split matches (with counts), a documented or data-verified shared source, or both; otherwise why it is not a Concern. |
| `n_test_identical_to_train`, `pct_test_identical_to_train` | Count and percentage of test series whose values appear in training, regardless of label. |
| `n_duplicate_groups_with_conflicting_labels` | Count of groups of identical series with conflicting labels, across the combined training and test data. |
| `split_provenance` | Who built the default split and by what rule, where documented. |
| `split_evidence` | Evidence tag(s) behind the split verdict. |
| `split_reasoning` | What the split tests and why a concern can arise. Rows that say "Same as X" carry X's explanation in brackets so every row stands alone. |

### Source relationships and transformations

| Column | Meaning |
|---|---|
| `multivariate_source` | `yes` when the dataset is one channel cut from a multivariate recording (48 datasets); otherwise `no`. |
| `multivariate_source_note` | Which source channels were retained or dropped. |
| `sibling_family` | Name of the group of datasets derived from the same source problem. |
| `family_members` | Related datasets; members in the UEA archive are marked. |
| `family_relation` | How the datasets are related, such as channel selection, relabelling or different splits. |
| `archive_transformation` | What the archive did to the source data (windowing, channel selection, contour unrolling, resampling, z-normalisation, ...). |

### Overall

| Column | Meaning |
|---|---|
| `overall_verdict` | Combines task construction and leakage, with qualifiers for unknown leakage, generated data or label meaning undocumented. The last qualifier occurs only for the four datasets with both `original_task = undocumented` and `label_origin = undocumented`. `real task with a documented split` applies to 5 datasets, and `real task; split separated by construction` to 1 (StarLightCurves). |
| `assumptions_and_inferences` | The assumptions the verdicts rest on: the new case assumed, the split evidence with its tags, who attached the label and on what evidence, and further inferences. |
| `open_questions` | Decisions a reader may contest: datasets outside the constructed set whose label was coarsened, is undocumented, or is a collectors' annotation counted as the source task; series indexed by frequency, phase, temperature or histogram bin (filed as ordered, non-temporal); datasets whose Concern rests on exact matches alone; structural source sharing that is inferred but not documented (Unclear rather than Concern); whether related periods count as clean. |
