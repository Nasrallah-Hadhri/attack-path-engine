from core.database import db

def initialize_schema():
    print("Running in In-Memory Mode: Schema initialization bypassed.")
    # We'll artificially link the two dummy IPs from the XML for the sake of the Attack Path demo
    # In a real tool, this would be derived from routing tables or Nmap traceroute
    db.G.add_edge("192.168.1.10", "192.168.1.20", type="CONNECTED_TO")
    print("Added mock CONNECTED_TO lateral edge between .10 and .20 for attack path demonstration.")
