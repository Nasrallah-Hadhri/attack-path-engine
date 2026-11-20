import os
from engine.attack_path import find_attack_paths

def generate_path_explanation(source_ip: str, target_ip: str, model: str = "gemini"):
    """
    Simulates sending the attack path to an LLM for explanation.
    In a real scenario, this would use litellm, langchain, or the google-generativeai SDK.
    """
    paths = find_attack_paths(source_ip, target_ip)
    
    if not paths:
        return "No attack path found between these assets. The target appears secure from this vector."
        
    # Take the highest risk path
    top_path = paths[0]
    path_nodes = top_path['path']
    risk = top_path['risk_score']
    
    # Format the graph data for the LLM
    prompt = f"""
You are an expert Cybersecurity Analyst. 
I have extracted an attack path from our Neo4j Graph Database.

Source Asset: {source_ip}
Target Asset: {target_ip}

Attack Path (Nodes traversed):
{' -> '.join(path_nodes)}

Total Calculated Risk Score (CVSS Sum): {risk}

Explain this attack path to a sysadmin. 
Do not invent new paths. Only use the nodes provided.
Suggest 3 concrete mitigation steps to break this chain.
"""

    # --- MOCK LLM RESPONSE ---
    # In production:
    # client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    # response = client.models.generate_content(model='gemini-2.5-pro', contents=prompt)
    # return response.text

    mock_llm_response = f"""### Security Analyst Report: Attack Path Analysis

Based on the graph traversal, an attacker starting at `{source_ip}` can reach the critical asset `{target_ip}` through the following path:

**Path Analysis:**
{ ' ➔ '.join(path_nodes) }

The total calculated risk score for this vector is **{risk}**.

**Explanation:**
The attacker compromises `{source_ip}`, discovers an exposed service, and exploits a known vulnerability (e.g., CVE) present in the path. Once that service is exploited, they gain execution on the host, allowing them to pivot and access the target `{target_ip}`.

**Recommended Mitigations to Break the Path:**
1. **Patch the Vulnerability:** Immediately apply the security patch for any CVEs listed in the path to eliminate the exploitation step.
2. **Network Segmentation:** Implement firewall rules to restrict traffic from `{source_ip}` to the intermediate services, ensuring only necessary ports are accessible.
3. **Least Privilege:** Ensure the compromised service runs with minimal permissions so an exploit cannot easily lead to full host compromise or lateral movement.
"""
    return {
        "prompt_sent": prompt,
        "llm_response": mock_llm_response
    }
