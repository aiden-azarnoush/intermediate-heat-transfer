# Applications and Advanced Topics

## The "Seat Belt Buckle Syndrome"

An interesting practical example of radiation heat transfer is the "seat belt buckle syndrome" where metal seat belt buckles in cars can become uncomfortable or even painful to touch on hot days, even though fabric parts at the same temperature do not cause discomfort.

This phenomenon involves multiple heat transfer mechanisms:

1.  **Greenhouse effect in the car:** Solar radiation enters through windows (glass transmits approximately 95% of visible light) but thermal radiation (5-12 $\mu$m) from heated surfaces cannot escape easily, causing the cabin to heat up.

2.  **Spectral properties of metal buckles:** While metal buckles appear reflective to the human eye, the nickel coating on seat belt buckles:

    -   Reflects blue light significantly

    -   Reflects some portion of red light

    -   Absorbs most of the green light

    -   Has high absorption in the infrared range

    -   Has very low emissivity in the thermal wavelengths

3.  **Material properties affecting heat transfer:**

    -   The metal buckle has high thermal diffusivity, making it difficult to cool by touch

    -   Fabric has low thermal diffusivity, so when touched, the surface cools quickly

    -   Human skin has heat flux sensors (not temperature sensors), so we perceive high heat flux as "hot"

    -   Metal requires removing significant heat to cool down, creating a high heat flux into skin

This example illustrates how spectral properties, material characteristics, and biological factors all contribute to a common thermal experience.

## Thermal vs. Non-Thermal Radiation

There is an important distinction between thermal and non-thermal radiation:

-   **Thermal radiation** follows the Planck distribution, with:

    -   Maximum achievable temperature limited to the source temperature

    -   Maximum efficiency limited by the Carnot efficiency $\eta = 1 - \frac{T_{low}}{T_{high}}$

    -   Examples: solar radiation, incandescent bulbs, heated objects

-   **Non-thermal radiation** has properties different from thermal equilibrium distribution:

    -   Can achieve much higher intensities and temperatures

    -   Examples: lasers, LEDs, fluorescent lights

    -   Not bound by the same thermodynamic limitations as thermal radiation

## Spectral Considerations in Radiation Analysis

While the radiation network method assumes gray surfaces, in reality:

-   For wavelength-dependent properties (non-gray surfaces):

    -   The network analysis can be performed separately for each wavelength

    -   Results can be integrated over all wavelengths

    -   This preserves the geometry (view factors) but accounts for spectral variations

-   For directional-dependent properties (non-diffuse surfaces):

    -   The radiation network analysis breaks down

    -   Alternative methods like Monte Carlo or ray-tracing are required

### Monte Carlo Methods

For complex radiation problems, Monte Carlo simulation offers a statistical approach:

-   Tracks the paths of simulated photon bundles

-   At each surface interaction, random numbers determine:

    -   Whether the photon is absorbed or reflected

    -   Direction of reflection (for diffuse surfaces)

-   After tracking millions of photons, statistical results provide radiation distribution

-   Particularly useful for non-diffuse surfaces or participating media

## Radiative Transfer Equation (RTE)

The radiative transfer equation (RTE) is the fundamental governing equation for radiation in participating media (like gases or combustion products):

-   Accounts for absorption, emission, and scattering within the medium

-   Combines differential and integral terms

-   Much more complex than the radiation network approach

-   Will be covered in more detail in future lectures

$$
\begin{gathered}
    \frac{d I}{d s}+\left(\alpha+\sigma_s\right) I=\alpha n^2 \frac{\sigma T_g^4}{\pi}+\frac{\sigma_s}{4 \pi} \int_0^{4 \pi} I\left(\Omega^{\prime}\right) \Phi\left(\Omega, \Omega^{\prime}\right) d \Omega^{\prime} \\
    I=I(\vec{r}, \vec{s}) \quad I\left(\Omega^{\prime}\right)=I\left(\overrightarrow{\mathbf{r}}, \vec{S}^{\prime}\right)
    \end{gathered}
$$

 where,

-   $\vec{r}=$ Position vector $\quad \vec{S}=$ direction vector

-   $n=$ refractive index

-   $\sigma_S=$ scattering coefficient

-   $\Phi=$ phase function (determines isotropic/arisotropic scattering)

-   $\Omega=$ solid angle

## Thermal Energy Equation for Participating Medium

$$
\rho C_p \frac{\partial T_g}{\partial t}+\vec{\nabla} \cdot\left(\rho c_p \vec{u} T_g\right)=\vec{\nabla} \cdot\left(\overrightarrow{\vec{k}} \vec{\nabla} T_g\right)+\iint_{4 \pi} \alpha\left(I-n^2 \frac{\sigma T_g^4}{\pi}\right) d \Omega
$$

 where $I(\vec{r}, \vec{S})$ needs to be solved from RTE.

Note:

-   These equations typically solved numerically.

-   We assumed gases/media are gray, ie., $\alpha$ is independent of $\lambda$.

-   We did not include source terms for non-thermal radiations.

## Knudsen Number and Continuum Approximation

The Knudsen number ($\operatorname{K_n}$) determines when continuum approximations are valid:

$$
\operatorname{K_n} = \frac{\text{mean free path}}{\text{characteristic length}}
$$

For radiation transport:

-   $\operatorname{K_n} < 0.01$: Continuum models valid (Navier-Stokes, HDE, RTE)

-   $0.01 < \operatorname{K_n} < 0.1$: Continuum models with corrections such as slip BC, ballistic-diffusive model

-   $0.1 < \operatorname{K_n} < 10$: Boltzmann Transport Equation (BTE) required

-   $\operatorname{K_n} > 10$: Particle-based models (ray tracing, photon transport) i.e., collision less BTE

The Boltzmann Transport Equation (BTE) becomes necessary when the mean free path is comparable to the problem dimensions, requiring statistical treatment of particle transport.

## The Boltzmann Transport Equation (BTE)

$$
\begin{aligned}
    & \frac{\partial f}{\partial t}=\left(\frac{\partial f}{\partial t}\right)_{\text {force }}+\left(\frac{\partial f}{\partial t}\right)_{\text {diffluison }}+\left(\frac{\partial f}{\partial t}\right)_{\text {sattering }} 
    \\[1em]
    & \frac{\partial f}{\partial t}+\vec{v} \cdot \vec{\nabla} f+\vec{a} \frac{\partial f}{\partial \vec{v}}=\left(\frac{\partial f}{\partial t}\right)_{\text {scattering }} 
    \\[1em]
    & \text { where }\left(\frac{\partial f}{\partial t}\right)_{\text {scatterina }}=\iint\left[\iint(\ldots . .) d_{p_A}^3 d_B^3\right] d \Omega \qquad {\text{Full BTE}}
    \\[1em]
    & \qquad \qquad \left(\frac{\partial f}{\partial t}\right)_{\text {scatterina }} \cong \nu\left(f_0-f\right) \qquad \text { gray BTE} 
    \end{aligned}
$$
