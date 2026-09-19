"""Original figures for Part III (thermal radiation). Every file replaces a textbook
figure of the same name. Run:  python make_figures.py
"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle, Polygon, Arc, Wedge, Ellipse
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 160})
INK, BLUE, ORANGE, GREEN, GRAY = "#1c2733", "#1f5fbf", "#d3541f", "#2a9d5c", "#8a97a8"
C1, C2, SIG = 3.7418e8, 1.4388e4, 5.670e-8            # W·µm⁴/m², µm·K

def save(fig, name): fig.tight_layout(); fig.savefig(name, dpi=160); plt.close(fig); print(" ", name)
def arrow(ax, p, q, **kw): ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=12, lw=1.2, color=kw.pop("color", INK), **kw))
def blank(ax, xlim, ylim): ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal"); ax.axis("off")
def planck(lam, T): return C1 / (lam ** 5 * (np.exp(C2 / (lam * T)) - 1))

# ---- spectral blackbody emissive power
lam = np.logspace(-1, 2, 600); fig, ax = plt.subplots(figsize=(6.2, 4))
for T, c in [(300, GRAY), (800, GREEN), (2000, BLUE), (5800, ORANGE)]:
    ax.loglog(lam, planck(lam, T), color=c, lw=2, label=f"T = {T} K" + (" (sun)" if T == 5800 else ""))
Ts = np.logspace(2, 4, 50); ax.loglog(2898 / Ts, planck(2898 / Ts, Ts), ":", color=INK, lw=1.2); ax.text(0.35, 3e6, "Wien: λmax T = 2898 µm·K", fontsize=8, rotation=-38)
ax.axvspan(0.4, 0.7, color="#ffe680", alpha=.4); ax.text(0.42, 3e-1, "visible", fontsize=8)
ax.set_xlabel("wavelength λ (µm)"); ax.set_ylabel(r"$E_{\lambda,b}$ (W/m²·µm)"); ax.set_ylim(1e-1, 1e9); ax.legend(frameon=False, fontsize=9); ax.grid(alpha=.3, which="both")
ax.set_title("Spectral blackbody emissive power (Planck's law)")
save(fig, "spectral_blackbodyu_emmisive_power.png")

# ---- band emission and the blackbody fraction function F(0->λT)
lt = np.logspace(2.3, 4.7, 800); frac = np.array([np.trapezoid(planck(np.linspace(0.05, v / 1000 * 1000, 2000) / 1000, 1000), np.linspace(0.05, v, 2000) / 1000) for v in lt[:0]])  # placeholder
def F0(lamT):
    x = np.linspace(1e-3, lamT / 1000, 4000)                      # work at T = 1000 K; F depends on λT only
    return np.trapezoid(planck(x, 1000), x) / (SIG * 1000 ** 4)
Fv = np.array([F0(v) for v in lt])
fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
l2 = np.linspace(0.1, 12, 500); T = 1000; ax[0].plot(l2, planck(l2, T), color=ORANGE, lw=2); m = (l2 >= 2) & (l2 <= 5)
ax[0].fill_between(l2[m], 0, planck(l2[m], T), color=ORANGE, alpha=.3); ax[0].text(3.5, 3e3, "band\nλ₁–λ₂", ha="center", fontsize=9)
ax[0].set_xlabel("λ (µm)"); ax[0].set_ylabel(r"$E_{\lambda,b}$ (W/m²·µm)"); ax[0].set_title("(a) emission in a spectral band, T = 1000 K"); ax[0].grid(alpha=.3)
ax[1].semilogx(lt, Fv, color=BLUE, lw=2); ax[1].axhline(0.5, color=GRAY, ls=":", lw=1); ax[1].axvline(4107, color=GRAY, ls=":", lw=1); ax[1].text(4300, 0.05, "λT = 4107 µm·K:\nhalf the power", fontsize=8)
ax[1].set_xlabel("λT (µm·K)"); ax[1].set_ylabel(r"$F_{(0\to\lambda)}$"); ax[1].set_title("(b) fraction of blackbody emission below λ"); ax[1].grid(alpha=.3, which="both"); ax[1].set_ylim(0, 1.02)
save(fig, "black_body_prop.png")

# ---- real surface vs blackbody emission, and gray-surface conditions
fig, ax = plt.subplots(figsize=(6, 3.6)); l2 = np.linspace(0.3, 20, 500); T = 1000
eps = 0.85 - 0.5 * np.exp(-((l2 - 8) / 2.5) ** 2) - 0.2 * (l2 < 2)
ax.plot(l2, planck(l2, T), color=INK, lw=2, label="blackbody, Eλ,b"); ax.plot(l2, eps * planck(l2, T), color=ORANGE, lw=2, label="real surface, Eλ = ελ Eλ,b"); ax.plot(l2, 0.8 * planck(l2, T), "--", color=GRAY, lw=1.5, label="gray surface, ε = 0.8")
ax.set_xlabel("λ (µm)"); ax.set_ylabel(r"$E_\lambda$ (W/m²·µm)"); ax.legend(frameon=False, fontsize=9); ax.grid(alpha=.3); ax.set_title("Blackbody, gray, and real surface emission at 1000 K")
save(fig, "emission_from_real_surfacew.png")
fig, ax = plt.subplots(2, 1, figsize=(6, 4.4), sharex=True); l2 = np.linspace(0.3, 30, 500)
ax[0].plot(l2, planck(l2, 5800) / planck(l2, 5800).max(), color=ORANGE, lw=2, label="irradiation Gλ (sun, 5800 K)"); ax[0].plot(l2, planck(l2, 400) / planck(l2, 400).max(), color=BLUE, lw=2, label="emission Eλ (surface, 400 K)")
ax[0].legend(frameon=False, fontsize=8); ax[0].set_ylabel("normalized"); ax[0].grid(alpha=.3)
e = np.where(l2 < 3, 0.9, np.where(l2 < 6, 0.9 - 0.6 * (l2 - 3) / 3, 0.3)); ax[1].plot(l2, e, color=INK, lw=2); ax[1].set_ylim(0, 1); ax[1].set_ylabel("ελ = αλ"); ax[1].set_xlabel("λ (µm)")
ax[1].axvspan(0.3, 3, color=ORANGE, alpha=.12); ax[1].axvspan(5, 30, color=BLUE, alpha=.12); ax[1].text(1.2, 0.15, "α = 0.9\n(solar band)", fontsize=8); ax[1].text(15, 0.4, "ε = 0.3\n(thermal band)", fontsize=8); ax[1].grid(alpha=.3)
fig.suptitle("Gray behaviour needs ελ constant over the bands where G and E are significant", fontsize=10)
save(fig, "gray_surface.png")

# ---- directional emissivity (polar, schematic)
fig, ax = plt.subplots(figsize=(6, 3.6), subplot_kw={"projection": "polar"}); th = np.linspace(-np.pi / 2, np.pi / 2, 300)
ax.plot(th, 0.9 * np.ones_like(th) * (1 - 0.6 * np.clip((abs(th) - 1.0) / 0.57, 0, 1) ** 2), color=BLUE, lw=2, label="nonconductor: ε(θ) ≈ constant to ~60°, then drops")
ax.plot(th, 0.15 * (1 + 1.4 * np.sin(abs(th)) ** 3 * (abs(th) < 1.4)) * (1 - 0.9 * np.clip((abs(th) - 1.4) / 0.17, 0, 1)), color=ORANGE, lw=2, label="conductor: low ε that rises toward grazing angles")
ax.set_theta_zero_location("N"); ax.set_thetamin(-90); ax.set_thetamax(90); ax.set_ylim(0, 1); ax.set_yticks([0.5, 1]); ax.legend(frameon=False, fontsize=8, loc="lower center", bbox_to_anchor=(.5, -.45))
ax.set_title("Directional total emissivity (schematic)", fontsize=10); save(fig, "directional_emmisivity.png")

# ---- electromagnetic spectrum
fig, ax = plt.subplots(figsize=(8, 2.4)); ax.set_xscale("log"); ax.set_xlim(1e-5, 1e5); ax.set_ylim(0, 1); ax.set_yticks([])
bands = [("γ, X rays", 1e-5, 1e-2, GRAY), ("UV", 1e-2, 0.4, "#9b7bd3"), ("visible", 0.4, 0.7, "#f2c14e"), ("infrared", 0.7, 100, ORANGE), ("microwaves", 100, 1e5, GREEN)]
for lab, a, b, c in bands: ax.axvspan(a, b, color=c, alpha=.45); ax.text(np.sqrt(a * b), 0.5, lab, ha="center", va="center", fontsize=9)
ax.axvspan(0.1, 100, ymin=0.05, ymax=0.15, color=INK, alpha=.8); ax.text(3, 0.22, "thermal radiation: 0.1 – 100 µm", ha="center", fontsize=9)
ax.set_xlabel("wavelength (µm)"); ax.set_title("The electromagnetic spectrum and the thermal band", fontsize=10); save(fig, "Electromagnetic radiation spectrum.png")

# ---- view factors: charts computed from the exact relations
def F_parallel(X, Y):
    a = np.sqrt((1 + X ** 2) * (1 + Y ** 2)) / np.sqrt(1 + X ** 2 + Y ** 2)
    return 2 / (np.pi * X * Y) * (np.log(a) + X * np.sqrt(1 + Y ** 2) * np.arctan(X / np.sqrt(1 + Y ** 2)) + Y * np.sqrt(1 + X ** 2) * np.arctan(Y / np.sqrt(1 + X ** 2)) - X * np.arctan(X) - Y * np.arctan(Y))
def F_disks(Ri, Rj): S = 1 + (1 + Rj ** 2) / Ri ** 2; return 0.5 * (S - np.sqrt(S ** 2 - 4 * (Rj / Ri) ** 2))
fig, ax = plt.subplots(1, 2, figsize=(10, 3.8)); X = np.logspace(-1, 1.3, 200)
for Y in [0.1, 0.2, 0.5, 1, 2, 5, 10]: ax[0].semilogx(X, F_parallel(X, Y), lw=1.8, label=f"Y/L = {Y:g}")
ax[0].set_xlabel("X/L"); ax[0].set_ylabel(r"$F_{ij}$"); ax[0].set_title("Aligned parallel rectangles"); ax[0].legend(frameon=False, fontsize=7, ncol=2); ax[0].grid(alpha=.3, which="both")
L_r = np.logspace(-1, 1, 200)
for rj in [0.3, 0.5, 1, 2, 4]: ax[1].semilogx(L_r, F_disks(1 / L_r, rj / L_r), lw=1.8, label=f"rj/ri = {rj:g}")
ax[1].set_xlabel("L / ri"); ax[1].set_ylabel(r"$F_{ij}$"); ax[1].set_title("Coaxial parallel disks"); ax[1].legend(frameon=False, fontsize=8); ax[1].grid(alpha=.3, which="both")
fig.suptitle("View factors computed from the relations in the table below", fontsize=10); save(fig, "view_factor.png")
fig, ax = plt.subplots(figsize=(5, 3.6)); blank(ax, (-1, 6), (-1, 4.5))
ax.add_patch(Polygon([[0, 0], [4, 0], [5, 1], [1, 1]], fc="#fbe3d6", ec=INK)); ax.add_patch(Polygon([[0, 3], [4, 3], [5, 4], [1, 4]], fc="#dfe7f5", ec=INK))
ax.text(2.5, 0.4, "Ai", ha="center"); ax.text(2.5, 3.4, "Aj", ha="center"); arrow(ax, (2.2, 0.8), (3.3, 3.1), color=ORANGE); ax.text(3.4, 2.0, "R", color=ORANGE)
ax.plot([2.2, 2.2], [0.8, 1.9], ":", color=INK); ax.text(2.3, 1.6, "ni, θi", fontsize=8); ax.plot([3.3, 3.3], [3.1, 2.2], ":", color=INK); ax.text(3.4, 2.5, "nj, θj", fontsize=8)
ax.text(2.5, -0.7, r"$F_{ij} = \frac{1}{A_i}\int_{A_i}\int_{A_j}\frac{\cos\theta_i\cos\theta_j}{\pi R^2}\,dA_i\,dA_j$", ha="center", fontsize=10)
ax.set_title("View factor between two surfaces", fontsize=10); save(fig, "view_factor_table.png")   # placeholder image; the table itself is typed in the notes

# ---- angles: plane angle, solid angle, emission from dA
fig, axs = plt.subplots(1, 3, figsize=(10, 3.2))
a = axs[0]; blank(a, (-.3, 2.6), (-.3, 2.4)); a.add_patch(Arc((0, 0), 4, 4, theta1=10, theta2=50, color=ORANGE, lw=2)); a.plot([0, 2 * np.cos(np.radians(10))], [0, 2 * np.sin(np.radians(10))], color=INK); a.plot([0, 2 * np.cos(np.radians(50))], [0, 2 * np.sin(np.radians(50))], color=INK)
a.text(1.3, 0.35, "r", fontsize=9); a.text(1.9, 1.25, "dl", color=ORANGE, fontsize=9); a.text(0.6, 0.55, "dα = dl / r", fontsize=9); a.set_title("(a) plane angle (rad)", fontsize=9)
a = axs[1]; blank(a, (-1.6, 1.6), (-.3, 2.6)); a.add_patch(Wedge((0, 0), 2, 60, 120, fc="#dfe7f5", ec=INK)); a.add_patch(Ellipse((0, 1.85), .9, .3, fc=ORANGE, ec=INK)); a.text(0, 2.25, "dAn", ha="center", color=ORANGE, fontsize=9); a.text(0.7, 0.9, "r", fontsize=9); a.text(-0.6, 0.6, "dω = dAn / r²", fontsize=9); a.set_title("(b) solid angle (sr)", fontsize=9)
a = axs[2]; blank(a, (-1.6, 1.6), (-.4, 2.6)); a.add_patch(Rectangle((-1.2, -0.15), 2.4, 0.15, fc="#c9d3de", ec=INK)); a.add_patch(Rectangle((-.25, -0.15), .5, .15, fc=ORANGE, ec=INK)); a.text(0, -0.4, "dA₁", ha="center", fontsize=9)
arrow(a, (0, 0), (0, 2.2), color=GRAY); a.text(0.05, 2.25, "n", fontsize=9); arrow(a, (0, 0), (1.2, 1.6), color=BLUE); a.add_patch(Arc((0, 0), 1.2, 1.2, theta1=53, theta2=90, color=INK)); a.text(0.25, 0.75, "θ", fontsize=9); a.text(1.25, 1.65, "I(θ, φ)", color=BLUE, fontsize=9); a.set_title("(c) emission from dA₁ into (θ, φ)", fontsize=9)
save(fig, "Mathematical_definitions_angles.png")
fig, ax = plt.subplots(figsize=(4.8, 4)); blank(ax, (-1.8, 1.8), (-.3, 2.2)); ax.add_patch(Arc((0, 0), 3.6, 3.6, theta1=0, theta2=180, color=GRAY, lw=1.2)); ax.add_patch(Rectangle((-1.5, -.12), 3, .12, fc="#c9d3de", ec=INK)); ax.add_patch(Rectangle((-.2, -.12), .4, .12, fc=ORANGE, ec=INK)); ax.text(0, -.32, "dA₁", ha="center", fontsize=9)
th0 = np.radians(55); arrow(ax, (0, 0), (1.8 * np.cos(th0), 1.8 * np.sin(th0)), color=BLUE); ax.add_patch(Ellipse((1.8 * np.cos(th0), 1.8 * np.sin(th0)), .35, .22, angle=-35, fc=ORANGE, ec=INK)); ax.text(1.35, 1.7, "dAn = r² sinθ dθ dφ", fontsize=8)
arrow(ax, (0, 0), (0, 1.9), color=GRAY); ax.text(.05, 1.95, "n", fontsize=9); ax.add_patch(Arc((0, 0), .9, .9, theta1=55, theta2=90, color=INK)); ax.text(.15, .55, "θ", fontsize=9); ax.text(-1.1, 1.7, "hemisphere\nof radius r", fontsize=8, color=GRAY)
ax.set_title("Solid angle subtended by dAn on the hemisphere", fontsize=10); save(fig, "solid_angle_sphere.png")

# ---- spectral and directional distribution (schematic), measuring intensity, blackbody cavity
fig, axs = plt.subplots(1, 2, figsize=(9, 3.2)); l2 = np.linspace(0.5, 15, 200); axs[0].plot(l2, planck(l2, 1500) / planck(l2, 1500).max(), color=ORANGE, lw=2); axs[0].set_xlabel("λ"); axs[0].set_ylabel("Eλ"); axs[0].set_yticks([]); axs[0].set_title("(a) spectral distribution", fontsize=9)
a = axs[1]; blank(a, (-1.6, 1.6), (-.3, 1.8)); a.add_patch(Rectangle((-1.3, -.12), 2.6, .12, fc="#c9d3de", ec=INK)); [arrow(a, (0, 0), (1.4 * np.cos(t) * (0.7 + 0.3 * np.sin(t)), 1.4 * np.sin(t) * (0.7 + 0.3 * np.sin(t))), color=BLUE) for t in np.radians(np.linspace(15, 165, 7))]; a.set_title("(b) directional distribution", fontsize=9)
save(fig, "spectral_and_directional.png")
fig, ax = plt.subplots(figsize=(5, 3.6)); blank(ax, (-1.8, 2.4), (-.3, 2.6)); ax.add_patch(Rectangle((-1.5, -.12), 3, .12, fc="#c9d3de", ec=INK)); ax.add_patch(Rectangle((-.2, -.12), .4, .12, fc=ORANGE, ec=INK)); ax.text(0, -.35, "dA₁ (emitter)", ha="center", fontsize=9)
th0 = np.radians(50); arrow(ax, (0, 0), (2.0 * np.cos(th0), 2.0 * np.sin(th0)), color=BLUE); ax.add_patch(Rectangle((1.15, 1.45), .5, .22, angle=-40, fc="#dfe7f5", ec=INK)); ax.text(1.5, 1.95, "detector dAn\n(solid angle dω)", fontsize=8)
arrow(ax, (0, 0), (0, 2.1), color=GRAY); ax.add_patch(Arc((0, 0), .9, .9, theta1=50, theta2=90, color=INK)); ax.text(.12, .55, "θ", fontsize=9); ax.text(-1.7, 2.2, r"$I_{\lambda,e} = \frac{dq}{dA_1\cos\theta\, d\omega\, d\lambda}$", fontsize=10)
ax.set_title("Measuring intensity: power per unit projected area, per solid angle", fontsize=9); save(fig, "measure_Intensity.png")
fig, ax = plt.subplots(figsize=(4.6, 3.6)); blank(ax, (-2, 2.4), (-2, 2)); ax.add_patch(Circle((0, 0), 1.7, fc="#fbe3d6", ec=INK, lw=2)); ax.add_patch(Circle((0, 0), 1.5, fc="white", ec=INK, lw=1))
ax.add_patch(Rectangle((1.45, -.2), .35, .4, fc="white", ec="white")); [arrow(ax, (1.6, 0), (2.3, y), color=ORANGE) for y in (-.5, 0, .5)]; ax.text(1.75, .7, "aperture:\nblackbody\nemission", fontsize=8)
for t in np.radians([20, 100, 160, 220, 300]): arrow(ax, (1.45 * np.cos(t), 1.45 * np.sin(t)), (0.9 * np.cos(t + .6), 0.9 * np.sin(t + .6)), color=GRAY)
ax.text(0, -1.9, "isothermal enclosure at T", ha="center", fontsize=9); ax.set_title("A cavity with a small hole behaves as a blackbody", fontsize=10); save(fig, "blackbody_cavity.png")

# ---- irradiation: reflection, absorption, transmission; and the opaque version
def irrad(name, opaque):
    fig, ax = plt.subplots(figsize=(5.2, 3.4)); blank(ax, (-2.4, 2.4), (-1.6, 1.8)); ax.add_patch(Rectangle((-2, -1.2), 4, 1.2, fc="#c9d3de" if opaque else "#dfe7f5", ec=INK))
    arrow(ax, (-1.8, 1.6), (-0.1, 0.05), color=ORANGE); ax.text(-1.9, 1.65, "G (irradiation)", fontsize=9, color=ORANGE); arrow(ax, (0.1, 0.05), (1.8, 1.6), color=BLUE); ax.text(1.0, 1.65, "ρG reflected", fontsize=9, color=BLUE)
    ax.text(0, -0.55, "αG absorbed", ha="center", fontsize=9)
    if not opaque: arrow(ax, (0.1, -0.1), (1.0, -1.5), color=GREEN); ax.text(1.05, -1.55, "τG transmitted", fontsize=9, color=GREEN); ax.text(-2.3, -1.5, "ρ + α + τ = 1", fontsize=9)
    else: ax.text(-2.3, -1.5, "opaque: ρ + α = 1", fontsize=9)
    ax.set_title("Irradiation at a " + ("opaque surface" if opaque else "semitransparent medium"), fontsize=10); save(fig, name)
irrad("irradiation.png", False); irrad("irradiation_2.png", True)

# ---- surface energy balance, two-surface exchange, networks, reradiating enclosure
fig, ax = plt.subplots(figsize=(5.4, 3.4)); blank(ax, (-2.6, 2.6), (-1.4, 1.8)); ax.add_patch(Rectangle((-2, -1.2), 4, 1.1, fc="#c9d3de", ec=INK)); ax.text(0, -0.65, "solid, conduction q″cond", ha="center", fontsize=9)
arrow(ax, (0, -0.9), (0, -0.1), color=INK); arrow(ax, (-1.2, 1.2), (-0.2, 0), color=ORANGE); ax.text(-2.4, 1.3, "G", color=ORANGE); arrow(ax, (0.2, 0), (1.2, 1.2), color=BLUE); ax.text(1.3, 1.3, "E + ρG (radiosity J)", color=BLUE, fontsize=9)
arrow(ax, (0.9, 0.05), (2.3, 0.05), color=GREEN); ax.text(1.0, 0.25, "q″conv = h(Ts − T∞)", color=GREEN, fontsize=8); ax.text(0, 1.55, "surface balance:  q″cond = q″conv + (E − αG)", ha="center", fontsize=9)
ax.set_title("Surface energy balance with radiation and convection", fontsize=10); save(fig, "multimode_heat_transfer.png")
fig, ax = plt.subplots(figsize=(5.2, 3.4)); blank(ax, (-1, 6), (-1, 4)); ax.add_patch(Polygon([[0, 0], [4, 0], [5, .8], [1, .8]], fc="#fbe3d6", ec=INK)); ax.add_patch(Polygon([[0, 3], [4, 3], [5, 3.8], [1, 3.8]], fc="#dfe7f5", ec=INK))
ax.text(2.5, .3, "A₁, T₁, ε₁", ha="center", fontsize=9); ax.text(2.5, 3.3, "A₂, T₂, ε₂", ha="center", fontsize=9); arrow(ax, (2.2, .9), (2.2, 2.9), color=ORANGE); arrow(ax, (2.9, 2.9), (2.9, .9), color=BLUE); ax.text(3.1, 1.9, "q₁→₂ − q₂→₁ = q₁₂", fontsize=9)
ax.set_title("Net radiation exchange between two surfaces", fontsize=10); save(fig, "ratitation_btw_two_surfaces.png")
def resistor(ax, x0, x1, y, label, top=True):
    xs = np.linspace(x0, x1, 40); zig = np.where((xs > x0 + .3 * (x1 - x0)) & (xs < x1 - .3 * (x1 - x0)), .18 * np.sin(20 * np.pi * (xs - x0) / (x1 - x0)), 0); ax.plot(xs, y + zig, color=INK, lw=1.5); ax.text((x0 + x1) / 2, y + (.35 if top else -.45), label, ha="center", fontsize=9)
fig, ax = plt.subplots(figsize=(6, 2.2)); blank(ax, (-.5, 6.5), (-1, 1.2)); resistor(ax, 0, 2, 0, "(1 − ε₁)/(ε₁A₁)"); resistor(ax, 2, 4, 0, "1/(A₁F₁₂)"); resistor(ax, 4, 6, 0, "(1 − ε₂)/(ε₂A₂)")
for x_, lab in [(0, "Eb1"), (2, "J₁"), (4, "J₂"), (6, "Eb2")]: ax.plot(x_, 0, "o", color=INK, ms=5); ax.text(x_, -.55, lab, ha="center", fontsize=9)
ax.text(3, .95, "surface resistance · space resistance · surface resistance", ha="center", fontsize=8, color=GRAY); ax.set_title("Radiation network for a two-surface enclosure", fontsize=10); save(fig, "circuit_form.png")
fig, ax = plt.subplots(figsize=(4.8, 2.2)); blank(ax, (-.5, 4.5), (-1, 1.2)); resistor(ax, 0, 4, 0, "(1 − εᵢ)/(εᵢAᵢ)"); ax.plot(0, 0, "o", color=INK); ax.plot(4, 0, "o", color=INK); ax.text(0, -.55, "Ebi = σTi⁴", ha="center", fontsize=9); ax.text(4, -.55, "Ji", ha="center", fontsize=9)
arrow(ax, (1, -.8), (3, -.8), color=ORANGE); ax.text(2, -1, "qi = (Ebi − Ji) / Ri", ha="center", fontsize=8, color=ORANGE); ax.set_title("Surface resistance", fontsize=10); save(fig, "radiation_network_definiton.png")
fig, ax = plt.subplots(figsize=(6, 3.6)); blank(ax, (-.5, 6.5), (-.6, 3.6)); pts = {"1": (0, 0), "2": (6, 0), "R": (3, 3)}
resistor(ax, 0, 6, 0, "1/(A₁F₁₂)", top=False); xs = np.linspace(0, 3, 40); ax.plot(xs, xs * 1.0 + np.where((xs > .9) & (xs < 2.1), .15 * np.sin(20 * np.pi * xs / 3), 0), color=INK, lw=1.5); ax.plot(6 - xs, xs * 1.0 + np.where((xs > .9) & (xs < 2.1), .15 * np.sin(20 * np.pi * xs / 3), 0), color=INK, lw=1.5)
ax.text(1.0, 1.9, "1/(A₁F₁R)", fontsize=9); ax.text(4.0, 1.9, "1/(A₂F₂R)", fontsize=9)
for k, (x_, y_) in pts.items(): ax.plot(x_, y_, "o", color=ORANGE if k == "R" else INK, ms=6)
ax.text(0, -.45, "J₁", ha="center"); ax.text(6, -.45, "J₂", ha="center"); ax.text(3, 3.25, "JR = EbR  (reradiating: qR = 0)", ha="center", fontsize=9, color=ORANGE)
ax.set_title("Three-surface enclosure with a reradiating surface", fontsize=10); save(fig, "re_radiation_surface.png")
# diagram-20250501: piecewise spectral emissivity integrated in parts
fig, ax = plt.subplots(figsize=(6, 3.4)); l2 = np.linspace(0.3, 12, 400); T = 1500; e = np.where(l2 < 2, 0.2, np.where(l2 < 5, 0.8, 0.5))
ax2 = ax.twinx(); ax.plot(l2, planck(l2, T), color=GRAY, lw=1.5, label="Eλ,b"); ax2.step(l2, e, where="post", color=ORANGE, lw=2, label="ελ"); ax2.set_ylim(0, 1); ax2.set_ylabel("ελ", color=ORANGE)
for a_, b_, v in [(0.3, 2, .2), (2, 5, .8), (5, 12, .5)]: m = (l2 >= a_) & (l2 <= b_); ax.fill_between(l2[m], 0, v * planck(l2[m], T), color=ORANGE, alpha=.25)
ax.set_xlabel("λ (µm)"); ax.set_ylabel("Eλ,b (W/m²·µm)"); ax.set_title("Total emissivity from a piecewise ελ: ε = Σ ελ,i [F(0→λi+1) − F(0→λi)]", fontsize=9); ax.grid(alpha=.3)
save(fig, "diagram-20250501.png")
print("done")
