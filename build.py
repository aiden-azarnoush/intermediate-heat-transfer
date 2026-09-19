"""
build.py -- convert the LaTeX lecture notes into an MkDocs Material site.

    python build.py            # writes docs/ and mkdocs.yml, compiles TikZ, then `mkdocs build --strict`

Sources are expected in  src/convection/  and  src/radiation/  (the LaTeX projects).
"""
import re, subprocess, shutil, hashlib
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
DOCS = ROOT / "docs"
PARTS = [  # folder, part title, slug, overview, chapters = [(chapter title, [file numbers merged in order])]
    ("conduction", "Part I · Conduction", "conduction",
     "Heat moving through a medium by molecular motion alone. This part sets up the two laws every conduction problem rests on, "
     "Fourier's rate law and conservation of energy, then works through the standard steady and transient solutions and a numerical method.",
     [("Introduction to Conduction", [1]), ("Steady One-Dimensional Conduction", [2]), ("Transient Conduction", [3])]),
    ("convection", "Part II · Convection", "convection",
     "Heat transfer between a surface and a moving fluid. The boundary layer is the central idea: it decides the heat transfer coefficient, "
     "and every correlation in this part is a way of getting it for a particular geometry and flow regime.",
     [("Introduction to Convection", [1, 2]),
      ("External Flow: Flat Plates, Wedges, and the Integral Method", [3, 4, 5]),
      ("Internal Flow", [6, 7]),
      ("Natural Convection", [8]),
      ("Boiling and Condensation", [9]),
      ("Turbulent Flow and Turbulence Models", [10]),
      ("Case Study: Thermal Management in Formula One", [11])]),
    ("radiation", "Part III · Thermal Radiation", "radiation",
     "Heat transfer by electromagnetic waves, which needs no medium at all. This part builds from the blackbody and real surface properties "
     "to view factors and the exchange between surfaces, ending with the network method and multimode problems.",
     [("Fundamentals of Thermal Radiation", [1]),
      ("Radiation Intensity, Surface Properties, and Blackbody Radiation", [2]),
      ("Kirchhoff's Law and View Factors", [3]),
      ("Radiation Exchange Between Surfaces", [4]),
      ("Applications and Advanced Topics", [5])]),
]
USE_BOXES = True   # False: definition boxes become plain bold titles
PREAMBLE = r"""\documentclass[border=6pt]{standalone}
\usepackage{amsmath,amssymb,amsfonts,bm,mathrsfs,tikz,pgfplots,circuitikz,xcolor,physics,commath,cancel}
\usetikzlibrary{arrows,arrows.meta,calc,positioning,decorations.pathmorphing,decorations.markings,shapes,patterns,angles,quotes,3d}
\pgfplotsset{compat=1.18}
\newcommand{\volume}{\mathcal{V}}\newcommand{\dxy}[2]{\partial_{#2}\,#1}\newcommand{\tang}{\top}
\begin{document}
%s
\end{document}
"""
SLIM_MACROS = r"""\newcommand{\volume}{\mathcal{V}}
\newcommand{\dxy}[2]{\partial_{#2}\,#1}
\newcommand{\tang}{\top}
"""


def compile_tikz(code: str, out_png: Path) -> bool:
    """Compile one TikZ/circuitikz block to a PNG. Returns False if it fails."""
    if out_png.exists():
        return True
    work = ROOT / "_tikz" / out_png.stem
    work.mkdir(parents=True, exist_ok=True)
    (work / "d.tex").write_text(PREAMBLE % code)
    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "d.tex"], cwd=work, capture_output=True, text=True, timeout=180)
    if not (work / "d.pdf").exists():
        print(f"    TikZ failed: {out_png.name}")
        return False
    subprocess.run(["pdftoppm", "-png", "-r", "170", "-singlefile", "d.pdf", "d"], cwd=work, check=True)
    shutil.copy(work / "d.png", out_png)
    return True


