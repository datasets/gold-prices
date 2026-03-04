# Update Script Maintenance Report

Date: 2026-03-03

- Investigated local updater setup failure caused by strict dependency pinning on this runtime.
- Updated `scripts/requirements.txt` to use compatible ranges:
  - `xlrd>=2.0.1`
  - `pandas>=2.2.3,<3.1`
- Updated `scripts/process.py` to gracefully skip PDF merge when upstream PDF endpoint serves non-PDF content.
- Executed updater (`python scripts/process.py`) and refreshed monthly/annual data from XLS sources while safely skipping blocked PDF merge.
- This improves cross-environment install reliability and prevents hard failures from upstream PDF source changes.
