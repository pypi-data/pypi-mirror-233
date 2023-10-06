# Python package template

Template for Python packages for qurix Technology.

## Structure

A normal Python package will start with the namespace `qurix` as in this sample package. A sample structure is as follows:

```text
.
├── LICENCE
├── Makefile
├── README.md
├── qurix
│   └── <domain>
│       └── <module-organization-level>
│           ├── __init__.py
│           ├── __version__.py
│           └── <module>
├── requirements.txt
├── setup.py
└── tests
    ├── __init__.py
    └── test_client.py
```

## Versioning and release

Package versions will be identified according to [semantic versioning](https://semver.org/lang/en). The release process will deploy in both [Test PyPI](https://test.pypi.org/) and [PyPI](https://pypi.org/).

```mermaid
gitGraph
    commit
    branch staging
    branch feature/some-feature
    checkout feature/some-feature
    commit
    commit
    checkout staging
    merge feature/some-feature id: "Test PyPI"
    checkout main
    merge staging id: "Release in PyPI" tag: "v0.1.0"
    branch fix/some-fix
    checkout fix/some-fix
    commit
    checkout staging
    merge fix/some-fix id: "Test PyPI again"
    checkout main
    merge staging id: "New fix release in PyPI" tag: "v0.1.1"
```

## Deployment

Using Github Actions. See `.github/worfklows/`