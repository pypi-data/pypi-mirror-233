import asyncio
import typer
import pandas as pd
from typing import List

try:
    from dotenv import load_dotenv
    load_dotenv('.env.local')
except:
    pass

from nandai.api import NandAIClient


cli = typer.Typer()
client = NandAIClient()


@cli.command()
def validate_one(prompt: str, response: str, context: str):
    """Validate a prompt-response pair with context."""
    print(f"Prompt: `{prompt}`, response: `{response}`, context: `{context}`")
    print("Running validation...")
    res = asyncio.run(client.validate([prompt], [response], context))
    print(f"\nResult: {res}")


@cli.command()
def validate(
        data_file: str,
        columns: str = typer.Option('prompt,response,context', '--columns', help="columns in data file, `context` is optional"),
        context: str = typer.Option('', '--context', '-c', help="additional context string that applies to all prompt-response pairs"),
        batch_size: int = 5,
        output: str = typer.Option('', '--output', '-o', help="Output file path"),
):
    """
    Validate prompt-response pairs from data file, supports 'csv' and 'jsonl' files.

    :return: File with additional columns: `NandScore`, `FactualInaccuraciesFound`, `Correction` (json string)
    """
    print(f"Data file: `{data_file}`, additional context: `{context}`")

    if data_file.endswith('.csv'):
        df = pd.read_csv(data_file)
    elif data_file.endswith('.jsonl') or data_file.endswith('.json'):
        df = pd.read_json(data_file, lines=True)
    else:
        raise ValueError(f"Unsupported data file type: `{data_file}`")

    cols = [c.strip() for c in columns.split(',')]
    df.columns = df.columns.str.strip()
    print("Running batch validation...")
    res = asyncio.run(client.batch_validate(df, context=context, batch_size=batch_size, columns=cols))

    if output:
        print(f"Saving result to `{output}`")
        if output.endswith('.jsonl') or output.endswith('.json'):
            res.to_json(output, orient='records', lines=True)
        elif output.endswith('.csv'):
            res.to_csv(output)
        else:
            raise ValueError(f"Unsupported output file type: `{output}`")
    else:
        print(f"\nResult: {res}")


if __name__ == "__main__":
    cli()
