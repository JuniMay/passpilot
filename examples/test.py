
from passpilot.config import Config
from passpilot.agent import Agent
from argparse import ArgumentParser

import zhipuai

argparser = ArgumentParser()
argparser.add_argument("-c", "--config", help="config file path")
argparser.add_argument("-k", "--api-key", help="api key for zhipuai")

args = argparser.parse_args()

zhipuai.api_key = args.api_key


config = Config()
config.load(args.config)
print(config.data)
agent = Agent(config)
agent.perform(config)

while True:
    pass

agent.quit()
