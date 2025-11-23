# Visualization Module

Visualize knowledge graphs, embeddings, and analytics with interactive and static visualizations using multiple rendering engines.

## Overview

- **Graph Visualization**: Interactive and static knowledge graph rendering
- **Embedding Visualization**: t-SNE, UMAP, PCA for high-dimensional data
- **Analytics Visualization**: Charts, plots, and dashboards
- **Temporal Visualization**: Time-series and evolution visualization
- **Export Formats**: HTML, PNG, SVG, PDF

---

## Algorithms Used

### Dimensionality Reduction
- **t-SNE (t-Distributed Stochastic Neighbor Embedding)**: Non-linear dimensionality reduction, preserves local structure
- **UMAP (Uniform Manifold Approximation and Projection)**: Faster than t-SNE, preserves global + local structure
- **PCA (Principal Component Analysis)**: Linear dimensionality reduction, `X_reduced = X * eigenvectors`

### Graph Layout Algorithms
- **Force-Directed Layout**: Spring-electrical model with Fruchterman-Reingold algorithm
- **Hierarchical Layout**: Tree-based layout with Sugiyama framework
- **Circular Layout**: Nodes arranged in circle, edges minimize crossings
- **Kamada-Kawai**: Energy-based layout minimizing edge length variance

---

## Main Classes

### KGVisualizer


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `visualize(graph, output)` | Visualize knowledge graph | Force-directed layout with PyVis/Cytoscape |
| `render_interactive(graph)` | Interactive HTML visualization | D3.js/PyVis rendering |
| `render_static(graph, format)` | Static image rendering | Graphviz/Matplotlib rendering |
| `export(graph, filename, format)` | Export visualization | Format-specific export (HTML/PNG/SVG) |
| `customize_style(node_style, edge_style)` | Customize appearance | Style application |

**Supported Engines:**
- **PyVis**: Interactive HTML with physics simulation
- **Cytoscape.js**: Web-based graph visualization
- **Graphviz**: Static high-quality diagrams
- **Matplotlib**: Python-native plotting
- **Plotly**: Interactive web visualizations

**Example:**

```python
from semantica.visualization import KGVisualizer

visualizer = KGVisualizer(
    engine="pyvis",  # pyvis, cytoscape, graphviz, matplotlib
    layout="force_directed",  # force_directed, hierarchical, circular
    width="100%",
    height="800px"
)

# Interactive visualization
visualizer.visualize(
    graph=kg,
    output="graph.html",
    show_physics=True,
    node_color_by="type",
    edge_width_by="weight"
)

# Static visualization
visualizer.render_static(
    graph=kg,
    format="png",
    output="graph.png",
    dpi=300
)
```

---

### EmbeddingVisualizer


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `visualize(embeddings, method)` | Visualize embeddings | Dimensionality reduction + scatter plot |
| `plot_tsne(embeddings, perplexity)` | t-SNE visualization | t-SNE with configurable perplexity |
| `plot_umap(embeddings, n_neighbors)` | UMAP visualization | UMAP with neighbor parameter |
| `plot_pca(embeddings, n_components)` | PCA visualization | PCA to 2D/3D |
| `plot_clusters(embeddings, labels)` | Cluster visualization | Color-coded scatter plot |

**t-SNE Parameters:**
- `perplexity`: Balance between local and global structure (5-50)
- `learning_rate`: Step size (10-1000)
- `n_iter`: Number of iterations (250-1000)

**UMAP Parameters:**
- `n_neighbors`: Local neighborhood size (2-100)
- `min_dist`: Minimum distance between points (0.0-0.99)
- `metric`: Distance metric (euclidean, cosine, manhattan)

**Example:**

```python
from semantica.visualization import EmbeddingVisualizer

visualizer = EmbeddingVisualizer()

# t-SNE visualization
visualizer.plot_tsne(
    embeddings=embeddings,
    labels=labels,
    perplexity=30,
    output="tsne.html"
)

# UMAP visualization
visualizer.plot_umap(
    embeddings=embeddings,
    n_neighbors=15,
    min_dist=0.1,
    output="umap.html"
)
```

---

### AnalyticsVisualizer


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `plot_metrics(metrics)` | Plot graph metrics | Bar/line charts |
| `plot_distribution(data, bins)` | Plot distributions | Histogram generation |
| `plot_timeline(events, timeline)` | Plot temporal data | Time-series visualization |
| `create_dashboard(components)` | Create dashboard | Multi-panel layout |

---

## Configuration

```yaml
# config.yaml - Visualization Configuration

visualization:
  kg:
    engine: pyvis  # pyvis, cytoscape, graphviz, matplotlib
    layout: force_directed
    width: "100%"
    height: "800px"
    physics_enabled: true
    node_size_by: degree
    node_color_by: type
    edge_width_by: weight
    
  embeddings:
    method: umap  # tsne, umap, pca
    n_components: 2
    perplexity: 30  # for t-SNE
    n_neighbors: 15  # for UMAP
    
  export:
    format: html  # html, png, svg, pdf
    dpi: 300  # for raster formats
    transparent_background: false
```

---

## See Also

- [Knowledge Graph Module](kg.md)
- [Embeddings Module](embeddings.md)
- [Export Module](export.md)
