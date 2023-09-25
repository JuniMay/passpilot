from passpilot.agent import Agent
from passpilot.config import Config
from argparse import ArgumentParser

argparser = ArgumentParser()
argparser.add_argument("-c", "--config", help="config file path")

args = argparser.parse_args()
agent = Agent()
config = Config()
config.load(args.config)
agent.perform(config)

while True:
    pass

agent.quit()
