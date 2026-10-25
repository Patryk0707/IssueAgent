from Agent import agent

agentObject=agent()

def codeInputToAgent():
    print("Enter code for the agent to check for errors")
    lines=[]
    while True:
        line=input()
        lines.append(line)
        if line=="END":
            break
    code="\n".join(lines)
    


    message=f"""
    Check for any errors with the code provided by the user. If there aren't any errors, say No errors. Otherwise provide them with what the issue was and what lines need to be replaced for the code to work.
    Code:{code}
    """
    return agentObject.nebiusAgent(message)

