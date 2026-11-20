from core.database import db

def ingest_assets_to_graph(assets: list):
    """
    Takes a list of parsed Nmap assets and ingests them into the In-Memory NetworkX graph.
    """
    for asset in assets:
        ip = asset.get('ip')
        os = asset.get('os', 'Unknown')
        
        if not ip:
            continue
            
        # 1. Add the Asset (Host) Node
        db.G.add_node(ip, type="Asset", ip=ip, os=os)
        
        # 2. Add Services and link to Asset
        for service in asset.get('services', []):
            port = service.get('port')
            protocol = service.get('protocol')
            name = service.get('name')
            product = service.get('product')
            version = service.get('version')
            
            service_id = f"{ip}:{port}/{protocol}"
            
            db.G.add_node(service_id, type="Service", id=service_id, port=port, protocol=protocol, name=name, product=product, version=version)
            db.G.add_edge(ip, service_id, type="RUNS")
            
    print(f"Ingested {len(assets)} assets. Graph now has {db.G.number_of_nodes()} nodes.")
    return True
