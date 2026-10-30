from Agent import agent

agentObject=agent()

def codeInputToAgent():
    print("Enter code for the agent to check for errors and type 'END' on a new line when finished entering code")
    lines=[]
    while True:
        line=input()
        lines.append(line)
        if line=="END":
            break
    code="\n".join(lines)

    message=f"""
    Check for any errors with the code provided by the user."END" is the end of the code and not part of the code. In your message the first line should be the short overview of the result containing the name of the error and the line number. It is used as a header for emails. If there aren't any errors, say No errors. Otherwise provide them with what the issue was and what lines need to be replaced for the code to work.
    Code:{code}
    """
    return agentObject.nebiusAgent(message)

