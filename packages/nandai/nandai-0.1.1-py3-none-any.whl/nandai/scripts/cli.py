import asyncio
import typer

try:
    from dotenv import load_dotenv
    load_dotenv('.env.local')
except:
    pass

from nandai.api import NandAIClient


cli = typer.Typer()
client = NandAIClient()


@cli.command()
def validate(prompt: str, response: str, context: str):
    print(f"Prompt: `{prompt}`, response: `{response}`, context: `{context}`")
    print("Running validation...")
    res = asyncio.run(client.validate([prompt], [response], context))
    print(f"\nResult: {res}")


if __name__ == "__main__":
    cli()
