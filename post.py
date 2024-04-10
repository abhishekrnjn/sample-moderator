import os
import click

from atproto import Client

@click.command()
@click.option('--handle', required=True, help='your Atproto handle')
@click.option('--password', required=True, help='password of your account')
@click.option('--api-url', required=True, help='API server for user\'s pds. Example: https://bsky.app/xrpc')
@click.option('--token', required=True, help='Token issued at Fujitsu Research Portal')
@click.option('--channel', required=True, help='Channel name')
@click.option('--post-file', required=True, help='path to your text file including post text')

def run(handle, password, api_url, token, channel, post_file) :
    # atproto setup
    client = Client(base_url=api_url)
    profile = client.login(handle, password, portal_token=token)
    print(f"Successfully logged in: {profile.handle}")

    # List joined channels
    response = client.app.fujitsu.channel.list_channel_info()
    joined_channel_list = [cinfo.channel_handle for cinfo in response.channel_info if channel in cinfo.channel_handle]
    channel_name = joined_channel_list[0]
    print("Selected channel: ", channel_name)

    # Posts text separated by blank lines as a single post from the text file to the channel
    # Read posts
    with open(post_file, 'r') as f:
        post = ""
        for line in f:
            if line.strip()!="":
                post += line
            else:
                if post:
                   # Post
                   client.send_channel_post(text=post,channel=channel_name)
                   post = ""
        if post:
           # Post the last part
           client.send_channel_post(text=post,channel=channel_name)
    return

if __name__ == '__main__' :
    run()
