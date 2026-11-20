from fastapi import APIRouter, UploadFile, File, HTTPException
from parsers.nmap_parser import parse_nmap_xml
from graph.ingest import ingest_assets_to_graph
from core.database import db

router = APIRouter()

@router.post("/upload")
async def upload_nmap_scan(file: UploadFile = File(...)):
    if not file.filename.endswith('.xml'):
        raise HTTPException(status_code=400, detail="Only Nmap XML files are supported.")
        
    content = await file.read()
    xml_content = content.decode("utf-8")
    
    # Parse the XML
    assets = parse_nmap_xml(xml_content)
    if not assets:
        raise HTTPException(status_code=400, detail="No assets found or invalid XML.")
        
    # Ingest the assets into Neo4j
    ingest_assets_to_graph(assets)
    
    return {
        "message": f"Successfully parsed {len(assets)} assets.",
        "assets": assets
    }

@router.post("/load-dummy")
def load_dummy_nmap():
    """
    Utility endpoint to load the dummy Nmap data directly for the dashboard demo.
    """
    import os
    file_path = os.path.join(os.path.dirname(__file__), "..", "tests", "dummy_nmap.xml")
    try:
        with open(file_path, "r") as f:
            xml_content = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    assets = parse_nmap_xml(xml_content)
    ingest_assets_to_graph(assets)
    return {"message": "Dummy Nmap data loaded into Graph!", "assets": assets}
