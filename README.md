# plotter_drawings

This is a collection of vector art generator scripts intended for use as the basis for pen plotter drawings, specifically on my AxiDraw V3/A3 though nothing in the code is particular to that machine.

The code makes use of the matplotlib library for drawing functions (while going out of its way to surpress most of the mathematical-plot-related chrome matplotlib provides), as well as vpype for post-processing the initial output into a more ready-to-draw form to feed to the pen plottter.

This is currently art code with a thin patina of software engineering on top; I'm hoping to significantly clean up the codebase on multiple fronts to reduce needless code repetition and better abstract the pure generative geometry of the scripts away from the specifics of matplotlib and any other crunchy dependencies, so the core code of any given script will be better adaptable to an arbitrary drawing context.
