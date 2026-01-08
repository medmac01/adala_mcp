
# Adala Justice MCP Server 🇲🇦⚖️

An **MCP (Model Context Protocol)** server that interfaces with the [Adala Justice](https://www.google.com/search?q=https://adala.justice.gov.ma) website (Moroccan Ministry of Justice).

This server allows LLMs (like Claude Desktop) to programmatically search for Moroccan laws, decrees, and legal documents, and download the corresponding PDFs directly to your local machine.

## ✨ Features

* **Search:** Query the Adala database using keywords (Arabic or French).
* **Metadata:** Retrieves detailed metadata including Law Type (Dahir, Arrêté, etc.), dates, and descriptions.
* **Download:** Automatically fetches and saves the PDF files associated with search results.
* **Protocol:** Built using the `fastmcp` Python library for high performance and easy extensibility.

## 🛠️ Prerequisites

* **Python 3.10+**
* **uv** (Recommended package manager) or `pip`
* **Claude Desktop** (for end-user interaction)

## 📦 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/adala-mcp.git
cd adala-mcp

```


2. **Create a virtual environment and install dependencies:**
Using `uv` (Recommended):
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install mcp[cli] httpx

```


Using standard `pip`:
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install mcp[cli] httpx

```



## ⚙️ Configuration (Claude Desktop)

To use this with Claude, you need to add the server to your configuration file.

1. **Locate the config file:**
* **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
* **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`


2. **Add the server definition:**
```json
{
  "mcpServers": {
    "adala": {
      "command": "/path/to/your/project/.venv/bin/python",
      "args": ["/path/to/your/project/server.py"]
    }
  }
}

```


*Note: Replace `/path/to/your/project/` with the actual absolute path to your folder. Using the python executable inside your venv is the safest way to ensure dependencies are found.*

## 🧪 Testing & Debugging

You can test the server without Claude using the MCP Inspector.

**Prerequisite:** You need Node.js installed to run the inspector.

```bash
npx @modelcontextprotocol/inspector uv run server.py

```

This will open a web interface at `http://localhost:5173` where you can manually run the tools and view the JSON output.

## ⚠️ Important: Handling the `BUILD_ID`

This tool wraps the internal Next.js API of the Adala website. The URL structure depends on a **Build ID** (e.g., `THP5ZL1eNCinRAZ1hWfN0`) which changes whenever the Ministry of Justice updates their website.

**If the tool stops working (returns 404 errors):**

1. Open [adala.justice.gov.ma](https://www.google.com/search?q=https://adala.justice.gov.ma) in your browser.
2. Right-click anywhere and select **Inspect** (or press `F12`).
3. Go to the **Network** tab.
4. Perform a search on the website.
5. Look for a request named `search.json`.
6. The URL will look like: `.../_next/data/NEW_ID_HERE/fr/search.json`.
7. Copy the `NEW_ID_HERE`.
8. Open `server.py` and update the variable:
```python
# Update this line with the new ID
BUILD_ID = "NEW_ID_HERE"

```



## 📚 Tools Reference

The server exposes the following tools to the LLM:

### `search_adala`

Searches the database for legal documents.

* **Inputs:**
* `keyword` (string): The search term (e.g., "faillite", "طلاق").
* `limit` (int): Max results to return (default: 5).


* **Returns:** JSON string containing titles, metadata, and relative file paths.

### `download_document`

Downloads a file found via search.

* **Inputs:**
* `relative_path` (string): The path returned by the search tool (e.g., `uploads/2024/...`).
* `save_filename` (string, optional): A custom name for the file.


* **Behavior:** Saves files to a `./downloads` folder in the project directory.

## 📄 License

This project is an unofficial open-source tool. Content retrieved is property of the Ministry of Justice of Morocco. Use responsibly and in accordance with the website's terms of service.