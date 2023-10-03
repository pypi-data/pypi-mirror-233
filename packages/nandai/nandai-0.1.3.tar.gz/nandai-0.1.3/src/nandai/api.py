from __future__ import annotations
import httpx
import pandas as pd
import os

from nandai.utils import batch_async


http_client = httpx.AsyncClient(timeout=60)


class NandAIClient:
    def __init__(
            self,
            url: str | None = None,
            api_key: str | None = None,
    ):
        self.url = url or os.getenv('NANDAI_API_URL') or ''
        self.api_key = api_key or os.getenv('NANDAI_API_KEY') or ''

    async def batch_validate(
            self,
            input: pd.DataFrame,
            columns: list[str] = ['prompt', 'response'],
            context: str | list[str] = [],
            batch_size: int = 10,
    ) -> pd.DataFrame:
        data = self._process_data(input, columns)
        context = self._process_context(context)

        async def func(row: pd.Series):
            res = await self.validate(
                prompts=[row['prompt']],
                responses=[row['response']],
                context=context,
               )
            print(f"res: {res}")
            row['raw_result'] = res
            row['result'] = res[0]['factuality']
            return row

        rows = [row for _, row in data.iterrows()]
        return pd.DataFrame(await batch_async(rows, func, batch_size))

    def _process_data(self, data: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        return data[columns]

    def _process_context(self, context: str | list[str]) -> str:
        if isinstance(context, str):
            context = [context]
        return '\n\n'.join(context)

    async def validate(self, prompts: list[str], responses: list[str], context: str):
        res = await http_client.post(
            url= f'{self.url}/llmeval',
            json={
                'prompt': prompts,
                'response': responses,
                'context': context,
                'excludes': [],
            },
            headers={
                'x-api-key': self.api_key,
            },
        )
        return res.json()
