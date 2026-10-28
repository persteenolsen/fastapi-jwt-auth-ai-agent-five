
import asyncio
import json
import logging

from langchain_mcp_adapters.client import MultiServerMCPClient

logging.basicConfig(level=logging.INFO)

# 27-10-2026 - Public MCP for testing
SIMPLY_MCP_URL = "https://mcp.simply.com/public"

# 27-10-2026 - Private MCP
# SIMPLY_MCP_URL = "https://mcp.simply.com/v2"

async def main():
    print(f"Connecting to Simply.com MCP:\n{SIMPLY_MCP_URL}\n")

    client = MultiServerMCPClient(
        {
            "simplycom": {
                "transport": "streamable_http",
                "url": SIMPLY_MCP_URL,
            }
        }
    )

    try:
        tools = await client.get_tools()

        print(f"\nSuccess! Discovered {len(tools)} tool(s):\n")

        for tool in tools:
            print(f"Tool: {tool.name}")
            print(f"Description: {tool.description}")

            schema = getattr(tool, "args_schema", None)

            if hasattr(schema, "model_json_schema"):
                schema = schema.model_json_schema()

            print(
                "Arguments:",
                json.dumps(schema, indent=2, default=str),
            )
            print("-" * 60)

    except Exception as exc:
        print("\nConnection or tool discovery failed.")
        print(f"Error type: {type(exc).__name__}")
        print(f"Error: {exc}")


if __name__ == "__main__":
    asyncio.run(main())
