# Intermediate Heat Transfer — lecture notes

**[Read the notes online →](https://aiden-azarnoush.github.io/intermediate-heat-transfer/)**

My notes on **conduction** (Part I), **convection** (Part II), and
**thermal radiation** (Part III), written from several textbooks in one
consistent notation and published as a website: a sidebar with every lecture and section, full-text
search, equations rendered with MathJax, light and dark mode, and a layout
that works on a phone. The LaTeX sources are in this repository too.

## Contents

**Part I · Conduction** — Fourier's law and the heat equation, boundary
conditions, thermal resistances, contact resistance, cylinders and the
critical radius, heat generation, fins, lumped capacitance, the exact
plane-wall and semi-infinite solutions, and an explicit finite-difference
solver in a few lines of Python.

**Part II · Convection** — introduction and the energy equation, boundary
layers, the Nusselt number and flat-plate heat transfer, wedge flow and
similarity, internal flow and temperature distributions, natural
convection, boiling and condensation, an introduction to turbulence
models, and a case study on thermal management in Formula One.

**Part III · Thermal Radiation** — blackbody radiation and real surfaces,
the wave and particle pictures of light, Kirchhoff's law, net exchange
between surfaces and view factors, and applications.

> [!NOTE]
> These are study notes, not a textbook. Definitions and key results are
> set off in boxes; derivations are worked in the text. Corrections are
> welcome as issues or pull requests.

## How the site is made

The notes are written in LaTeX (`src/conduction/`, `src/convection/`,
`src/radiation/`). Every figure is original: the plots are computed from the
equations in the notes and the schematics are drawn, all by the
`make_figures.py` script in each part's `pics/` folder, so they can be
regenerated and changed. Correlation and view-factor tables are typed into
the notes.
`build.py` converts them to Markdown with pandoc, compiles every TikZ and
circuitikz diagram to an image with pdflatex, turns the definition boxes
into callouts, merges the lecture files into topical chapters (the `PARTS`
table at the top of `build.py` says which files make which chapter, and is
the place to reorganize), and writes `docs/` and `mkdocs.yml` for
[MkDocs](https://www.mkdocs.org/) with the Material theme. Pushing to
`main` publishes the site through the GitHub Actions workflow in
`.github/workflows/deploy.yml`.

## Rebuild after editing the notes

```bash
pip install -r requirements.txt      # mkdocs-material, pyyaml
# also needed: pandoc, pdflatex (TeX Live with tikz, pgfplots, circuitikz), pdftoppm
python build.py                      # regenerates docs/ and mkdocs.yml, then builds the site
mkdocs serve                         # preview at http://127.0.0.1:8000
```

Commit the regenerated `docs/` and `mkdocs.yml` together with the LaTeX
change and push; the site updates by itself.

> [!TIP]
> To preview without the LaTeX toolchain, `pip install mkdocs-material`
> and `mkdocs serve` are enough: the converted Markdown is committed.

## Repository layout

```
src/conduction/, src/convection/, src/radiation/
                                  LaTeX sources (main.tex, main/lec_*.tex, pics/, tikz/, diagrams/)
build.py                          LaTeX -> Markdown -> site converter
docs/                             generated Markdown, images, and assets (committed)
mkdocs.yml                        generated site configuration
.github/workflows/deploy.yml      publishes to GitHub Pages on every push
```

## Author and license

**Aiden Azarnoush**. Text and figures: CC BY 4.0. Code (`build.py` and the
figure scripts): MIT.

---

*Dedicated to my beloved mother, Simin Nematpour.*
