# PageRank Importance Analysis

## Abstract
This project provides a robust, lightweight Python implementation of the **PageRank algorithm**, originally developed by Larry Page and Sergey Brin for ranking web pages. The script utilizes the **power iteration method** to calculate a probability distribution representing the likelihood that a person randomly clicking on links will arrive at any particular node. It handling complex graph structures, including "dangling nodes" (nodes with zero outbound links), through a stochastic redistribution mechanism.

## Motivation
Measuring the relative importance of elements within a networked system is a fundamental task in various fields, including search engine optimization (SEO), social network analysis, and bibliometrics. While many implementations exist, this tool aims to provide a transparent and extensible framework that combines core algorithmic logic with automated connectivity statistics, directly facilitating quantitative research and data analysis.

## Implementation Details
The algorithm computes the stationary distribution of a Markov chain using the following iterative formula:

$$
PR(v) = \frac{1-d}{N} + d \left( \sum_{u \in In(v)} \frac{PR(u)}{Out(u)} + \sum_{s \in Dangling} \frac{PR(s)}{N} \right)
$$

Where:
- $d$ is the **damping factor** (default: 0.85).
- $N$ is the total number of nodes in the graph.
- $PR(u)$ is the PageRank of node $u$.
- $Out(u)$ is the outbound degree of node $u$.

The script employs **NumPy** for optimized vector operations, ensuring scalability for medium-sized datasets.

## Usage
### Prerequisites
- Python 3.7+
- NumPy

### Execution
Provide a text file representing a directed graph where each line contains a source node and a target node separated by whitespace:
```bash
python pagerank.py <filename>
```

## Output Format
The results are exported to a structured `results.csv` file containing:
- **rank**: The ordinal position based on importance.
- **node_id**: The original identifier from the input file.
- **pagerank_score**: The normalized probability score.
- **contribution_percentage**: The percentage share of the total network importance.
- **incoming_links**: Count of edges pointing to the node.
- **outgoing_links**: Count of edges originating from the node.
- **total_links**: Combined link count (in + out).

---
*Created for node importance analysis and graph topology research.*
