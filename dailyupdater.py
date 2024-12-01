import os
import pickle
import datetime
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Pushbullet Notification Function
def send_pushbullet_notification(title, message):
    url = "https://api.pushbullet.com/v2/pushes"
    headers = {
        "Access-Token": os.getenv("PUSHBULLET_API_KEY"),  # Retrieve the API key from the environment
        "Content-Type": "application/json",
    }
    data = {
        "type": "note",
        "title": title,
        "body": message,
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Notificação enviada com sucesso!")
    else:
        print(f"Falha ao enviar notificação: {response.status_code}, {response.text}")

# Medication Object
class Medication:
    def __init__(self, name, stock, daily_intake, is_sleeping_med=False):
        self.name = name
        self.stock = stock
        self.daily_intake = daily_intake
        self.is_sleeping_med = is_sleeping_med

    def update_stock(self, amount):
        self.stock += amount
        # Prevent stock from going below zero
        if self.stock < 0:
            self.stock = 0

    def predict_end_date(self):
        if self.daily_intake == 0:
            return "Uso SOS, sem previsão de término.", "[Uso SOS, sem data para compra]"
        today = datetime.date.today()
        days_left = self.stock // self.daily_intake
        end_date = today + datetime.timedelta(days=days_left)
        buy_date = end_date - datetime.timedelta(days=10)
        return end_date, buy_date


# Check Stock and Send Notifications
def check_stock_and_notify(medication):
    end_date, buy_date = medication.predict_end_date()
    if medication.stock == 10:
        send_pushbullet_notification(
            "Lembrete de Medicamento",
            f"⚠️ Ian tem apenas 10 comprimidos de {medication.name}. Compre em {buy_date}."
        )
    elif medication.stock == 5:
        send_pushbullet_notification(
            "Alerta Crítico",
            f"⚠️ Crítico! Apenas 5 comprimidos restantes de {medication.name}. Compre imediatamente!"
        )
    elif medication.stock == 4:
        send_pushbullet_notification(
            "Alerta Crítico",
            f"⚠️ Restam somente 4 comprimidos de {medication.name}. Não esqueça de comprar!"
        )
    elif medication.stock == 3:
        send_pushbullet_notification(
            "Alerta Grave",
            f"⚠️ Atenção! Restam só 3 comprimidos de {medication.name}. Compre urgentemente!"
        )
    elif medication.stock == 2:
        send_pushbullet_notification(
            "Alerta Urgente",
            f"⚠️ Urgente! Apenas 2 comprimidos de {medication.name}. Reponha o estoque já!"
        )
    elif medication.stock == 1:
        send_pushbullet_notification(
            "Alerta Extremo",
            f"🚨 Só resta 1 comprimido de {medication.name}! Compre HOJE!"
        )
    elif medication.stock == 0:
        send_pushbullet_notification(
            "ALERTA URGENTE!",
            f"🚨 SEM REMÉDIO! Não há mais comprimidos de {medication.name}! VOCÊ PRECISA COMPRAR AGORA!!!!!!!"
        )


# Load Medications
def load_medications(filename="medications.pkl"):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []

# Save Medications
def save_medications(medications, filename="medications.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(medications, file)

# Get Last Run Date
def get_last_run_date(filename="last_run_date.txt"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return datetime.datetime.strptime(file.read().strip(), "%Y-%m-%d").date()
    else:
        return None

# Save Current Date as Last Run Date
def save_last_run_date(filename="last_run_date.txt"):
    with open(filename, "w") as file:
        file.write(datetime.date.today().strftime("%Y-%m-%d"))

# Daily Updater
def daily_updater():
    medications = load_medications()
    if not medications:
        print("Nenhum medicamento cadastrado.")
        return

    last_run_date = get_last_run_date()
    today = datetime.date.today()

    # If the program was not run today, calculate the days passed and adjust the stock
    if last_run_date:
        # Check if the last run was not today
        if last_run_date != today:
            days_passed = (today - last_run_date).days
            if days_passed > 0:
                print(f"Passaram {days_passed} dias desde a última execução. Ajustando os estoques.")
                for med in medications:
                    if med.daily_intake > 0:
                        med.update_stock(-med.daily_intake * days_passed)  # Subtract the appropriate number of pills
                    check_stock_and_notify(med)  # Check stock and send notifications
        else:
            print("Já foi executado hoje. Nenhuma alteração nos estoques.")
    else:
        print("Este é o primeiro uso ou a data não foi salva.")

    # Update the stock daily for non-SOS medications if it's a new day
    for med in medications:
        if last_run_date != today and med.daily_intake > 0:
            med.update_stock(-med.daily_intake)  # Subtract one day's worth of stock for non-SOS meds
        check_stock_and_notify(med)

        # Display updated stock for reference (optional)
        print(f"{med.name} atualizado: {med.stock} comprimidos restantes.")

    # Save updated medications and current date as last run date
    save_medications(medications)
    save_last_run_date()


# Main
if __name__ == "__main__":
    daily_updater()
