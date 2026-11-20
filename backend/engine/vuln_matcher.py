from core.database import db

MOCK_CVE_DB = {
    "Apache httpd": {
        "2.4.41": [
            {"cve_id": "CVE-2021-44228", "severity": "CRITICAL", "cvss": 10.0, "description": "Log4Shell mock (Apache illustrative)"},
            {"cve_id": "CVE-2021-44790", "severity": "HIGH", "cvss": 9.8, "description": "Possible buffer overflow in mod_lua"}
        ]
    },
    "PostgreSQL DB": {
        "14.2": [
            {"cve_id": "CVE-2022-1552", "severity": "HIGH", "cvss": 8.8, "description": "Autovacuum, REINDEX, and others omit privilege checks"}
        ]
    }
}

def match_vulnerabilities():
    """
    Scans the in-memory graph for services, matches them against the mock CVE database,
    and creates Vulnerability nodes and [:AFFECTED_BY] relationships.
    """
    matched_count = 0
    
    # Iterate over a copy of the nodes list so we can add new nodes safely
    nodes = list(db.G.nodes(data=True))
    
    for node_id, data in nodes:
        if data.get('type') == 'Service':
            product = data.get('product')
            version = data.get('version')
            
            if product in MOCK_CVE_DB and version in MOCK_CVE_DB[product]:
                vulns = MOCK_CVE_DB[product][version]
                
                for vuln in vulns:
                    cve_id = vuln['cve_id']
                    
                    # Add Vulnerability node if it doesn't exist
                    if cve_id not in db.G:
                        db.G.add_node(cve_id, type="Vulnerability", cve_id=cve_id, severity=vuln['severity'], cvss=vuln['cvss'], description=vuln['description'])
                    
                    # Link Service to Vulnerability
                    db.G.add_edge(node_id, cve_id, type="AFFECTED_BY")
                    matched_count += 1
                    
    return matched_count
