# Arthur Client

This library provides a lightweight Python API for interacting with [Arthur's REST API](https://docs.arthur.ai/reference/getting-started-with-your-api).  

### Example: Fetch Models

```python
from typing import List
from arthur.client.rest import ArthurClient
from arthur.client.rest.models.models import ModelResponse

# create client
client = ArthurClient(url="https://app.arthur.ai",
                      login="<my_username>")
# enter your password when prompted

# fetch first page of models
models_p1: List[ModelResponse] = client.models.get_paginated_models(page=1, page_size=10).data

# print model names
print(f"Found {len(models_p1)} models on first page: {', '.join([m.display_name for m in models_p1])}")
```

