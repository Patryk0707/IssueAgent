from Agent import agent
from gitingest import ingest
import contextlib
from loguru import logger
def checkRepoByCode(repo):
    agentObject=agent()

    with contextlib.suppress(ValueError):
        logger.remove()
    try:
# Pull from a specific branch (e.g., 'development' or 'v2-release')
        summary, tree, content = ingest(repo)
    except Exception as E:
        return f"Could not access repository. Please make sure the github repository is public and the URL is correct: {repo}"


# Pull only from a specific subfolder inside a branch to save space
#summary, tree, content = ingest("https://github.com/src/requests")

    codebase_context = f"{tree}\n\n{content}"
    message=f"""
    Check for any errors with the code in the github repository provided by the user. In your message the first line should be the short overview of the result containing the name of the error and the line number. It is used as a header for emails. If there aren't any errors, say No errors. Otherwise provide them with what the issue was and what lines need to be replaced in what file for the code to work in a easy to read layout.Use readme file for context if it exists
    files in repository:{codebase_context}
    """
    return agentObject.nebiusAgent(message)