def preprocess(tex: str, part_dir: Path, gen_dir: Path, tag: str) -> str:
    """Resolve \\input, compile TikZ to images, turn custom boxes into markers pandoc keeps as text."""
    # resolve \input{...} of tikz/diagram files
    def inp(m):
        p = part_dir / (m.group(1) if m.group(1).endswith(".tex") else m.group(1) + ".tex")
        return p.read_text() if p.exists() else ""
    tex = re.sub(r"\\input\{([^}]+)\}", inp, tex)
    # compile tikzpicture / circuitikz blocks
    n = 0
    def pic(m):
        nonlocal n
        n += 1
        code = m.group(0)
        name = f"{tag}-tikz-{n}-{hashlib.md5(code.encode()).hexdigest()[:6]}.png"
        ok = compile_tikz(code, gen_dir / name)
        return f"\\includegraphics[width=0.7\\linewidth]{{gen/{name}}}" if ok else ""
    tex = re.sub(r"\\begin\{(tikzpicture|circuitikz)\}.*?\\end\{\1\}", pic, tex, flags=re.S)
    # boxes -> text markers
    tex = re.sub(r"\\begin\{definition\}\[(.*?)\]", lambda m: f"\n\nDEFBOXSTART {m.group(1)}\n\n", tex)
    tex = tex.replace("\\begin{definition}", "\n\nDEFBOXSTART Definition\n\n").replace("\\end{definition}", "\n\nDEFBOXEND\n\n")
    tex = re.sub(r"\\begin\{exa\}(\[(.*?)\])?", lambda m: f"\n\nEXBOXSTART {m.group(2) or 'Example'}\n\n", tex).replace("\\end{exa}", "\n\nDEFBOXEND\n\n")
    # wrapfigure -> figure; drop layout-only commands
    tex = re.sub(r"\\begin\{wrapfigure\}(\[[^\]]*\])?\{[^}]*\}\{[^}]*\}", "\\\\begin{figure}", tex).replace("\\end{wrapfigure}", "\\end{figure}")
    tex = re.sub(r"\\(addcontentsline|thispagestyle|pagestyle)\{[^}]*\}(\{[^}]*\})?(\{[^}]*\})?", "", tex)
    tex = re.sub(r"\\(newpage|clearpage|FloatBarrier|centering|noindent|vspace\*?\{[^}]*\}|hspace\*?\{[^}]*\}|small|footnotesize|normalsize|large)", "", tex)
    tex = re.sub(r"\\begin\{minipage\}.*?\}\s*", "", tex).replace("\\end{minipage}", "")
    tex = re.sub(r"\\caption\[[^\]]*\]", "\\\\caption", tex)
    return tex


def postprocess(md: str, slug: str) -> str:
    """Figures -> markdown images (MkDocs rewrites those paths), display math on its own
    lines, then markers -> admonitions with everything inside indented."""
    # figures: pandoc emits <figure><img src="pics/..."/><figcaption>..</figcaption></figure>
    def fig(m):
        src, cap = m.group(1), (m.group(2) or "").strip()
        src = re.sub(r"^(\.\./)?", "", src)
        return (f'<figure markdown="span">\n![{cap}](../assets/{slug}/{src}){{ width="72%" }}\n' + (f"<figcaption>{cap}</figcaption>\n" if cap else "") + "</figure>")
    md = re.sub(r'<figure[^>]*>\s*<img src="([^"]+)"[^>]*/?>\s*(?:<figcaption>(.*?)</figcaption>)?\s*</figure>', fig, md, flags=re.S)
    md = re.sub(r"!\[(.*?)\]\((?:\.\./)?((?:pics|gen)/[^)\s]+)\)(\{[^}]*\})?",
                lambda m: f'<figure markdown="span">\n![{m.group(1)}](../assets/{slug}/{m.group(2)}){{ width="72%" }}\n' + (f"<figcaption>{m.group(1)}</figcaption>\n" if m.group(1) else "") + "</figure>", md)
    # display math on its own lines for arithmatex
    md = re.sub(r"\$\$(.+?)\$\$", lambda m: "\n\n$$\n" + m.group(1).strip() + "\n$$\n\n", md, flags=re.S)
    # boxes
    lines, out, box = md.splitlines(), [], None
    for ln in lines:
        st = ln.strip()
        if st.startswith("DEFBOXSTART ") or st.startswith("EXBOXSTART "):
            kind = "abstract" if st.startswith("DEF") else "example"
            title = st.split(" ", 1)[1].strip()
            if USE_BOXES: out += [f'!!! {kind} "{title}"', ""]; box = kind
            else: out += [f"**{title}**", ""]
            continue
        if st == "DEFBOXEND":
            box = None; out.append(""); continue
        out.append(("    " + ln) if (box and ln.strip()) else ln)
    md = "\n".join(out)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"


