from passpilot.agent import Agent
from passpilot.config import Config
import difflib

agent = Agent()

config = Config()

config.load('./douban.toml')

agent.perform(config)

# URL = "https://accounts.douban.com/passport/login"
# agent.visit(URL)

# agent.random_delay(1, 2)
# agent.click("//li[@class='account-tab-account']")

# html_before = agent.html()
# agent.humanoid_type("//input[@id='username']", "12233334444")
# agent.random_delay(1, 2)
# agent.humanoid_type("//input[@id='password']", "python")
# agent.random_delay(1, 2)
# agent.enter()

# html_after = agent.html()

# diff = difflib.HtmlDiff(wrapcolumn=50).make_file(
#     html_before.splitlines(), html_after.splitlines(), context=True)

# with open("diff.html", "w") as f:
#     f.write(diff)

while True:
    pass

agent.quit()
