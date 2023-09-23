from passpilot.agent import Agent

import difflib

agent = Agent()

URL = "https://accounts.douban.com/passport/login"
agent.visit(URL)

html_before = agent.html()

agent.scroll_to("//input[@type='text']")
agent.humanoid_type("//input[@type='phone']", "12233334444")
agent.random_delay(1, 2)
agent.humanoid_type("//input[@type='text']", "python")
agent.random_delay(1, 2)
agent.enter()

html_after = agent.html()

diff = difflib.HtmlDiff(wrapcolumn=50).make_file(
    html_before.splitlines(), html_after.splitlines(), context=True)

with open("diff.html", "w") as f:
    f.write(diff)

# while True:
#     pass

agent.quit()
