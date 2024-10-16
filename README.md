# Resume

## Build
This repo defines a GitHub workflow for building and releasing the resume PDF
(see [build-resume.yml](https://github.com/j43cheun/Resume/blob/main/.github/workflows/build-resume.yml)).
A commit to the [`main`](https://github.com/j43cheun/Resume/tree/main) branch
will automatically trigger a build and release of a resume PDF based on the
resume contents at the time of commit.

### Local Build (Ubuntu)
> [!TIP]
> These instructions also work for Ubuntu on Windows Subsystem on Linux 2
> (WSL2). Instructions for setting up Ubuntu on WSL2 are available
> [here](https://documentation.ubuntu.com/wsl/en/latest/guides/install-ubuntu-wsl2/).

#### Setup
Install the `texlive-full` software package.
```bash
sudo apt-get update
sudo apt-get install texlive-full
```

#### Build
Run the `xelatex` command from the repo's root directory to build `resume.pdf`.
The generated file will be output to the repo's root directory.
```bash
xelatex resume.tex
```
