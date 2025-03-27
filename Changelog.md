# Dash File Cache

{:toc}

## CHANGELOG

### 0.2.0 @ 03/25/2025

#### :mega: New

1. Add the Dash component project based on TypeScript. The project contains a `PlainDownloader` component.
2. Add the default downloader component `Downloader`. It is implemented by using `StreamSaver.js`.

#### :floppy_disk: Change

1. Drop the legacy `components.downloader` module because it has been replaced by `components.PlainDownloader` now.
2. Update the `examples/download_file` to match the usage of the new `Downloader` component.

### 0.1.2 @ 10/13/2024

#### :wrench: Fix

1. Fix: Correct a typo of the html tags in the readme file.
2. Fix: Fix typos in the docstrings.
3. Fix: Make `caches.typehints.Deferred` used by other modules.
4. Fix: Add `caches.typehints.Deferred` to the `__all__` list of the module.
5. Fix: Correct the keywords in `pyproject.toml`.

#### :floppy_disk: Change

1. Remove unused `utilities.no_cache`.
2. Adjust the ignore list of `pyright`, `black` and `flake8`.
3. Adjust the typehints of `services.data.ServiceData`.

### 0.1.1 @ 10/09/2024

#### :floppy_disk: Change

1. Adjust the project information.
2. Adjust indents of docker scripts.
3. Reduce the code complexity of `services.data.ServiceData.stream(...)`.
4. Add the `/docs` folder in the ignore list.

### 0.1.0 @ 10/09/2024

#### :mega: New

1. Create this project.
2. Finish the first version of the pacakge `dash_file_cache`.
3. Add the Dash demos `examples/*.py`.
4. Add the unittests `tests/*.py` and the `pytest` configuration `conftest.py`.
5. Add configurations `pyproject.toml`.
6. Add the devloper's environment folder `./docker` and the `Dockerfile`.
7. Add the community guideline files: `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, and `review_checklist.md`.
8. Add the issue and pull request templates.
9. Configure the github workflows.
