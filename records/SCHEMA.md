# Dataset record schema

Each `records/<Name>.yaml` describes the source problem, its conversion into an archive
dataset, and the resulting benchmark. Text fields include source quotations and reasoning;
`references` lists the sources. The CSV holds the final task-construction and split verdicts;
the record's `verdict` describes modality and provenance, not those CSV assessments.

## Identity

| Field | Meaning |
|---|---|
| `name` | Archive dataset name. |
| `archive` | List of archives containing the dataset (`UCR` here). |
| `archive_type_tag` | The archive's type tag. |
| `n_train`, `n_test` | Default training and test set sizes. |
| `series_length` | Samples per series, or `variable`. |
| `n_channels` | Channels per archive series. |
| `n_classes` | Number of classes. |

## `original_problem`

| Field | Meaning |
|---|---|
| `description` | Why the source data were collected and what problem they addressed. |
| `prediction_target` | The source prediction target, with any distinction from the archive label. |
| `input_as_originally_posed` | Original input, such as an image, spectrum or physiological recording. |
| `task_family` | Application category, such as `activity-recognition`, `spectroscopy` or `synthetic-demo`. Some records use `biometric-identification` for the archive's identity target; consult `prediction_target` for the source task. |
| `stakeholder_and_use` | Who would use the prediction and why, if anyone. |
| `source` | Publication or data release supporting the account, including what was read. |
| `provenance_confidence` | `high`, `medium` or `low`: how well the sources establish the original problem. |

## `translation`

| Field | Meaning |
|---|---|
| `transformation` | List of operations used to form the archive series, such as windowing, channel selection or normalisation. |
| `what_the_x_axis_is` | Meaning of the series axis: `time`, `wavelength`, `frequency`, `phase`, `temperature`, `arc-length`, `position` or `index`. |
| `sampling` | Sampling rate, duration or spacing. |
| `information_lost_or_added` | What the conversion discarded or imposed. |
| `label_semantics_changed` | Whether the label meaning changed, and how. |

## `benchmark_task`

| Field | Meaning |
|---|---|
| `description` | What the archive asks a classifier to predict. |
| `is_same_as_original` | `yes`, `narrowed` (restricted scope), `different-task` (changed target or problem), or `no-original-exists` (no original prediction problem). |

## Assessment and sources

| Field | Meaning |
|---|---|
| `verdict` | `native-tsc` (temporal signals), `ordered-not-temporal` (a non-time axis), `translated-modality` (another input modality converted to a series), `synthetic` (generated demonstration), or `unclear` (insufficient provenance or undocumented label meaning). |
| `verdict_rationale` | Explanation of the record's verdict. |
| `known_issues` | List of concerns and qualifications, including duplicates, label changes, split sharing and inferences. |
| `archive_page` | Optional copy of archive-page information: `description` (page text), `donated_by` (credited donor), `data_source_link` and `second_link` (source links). |
| `references` | List of citations and URLs. |

## `empirical`

Recorded experiment results and settings, grouped under `permutation_test` and
`tabular_baseline`. Accuracies are proportions; gaps are accuracy differences.

| Field within `permutation_test` | Meaning |
|---|---|
| `model` | Classifier and settings. |
| `acc_original`, `acc_permuted` | Accuracy before and after applying a fixed permutation of the series axis. |
| `drop` | Original accuracy minus permuted accuracy. |
| `permutation` | How the permutation was applied. |
| `variant` | Data variant used. |
| `seed`, `runtime_s`, `run` | Random seed, runtime in seconds and run date. |

| Field within `tabular_baseline` | Meaning |
|---|---|
| `model` | Tabular classifier and comparison model. |
| `acc_minirocket` | MiniRocket accuracy. |
| `acc_raw_values`, `acc_summary_stats` | Tabular classifier accuracy using raw values or summary statistics. |
| `summary_stats` | Statistics used as features. |
| `gap_raw`, `gap_summary` | MiniRocket accuracy minus the corresponding tabular accuracy. |
| `seed`, `runtime_s`, `run` | Random seed, runtime in seconds and run date. |
