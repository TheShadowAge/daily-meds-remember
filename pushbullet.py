import requests

def send_pushbullet_notification(title, message):
    url = "https://api.pushbullet.com/v2/pushes"
    headers = {
        "Access-Token": "o.opdC18awENiGE6dVYGS29cckfU6LSg8P",  # Replace with your Pushbullet Access Token
        "Content-Type": "application/json",
    }
    data = {
        "type": "note",  # Push type: note for text notifications
        "title": title,
        "body": message,
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Notification sent successfully!")
    else:
        print(f"Failed to send notification: {response.status_code}, {response.text}")

# Example Usage
send_pushbullet_notification(
    "Medication Alert",
    "⚠️ You have only 5 pills left for Desvenlafaxina. Restock soon!"
)
