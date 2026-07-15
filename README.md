# Resume
This repo contains the LaTeX files for my resume. It uses the
[Awesome-CV](https://github.com/posquit0/Awesome-CV) LaTeX template from
[posquit0](https://github.com/posquit0).

## Build
This repo defines a GitHub workflow for building and releasing the resume PDF
(see [build-resume.yml](https://github.com/j43cheun/Resume/blob/main/.github/workflows/build-resume.yml)).
A commit to the [`main`](https://github.com/j43cheun/Resume/tree/main) branch
will automatically trigger a build and release of a resume PDF based on the
resume contents at the time of commit.

<div>
  <a href="https://github.com/j43cheun/Resume/actions/workflows/build-resume.yml">
    <img alt="GitHub Actions" src="https://github.com/j43cheun/Resume/actions/workflows/build-resume.yml/badge.svg" />
  </a>
</div>

Every build also runs [`scripts/validate_ats.py`](scripts/validate_ats.py) against
the compiled PDF, which checks for structural/text-extraction issues that can
break ATS parsing (multi-page overflow, non-embedded fonts, missing-space
run-on words, and small-caps fonts silently corrupting capital letters). It
doesn't validate anything about the resume's actual content, just that the
PDF's text layer is sound. A failing check fails the build.

### ATS Validation
To run the same check locally after building `resume.pdf` (requires
[`poppler-utils`](https://poppler.freedesktop.org/) for `pdftotext`/`pdffonts`/
`pdfinfo`, and Python 3):
```bash
# Ubuntu/WSL2: sudo apt-get install poppler-utils
# macOS:       brew install poppler
python3 scripts/validate_ats.py resume.pdf
```
Pass `--max-pages N` to allow more than one page.

### Personal Contact Info
Since this repo is public, a fresh checkout (including CI, and the copy linked
from LinkedIn) builds with a placeholder email and no phone number, rather than
real contact info. To build a copy with your real details for job
applications, copy the example file and fill it in — it's gitignored, so it
never gets committed:
```bash
cp resume/personal-info.tex.example resume/personal-info.tex
# then edit resume/personal-info.tex with your real phone number and email
```

### Local Build (Ubuntu)
> [!TIP]
> These instructions also work for Ubuntu on Windows Subsystem on Linux 2
> (WSL2). Instructions for setting up Ubuntu on WSL2 are available
> [here](https://documentation.ubuntu.com/wsl/en/latest/guides/install-ubuntu-wsl2/).

> [!TIP]
> Try to match the TeX Live version installed here to the year pinned in
> [build-resume.yml](.github/workflows/build-resume.yml) (`texlive/texlive:TL${YEAR}-historic`).
> A mismatched TeX Live version between local and CI can silently change font
> packages and break the layout in ways that only show up in one environment.

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

### Local Build (macOS)
> [!TIP]
> Try to match the TeX Live version installed here to the year pinned in
> [build-resume.yml](.github/workflows/build-resume.yml) (`texlive/texlive:TL${YEAR}-historic`).
> A mismatched TeX Live version between local and CI can silently change font
> packages and break the layout in ways that only show up in one environment.

#### Setup
Install [MacTex](https://www.tug.org/mactex/mactex-download.html).

#### Build
Run the `xelatex` command from the repo's root directory to build `resume.pdf`.
The generated file will be output to the repo's root directory.
```bash
xelatex resume.tex
```
