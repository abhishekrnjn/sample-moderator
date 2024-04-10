import os
import click

from atproto import Client
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate

@click.command()
@click.option('--handle', required=True, help='your Atproto handle')
@click.option('--password', required=True, help='password of your account')
@click.option('--api-url', required=True, help='API server for user\'s pds. Example: https://bsky.app/xrpc')
@click.option('--token', required=True, help='Token issued at Fujitsu Research Portal')
@click.option('--channel', required=True, help='Channel name')
@click.option('--model-name', help='OpenAI model name', default='gpt-3.5-turbo')
@click.option('--prompt-file', required=True, help='path to your prompt file')
@click.option('--cert', help='path to cert file to atproto server', default=None)
def run(handle, password, api_url, token, channel, model_name, prompt_file, cert) :
    
    # atproto setup
    client = Client(base_url=api_url)
    profile = client.login(handle, password, portal_token=token)
    print(f"Successfully logged in: {profile.handle}")
    
    # OpenAI and prompt setup
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        print("set openai key: OPENAI_API_KEY")

    chat = ChatOpenAI(model_name=model_name,
                      max_tokens=300)
    
    with open(prompt_file) as f:
        template = f.read()

    prompt = PromptTemplate(
        template=template,
        input_variables = ["post"],
    )
    
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
        for record in response.records :
            value = record.value.model_dump()
            post_handle = value['handle']
            text = value['text']
            
            formatted_prompt = prompt.format(post=text)
            messages = [HumanMessage(content=formatted_prompt)]
            result = chat.invoke(messages).content
            
            print(formatted_prompt)
            print(result)
            print('---')
    
    return 

if __name__ == '__main__' :
    
    run()