window.MathJax = {
  tex: {inlineMath: [["\\(", "\\)"], ["$", "$"]], displayMath: [["\\[", "\\]"], ["$$", "$$"]], processEscapes: true, processEnvironments: true,
        packages: {"[+]": ["boldsymbol", "cancel", "physics"]},
        macros: {volume: "\\mathcal{V}", dxy: ["\\partial_{#2}\\,#1", 2], tang: "\\top", abs: ["\\left|#1\\right|", 1]}},
  loader: {load: ["[tex]/boldsymbol", "[tex]/cancel", "[tex]/physics"]},
  options: {ignoreHtmlClass: ".*|", processHtmlClass: "arithmatex"}
};
document$.subscribe(() => { MathJax.startup.output.clearCache(); MathJax.typesetClear(); MathJax.texReset(); MathJax.typesetPromise(); });
