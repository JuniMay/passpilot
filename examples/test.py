
from passpilot.config import Config
from passpilot.agent import Agent
from argparse import ArgumentParser
import os
import openai

argparser = ArgumentParser()
argparser.add_argument("-c", "--config", help="config file path")
argparser.add_argument("-k", "--api-key", help="api key for openai")

args = argparser.parse_args()

if args.api_key!=None:
    openai.api_key = args.api_key
else:
    openai.api_key=os.getenv("OPENAI_API_KEY")
print(args.api_key,os.getenv("OPENAI_API_KEY"))



config = Config()
config.load(args.config)
print(config.data)
agent = Agent(config)
agent.perform(config)

while True:
    pass

agent.quit()
