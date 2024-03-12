# AI-moderator sample scripts

This repository provides sample scripts for AI moderator.

## Setup

### Requirements

 - Python 3.8.1 or newer

If you need information to set up your environment, please see [here](docs/setup.md) and select your preferred tools from options of poetry, pip, and docker, before running our samples.

 - Environment where LLM(OpenAI API or Llama2 or Claude) is available
   - OpenAI https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key
   - Llama2 https://llama.meta.com/get-started/#getting-the-models
   - Claude https://www.anthropic.com/api


 - [Creating Fujitsu Research Portal (FRP) account](https://en-portal.research.global.fujitsu.com/content/creating_account_v1.3.pdf)

 - [Creating Federated SNS account](https://en-portal.research.global.fujitsu.com/content/FeS%20Application%20User%20Manual_en.pdf)

### Installation

1. In the working directory run:

```
git clone https://github.com/FujitsuResearch/sample-moderator.git
```

2. Choose one of the following options and run.


 - Poetry:
```
cd sample-moderator
poetry update
```

 - Pip:
```
pip install -U git+https://github.com/FujitsuResearch/atproto-python.git
pip install -U langchain langchain-openai
```

 - Docker: Before building, write your OpenAI API key in the Dockerfile
```
docker build -t python:atproto -f Dockerfile .
docker run -it --name atproto python:atproto /bin/bash
```

### Authenticate your account

Please issue an API access token on [Fujitsu Research Portal](https://en-portal.research.global.fujitsu.com/), following [this document](https://en-portal.research.global.fujitsu.com/content/issuing_api_tokens_v1.1.pdf). 

Please note that this token expires in 24 hours. You will need to re-authenticate after it expires.


## Run scripts
### Send posts (Option)
sample-post.py posts text separated by blank lines in a text file as a single post to the channel on Federated SNS.
```
python sample-post.py \
  --handle <your handle name on Federated SNS like: [***].federated-sns-server[XX].research.global.fujitsu.com> \
  --password <your password on Federated SNS> \
  --api-url <URL like: https://federated-sns-server[XX].research.global.fujitsu.com/xrpc> \
  --token <your Azure AD token issued at Fujitsu Research Portal> \
  --channel <channel name> \
  --post-file <path to a text file including post text like: input/sample-post.txt>
```
Hints about environmental variables and parameters:
 - `--handle`  Handle name can confirm at "Profile" on Federated SNS.
 - `--api-url` should be a same domain with your handle name. if your handle is on server01, the api-url is also on the same domain like `https://federated-sns-server01.research.global.fujitsu.com/xrpc`.
 - `--channel` If the channel name is "test-channel.federated-sns-server01.research.global.fujitsu.com", specify the parameter like: `--channel test-channel`

### Get posts and inference
OpenAI version:
```
export OPENAI_API_KEY="<your api key>"
python sample-openai.py \
  --handle <your handle name on Federated SNS like: [***].federated-sns-server[XX].research.global.fujitsu.com> \
  --password <your password on Federated SNS> \
  --api-url <URL like: https://federated-sns-server[XX].research.global.fujitsu.com/xrpc> \
  --token <your API access token issued at Fujitsu Research Portal> \
  --channel <the name of channel to get posts on Federated SNS> \
  --prompt-file <path to a prompt file at local> 
```

Local LLM version (e.g. Llama2):
```
# The sample requires additional packages: transformers and langchain-community
# pip install transformers langchain-community
python sample-llama2-local.py \
  --handle <your handle name on Federated SNS like: [***].federated-sns-server[XX].research.global.fujitsu.com>  \
  --password <your password on Federated SNS> \
  --api-url <URL like: https://federated-sns-server[XX].research.global.fujitsu.com/xrpc> \
  --token <your API access token issued at Fujitsu Research Portal> \
  --channel <the name of channel to get posts on Federated SNS> \
  --model-name meta-llama/Llama-2-7b-chat-hf \
  --prompt-file <path to a prompt file at local> 
```

Anthropic Claude version:
```
# The sample requires an additional package: langchain-anthropic
# pip install langchain-anthropic
export ANTHROPIC_API_KEY="<your api key>"
python sample-claude.py \
  --handle <your handle name on Federated SNS like: [***].federated-sns-server[XX].research.global.fujitsu.com> \
  --password <your password on Federated SNS> \
  --api-url <URL like: https://federated-sns-server[XX].research.global.fujitsu.com/xrpc> \
  --token <your API access token issued at Fujitsu Research Portal> \
  --channel <the name of channel to get posts on Federated SNS> \
  --prompt-file <path to a prompt file at local> 
```

Hints about environmental variables and parameters:
 - `OPENAI_API_KEY` Log in to the OpenAI website with your own account and issue `OPENAI_API_KEY`.
 - `--handle`  Handle name can confirm at "Profile" on Federated SNS.
 - `--api-url` should be a same domain with your handle name. if your handle is on server01, the api-url is also on the same domain like `https://federated-sns-server01.research.global.fujitsu.com/xrpc`.
  - `--channel` If the channel name is "test-channel.federated-sns-server01.research.global.fujitsu.com", specify the parameter like: `--channel test-channel`
 - `--prompt-file` Prompt files are in `sample-moderator/input/`

You can also run this sample script with OpenAI using [sample.ipynb](https://colab.research.google.com/github/FujitsuResearch/sample-moderator/blob/main/sample.ipynb).
