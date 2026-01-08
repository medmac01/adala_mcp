from mcp.server.fastmcp import FastMCP
import httpx
import os
import json

# Initialize the MCP server
mcp = FastMCP("adala-search")

# Constants
BASE_URL = "https://adala.justice.gov.ma"
# CAUTION: This ID (THP5...) is a Next.js Build ID. 
# If the website is updated/redeployed, this ID might change, breaking the JSON endpoint.
# If it stops working, visit the site, inspect network traffic, and get the new ID.
BUILD_ID = "THP5ZL1eNCinRAZ1hWfN0" 

@mcp.tool()
async def search_adala(keyword: str, limit: int = 5) -> str:
    """
    Search for legal documents, laws, and decrees on the Adala Justice website.
    
    Args:
        keyword: The search term (e.g., "طلاق", "شركة", "Dahir").
        limit: Number of results to return (default 5).
    """
    url = f"{BASE_URL}/_next/data/{BUILD_ID}/fr/search.json"
    
    params = {
        "term": keyword,
        "themes": "",
        "resources": "",
        "type": "",
        "number": "",
        "start_date": "",
        "end_date": "",
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            # Navigate the JSON structure provided in your example
            raw_results = data.get("pageProps", {}).get("searchResult", {}).get("data", [])
            
            processed_results = []
            for item in raw_results[:limit]:
                # Extract relevant info
                file_path = item.get("path")
                full_download_url = f"{BASE_URL}/{file_path}" if file_path else "N/A"
                
                entry = {
                    "title": item.get("name"),
                    "type": item.get("type"), # e.g., PDF
                    "law_type": item.get("fileMeta", {}).get("LawType", {}).get("name"),
                    "date": item.get("fileMeta", {}).get("gregorianDate"),
                    "relative_path": file_path, # This is used for the download tool
                    "download_url": full_download_url
                }
                processed_results.append(entry)
                
            if not processed_results:
                return "No results found for that keyword."

            return json.dumps(processed_results, ensure_ascii=False, indent=2)

        except Exception as e:
            return f"Error connecting to Adala: {str(e)}"

@mcp.tool()
async def download_document(relative_path: str, save_filename: str = None) -> str:
    """
    Download a specific legal document found via search.
    
    Args:
        relative_path: The 'relative_path' returned from the search_adala tool (e.g., 'uploads/2024/04/01/filename.pdf').
        save_filename: Optional name to save the file as. If not provided, derives from the original filename.
    """
    download_url = f"{BASE_URL}/api/{relative_path}"
    
    # Create a 'downloads' directory if it doesn't exist
    os.makedirs("downloads", exist_ok=True)
    
    # Determine filename
    if not save_filename:
        save_filename = os.path.basename(relative_path)
    
    # Ensure extension matches
    if not save_filename.lower().endswith(".pdf"):
        save_filename += ".pdf"
        
    local_path = os.path.join("downloads", save_filename)

    async with httpx.AsyncClient() as client:
        try:
            async with client.stream("GET", download_url) as response:
                response.raise_for_status()
                with open(local_path, "wb") as f:
                    async for chunk in response.aiter_bytes():
                        f.write(chunk)
            
            return f"Successfully downloaded file to: {os.path.abspath(local_path)}"
        except Exception as e:
            return f"Failed to download file: {str(e)}"

if __name__ == "__main__":
    mcp.run()
