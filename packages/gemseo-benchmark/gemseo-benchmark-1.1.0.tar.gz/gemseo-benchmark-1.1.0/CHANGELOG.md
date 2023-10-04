<!--
Copyright 2021 IRT Saint Exupéry, https://www.irt-saintexupery.com

This work is licensed under the Creative Commons Attribution-ShareAlike 4.0
International License. To view a copy of this license, visit
http://creativecommons.org/licenses/by-sa/4.0/ or send a letter to Creative
Commons, PO Box 1866, Mountain View, CA 94042, USA.
-->

<!--
Changelog titles are:
- Added: for new features.
- Changed: for changes in existing functionality.
- Deprecated: for soon-to-be removed features.
- Removed: for now removed features.
- Fixed: for any bug fixes.
- Security: in case of vulnerabilities.
-->

# Changelog

All notable changes of this project will be documented here.

The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.0.0)
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

# Version 1.1.0 (September 2023)

## Added

### Results

- The names of functions and the number of variables are stored in the
    performance history files.

### Report

- The optimization histories can be displayed on a logarithmic scale.

### Scenario

- The options `custom_algos_descriptions` and
    `max_eval_number_per_group` of `Report`{.interpreted-text
    role="class"} can be passed through `Scenario`{.interpreted-text
    role="class"}.

## Fixed

### Report

- The sections of the PDF report are correctly numbered.
- The graphs of the PDF report are anchored to their expected
    locations.

# Version 1.0.0 (June 2023)

First version.
