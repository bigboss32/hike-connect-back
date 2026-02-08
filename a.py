import os
import requests


def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandbox63dc323f9f7445e8aa2c56548c8c87ec.mailgun.org/messages",
        auth=(
            "api",
            os.getenv("API_KEY", "41da8d6a34f2809ad8f8eeda2715271f-f39109fe-0c658bbb"),
        ),
        data={
            "from": "Mailgun Sandbox <postmaster@sandbox63dc323f9f7445e8aa2c56548c8c87ec.mailgun.org>",
            "to": "Miguel angel <portaes199888@gmail.com>",
            "subject": "Hello Miguel angel",
            "text": "Congratulations Miguel angel, you just sent an email with Mailgun! You are truly awesome!",
        },
    )


if __name__ == "__main__":
    response = send_simple_message()

    print("Status:", response.status_code)
    print("Response:", response.text)
