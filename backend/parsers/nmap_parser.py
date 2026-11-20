import xml.etree.ElementTree as ET

def parse_nmap_xml(xml_content: str):
    """
    Parses Nmap XML output and returns a list of assets and their services.
    """
    try:
        root = ET.fromstring(xml_content)
    except Exception as e:
        print(f"Failed to parse XML: {e}")
        return []

    assets = []
    
    for host in root.findall('host'):
        asset_data = {
            'ip': None,
            'os': None,
            'services': []
        }
        
        # Get IP address
        address = host.find('address')
        if address is not None and address.get('addrtype') == 'ipv4':
            asset_data['ip'] = address.get('addr')
            
        # Get OS matches
        os = host.find('os')
        if os is not None:
            osmatch = os.find('osmatch')
            if osmatch is not None:
                asset_data['os'] = osmatch.get('name')
                
        # Get Services (Ports)
        ports = host.find('ports')
        if ports is not None:
            for port in ports.findall('port'):
                state = port.find('state')
                if state is not None and state.get('state') == 'open':
                    service = port.find('service')
                    service_name = service.get('name') if service is not None else 'unknown'
                    service_product = service.get('product') if service is not None else ''
                    service_version = service.get('version') if service is not None else ''
                    
                    asset_data['services'].append({
                        'port': port.get('portid'),
                        'protocol': port.get('protocol'),
                        'name': service_name,
                        'product': service_product,
                        'version': service_version
                    })
                    
        assets.append(asset_data)
        
    return assets
