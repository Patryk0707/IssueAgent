def codeInputToAgent(agent):
    code=input("Enter code for the agent to check for errors")
    message=f"""
    Check for any errors with the code provided by the user. If there aren't any errors, say No errors. Otherwise provide them with what the issue was and what lines need to be replaced for the code to work.
    Code:{code}
    """
    return agent.nebiusAgent(message)

