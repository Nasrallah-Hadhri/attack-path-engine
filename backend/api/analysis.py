from fastapi import APIRouter, HTTPException
from engine.vuln_matcher import match_vulnerabilities
from engine.attack_path import find_attack_paths
from ai.llm_analyst import generate_path_explanation

router = APIRouter()

@router.post("/match-vulns")
def trigger_vuln_matching():
    """
    Triggers the vulnerability matching engine to find CVEs for discovered services.
    """
    count = match_vulnerabilities()
    return {"message": f"Successfully matched and created {count} vulnerability relationships."}

@router.get("/graph")
def get_entire_graph():
    """
    Returns the entire in-memory graph to draw it on the frontend.
    """
    from core.database import db
    nodes = []
    edges = []
    for node, data in db.G.nodes(data=True):
        label = str(node)
        if data.get('type') == 'Vulnerability':
            label = data.get('cve_id')
        elif data.get('type') == 'Service':
            label = data.get('name')
        nodes.append({"id": node, "label": label, "group": data.get('type', 'Unknown')})
        
    for u, v, data in db.G.edges(data=True):
        edges.append({"from": u, "to": v, "label": data.get('type', '')})
        
    return {"nodes": nodes, "edges": edges}

@router.get("/attack-path")
def get_attack_paths(source_ip: str, target_ip: str):
    """
    Calculates the attack paths from a source IP to a target IP using NetworkX.
    """
    paths = find_attack_paths(source_ip, target_ip)
    
    if not paths:
        return {"message": "No paths found.", "paths": []}
        
    return {
        "message": f"Found {len(paths)} potential attack paths.",
        "paths": paths
    }

@router.get("/explain-path")
def explain_attack_path(source_ip: str, target_ip: str):
    """
    Uses the AI Analyst to explain an attack path and recommend mitigations.
    """
    explanation = generate_path_explanation(source_ip, target_ip)
    return {"explanation": explanation}
