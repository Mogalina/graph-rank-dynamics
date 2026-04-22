import sys
import os
import csv
import numpy as np

def load_graph_from_file(file_path) -> tuple[int, list[list[int]], np.ndarray, np.ndarray]:
    raw_edges: list[tuple[int, int]] = []
    maximum_node_id: int = 0
    
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return None, None, None, None
    
    with open(file_path, 'r') as graph_file:
        for line_content in graph_file:
            clean_line: str = line_content.strip()
            if not clean_line or clean_line.startswith('#'):
                continue
                
            try:
                parts: list[str] = clean_line.split()
                if len(parts) >= 2:
                    source_id: int = int(parts[0])
                    target_id: int = int(parts[1])
                    raw_edges.append((source_id, target_id))
                    maximum_node_id = max(maximum_node_id, source_id, target_id)
            except ValueError:
                continue
    
    total_nodes: int = maximum_node_id + 1
    graph_adjacency_list: list[list[int]] = [[] for _ in range(total_nodes)]
    in_degrees: np.ndarray = np.zeros(total_nodes, dtype=int)
    out_degrees: np.ndarray = np.zeros(total_nodes, dtype=int)
    
    for source, target in raw_edges:
        graph_adjacency_list[source].append(target)
        out_degrees[source] += 1
        in_degrees[target] += 1
        
    return total_nodes, graph_adjacency_list, in_degrees, out_degrees

def calculate_pagerank_scores(
    total_nodes: int, 
    adjacency_list: list[list[int]], 
    outbound_link_counts: np.ndarray,
    damping_factor: float = 0.85, 
    max_iterations: int = 100, 
    convergence_tolerance: float = 1e-4
) -> np.ndarray:
    if total_nodes == 0:
        return np.array([])
    
    current_iteration_ranks: np.ndarray = np.ones(total_nodes) / total_nodes
    
    for cycle_index in range(max_iterations):
        updated_ranks: np.ndarray = np.zeros(total_nodes)
        dangling_node_rank_total: float = np.sum(current_iteration_ranks[outbound_link_counts == 0])
        
        for source_node in range(total_nodes):
            if outbound_link_counts[source_node] > 0:
                rank_contribution: float = current_iteration_ranks[source_node] / outbound_link_counts[source_node]
                for target_node in adjacency_list[source_node]:
                    updated_ranks[target_node] += rank_contribution

        jump_constant: float = (1.0 - damping_factor) / total_nodes
        leakage_term: float = (damping_factor * dangling_node_rank_total) / total_nodes
        
        final_iteration_ranks: np.ndarray = jump_constant + (damping_factor * updated_ranks) + leakage_term
        
        if np.sum(np.abs(final_iteration_ranks - current_iteration_ranks)) < convergence_tolerance:
            break
        
        current_iteration_ranks = final_iteration_ranks
        
    return current_iteration_ranks

def save_pagerank_to_csv(
    scores: np.ndarray, 
    in_degrees: np.ndarray, 
    out_degrees: np.ndarray, 
    output_filename: str = "results.csv"
) -> None:
    if scores.size == 0:
        print("No results to save.")
        return

    sorted_node_indices: np.ndarray = np.argsort(scores)[::-1]
    
    try:
        with open(output_filename, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            
            csv_writer.writerow([
                'rank', 'node_id', 'pagerank_score', 'contribution_percentage', 
                'incoming_links', 'outgoing_links', 'total_links'
            ])
            
            for rank_pos, node_id in enumerate(sorted_node_indices):
                score_value: float = scores[node_id]
                percentage_str: str = f"{score_value * 100:.3f}%"
                
                in_deg = int(in_degrees[node_id])
                out_deg = int(out_degrees[node_id])
                
                csv_writer.writerow([
                    rank_pos + 1, 
                    node_id, 
                    f"{score_value:.8f}", 
                    percentage_str,
                    in_deg,
                    out_deg,
                    in_deg + out_deg
                ])
                
        print(f"Results successfully exported to: {output_filename}")
        
    except IOError as e:
        print(f"Error: Could not write results to file. {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pagerank.py <filename>")
        sys.exit(1)
    
    total_node_count, adjacency_map, in_deg_arr, out_deg_arr = load_graph_from_file(sys.argv[1])
    
    if total_node_count is not None:
        final_pagerank_results: np.ndarray = calculate_pagerank_scores(
            total_node_count, 
            adjacency_map, 
            out_deg_arr
        )
        
        save_pagerank_to_csv(final_pagerank_results, in_deg_arr, out_deg_arr)
