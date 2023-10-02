This is a simple example of how I've been making OpenAI API calls.

I've created pydantic objects to match the OpenAI objects, and then implement a couple of nice helpers on top.

Most importantly `.iterator` (and optionally an async `.aiterator`) that automatically execute function as needed, if allowed. To go along with this, the `Function` BaseModel can be created from an existing annotated callable which really streamlines the whole process..