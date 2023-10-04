import asyncio
import typer
import pandas as pd

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
    """Validate a prompt-response pair with context."""
    print(f"Prompt: `{prompt}`, response: `{response}`, context: `{context}`")
    print("Running validation...")
    res = asyncio.run(client.validate([prompt], [response], context))
    print(f"\nResult: {res}")


@cli.command()
def batch_validate(data_file: str, context: str = '', batch_size: int = 5, output: str = ''):
    """
    Validate a batch of prompt-response pairs from data file, supports 'csv' and 'jsonl' files.
    Columns should be `prompt` and `response`, you can optionaly add `context` column for each pair.
    `--context` can add additional context that shared by all prompt-response pair.
    """
    print(f"Data file: `{data_file}`, additional context: `{context}`")

    if data_file.endswith('.csv'):
        df = pd.read_csv(data_file)
    elif data_file.endswith('.jsonl'):
        df = pd.read_json(data_file, lines=True)
    else:
        raise ValueError(f"Unsupported data file type: `{data_file}`")

    df.columns = df.columns.str.strip()
    print("Running batch validation...")
    res = asyncio.run(client.batch_validate(df, context=context, batch_size=batch_size))

    if output:
        print(f"Saving result to `{output}`")
        if output.endswith('.jsonl'):
            res.to_json(output, orient='records', lines=True)
        elif output.endswith('.csv'):
            res.to_csv(output)
        else:
            raise ValueError(f"Unsupported output file type: `{output}`")
    else:
        print(f"\nResult: {res}")


if __name__ == "__main__":
    cli()
