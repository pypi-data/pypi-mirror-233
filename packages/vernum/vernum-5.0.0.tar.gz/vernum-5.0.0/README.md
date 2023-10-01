# VerNum


Version numbering for project releases

<a href="https://www.flaticon.com/free-icons/rat" title="rat icons">Rat icons created by Freepik - Flaticon</a>

## Warning: Breaking Changes

Starting in VerNum v4.0.0:

- No longer generates a `.version` file - file generation is the responsibility of an outer script
- Includes `alpha` and `beta` increments
- Supports the `--set-current` option to receive the current version number from a source other than Git tags
- Requires an increment - `patch` is no longer the default
- No longer checks Git status before proceeding
- No longer provides the option to automatically update the Git tag, and no longer supports the `dry-run` option

## Default functionality

- Read the Git tags in the current branch that match the pattern e.g. "v5.6.1" and pick the highest value
- Increment the version number for major, minor, patch, alpha, or beta releases
- Return the new version for later use

## Installation

Requires Python 3 to run the command; your project can be anything.

```
pip3 install vernum
```


## Usage (CLI)

Requirements:

- CD to the root of the project before running it
- Be on the branch that you use for releases (i.e. `master`)
- Be fully up-to-date in git (i.e. merged, committed, and pushed)

Then run the command, specifying the increment to trigger the change:

- `major` change e.g. 5.6.2 to 6.0.0
- `minor` change e.g. 5.6.2 to 5.7.0
- `patch` change e.g. 5.6.2 to 5.6.3
- `beta` change e.g. 5.7.beta3 to 5.7.beta4
- `alpha` change e.g. 5.7.alpha8 to 5.7.alpha9
- Leave it out for no change, just to view the current version

## Source of truth

The default behaviour assumes that the source of truth for the current version comes from the highest valued Git tag in the current branch (based on a regular expression match) but VerNum does not actually update the Git tag. Note that a "v" at the beginning of the input version number is optional; it's not included in the output.

Alternatively, use the `--set-current` option to define a different current version to reference rather than a Git tag. The override is useful for:

- Bootstrapping a repo that has previous versions
- Using a downstream system as the source of truth for version numbers (such as an artifact repository)
- Fixing errors in the Git tag history

To update the Git tag, try something like:

```bash
vernum patch
git tag -a "cat $(.version)" -m "cat $(.version)"
git push origin "cat $(.version)"
```

## Usage (GitLab CI/CD)

VerNum is designed for use withing GitLab CI/CD, and includes a CI/CD configuration template to support the most common use case

Use the provided `vernum.gitlab-ci.yml` to use it in GitLab. Here's an example:

```yaml
include:
  - project: 'steampunk-wizard/projects/vernum'
    ref: stable
    file: 'vernum.gitlab-ci.yml'
    inputs:
        resolution-limit: alpha

---

deliver:
    extends: .release
    script:
        - echo "Edit this script to build and deliver v$(cat .version)"
```

The bundled CI/CD configuration assumes that version number incrementing is a manual process. It will only run deployments if the `$VERNUM` variable is set to a value other than `none`. The configuration includes options and a description to populate the "Run Pipeline" form in GitLab, making it easy to increment the version number and deliver a new release.

The `resolution-limit` input specifies the **limit** for the increment in the Run Pipeline form. It is NOT the actual increment, which is based on the environment variable. The limit must be either `patch` (which includes 3 options) or `alpha` (which includes all 5).

For an alternative to running a manual job to increment the version and deliver a new release, consider the GitLab CLI:

```bash
glab ci run --variables VERNUM:patch
```
