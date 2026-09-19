"""Original figures for Part II (convection). Every file replaces a textbook figure
of the same name. Computed curves use the equations in the notes; the rest are
schematics drawn here.   Run:  python make_figures.py
"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle, Polygon, Arc
from scipy.integrate import solve_ivp, solve_bvp
from scipy.optimize import brentq

plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 160})
INK, BLUE, ORANGE, GREEN, GRAY = "#1c2733", "#1f5fbf", "#d3541f", "#2a9d5c", "#8a97a8"

def save(fig, name): fig.tight_layout(); fig.savefig(name, dpi=160); plt.close(fig); print(" ", name)
def arrow(ax, p, q, **kw): ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=12, lw=1.2, color=kw.pop("color", INK), **kw))
def blank(ax, xlim, ylim): ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal"); ax.axis("off")
def wall(ax, x0, x1, y=0, h=0.15): ax.add_patch(Rectangle((x0, y - h), x1 - x0, h, fc="#c9d3de", ec=INK, hatch="////", lw=1))
def bl_edge(ax, x0, x1, y0, scale, p=0.5, **kw): x = np.linspace(x0, x1, 100); ax.plot(x, y0 + scale * ((x - x0) / (x1 - x0)) ** p, "--", color=kw.get("color", INK), lw=1.2)
def profile(ax, x, ymax, n=7, shape=lambda s: s ** (1 / 7) if False else 1 - (1 - s) ** 2, u=1.0):
    ys = np.linspace(0, ymax, 40); ax.plot(x + u * shape(ys / ymax), ys, color=BLUE, lw=1.5)
    for y in np.linspace(0, ymax, n)[1:]: arrow(ax, (x, y), (x + u * shape(y / ymax), y), color=BLUE)

# ====================================================== Blasius: solve f''' + f f''/2 = 0
def blasius():
    def shoot(s):
        sol = solve_ivp(lambda t, y: [y[1], y[2], -0.5 * y[0] * y[2]], [0, 10], [0, 0, s], rtol=1e-9, atol=1e-11)
        return sol
    s = brentq(lambda s: shoot(s).y[1, -1] - 1, 0.2, 0.5)
    sol = shoot(s); eta = np.linspace(0, 8, 300); f, fp, fpp = sol.sol(eta) if False else (np.interp(eta, sol.t, sol.y[0]), np.interp(eta, sol.t, sol.y[1]), np.interp(eta, sol.t, sol.y[2]))
    return eta, f, fp, fpp, s
eta, f, fp, fpp, fpp0 = blasius()
fig, ax = plt.subplots(figsize=(6, 3.8))
ax.plot(eta, f, color=GREEN, lw=2, label="f"); ax.plot(eta, fp, color=BLUE, lw=2, label="f′ = u/u∞"); ax.plot(eta, fpp, color=ORANGE, lw=2, label="f″")
ax.axhline(0.99, color=GRAY, lw=.8, ls=":"); ax.text(5.2, 1.03, "u/u∞ = 0.99 at η ≈ 5.0", fontsize=9, color=GRAY)
ax.set_xlabel(r"$\eta = y\sqrt{u_\infty/(\nu x)}$"); ax.set_ylabel("f, f′, f″"); ax.set_xlim(0, 8); ax.set_ylim(0, 2.2); ax.legend(frameon=False); ax.grid(alpha=.3)
ax.set_title(f"Blasius solution: f‴ + ½ f f″ = 0,  f″(0) = {fpp0:.4f}")
save(fig, "Belasisus_sol.png")

# ====================================================== thermal profiles over a flat plate for several Pr
fig, ax = plt.subplots(figsize=(6, 3.8))
fsol = solve_ivp(lambda t, y: [y[1], y[2], -0.5 * y[0] * y[2]], [0, 12], [0, 0, fpp0], dense_output=True, rtol=1e-9)
for Pr, c in [(0.1, GREEN), (0.7, BLUE), (1, GRAY), (7, ORANGE), (100, INK)]:
    # theta'' + (Pr/2) f theta' = 0, theta(0)=0, theta(inf)=1  ->  theta' = C exp(-Pr/2 int f)
    e = np.linspace(0, 12, 2000); F = fsol.sol(e)[0]; If = np.concatenate([[0], np.cumsum(0.5 * (F[1:] + F[:-1]) * np.diff(e))])
    tp = np.exp(-0.5 * Pr * If); th = np.concatenate([[0], np.cumsum(0.5 * (tp[1:] + tp[:-1]) * np.diff(e))]); th /= th[-1]
    ax.plot(th, e, color=c, lw=2, label=f"Pr = {Pr:g}")
ax.plot(fp, eta, "--", color=BLUE, lw=1, label="velocity, u/u∞")
ax.set_ylim(0, 8); ax.set_xlim(0, 1.05); ax.set_xlabel(r"$\theta = (T - T_s)/(T_\infty - T_s)$"); ax.set_ylabel("η"); ax.legend(frameon=False, fontsize=9); ax.grid(alpha=.3)
ax.set_title("Thermal profiles: the thermal layer is thin for large Pr")
save(fig, "thermal_profile_flat_plate.png")

# ====================================================== h(x) and C_f(x) along a plate (air, u = 10 m/s, transition at Re = 5e5)
nu, kf, Pr, U = 1.5e-5, 0.026, 0.71, 10.0
x = np.linspace(0.005, 2, 600); Re = U * x / nu; xt = 5e5 * nu / U
h = np.where(Re < 5e5, 0.332 * Re ** .5 * Pr ** (1 / 3), 0.0296 * Re ** .8 * Pr ** (1 / 3)) * kf / x
fig, ax = plt.subplots(figsize=(6, 3.6))
ax.plot(x, h, color=ORANGE, lw=2); ax.axvline(xt, color=GRAY, ls=":", lw=1); ax.text(xt + .03, h.max() * .8, "transition\nRe = 5×10⁵", fontsize=9, color=GRAY)
ax.set_xlabel("x (m)"); ax.set_ylabel("h (W/m²K)"); ax.set_ylim(0, h.max() * 1.1); ax.grid(alpha=.3)
ax.set_title("Local h along a flat plate: laminar x⁻½, then turbulent x⁻⅕ (air, 10 m/s)")
save(fig, "h_vs_x.png")
cf = np.where(Re < 5e5, 0.664 * Re ** -.5, 0.0592 * Re ** -.2)
fig, ax = plt.subplots(figsize=(6, 3.6)); ax.plot(x, cf * 1e3, color=BLUE, lw=2); ax.axvline(xt, color=GRAY, ls=":", lw=1)
ax.set_xlabel("x (m)"); ax.set_ylabel(r"$C_f \times 10^3$"); ax.set_ylim(0, 8); ax.grid(alpha=.3)
ax.set_title("Local friction coefficient: drops as x⁻½, jumps at transition")
save(fig, "fig_5.png")

# ====================================================== drag coefficient of a cylinder and a sphere (standard empirical fits)
Re = np.logspace(-1, 6, 400)
cd_sph = 24 / Re * (1 + 0.15 * Re ** .687) + 0.42 / (1 + 4.25e4 * Re ** -1.16)         # Clift-Gauvin
cd_cyl = 1.18 + 6.8 / Re ** .89 + 1.96 / Re ** .5 - 0.0004 * Re / (1 + 3.64e-7 * Re ** 2)   # Cheng (2009) fit
fig, ax = plt.subplots(figsize=(6, 3.8))
ax.loglog(Re, cd_cyl, color=ORANGE, lw=2, label="cylinder"); ax.loglog(Re, cd_sph, color=BLUE, lw=2, label="sphere")
ax.axvspan(2e5, 5e5, color=GRAY, alpha=.15); ax.text(2.2e5, 30, "drag crisis:\nBL turns turbulent", fontsize=8, color=GRAY)
ax.set_xlabel("Re = u∞D/ν"); ax.set_ylabel(r"$C_D$"); ax.set_ylim(0.05, 300); ax.legend(frameon=False); ax.grid(alpha=.3, which="both")
ax.set_title("Drag coefficient in cross flow (empirical correlations)")
save(fig, "cd_vs_Re.png")

# ====================================================== local Nusselt number around a cylinder (schematic based on the front-stagnation solution)
th = np.linspace(0, 180, 361); fig, ax = plt.subplots(figsize=(6, 3.8))
for Re_, c in [(7e4, GREEN), (1.4e5, BLUE), (2.2e5, ORANGE)]:
    front = 1.14 * Re_ ** .5 * 0.71 ** .4 * np.clip(1 - (th / 90) ** 3, 0.12, None)
    sep = 80 if Re_ < 2e5 else 140
    wake = front[np.argmin(abs(th - sep))] * (1 + 1.6 * np.clip((th - sep) / (180 - sep), 0, 1) ** .8)
    nu_ = np.where(th < sep, front, wake); ax.plot(th, nu_, color=c, lw=2, label=f"Re ≈ {Re_:.0e}")
ax.set_xlabel("θ from the front stagnation point (degrees)"); ax.set_ylabel(r"$Nu_\theta$"); ax.set_xlim(0, 180); ax.legend(frameon=False); ax.grid(alpha=.3)
ax.set_title("Local Nu around a cylinder: minimum at separation, recovery in the wake\n(schematic; front part from the laminar stagnation solution)", fontsize=10)
save(fig, "nusselt_angular_theta.png")

# ====================================================== axial temperature in a tube
xx = np.linspace(0, 1, 200); fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
ax[0].plot(xx, 20 + 40 * xx, color=BLUE, lw=2, label=r"$T_m$"); ax[0].plot(xx, 35 + 40 * xx, color=ORANGE, lw=2, label=r"$T_s$")
ax[0].fill_between(xx, 20 + 40 * xx, 35 + 40 * xx, color=GRAY, alpha=.15); ax[0].set_title("(a) constant surface heat flux"); ax[0].text(.5, 42, r"$T_s - T_m$ = const", ha="center", fontsize=9)
ax[1].plot(xx, 80 - 60 * np.exp(-3 * xx), color=BLUE, lw=2, label=r"$T_m$"); ax[1].axhline(80, color=ORANGE, lw=2, label=r"$T_s$")
ax[1].set_title("(b) constant surface temperature"); ax[1].text(.55, 50, r"$T_s - T_m$ decays exponentially", fontsize=9)
for a in ax: a.set_xlabel("x / L"); a.set_ylabel("T (°C)"); a.legend(frameon=False, loc="lower right"); a.grid(alpha=.3)
save(fig, "axial_temp_pipe.png")

# ====================================================== boiling curve (schematic)
dT = np.logspace(0, 3, 400)
q = np.where(dT < 5, 1e3 * dT ** 1.3, np.where(dT < 30, 1e3 * 5 ** 1.3 * (dT / 5) ** 3.2, np.where(dT < 120, 1.3e6 * (dT / 30) ** -1.3, 2.2e5 * (dT / 120) ** 2.6)))
fig, ax = plt.subplots(figsize=(6.4, 4)); ax.loglog(dT, q, color=ORANGE, lw=2.5)
for x_, lab in [(2, "free\nconvection"), (12, "nucleate\nboiling"), (60, "transition\nboiling"), (300, "film\nboiling")]: ax.text(x_, 3e3, lab, ha="center", fontsize=9, color=INK)
ax.annotate("critical heat flux q″max", (30, 1.3e6), (60, 3e6), fontsize=9, arrowprops=dict(arrowstyle="->", color=INK))
ax.annotate("Leidenfrost point q″min", (120, 2.2e5), (200, 6e4), fontsize=9, arrowprops=dict(arrowstyle="->", color=INK))
ax.set_xlabel(r"excess temperature $\Delta T_e = T_s - T_{sat}$ (K)"); ax.set_ylabel(r"heat flux q″ (W/m²)"); ax.set_ylim(1e3, 1e7); ax.grid(alpha=.3, which="both")
ax.set_title("Pool boiling curve for water at 1 atm (schematic)")
save(fig, "heatflux_boiling_cruve.png")

# ====================================================== natural convection similarity (Ostrach): f''' + 3ff'' - 2f'^2 + θ = 0, θ'' + 3Pr f θ' = 0
def ostrach(Pr):
    def rhs(e, y): return np.vstack([y[1], y[2], -3 * y[0] * y[2] + 2 * y[1] ** 2 - y[3], y[4], -3 * Pr * y[0] * y[4]])
    def bc(a, b): return np.array([a[0], a[1], a[3] - 1, b[1], b[3]])
    e = np.linspace(0, 10, 200); y0 = np.zeros((5, e.size)); y0[3] = np.exp(-e); y0[1] = e * np.exp(-e)
    return solve_bvp(rhs, bc, e, y0, tol=1e-6, max_nodes=20000)
fig, ax = plt.subplots(1, 2, figsize=(9, 3.6))
for Pr, c in [(0.72, BLUE), (1, GRAY), (10, ORANGE), (100, GREEN)]:
    s = ostrach(Pr); e = np.linspace(0, 8, 300); y = s.sol(e)
    ax[0].plot(e, y[1], color=c, lw=2, label=f"Pr = {Pr:g}"); ax[1].plot(e, y[3], color=c, lw=2, label=f"Pr = {Pr:g}")
ax[0].set_ylabel(r"$f'(\eta)$  (velocity)"); ax[1].set_ylabel(r"$\theta(\eta)$  (temperature)")
for a in ax: a.set_xlabel(r"$\eta = (y/x)(Gr_x/4)^{1/4}$"); a.legend(frameon=False, fontsize=9); a.grid(alpha=.3); a.set_xlim(0, 8)
fig.suptitle("Similarity solution for natural convection on a vertical plate (computed)", fontsize=11)
save(fig, "natural_convection_similarity.png")

# ====================================================== schematics
# fig_1: differential control volume dx dy
fig, ax = plt.subplots(figsize=(5, 3.6)); blank(ax, (-1, 6), (-1, 4))
ax.add_patch(Rectangle((1.5, 1), 2, 1.5, fc="#eef3fb", ec=INK, lw=1.5)); ax.text(2.5, 1.75, "dx · dy", ha="center", va="center")
arrow(ax, (0.6, 1.75), (1.5, 1.75), color=BLUE); ax.text(0.2, 2.0, r"$\rho u c_p T$", fontsize=9, color=BLUE); arrow(ax, (3.5, 1.75), (4.4, 1.75), color=BLUE); ax.text(3.6, 2.0, r"$\rho u c_p T + \partial_x(\cdot)dx$", fontsize=9, color=BLUE)
arrow(ax, (2.5, 0.2), (2.5, 1), color=ORANGE); ax.text(2.6, 0.3, r"$q''_y$", fontsize=9, color=ORANGE); arrow(ax, (2.5, 2.5), (2.5, 3.3), color=ORANGE); ax.text(2.6, 2.9, r"$q''_y + \partial_y q''_y dy$", fontsize=9, color=ORANGE)
ax.set_title("Energy balance on a differential control volume", fontsize=10); save(fig, "fig_1.png")

# fig_2, fig_3, fig_4, fig_6/7 (concentration), fig_8, fig_9: boundary layer sketches
def bl_sketch(name, title, thermal=False, turbulent=False, conc=False):
    fig, ax = plt.subplots(figsize=(7, 3.4)); blank(ax, (-0.5, 9), (-0.4, 3.2)); wall(ax, 0, 8.5)
    for y in np.linspace(0.6, 2.8, 5): arrow(ax, (-0.5, y), (0.2, y), color=BLUE)
    ax.text(-0.5, 3.0, "u∞, T∞", color=BLUE, fontsize=10)
    if turbulent:
        bl_edge(ax, 0, 3.2, 0, 0.9, 0.5); xs = np.linspace(3.2, 8.5, 100); ax.plot(xs, 0.9 + 1.4 * ((xs - 3.2) / 5.3) ** 0.8, "--", color=INK, lw=1.2)
        ax.axvspan(3.0, 4.2, color=GRAY, alpha=.15); ax.text(1.2, 2.4, "laminar", fontsize=9); ax.text(3.0, 2.9, "transition", fontsize=9); ax.text(6.2, 2.9, "turbulent", fontsize=9)
        profile(ax, 1.6, 0.6); profile(ax, 6.5, 2.0, shape=lambda s: s ** (1 / 7))
    else:
        bl_edge(ax, 0, 8.5, 0, 2.2, 0.5); profile(ax, 2, 1.1); profile(ax, 5.5, 1.8)
        ax.text(6.5, 2.4, "δ(x)" if not thermal else "δt(x)", fontsize=10)
    if thermal: ax.text(4.5, -0.35, "Ts", fontsize=10, color=ORANGE)
    if conc: ax.text(-0.5, 3.0, "u∞, CA,∞", color=BLUE, fontsize=10); ax.text(4.5, -0.35, "CA,s", fontsize=10, color=ORANGE)
    ax.set_title(title, fontsize=10); save(fig, name)
bl_sketch("fig_2.png", "Velocity boundary layer on a flat plate: u = 0 at the wall, u → u∞ at δ")
bl_sketch("fig_3.png", "Laminar, transition, and turbulent regions along a flat plate", turbulent=True)
bl_sketch("fig_6.png", "Thermal boundary layer: T = Ts at the wall, T → T∞ at δt", thermal=True)
bl_sketch("fig_7.png", "Species concentration boundary layer, by analogy", conc=True)
fig, ax = plt.subplots(figsize=(5.5, 3.6)); ys = np.linspace(0, 1, 100)
ax.plot(1 - (1 - ys) ** 2, ys, color=BLUE, lw=2, label="laminar"); ax.plot(ys ** (1 / 7), ys, color=ORANGE, lw=2, label="turbulent (1/7 power law)")
ax.set_xlabel("u / u∞"); ax.set_ylabel("y / δ"); ax.legend(frameon=False); ax.grid(alpha=.3); ax.set_title("Turbulent profiles are fuller: larger gradient at the wall")
save(fig, "fig_4.png")
fig, ax = plt.subplots(figsize=(6, 3.4)); xs = np.linspace(0.02, 1, 200)
ax.plot(xs, xs ** -.5, color=ORANGE, lw=2, label=r"local $h_x \propto x^{-1/2}$"); ax.plot(xs, 2 * xs ** -.5, color=BLUE, lw=2, label=r"average $\bar h_x = 2 h_x$")
ax.set_ylim(0, 8); ax.set_xlabel("x"); ax.set_ylabel("h"); ax.legend(frameon=False); ax.grid(alpha=.3); ax.set_title("Local and average heat transfer coefficients (laminar plate)")
save(fig, "fig_8.png")
fig, ax = plt.subplots(figsize=(5, 3)); blank(ax, (-0.5, 6), (-0.4, 2.6)); wall(ax, 0, 5.5); bl_edge(ax, 0, 5.5, 0, 1.6)
arrow(ax, (2.5, 0.8), (4.3, 0.8), color=BLUE); ax.text(4.4, 0.7, "u", color=BLUE); arrow(ax, (2.5, 0.8), (2.5, 1.3), color=ORANGE); ax.text(2.6, 1.3, "v ≪ u", color=ORANGE)
ax.set_title("Inside the layer: v ≪ u, ∂/∂y ≫ ∂/∂x", fontsize=10); save(fig, "fig_9.png")

# integral_method: control volume in the boundary layer
fig, ax = plt.subplots(figsize=(6, 3.6)); blank(ax, (-0.5, 8), (-0.4, 3.4)); wall(ax, 0, 7.5); bl_edge(ax, 0, 7.5, 0, 2.0)
ax.add_patch(Rectangle((3, 0), 1.2, 2.6, fc="#eef3fb", ec=INK, lw=1.5)); ax.text(3.6, 2.8, "h ≥ δ", ha="center", fontsize=9)
ax.text(3.0, -0.35, "x", fontsize=9); ax.text(4.1, -0.35, "x + dx", fontsize=9)
profile(ax, 3.0, 1.5, n=5, u=0.9); arrow(ax, (4.2, 2.3), (5.2, 2.3), color=BLUE); ax.text(5.3, 2.2, "u∞", color=BLUE)
arrow(ax, (3.6, 2.6), (3.6, 3.2), color=ORANGE); ax.text(3.7, 3.0, "mass out the top", fontsize=8, color=ORANGE)
ax.text(3.6, -0.0, "τw", ha="center", va="top", fontsize=9, color=ORANGE)
ax.set_title("Control volume for the momentum integral equation", fontsize=10); save(fig, "integral_method.png")

# super_position_themal_BL and unheated_source
for name, title in [("super_position_themal_BL.png", "Superposition: a heated strip starting at ξ adds its own thermal layer"), ("unheated_source.png", "Unheated starting length ξ: the velocity layer starts at 0, the thermal layer at ξ")]:
    fig, ax = plt.subplots(figsize=(6.5, 3.2)); blank(ax, (-0.5, 8.5), (-0.5, 3)); wall(ax, 0, 8)
    ax.add_patch(Rectangle((3, -0.15), 5, 0.15, fc=ORANGE, ec=INK)); ax.text(5.5, -0.45, "heated: Ts", ha="center", fontsize=9, color=ORANGE); ax.text(1.5, -0.45, "unheated: T∞", ha="center", fontsize=9)
    bl_edge(ax, 0, 8, 0, 2.4); xs = np.linspace(3, 8, 80); ax.plot(xs, 1.3 * ((xs - 3) / 5) ** 0.5, "--", color=ORANGE, lw=1.4)
    ax.text(6.8, 2.6, "δ", fontsize=10); ax.text(7.2, 1.0, "δt", fontsize=10, color=ORANGE); ax.text(2.95, -0.85, "ξ", ha="center", fontsize=10)
    for y in np.linspace(0.5, 2.5, 4): arrow(ax, (-0.5, y), (0.1, y), color=BLUE)
    ax.set_title(title, fontsize=10); save(fig, name)

# wedge
fig, ax = plt.subplots(figsize=(6, 3.4)); blank(ax, (-1, 7), (-2.6, 2.6))
ax.add_patch(Polygon([[0, 0], [6, 1.8], [6, -1.8]], fc="#d9c9a8", ec=INK, lw=1.5)); ax.add_patch(Arc((0, 0), 2.2, 2.2, theta1=-16.7, theta2=16.7, color=ORANGE, lw=1.5)); ax.text(1.3, 0, "βπ", color=ORANGE, va="center")
for y in np.linspace(-2, 2, 5): arrow(ax, (-1, y), (-0.2, y), color=BLUE)
xs = np.linspace(0, 6, 60); ax.plot(xs, 0.3 * xs + 0.9 * (xs / 6) ** .5, "--", color=INK, lw=1.2); ax.plot(xs, -0.3 * xs - 0.9 * (xs / 6) ** .5, "--", color=INK, lw=1.2)
ax.text(4.2, 2.35, "boundary layer", fontsize=9); ax.text(-1, 2.35, "u∞", color=BLUE)
ax.set_title("Flow over a wedge: outer flow accelerates as u∞(x) ∝ xᵐ, m = β/(2 − β)", fontsize=10); save(fig, "wedge.png")

# flow_over_cylinder and flow_pattern
fig, ax = plt.subplots(figsize=(6, 3.6)); blank(ax, (-3, 4.5), (-2.4, 2.4)); ax.add_patch(Circle((0, 0), 1, fc="#c9d3de", ec=INK, lw=1.5))
th_ = np.linspace(0, np.pi, 100); ax.plot(1.25 * np.cos(th_), 1.25 * np.sin(th_), "--", color=INK, lw=1); ax.plot(1.25 * np.cos(th_), -1.25 * np.sin(th_), "--", color=INK, lw=1)
for y in np.linspace(-2, 2, 5): arrow(ax, (-3, y), (-2.2, y), color=BLUE)
ax.plot([np.cos(np.radians(100)), 3.5], [np.sin(np.radians(100)), 1.9], color=GRAY, lw=1, ls=":"); ax.plot([np.cos(np.radians(-100)), 3.5], [np.sin(np.radians(-100)), -1.9], color=GRAY, lw=1, ls=":")
ax.text(1.4, 0, "wake", fontsize=10); ax.text(-1.9, 0.15, "stagnation\nθ = 0", fontsize=8, ha="right"); ax.text(0.2, 1.45, "separation\nθ ≈ 80°", fontsize=8)
ax.text(-1.5, -2.3, "favorable dp/dx", fontsize=8, color=GREEN); ax.text(0.6, -2.3, "adverse dp/dx", fontsize=8, color=ORANGE)
ax.set_title("Boundary layer around a cylinder: growth, separation, wake", fontsize=10); save(fig, "flow_over_cylinder.png")
fig, axs = plt.subplots(1, 4, figsize=(10, 2.6))
for a, (t, wake) in zip(axs, [("Re < 5: creeping", 0), ("5–40: attached eddies", 1), ("40–200: Kármán street", 2), ("> 200: turbulent wake", 3)]):
    blank(a, (-1.8, 4), (-1.6, 1.6)); a.add_patch(Circle((0, 0), .6, fc="#c9d3de", ec=INK))
    if wake == 0:
        for y in (-1, -.5, .5, 1): xs = np.linspace(-1.8, 4, 60); a.plot(xs, y + 0.4 * np.sign(y) * np.exp(-xs ** 2 / .8) * (abs(y) < 1.2), color=BLUE, lw=1)
    elif wake == 1: a.add_patch(Circle((1.1, .35), .3, fc="none", ec=BLUE)); a.add_patch(Circle((1.1, -.35), .3, fc="none", ec=BLUE))
    elif wake == 2:
        for k in range(4): a.add_patch(Circle((1 + .8 * k, .45 * (-1) ** k), .28, fc="none", ec=BLUE))
    else:
        xs = np.linspace(.7, 4, 200); a.plot(xs, .5 * np.sin(6 * xs) * np.exp(-.1 * xs) + .3 * np.sin(17 * xs), color=BLUE, lw=.9)
    a.set_title(t, fontsize=8)
fig.suptitle("Flow regimes past a cylinder with increasing Reynolds number (schematic)", fontsize=10); save(fig, "flow_pattern.png")

# internal flow: velocity and thermal layer development, control volume, summary
for name, title, lab in [("velocity_BL_in_pipe.png", "Hydrodynamic development in a tube: layers merge into fully developed flow", "δ"), ("thermal_BL_in_pipe.png", "Thermal development in a tube: the thermal layers merge at x_fd,t", "δt")]:
    fig, ax = plt.subplots(figsize=(7, 3)); blank(ax, (-0.5, 9), (-1.6, 1.8)); ax.add_patch(Rectangle((0, -1), 8.5, 2, fc="#f4f7fb", ec=INK, lw=1.5))
    xs = np.linspace(0, 5, 80); ax.plot(xs, 1 - (xs / 5) ** .6, "--", color=ORANGE if lab == "δt" else INK); ax.plot(xs, -1 + (xs / 5) ** .6, "--", color=ORANGE if lab == "δt" else INK)
    for y in np.linspace(-.8, .8, 5): arrow(ax, (-0.5, y), (0.1, y), color=BLUE)
    ax.text(5.2, 1.15, "fully developed →", fontsize=9); ax.text(1.5, 1.15, f"{lab}(x) growing", fontsize=9); ax.text(4.9, -1.5, "x_fd", fontsize=9)
    ax.set_title(title, fontsize=10); save(fig, name)
fig, ax = plt.subplots(figsize=(6, 3)); blank(ax, (-0.5, 7), (-1.8, 2)); ax.add_patch(Rectangle((0, -1), 6.5, 2, fc="#f4f7fb", ec=INK, lw=1.5)); ax.add_patch(Rectangle((2.5, -1), 1.2, 2, fc="#eef3fb", ec=INK, lw=1.5))
arrow(ax, (1.3, 0), (2.4, 0), color=BLUE); ax.text(1.0, .25, r"$\dot m c_p T_m$", fontsize=9, color=BLUE); arrow(ax, (3.8, 0), (4.9, 0), color=BLUE); ax.text(3.9, .25, r"$\dot m c_p (T_m + dT_m)$", fontsize=9, color=BLUE)
arrow(ax, (3.1, 1.6), (3.1, 1.05), color=ORANGE); ax.text(3.2, 1.45, r"$q''_s\, P\, dx$", fontsize=9, color=ORANGE); ax.text(3.1, -1.4, "dx", ha="center", fontsize=9)
ax.set_title("Energy balance on a slice of the tube flow", fontsize=10); save(fig, "control_volume_pipe.png")
fig, ax = plt.subplots(figsize=(7, 3.2)); ax.axis("off")
rows = [["Condition", "Tₘ(x)", "h in the developed region", "Nu (laminar, developed)"],
        ["constant q″s", "linear in x", "constant; Ts − Tm constant", "4.36"],
        ["constant Ts", "exponential approach to Ts", "constant; Ts − Tm decays", "3.66"]]
t = ax.table(cellText=rows[1:], colLabels=rows[0], loc="center", cellLoc="center"); t.auto_set_font_size(False); t.set_fontsize(9); t.scale(1, 1.6)
ax.set_title("Internal flow summary", fontsize=10); save(fig, "internal_heat_flow_summary.png")

# natural convection sketches
fig, ax = plt.subplots(figsize=(3.6, 4)); blank(ax, (-0.5, 3.5), (-0.3, 5)); ax.add_patch(Rectangle((0, 0), 0.25, 4.6, fc=ORANGE, ec=INK)); ax.text(0.12, 4.75, "Ts > T∞", ha="center", fontsize=9, color=ORANGE)
ys = np.linspace(0, 4.6, 80); ax.plot(0.25 + 1.6 * (ys / 4.6) ** .25, ys, "--", color=INK); ax.text(1.9, 4.2, "δ(x)", fontsize=9)
for y in (1, 2.4, 3.8): arrow(ax, (0.5, y), (0.5, y + .55), color=BLUE); ax.text(2.4, 2.2, "buoyant\nflow", fontsize=9, color=BLUE); arrow(ax, (3.0, 1.4), (3.0, 0.4), color=GRAY); ax.text(3.05, 0.5, "g", fontsize=9)
ax.set_title("Natural convection on a\nvertical hot plate", fontsize=10); save(fig, "natural_convection.png")
fig, axs = plt.subplots(1, 4, figsize=(10, 2.8))
for a, (t, kind) in zip(axs, [("vertical plate", "v"), ("hot face up", "u"), ("hot face down", "d"), ("enclosure", "e")]):
    blank(a, (-1.5, 1.5), (-1.5, 1.5))
    if kind == "v": a.add_patch(Rectangle((-0.1, -1.2), .2, 2.4, fc=ORANGE, ec=INK)); [arrow(a, (.4, y), (.4, y + .5), color=BLUE) for y in (-1, 0, .8)]
    if kind == "u": a.add_patch(Rectangle((-1.2, -0.1), 2.4, .2, fc=ORANGE, ec=INK)); [arrow(a, (x_, .2), (x_, .9), color=BLUE) for x_ in (-.7, 0, .7)]
    if kind == "d": a.add_patch(Rectangle((-1.2, -0.1), 2.4, .2, fc=ORANGE, ec=INK)); arrow(a, (-.3, -.3), (-1.2, -.3), color=BLUE); arrow(a, (.3, -.3), (1.2, -.3), color=BLUE); a.text(0, -1, "stable, weak flow", ha="center", fontsize=8)
    if kind == "e": a.add_patch(Rectangle((-1, -1), 2, 2, fc="none", ec=INK, lw=1.5)); a.plot([-1, -1], [-1, 1], color=ORANGE, lw=4); a.plot([1, 1], [-1, 1], color=BLUE, lw=4); [arrow(a, p, q, color=GRAY) for p, q in [((-.6, -.6), (-.6, .6)), ((.6, .6), (.6, -.6)), ((-.5, .8), (.5, .8)), ((.5, -.8), (-.5, -.8))]]
    a.set_title(t, fontsize=9)
fig.suptitle("Natural convection configurations: the geometry sets the correlation", fontsize=10); save(fig, "natural_convection_big_picture.png")
print("done")
