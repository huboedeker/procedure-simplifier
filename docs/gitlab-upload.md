# Uploading to GitLab

This folder is a source repository layout, not an npm project. GitLab hosts the source, issues and CI; Python wheels are an optional later distribution channel. No remote, account, token or visibility choice is embedded in this bundle. No upload was performed.

1. Create a **blank project** in the desired GitLab namespace. Choose visibility yourself; a private starting project is suitable for reviewing the framework before sharing. MIT is included, independently of project visibility. Avoid initializing the remote with a second README to keep the first push simple.
2. Extract the repository ZIP and open a terminal in its root, where pyproject.toml is located. Review LICENSE and docs; confirm no real case inputs/runs have been added. tools/check_distribution.py checks the prepared bundle but is not a general secrets detector.
3. Initialize and push using the exact URL GitLab shows:

```sh
git init -b main
git add .
git status
git commit -m "Package procedure simplifier framework 0.8.0"
git remote add origin <paste-your-project-clone-url>
git push -u origin main
```

Replace the angle-bracket placeholder before running it. Authenticate with your normal SSH setup or Git credential manager. Do not put access tokens in files, remote URLs committed to scripts, or CI logs. This bundle contains no .git history or configured identity.

4. Enable/use an appropriate GitLab runner and inspect the pipeline. The included CI configuration tests and builds distribution artifacts; it has not been executed on your GitLab account. It does not publish packages, call a model, upload case files or deploy a service.
5. After successful review/testing, create a release/tag using your normal GitLab process. The package version starts at0.8.0. Build a wheel/sdist with `python -m build` if you want installable downloads. Source development and installed-wheel smoke checks should both pass.

An optional later step is GitLab's PyPI package registry. Add an explicit publishing job and use protected CI credentials/job tokens according to your GitLab configuration. There is no automatic publishing job here. A JavaScript/npm wrapper is only useful if a future Node-based host or interface needs one; adding it now would retain the Python dependency while increasing packaging work.

Official references: [Python packaging guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/), [project script entry points](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/), [GitLab PyPI registry](https://docs.gitlab.com/user/packages/pypi_repository/).
