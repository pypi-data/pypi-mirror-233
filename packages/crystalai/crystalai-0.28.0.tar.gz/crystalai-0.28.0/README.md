# Crystal Computing AI Python Library

The Crystal Computing AI Python library provides convenient access to the Crystal Computing AI API
from applications written in the Python language. It includes a
pre-defined set of classes for API resources that initialize
themselves dynamically from API responses which makes it compatible
with a wide range of versions of the Crystal Computing AI API.

You can find usage examples for the Crystal Computing AI Python library in our [API reference](https://platform.crystalcomputing.com/docs/api-reference?lang=python) and the [Crystal Computing AI Cookbook](https://github.com/openai/openai-cookbook/).

## Credit

This library is forked from the OpenAI Python Library which is forked from the [Stripe Python Library](https://github.com/stripe/stripe-python).

## Installation

To start, ensure you have Python 3.7.1 or newer. If you just
want to use the package, run:

```sh
pip install --upgrade crystalai
```

After you have installed the package, import it at the top of a file:

```python
import crystalai
```

To install this package from source to make modifications to it, run the following command from the root of the repository:

```sh
python setup.py install
```

### Optional dependencies

Install dependencies for [`crystalai.embeddings_utils`](crystalai/embeddings_utils.py):

```sh
pip install crystalai[embeddings]
```

Install support for [Weights & Biases](https://wandb.me/openai-docs) which can be used for fine-tuning:

```sh
pip install crystalai[wandb]
```

Data libraries like `numpy` and `pandas` are not installed by default due to their size. They’re needed for some functionality of this library, but generally not for talking to the API. If you encounter a `MissingDependencyError`, install them with:

```sh
pip install crystalai[datalib]
```

## Usage

The library needs to be configured with your Crystal Computing AI account's private API key which is available on our [developer platform](https://platform.crystalcomputing.com/account/api-keys). Either set it as the `CRYSTALAI_API_KEY` environment variable before using the library:

```bash
export CRYSTALAI_API_KEY='crystal_...'
```

Or set `crystalai.api_key` to its value:

```python
crystalai.api_key = "crystal_..."
```

Examples of how to use this library to accomplish various tasks can be found in the [Crystal Computing AI Cookbook](https://github.com/openai/openai-cookbook/). It contains code examples for: classification using fine-tuning, clustering, code search, customizing embeddings, question answering from a corpus of documents. recommendations, visualization of embeddings, and more.

Most endpoints support a `request_timeout` param. This param takes a `Union[float, Tuple[float, float]]` and will raise an `openai.error.Timeout` error if the request exceeds that time in seconds (See: https://requests.readthedocs.io/en/latest/user/quickstart/#timeouts).

### Chat completions

Chat models such as `gpt-3.5-turbo` and `gpt-4` can be called using the [chat completions endpoint](https://platform.crystalcomputing.com/docs/api-reference/chat/create).

```python
completion = crystalai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}])
print(completion.choices[0].message.content)
```

You can learn more in our [chat completions guide](https://platform.crystalcomputing.com/docs/guides/gpt/chat-completions-api).

### Completions

Text models such as `babbage-002` or `davinci-002` (and our [legacy completions models](https://platform.crystalcomputing.com/docs/deprecations/deprecation-history)) can be called using the completions endpoint.

```python
completion = crystalai.completion.create(model="davinci-002", prompt="Hello world")
print(completion.choices[0].text)
```

You can learn more in our [completions guide](https://platform.crystalcomputing.com/docs/guides/gpt/completions-api).

### Embeddings

Embeddings are designed to measure the similarity or relevance between text strings. To get an embedding for a text string, you can use following:

```python
text_string = "sample text"

model_id = "text-embedding-ada-002"

embedding = crystalai.Embedding.create(input=text_string, model=model_id)['data'][0]['embedding']
```

You can learn more in our [embeddings guide](https://platform.crystalcomputing.com/docs/guides/embeddings/embeddings).

### Fine-tuning

Fine-tuning a model on training data can both improve the results (by giving the model more examples to learn from) and lower the cost/latency of API calls by reducing the need to include training examples in prompts.

```python
# Create a fine-tuning job with an already uploaded file
crystalai.FineTuningJob.create(training_file="file-abc123", model="gpt-3.5-turbo")

# List 10 fine-tuning jobs
crystalai.FineTuningJob.list(limit=10)

# Retrieve the state of a fine-tune
crystalai.FineTuningJob.retrieve("ft-abc123")

# Cancel a job
crystalai.FineTuningJob.cancel("ft-abc123")

# List up to 10 events from a fine-tuning job
crystalai.FineTuningJob.list_events(id="ft-abc123", limit=10)

# Delete a fine-tuned model (must be an owner of the org the model was created in)
crystalai.Model.delete("ft:gpt-3.5-turbo:acemeco:suffix:abc123")
```

You can learn more in our [fine-tuning guide](https://platform.crystalcomputing.com/docs/guides/fine-tuning).

To log the training results from fine-tuning to Weights & Biases use:

```
crystalai wandb sync
```

For more information, read the [wandb documentation](https://docs.wandb.ai/guides/integrations/openai) on Weights & Biases.

### Moderation

Crystal Computing AI provides a free Moderation endpoint that can be used to check whether content complies with the Crystal Computing AI [content policy](https://platform.crystalcomputing.com/docs/usage-policies).

```python
moderation_resp = crystalai.Moderation.create(input="Here is some perfectly innocuous text that follows all Crystal Computing AI content policies.")
```

You can learn more in our [moderation guide](https://platform.crystalcomputing.com/docs/guides/moderation).

### Async API

Async support is available in the API by prepending `a` to a network-bound method:

```python
async def create_chat_completion():
    chat_completion_resp = await crystalai.ChatCompletion.acreate(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}])
```

To make async requests more efficient, you can pass in your own
`aiohttp.ClientSession`, but you must manually close the client session at the end
of your program/event loop:

```python
from aiohttp import ClientSession
crystalai.aiosession.set(ClientSession())

# At the end of your program, close the http session
await crystalai.aiosession.get().close()
```

### Command-line interface

This library additionally provides an `crystalai` command-line utility
which makes it easy to interact with the API from your terminal. Run
`crystalai api -h` for usage.

```sh
# list models
crystalai api models.list

# create a chat completion (gpt-3.5-turbo, gpt-4, etc.)
crystalai api chat_completions.create -m gpt-3.5-turbo -g user "Hello world"

# create a completion (text-davinci-003, text-davinci-002, ada, babbage, curie, davinci, etc.)
crystalai api completions.create -m ada -p "Hello world"

# generate images via DALL·E API
crystalai api image.create -p "two dogs playing chess, cartoon" -n 1

# using crystalai through a proxy
crystalai --proxy=http://proxy.com api models.list
```
