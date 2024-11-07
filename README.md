# Applied Data Structures and Algorithms (ADSA) Framework

## Overview
The **Applied Data Structures and Algorithms (ADSA)** framework is a Python-based toolkit designed for creating, analyzing, manipulating, and visualizing data structures. This modular framework allows users to load, modify, and plot data structures such as graphs, trees, and networks, with support for machine learning and deep learning applications. Built on a variety of Python libraries, ADSA is tailored to handle both general data structure manipulations and complex tasks like graph neural network analysis.

## Framework Structure
The framework is organized as follows:

```
class/
├── fall_22 --- USC Class: csci_570_analysis_of_algorithms
├── summer_and_fall_23 --- USC Class: csci_570_analysis_of_algorithms
├── fall_24 --- UF Class: cop_5536_advanced_data_structures
├── leetcode_dynamic_programming
framework/
├── algorithms.py
├── data_loader.py
├── data_plotter.py
├── data_structures.py
└── neural_networks.py
```

### Modules

1. **`algorithms.py`**  
   - **Purpose**: Implements algorithms for manipulating data structures.
   - **Details**: This module focuses on operations that can be performed on any data structure, such as `insert`, `delete`, `search`, and `traversal`. 
   - **Dependencies**: Primarily based on **NetworkX** for graph algorithms and **NumPy** for efficient computations.

2. **`data_loader.py`**  
   - **Purpose**: Provides functionality for loading and importing data into various data structures.
   - **Details**: Supports loading from different file types (CSV, JSON, etc.) and sources (databases, APIs). Includes built-in sample data for quick experimentation.
   - **Dependencies**: Uses **pandas** for tabular data handling and pure Python functions for general loading purposes.

3. **`data_plotter.py`**  
   - **Purpose**: Visualizes data structures and outputs from machine learning models.
   - **Details**: Focuses on plotting and visualizing both static and dynamic structures. Provides graphical representations of graphs, neural network outputs, and other data structure results.
   - **Dependencies**: Based on **matplotlib** for visualization, along with **seaborn** for enhanced plotting capabilities.

4. **`data_structures.py`**  
   - **Purpose**: Defines and manipulates various data structures.
   - **Details**: Includes functions to create and manipulate specific structures like graphs, trees, and heaps, often leveraging custom implementations to work with structures loaded through `data_loader.py`.
   - **Dependencies**: Primarily pure Python; optionally integrates with **graph-tool** and **Graph for Scala** for specialized structures.

5. **`neural_networks.py`**  
   - **Purpose**: Applies machine learning and deep learning techniques to graph data.
   - **Details**: Implements neural network models, especially Graph Neural Networks, to analyze relationships within graph structures.
   - **Dependencies**: Relies on **PyG (PyTorch Geometric)** for deep learning on graphs, and **DGL (Deep Graph Library)** as an optional addition.

## Required Libraries
This framework leverages several popular libraries to provide robust functionality and visualization options. Below are the primary libraries and their uses:

- **NetworkX**: Essential for graph manipulation and algorithmic support (shortest path, clustering, centrality measures). NetworkX provides an intuitive Python interface for building and analyzing graph structures.
  
- **PyG (PyTorch Geometric)**: Used for deep learning applications on graph data. PyG provides a suite of tools to implement and train Graph Neural Networks (GNNs) and supports large-scale graph learning.

- **matplotlib**: Core library for visualizing data structures and algorithmic results. Useful for plotting graphs, neural network outputs, and other structural representations.
  
- **pandas**: Simplifies the data loading process by allowing structured data to be easily manipulated and prepared for analysis or visualization.

- **graph-tool**: An efficient library for handling and analyzing large graphs. Particularly useful for network science applications where performance is critical.

- **GraphStream (Java)**: Enables dynamic graph visualization, making it useful for real-time network analysis. Often employed alongside NetworkX for static processing and GraphStream for dynamic visualization.

- **DGL (Deep Graph Library)**: An alternative to PyG, offering additional tools for graph-based deep learning. Its architecture allows for modular experimentation with different GNN layers and models.

- **SNAP for Python (Snap.py)**: Suitable for social network analysis and large-scale network algorithms. Optimized for performance in handling massive networks.

- **Elastic X-Pack Graph**: Offers advanced graph analytics in the context of Elasticsearch. Useful for users interested in integrating their analysis with Elasticsearch for indexing and querying capabilities.

### Optional Libraries
For more specific or advanced use cases, the following libraries are also compatible with ADSA:

- **Graph for Scala**: Ideal for Scala users looking to integrate with Python workflows. It provides tools to handle complex graph structures and high-performance algorithms.
  
- **Blitz Introduction to DGL**: Aimed at newcomers to the Deep Graph Library, offering tutorials and basic implementations to help users understand the library’s applications.

## Usage Examples
1. **Algorithms**: `algorithms.py` allows users to perform standard operations like insertion, deletion, and searching within various data structures, using NetworkX for efficient graph handling.
   
2. **Loading Data**: `data_loader.py` can be used to load graphs from CSV files and perform initial data cleaning using pandas.

3. **Visualization**: `data_plotter.py` provides a function to visualize clustering coefficients of nodes in a graph structure, using matplotlib for plotting.

4. **Machine Learning on Graphs**: `neural_networks.py` lets users run GNN models on graph structures to analyze patterns and predict relationships.

This framework aims to be an all-in-one toolkit for those working in applied data structures and algorithmic analysis, making it ideal for both academic research and industrial applications. We encourage users to contribute to the project by adding more algorithms, enhancing documentation, and creating new applications.
```
