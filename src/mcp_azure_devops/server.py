"""
Azure DevOps MCP Server

A simple MCP server that exposes Azure DevOps capabilities.
"""
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))
import argparse

from mcp.server.fastmcp import FastMCP

from mcp_azure_devops.features import register_all
from mcp_azure_devops.utils import register_all_prompts

# Create a FastMCP server instance with a name
mcp = FastMCP("Azure DevOps")

# Register all features
register_all(mcp)
register_all_prompts(mcp)

def main():
    """Entry point for the command-line script."""
    parser = argparse.ArgumentParser(
        description="Run the Azure DevOps MCP server")
    parser.add_argument('--tool', type=str, help='Name of the tool to run (e.g., get_projects)')
    parser.add_argument('--tool-args', type=str, nargs='*', help='Arguments for the tool in key=value format')
    args = parser.parse_args()

    if args.tool:
        # Prepare tool arguments as kwargs
        tool_kwargs = {}
        if args.tool_args:
            for arg in args.tool_args:
                if '=' in arg:
                    k, v = arg.split('=', 1)
                    tool_kwargs[k] = v
        # Call the tool using FastMCP's call_tool method (expects 'arguments' dict) and await it
        import asyncio
        result = asyncio.run(mcp.call_tool(args.tool, arguments=tool_kwargs))
        print(result)
    else:
        # Start the server as usual
        mcp.run()

if __name__ == "__main__":
    main()
