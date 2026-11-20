import networkx as nx
from core.database import db

def find_attack_paths(source_ip: str, target_ip: str):
    """
    Finds all simple paths between a source asset and a target asset using the In-Memory NetworkX graph.
    """
    G = db.G
    
    if source_ip not in G or target_ip not in G:
        return []
        
    # Make undirected for simple reachability
    UG = G.to_undirected()
    
    paths = []
    try:
        # Find shortest paths
        nx_paths = nx.shortest_simple_paths(UG, source=source_ip, target=target_ip)
        
        # Retrieve up to 5 paths
        for _ in range(5):
            try:
                path = next(nx_paths)
                
                # Calculate Risk Score
                risk_score = 0
                for node in path:
                    node_data = G.nodes.get(node, {})
                    if node_data.get('type') == 'Vulnerability':
                        risk_score += float(node_data.get('cvss', 0.0))
                        
                paths.append({
                    "path": path,
                    "risk_score": risk_score,
                    "length": len(path)
                })
            except StopIteration:
                break
    except nx.NetworkXNoPath:
        pass
        
    # Sort paths by risk score descending
    paths.sort(key=lambda x: x['risk_score'], reverse=True)
    return paths
