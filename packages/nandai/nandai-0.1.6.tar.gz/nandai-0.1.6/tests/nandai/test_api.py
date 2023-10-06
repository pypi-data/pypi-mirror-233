from __future__ import annotations

import json
import pandas as pd
import pytest

from nandai import NandAIClient


validate_response = json.loads("""
[
  {
    "factuality": true,
    "reasonings": [
      {
        "reasoning": "The given text is factual because the evidence provided states that 'a=1'.",
        "error": "None",
        "correction": "N/A",
        "reference": [
          "Additional Context"
        ],
        "factuality": true,
        "source": "the value of a is 1",
        "claim": "The value of a is 1"
      }
    ]
  }
]
""")


@pytest.mark.asyncio
async def test_client_validate(mock_http_post):
    mock_http_post.return_value = validate_response

    client = NandAIClient()
    res = await client.batch_validate(pd.DataFrame({
        'prompt': ['what value is a'],
        'response': ['the value of a is 1'],
    }), context='a=1')

    assert res['result'][0] == True
    assert res['raw_result'][0] == validate_response
