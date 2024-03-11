import os
import click
import torch
import transformers
from transformers import AutoTokenizer

from atproto import Client
from langchain_community.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate

@click.command()
@click.option('--handle', required=True, help='your Atproto handle')
@click.option('--password', required=True, help='password of your account')
@click.option('--api-url', required=True, help='API server for user\'s pds. Example: https://bsky.app/xrpc')
@click.option('--token', required=True, help='Token issued at Fujitsu Research Portal')
@click.option('--channel', required=True, help='Channel name')
@click.option('--model-name', help='Model name in HuggingFace', default='meta-llama/Llama-2-7b-chat-hf')
@click.option('--cache-dir', help='path to model cache', default=None)
@click.option('--prompt-file', required=True, help='path to your prompt file')
@click.option('--cert', help='path to cert file to atproto server', default=None)
def run(handle, password, api_url, token, channel, model_name, cache_dir, prompt_file, cert) :
    
    # atproto setup
    client = Client(base_url=api_url)
    profile = client.login(handle, password, portal_token=token)
    print(f"Successfully logged in: {profile.handle}")
    
    if torch.cuda.is_available():
        device = torch.device('cuda')
        print(f'There are {torch.cuda.device_count()} GPU(s) available.')
        print('Device name:', torch.cuda.get_device_name(0))
    else:
        print('No GPU available, using the CPU instead.')
        device = torch.device('cpu')
    
    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
    if cache_dir is not None :
        model_kwargs = {"cache_dir": cache_dir}
    else :
        model_kwargs = None
    
    pipeline = transformers.pipeline(
        "text-generation", model=model_name, tokenizer=tokenizer, max_new_tokens=300,
        model_kwargs=model_kwargs,
        device=device
    )
    hf = HuggingFacePipeline(pipeline=pipeline,
                            batch_size=2, # adjust as needed based on GPU map and model size.
                            )
    
    with open(prompt_file) as f:
        template = f.read()

    prompt = PromptTemplate(
        template=template,
        input_variables = ["post"],
    )
    chain = prompt | hf
    
    # List joined channels
    response = client.app.fujitsu.channel.list_channel_info()
    joined_channel_list = [cinfo.channel_handle for cinfo in response.channel_info if channel in cinfo.channel_handle ]
    channel_name = joined_channel_list[0]
    print("Selected channel: ", channel_name)
    
    # Get posts in the channel and Run the chat model
    limit = 5
    flag = True
    cursor = None
    while flag :
        
        # Get posts
        response = client.get_channel_records(
                        channel=channel_name,
                        cursor=cursor,
                        limit=limit,
                    )
        if len(response.records) < limit :
            flag = False
        cursor = response.cursor
        
        # Run the LLM for each post
        text_list = []
        for record in response.records :
            value = record.value.model_dump()
            post_handle = value['handle']
            text = value['text']
            text_list.append({"post": text})
            
        results = chain.batch(text_list)
        for i, result in enumerate(results):
            print(prompt.format(post=text_list[i]["post"]))
            print(result)
            print('---')
    
    return 

if __name__ == '__main__' :
    
    run()