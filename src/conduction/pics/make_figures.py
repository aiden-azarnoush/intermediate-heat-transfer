"""Figures for Part I (conduction). All computed; run: python make_figures.py"""
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})

# 1. plane wall with uniform generation: T(x) parabola, and the linear case
L, k, q = 0.05, 20.0, 2e5; T1, T2 = 100, 40
x = np.linspace(0, L, 200)
Tlin = T1 + (T2 - T1) * x / L
Tgen = Tlin + q / (2 * k) * x * (L - x)
fig, ax = plt.subplots(figsize=(6, 3.6))
ax.plot(x * 1e3, Tlin, "--", color="#66768a", label="no generation: linear")
ax.plot(x * 1e3, Tgen, color="#d3541f", lw=2, label=r"uniform generation $\dot q$: parabola")
ax.set_xlabel("x (mm)"); ax.set_ylabel("T (°C)"); ax.legend(frameon=False); ax.grid(alpha=.3)
ax.set_title("Steady conduction in a plane wall")
fig.tight_layout(); fig.savefig("plane_wall_generation.png", dpi=160); plt.close(fig)

# 2. fin: temperature along an adiabatic-tip fin for several mL, and efficiency vs mL
mL = np.array([0.5, 1, 2, 4]); xi = np.linspace(0, 1, 200)
fig, ax = plt.subplots(1, 2, figsize=(9, 3.6))
for v in mL:
    ax[0].plot(xi, np.cosh(v * (1 - xi)) / np.cosh(v), lw=2, label=f"mL = {v:g}")
ax[0].set_xlabel("x / L"); ax[0].set_ylabel(r"$\theta/\theta_b = (T-T_\infty)/(T_b-T_\infty)$"); ax[0].legend(frameon=False); ax[0].grid(alpha=.3)
ax[0].set_title("Temperature along a fin (adiabatic tip)")
v = np.linspace(0.01, 5, 300); ax[1].plot(v, np.tanh(v) / v, color="#d3541f", lw=2)
ax[1].set_xlabel("mL"); ax[1].set_ylabel(r"fin efficiency $\eta_f = \tanh(mL)/mL$"); ax[1].grid(alpha=.3); ax[1].set_ylim(0, 1.05)
ax[1].set_title("Longer fins give diminishing returns")
fig.tight_layout(); fig.savefig("fin.png", dpi=160); plt.close(fig)

# 3. lumped capacitance vs. the exact one-term plane-wall solution (centre temperature), several Bi
def zeta1(Bi):
    from scipy.optimize import brentq
    return brentq(lambda z: z * np.tan(z) - Bi, 1e-6, np.pi / 2 - 1e-6)
Fo = np.linspace(0, 3, 300)
fig, ax = plt.subplots(figsize=(6, 3.6))
for Bi, c in [(0.05, "#2a9d5c"), (0.5, "#1f5fbf"), (5, "#d3541f")]:
    z = zeta1(Bi); C1 = 4 * np.sin(z) / (2 * z + np.sin(2 * z))
    ax.plot(Fo, C1 * np.exp(-z * z * Fo), color=c, lw=2, label=f"exact, Bi = {Bi:g}")
    ax.plot(Fo, np.exp(-Bi * Fo), ":", color=c, lw=1.8, label=f"lumped, Bi = {Bi:g}")
ax.set_xlabel(r"Fourier number Fo = $\alpha t / L^2$"); ax.set_ylabel(r"$\theta_0/\theta_i$ (centre)"); ax.set_yscale("log"); ax.set_ylim(1e-3, 1.2)
ax.legend(frameon=False, ncol=2, fontsize=8); ax.grid(alpha=.3, which="both")
ax.set_title("Lumped capacitance is accurate only for small Biot number")
fig.tight_layout(); fig.savefig("lumped_vs_exact.png", dpi=160); plt.close(fig)

# 4. explicit finite-difference solution of 1D transient conduction (the code in the notes)
Lw, alpha, nx = 0.02, 1e-5, 41
dx = Lw / (nx - 1); dt = 0.4 * dx * dx / alpha; T = np.full(nx, 20.0); T[0] = T[-1] = 100.0
fig, ax = plt.subplots(figsize=(6, 3.6)); xs = np.linspace(0, Lw, nx) * 1e3
for n in range(0, 401):
    if n in (0, 25, 100, 400): ax.plot(xs, T, lw=2, label=f"t = {n * dt:.1f} s")
    T[1:-1] = T[1:-1] + alpha * dt / dx ** 2 * (T[2:] - 2 * T[1:-1] + T[:-2])
ax.set_xlabel("x (mm)"); ax.set_ylabel("T (°C)"); ax.legend(frameon=False); ax.grid(alpha=.3)
ax.set_title("Explicit finite differences: a slab heated from both faces")
fig.tight_layout(); fig.savefig("fd_transient.png", dpi=160); plt.close(fig)
print("figures written")
