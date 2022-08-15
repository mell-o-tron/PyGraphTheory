# PyGraphTheory
Collection of graph algorithms and visualizations

## Current features and usage
You can set the number of vertices you want your graph to have (in the code), and:
- Press `E` to add a random edge
- Press `Space` to randomize the position of the vertices (currently uses Poisson Disk Sampling)
- Press `B` (for "BFS") to find and highlight the connected components of the graph
- Press `R` to generate a random graph, where each edge is present with some probability *p*

## Feature ideas
- Add better rules for visualization, e.g. ~~minimum distance between the vertices~~ (done!!), don't let the distance between each edge $(v, w)$ and the vertices in $V \setminus \\{v, w\\}$ go below a certain distance
- Visualize the presence of cycles
- Coloring algorithms? 
- Planarity testing?
- Visualization of quotient graphs?
- Better suddivision of the code, which might eventually turn into a library or something.

## Preview

![](https://github.com/mell-o-tron/PyGraphTheory/blob/main/connected_components.png)

(Three connected components, colored to reflect their order (bluish if closer to 1, reddish if closer to $|V|$)) and their index (the green component), in order to make it easier to distinguish them)
