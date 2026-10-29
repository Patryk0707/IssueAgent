import os
import urllib.request

# ntfy configuration
ntfy_server = os.environ.get("NTFY_SERVER", "https://ntfy.sh")
ntfy_topic = os.environ.get("NTFY_TOPIC", "")


def send_ntfy(title="IssueAgent notification", message="No message was provided", topic=None):
    topic = topic or ntfy_topic # User can enter a custom topic
    if not topic:
        print("NTFY_TOPIC is not set, notification not sent.")
        return False

    # Connect to server and send
    request = urllib.request.Request(
        f"{ntfy_server}/{topic}",
        data=message.encode("utf-8"),
        headers={"Title": title.encode("utf-8").decode("latin-1")},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10):
            return True
    except Exception as e:
        print(f"Failed to send ntfy notification: {e}")
        return False