# Intermediate Heat Transfer

Lecture notes on **convection** and **thermal radiation**, written while
teaching myself the subject properly, from several textbooks, in one
consistent notation. They are organized the way a course is: part by part,
lecture by lecture, with the definitions and key results set off in boxes.

<div class="grid cards" markdown>

-   **Part I · Conduction**

    ---

    Fourier's law and the heat equation, boundary conditions, thermal
    resistances, fins, lumped capacitance, exact transient solutions, and
    a finite-difference solver in a few lines of Python.

    [:octicons-arrow-right-24: Open Part I](conduction/index.md)

-   **Part II · Convection**

    ---

    Boundary layers, the energy equation, similarity and integral
    solutions, external and internal flow correlations, natural
    convection, and boiling.

    [:octicons-arrow-right-24: Open Part II](convection/index.md)

-   **Part III · Thermal Radiation**

    ---

    Blackbody radiation, real surfaces, view factors, radiation
    exchange between surfaces, and the network method.

    [:octicons-arrow-right-24: Open Part III](radiation/index.md)

</div>

!!! tip "How to use these notes"
    Open a part in the sidebar to see its chapters; open a chapter and its
    sections appear beneath it, so you can jump without scrolling.
    Boxes marked **Definition** hold the results worth remembering.
    Search (top right) works across all lectures.

!!! note "About the figures and code"
    Every figure in these notes is original: the plots are computed from the
    equations in the text by the Python scripts kept next to the notes
    (`make_figures.py` in each part), and the schematics are drawn by the same
    scripts. Where code is shown in the text, it is the code that made the
    figure, so you can run and change it.

*Written by Aiden Azarnoush.*

---

*Dedicated to my beloved mother, Simin Nematpour.*