def convert(part_dir: Path, files: list, slug: str, assets: Path, chapter: str) -> str:
    gen = assets / "gen"; gen.mkdir(parents=True, exist_ok=True)
    tex = ""
    for n in files:
        t = (part_dir / "main" / f"lec_{n}.tex").read_text()
        tex += "\n\n" + preprocess(t, part_dir, gen, f"{slug}{n}")
    tmp = ROOT / "_tikz" / f"{slug}_{'-'.join(map(str, files))}.tex"; tmp.parent.mkdir(exist_ok=True)
    tmp.write_text(SLIM_MACROS + tex)
    r = subprocess.run(["pandoc", str(tmp), "-f", "latex", "-t", "markdown_strict+tex_math_dollars+pipe_tables+fenced_code_blocks+raw_html+footnotes",
                        "--wrap=none", "--markdown-headings=atx", "--shift-heading-level-by=1"], capture_output=True, text=True, cwd=part_dir)
    if r.returncode:
        print(r.stderr[:400])
    md = postprocess(r.stdout, slug)
    # one H1 per page; drop H2s that repeat the chapter title or an earlier H2 (merged files)
    out, seen, promote = [], set(), False
    for ln in md.splitlines():
        m = re.match(r"^## (.+?)\s*$", ln)
        if m:
            key = m.group(1).strip().lower()
            if key == chapter.lower() or key in seen:
                promote = True          # its subsections become the sections of this chapter
                continue
            seen.add(key); promote = False
        elif promote and re.match(r"^#{3,6} ", ln):
            ln = ln[1:]                 # H3 -> H2, H4 -> H3, ...
        out.append(ln)
    # a page whose only H2 is the file's own title (or that has none) should use its subsections as sections
    h2s = [i for i, ln in enumerate(out) if ln.startswith("## ")]
    if len(h2s) <= 1:
        first_heading = next((i for i, ln in enumerate(out) if re.match(r"^#{2,6} ", ln)), None)
        if len(h2s) == 1 and h2s[0] == first_heading:
            out.pop(h2s[0])
        out = [ln[1:] if re.match(r"^#{3,6} ", ln) else ln for ln in out]
    return f"# {chapter}\n\n" + "\n".join(out).strip() + "\n"


