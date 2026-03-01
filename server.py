from fastmcp import FastMCP
import httpx

# Initialize with a broader name
mcp = FastMCP("UnifiedManager")

# Base URLs for your Spring Boot services
BASE_URL = "http://localhost:8080"

# --- ACCOUNTS TOOLS ---
@mcp.tool()
async def get_all_accounts() -> str:
    """Fetch all accounts and return as a clean table."""
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/accounts")
        data = res.json()
        
        # Format as a Markdown Table
        table = "| ID | Name | Balance |\n|---|---|---|\n"
        for acc in data:
            table += f"| {acc.get('id')} | {acc.get('name')} | {acc.get('balance')} |\n"
        return table

# --- TRANSACTIONS TOOLS ---
@mcp.tool()
async def get_recent_transactions(account_id: int) -> str:
    """Fetch recent transactions for a specific account ID."""
    async with httpx.AsyncClient() as client:
        # Assuming your Spring Boot has this endpoint
        res = await client.get(f"{BASE_URL}/transactions/{account_id}")
        return str(res.json())

# --- TODO TOOLS ---
@mcp.tool()
async def list_pending_tasks() -> str:
    """Get the list of pending todos."""
    async with httpx.AsyncClient() as client:
        # Assuming your Spring Boot has this endpoint
        res = await client.get(f"{BASE_URL}/todos?status=pending")
        return str(res.json())
    
@mcp.tool()
async def get_transaction_link(account_id: int, action: str) -> str:
    """
    Generates a direct link to the Angular app for a specific action.
    """
    # Assuming your Angular app runs on port 4200
    base_url = "http://localhost:4200/transactions"
    return f"To perform a {action}, please visit: {base_url}?accId={account_id}"

if __name__ == "__main__":
    mcp.run()