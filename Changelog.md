# Dash File Cache

[toc]

## CHANGELOG

### 0.2.0 @ 04/02/2025

#### :mega: New

1. Bump the document to the new version `0.2.0`.
2. Update the tutorials for introducing the newly implemented downloader components.
3. Update the example script explanation `/examples/download-file`.

#### :wrench: Fix

1. Fix: Add the missing version tags for the old version documents.
2. Fix: Correct a bad import in `zh-cn/docs/usages/downloader`.

#### :floppy_disk: Change

1. Bump the `yarn` version from `4.4.1` to `4.7.0`.
2. Bump the `docusaurus` version from `3.5.2` to `3.7.0`.
3. Bump the `typescript` version from `5.5.2` to `5.8.2`.
4. Bump the dependencies versions to handle the vulnerabilities.
5. Clean up the workspace and formatter configurations.
6. Bump the website source codes to the newest status.
7. Update the overview diagrams of the whole pacakge.

### 0.1.2 @ 10/30/2024

#### :wrench: Fix

1. Fix: Complete some missing translations in the `zh-cn` doc.
2. Fix: Change the edit URLs of the `zh-cn` doc from the original `en` version to the `zh-cn` version.

### 0.1.2 @ 10/30/2024

#### :mega: New

1. Finalize the `zh-cn` translation of the document version `0.1.2`.

#### :wrench: Fix

1. Fix: Correct some typos in the English documents.
2. Fix: Fix a typo causing the broken anchor issue.
3. Fix: Make the action step of `yarn install` synchronized with the newest API.
4. Fix: `zh-cn` document cannot handle the line break correctly. Remove the unexpected line breaks.
5. Fix: Correct another typo caused by a wrong symbol.

### 0.1.2 @ 10/28/2024

#### :mega: New

1. Upgrade the document design to the latest version, where the versions of the source
   codes and examples will be centralized and automatically inferred.

#### :floppy_disk: Change

1. Change the configurations of the code formatter.
2. Move figures to the global space.
3. Modify the format of the license from `.md` to `.mdx`.

### 0.1.2 @ 10/14/2024

#### :mega: New

1. Synchronize the document contents to the newest version.

#### :wrench: Fix

1. Fix: Remove a duplicated part in `/docs/apis/caches/memory/CacheQueue`.
2. Fix: Correct a typo in the title of `/docs/category/examples`.
3. Fix: The alias of `Downloader` should be listed in `/docs/apis`.

#### :floppy_disk: Change

1. Update the link of "fire an issue".
2. Make some URLs delegated to `./src/envs`.

### 0.1.0 @ 10/13/2024

#### :mega: New

1. Create this project.
2. Upload the first version of the document, containing the tutorial and API docs.

#### :wrench: Fix

1. Fix: The workflow `setup/node` is not compatible with `Yarn@4`, adjust the workflow
   load `yarn` correctly.
