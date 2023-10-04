# pre-commit-update

![Version](https://img.shields.io/pypi/pyversions/pre-commit-update)
![Downloads](https://pepy.tech/badge/pre-commit-update)
![Formatter](https://img.shields.io/badge/code%20style-black-black)
![License](https://img.shields.io/pypi/l/pre-commit-update)

**pre-commit-update** is a simple CLI tool to check and update pre-commit hooks.

## Table of contents

1. [ Reasoning ](#reasoning)
2. [ Installation ](#installation)
3. [ Usage ](#usage)
    1. [ Pipeline usage example ](#usage-pipeline)
    2. [ pre-commit hook usage example ](#usage-hook)
    3. [ pyproject.toml usage example ](#usage-pyproject)

<a name="reasoning"></a>
## 1. Reasoning

`pre-commit` is a nice little tool that helps you polish your code before releasing it into the wild.
It is fairly easy to use. A single `pre-commit-config.yaml` file can hold multiple hooks (checks) that will go through
your code or repository and do certain checks. The trick is that file is static and once you pin your hook versions
after a while they get outdated.

`pre-commit` has a CLI that helps with that by making use of `pre-commit autoupdate` command so the question is
why the f* are you reading this?

`pre-commit-update` was created mostly because there is no easy way to update your hooks by using
`pre-commit autoupdate` and avoiding non-stable (alpha, beta, ...) hook versions. `pre-commit-update` comes
with a CLI that can be configured to solve that problem - along with other use cases.

Other than that - I was bored ^^


<a name="installation"></a>
## 2. Installation

`pre-commit-update` is available on PyPI:
```console 
$ python -m pip install pre-commit-update
```
Python >= 3.7 is supported.

**NOTE:** Please make sure that `git` is installed.


<a name="usage"></a>
## 3. Usage

`pre-commit-update` CLI can be used as below:

```console
Usage: pre-commit-update [OPTIONS]

Options:
  -d, --dry-run       Dry run only checks for the new versions without
                      updating
  -a, --all-versions  Include the alpha/beta versions when updating
  -v, --verbose       Display the complete output
  -e, --exclude TEXT  Exclude specific repo(s) by the `repo` url trim
  -k, --keep TEXT     Keep the version of specific repo(s) by the `repo` url trim (still checks for the new versions)
  -h, --help          Show this message and exit.
```

If you want to just check for updates (without updating `pre-commit-config.yaml`), for example, you would use:
```python
pre-commit-update -d
OR
pre-commit-update --dry-run
```

**NOTE:** If you are to use the `exclude` or `keep` options, please pass the repo url trim as a parameter.
Keep in mind that if you have multiple hooks (id's) configured for a single repo and you `exclude` that repo,
**NONE** of the hooks will be updated, whole repo will be excluded.

Example of repo url trim: https://github.com/ambv/black -> `black` (you will only pass `black` as a parameter to
`exclude` or `keep`)

<a name="usage-pipeline"></a>
### Pipeline usage example
#### GitLab job:

```yaml
pre-commit-hooks-update:
  stage: update
  script:
    # install git if not present in the image
    - pip install pre-commit-update
    - pre-commit-update --dry-run
  except:
    - main
  when: manual
  allow_failure: true
```

**NOTE:** This is just an example, feel free to do your own configuration

<a name="usage-hook"></a>
### pre-commit hook usage example

You can also use `pre-commit-update` as a hook in your `pre-commit` hooks:

```yaml
- repo: https://gitlab.com/vojko.pribudic/pre-commit-update
  rev: v0.0.9
  hooks:
    - id: pre-commit-update
      args: [--dry-run --exclude black --keep isort]
```

<a name="usage-pyproject"></a>
### pyproject.toml usage example

You can configure `pre-commit-update` in your `pyproject.toml` as below (feel free to do your own configuration):

```toml
[tool.pre-commit-update]
dry_run = true
all_versions = false
verbose = true
exclude = ["isort"]
keep = ["black"]
```

**NOTE:** If some of the options are missing (for example `exclude` option), `pre-commit-update`
will use default value for that option (default for `exclude` option would be an empty list).

***IMPORTANT*** If you invoke `pre-commit-update` with any flags (e.g. `pre-commit-update -d`),
`pyproject.toml` configuration will be **ignored**. If you configure `pre-commit-update` via `pyproject.toml`
you should only run `pre-commit-update` (without any flags / arguments).
