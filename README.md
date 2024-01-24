# License Check Github Action
This action finds and checks all licenses used by dependencies of a software project and can be configured to fail with an error message on invalid licenses.

Dependencies are detected using the respective languages' package manager.

## Supported Languages

* Python3 via pip
* CPP via Conan
* Rust via Cargo
* JavaScript via NPM

## Inputs

### `generate-notice-file`

Shall a notice file be generated? Default `false`

### `notice-file-name`

The name of the notice file. Default `"NOTICE-GENERATED"`

### `fail-on-violation`

Shall the action fail if a license violation is detected? Default `false`

### `config-file-path`

**Required** Path to the config file for the license checker.

### `generate-dash`

This option enables the capability to generate the input file for [Eclipse Dash License Tool](https://github.com/eclipse/dash-licenses) based on `NOTICE-3RD-PARTY-CONTENT` file in ClearlyDefined format based on [ClearDefined Schema](https://docs.clearlydefined.io/using-data).

## Config file syntax

### `whitelist-file-path` (string)

**Required** The path relative to repository where the whitelist for allowed licenses is located.

### `scan-dirs` (list)

**Required** A list of directories to scan.

### `scan-dirs[*].path` (string)

**Required** The path, relative to the repository root, of the directory to scan.

### `scan-dirs[*].decision-file` (string)

The path to the file to overwrite license decisions. Defaults to `dependency_decisions_overwrites.yml`.

### `scan-dirs[*].python-version` (integer)

In case the dir is a python project, this can be used to adjust the Python version. Supported values are either `2` or `3`. Defaults to `3`.

### `scan-dirs[*].python-pip-included-requirement-files` (list[str])

In case the dir is a Python project this allows to pass a list of requirement file paths (relative to the dir) which to consider for resolving dependencies. Defaults to `requirements.txt`.

### `scan-dirs[*].cpp-conan-included-profile-files` (list[str])

In case the dir is a cpp/conan project this allows to pass a list of profile file paths (relative to the dir) which are considered for resolving dependencies. Defaults to the default conan profile.

## Example usage

### Workflow `{repo}/.github/workflows/license-check.yml`
```yaml
jobs:
  check-licenses:
    runs-on: ubuntu-latest
    name: Check Software Licenses

    steps:
      - name: Clone License Checker Repo
        uses: actions/checkout@v4
        with:
          repository: eclipse-velocitas/license-check
          ref: v1
          path: .github/actions/license-check

      - name: Run License Checker
        uses: ./.github/actions/license-check
        with:
          config-file-path: ./.licensecheck.yml
```

### Config file `{repo}/.licensecheck.yml`
```yaml
whitelist-file-path: ./whitelisted-licenses.txt
scan-dirs:
  - path: ./src
    python-version: 2
    python-pip-included-requirement-files:
      - my-requirements.txt
      - dev-requirements.txt
  - path: ./my-cpp-proj
    cpp-conan-included-profile-files:
      - ./profiles/prof1
      - ./profiles/prof2
```

## Advanced topics

### Limitations

The currently used version (v7.0.1) of the Pivotal License Finder has limited support for the Conan Package Manager:
* No direct support of conanfile.py; as a workaround you can add an empty conanfile.txt aside of your conanfile.py.
* It expects a file called "LICENSE*" in some subfolder of the package. If this is not present the scan will fail.
* It internally uses "conan install" to determine the dependencies, which tries to download those from Conan-Center.
  If no pre-built package is available it will try to build the source code locally, which will fail as the actually needed
  build environment cannot be well-known by this License Checker.
  As a workaround, the using repository should do this step before calling the License Checker.


### Caveats

Dependencies and their licenses are only detected _if_ they are added using the respective language's package manager.

Manually added dependencies like locally stored libraries are **NOT** detected!

### Dependencies
* `Pivotal/licenseFinder` -> checking requirements.txt files, released under MIT license: [link](https://github.com/pivotal/LicenseFinder)
* `Workflow/license-checker` -> checking used actions licenses

## Contributing

For guidance on setting up a development environment and how to make a contribution to the Velocitas License Check, see the [contributing guidelines](./CONTRIBUTING.md).