def main():
    if DOCS.exists():
        shutil.rmtree(DOCS)
    (DOCS / "assets").mkdir(parents=True)
    nav = []
    for folder, part_title, slug, overview, chapters in PARTS:
        part_dir = SRC / folder
        assets = DOCS / "assets" / slug
        if (part_dir / "pics").exists():
            shutil.copytree(part_dir / "pics", assets / "pics", ignore=shutil.ignore_patterns("*.py", "__pycache__"))
        (DOCS / slug).mkdir(parents=True, exist_ok=True)
        entries, listing = [], []
        for k, (title, files) in enumerate(chapters, 1):
            md = convert(part_dir, files, slug, assets, title)
            fname = f"{k:02d}-{re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:60]}.md"
            (DOCS / slug / fname).write_text(md)
            entries.append({title: f"{slug}/{fname}"})
            listing.append(f"{k}. [{title}]({fname})")
            print(f"  {part_title} · {title}")
        (DOCS / slug / "index.md").write_text(f"# {part_title}\n\n{overview}\n\n## Chapters\n\n" + "\n".join(listing) + "\n")
        nav.append({part_title: [f"{slug}/index.md"] + entries})
    (DOCS / "index.md").write_text((ROOT / "index_template.md").read_text())
    shutil.copy(ROOT / "extra.css", DOCS / "extra.css")
    (DOCS / "javascripts").mkdir(exist_ok=True)
    (DOCS / "javascripts" / "mathjax.js").write_text(MATHJAX_JS)
    # mkdocs.yml
    import yaml
    cfg = {
        "site_name": "Intermediate Heat Transfer",
        "site_description": "Lecture notes on convection and thermal radiation, by Aiden Azarnoush",
        "site_author": "Aiden Azarnoush",
        "site_url": "https://aiden-azarnoush.github.io/intermediate-heat-transfer/",
        "repo_url": "https://github.com/aiden-azarnoush/intermediate-heat-transfer",
        "repo_name": "aiden-azarnoush/intermediate-heat-transfer",
        "copyright": 'Written by Aiden Azarnoush · <a href="https://aiden-azarnoush.github.io">aiden-azarnoush.github.io</a> · <a href="https://github.com/aiden-azarnoush">all repositories</a> · Found this useful? <a href="https://paypal.me/azarnoush">☕ Buy me a coffee</a> · <a href="https://paypal.me/azarnoush/3">$3</a> · <a href="https://paypal.me/azarnoush/5">$5</a> · <a href="https://paypal.me/azarnoush">other</a>',
        "theme": {"name": "material", "features": ["navigation.indexes", "navigation.top", "navigation.footer", "toc.integrate", "toc.follow", "search.suggest", "search.highlight", "content.code.copy"],
                  "palette": [{"scheme": "slate", "primary": "indigo", "accent": "indigo", "toggle": {"icon": "material/brightness-4", "name": "Switch to light mode"}},
                              {"scheme": "default", "primary": "indigo", "accent": "indigo", "toggle": {"icon": "material/brightness-7", "name": "Switch to dark mode"}}],
                  "font": {"text": "Source Serif 4", "code": "JetBrains Mono"}},
        "markdown_extensions": ["admonition", "attr_list", "md_in_html", "tables", "footnotes", "pymdownx.details", "pymdownx.superfences", "pymdownx.highlight", "pymdownx.inlinehilite",
                                {"pymdownx.arithmatex": {"generic": True}}, {"toc": {"permalink": True, "toc_depth": 3}}],
        "extra_javascript": ["javascripts/mathjax.js", "https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js"],
        "extra_css": ["extra.css"],
        "nav": [{"Home": "index.md"}] + nav,
    }
    (ROOT / "mkdocs.yml").write_text(yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True))
    r = subprocess.run(["mkdocs", "build", "--strict"], cwd=ROOT, capture_output=True, text=True)
    print(r.stdout[-1500:], r.stderr[-1500:])
    print("build", "OK" if r.returncode == 0 else "FAILED")


MATHJAX_JS = r"""window.MathJax = {
  tex: {inlineMath: [["\\(", "\\)"], ["$", "$"]], displayMath: [["\\[", "\\]"], ["$$", "$$"]], processEscapes: true, processEnvironments: true,
        packages: {"[+]": ["boldsymbol", "cancel", "physics"]},
        macros: {volume: "\\mathcal{V}", dxy: ["\\partial_{#2}\\,#1", 2], tang: "\\top", abs: ["\\left|#1\\right|", 1]}},
  loader: {load: ["[tex]/boldsymbol", "[tex]/cancel", "[tex]/physics"]},
  options: {ignoreHtmlClass: ".*|", processHtmlClass: "arithmatex"}
};
document$.subscribe(() => { MathJax.startup.output.clearCache(); MathJax.typesetClear(); MathJax.texReset(); MathJax.typesetPromise(); });
"""

if __name__ == "__main__":
    main()
