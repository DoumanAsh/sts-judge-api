# sts-judge-api

## Initial setup

```
uv sync
uv run manage.py createcachetable
```

### Start server

```
uv run manage.py runserver 8080
```

## Run tests

```
uv run pytest
```
### Coverage report

```
uv run python -m pytest --cov --cov-config=pyproject.toml --cov-report=html
```

## Methodology

[sentence-transformers](https://github.com/UKPLab/sentence-transformers) are selected for ability to be context aware enabling to enable comparison without regard for sentence order when computing similarity score, while having small hardware requirements

Model [STS-multilingual-mpnet-base-v2](https://huggingface.co/Gameselo/STS-multilingual-mpnet-base-v2) was selected based on having decent score in [leaderboard](https://huggingface.co/spaces/mteb/leaderboard) while having small memory footprint

When dealing with a more complex sentences or paragraphs of text, a better choice might be tensorflow's [Universal Sentence Encoder](https://www.tensorflow.org/hub/tutorials/semantic_similarity_with_tf_hub_universal_encoder)
