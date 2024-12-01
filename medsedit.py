import pickle
import datetime

# Medication Object
class Medication:
    def __init__(self, name, stock, daily_intake, is_sleeping_med=False):
        self.name = name
        self.stock = stock
        self.daily_intake = daily_intake
        self.is_sleeping_med = is_sleeping_med

    def update_stock(self, amount):
        self.stock += amount

    def predict_end_date(self):
        if self.daily_intake == 0:
            return "Uso SOS, sem previsão de término.", "Uso SOS, sem data para compra."
        today = datetime.date.today()  # This creates a datetime.date object
        days_left = self.stock // self.daily_intake
        end_date = today + datetime.timedelta(days=days_left)  # This is also a datetime.date object
        buy_date = end_date - datetime.timedelta(days=10)  # Also a datetime.date object
        return end_date, buy_date  # Return datetime.date objects

    def __str__(self):
        return f"{self.name}: {self.stock} comprimidos restantes."

# Save Medications
def save_medications(medications, filename="medications.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(medications, file)

# Load Medications
def load_medications(filename="medications.pkl"):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []

# List Medications
def list_medications(medications):
    if not medications:
        print("Nenhum medicamento cadastrado.")
        return
    print("\nMedicamentos cadastrados:")
    for i, med in enumerate(medications, start=1):
        print(f"{i} - {med.name}: {med.stock} comprimidos restantes")
    print()

# Add Medication
def add_medication(medications):
    name = input("Nome do medicamento: ")
    stock = int(input("Quantidade inicial de comprimidos: "))
    daily_intake = int(input("Quantidade diária (0 para SOS): "))
    is_sleeping_med = input("É um medicamento para dormir? (s/n): ").strip().lower() == 's'
    med = Medication(name, stock, daily_intake, is_sleeping_med)
    medications.append(med)
    save_medications(medications)
    print(f"{name} adicionado com sucesso!\n")

# Edit Medication
def edit_medication(medications):
    list_medications(medications)
    choice = int(input("Escolha o número do medicamento para editar: ")) - 1
    if 0 <= choice < len(medications):
        med = medications[choice]
        print(f"Editando {med.name}:")
        print("1 - Adicionar comprimidos")
        print("2 - Remover comprimidos")
        print("3 - Atualizar quantidade exata")
        action = input("Escolha uma ação: ").strip()
        if action == '1':
            amount = int(input("Quantos comprimidos deseja adicionar? "))
            med.update_stock(amount)
            print(f"Adicionados {amount} comprimidos a {med.name}.")
        elif action == '2':
            amount = int(input("Quantos comprimidos deseja remover? "))
            med.update_stock(-amount)
            print(f"Removidos {amount} comprimidos de {med.name}.")
        elif action == '3':
            exact_amount = int(input("Nova quantidade exata de comprimidos: "))
            med.stock = exact_amount
            print(f"Quantidade de {med.name} atualizada para {exact_amount}.")
        else:
            print("Opção inválida.")
        save_medications(medications)
    else:
        print("Medicamento inválido.")

# View Predictions
def view_predictions(medications):
    for med in medications:
        end_date, buy_date = med.predict_end_date()
        
        # Check if end_date and buy_date are datetime.date objects or strings
        if isinstance(end_date, datetime.date) and isinstance(buy_date, datetime.date):
            # Format the dates as DD/MM/YYYY
            end_date_str = end_date.strftime("%d/%m/%Y")
            buy_date_str = buy_date.strftime("%d/%m/%Y")
            print(f"{med.name}:")
            print(f"  Previsão de término: {end_date_str}")
            print(f"  Data sugerida para compra: {buy_date_str}\n")
        else:
            # Handle the case where end_date is a string (e.g., for SOS medications)
            print(f"{med.name}:")
            print(f"  {end_date}")  # This will print the string like "Uso SOS, sem previsão de término."

# Remove Medication
def remove_medication(medications):
    display_medications(medications)
    if not medications:
        return
    try:
        choice = int(input("Selecione o número do medicamento para remover: ")) - 1
        med = medications.pop(choice)
        print(f"Medicamento {med.name} removido com sucesso.")
    except (IndexError, ValueError):
        print("Seleção inválida.")

# Skip Sleeping Medication
def skip_sleeping_medication(medications):
    for med in medications:
        if med.is_sleeping_med:
            print(f"Pulando {med.name} hoje (nenhuma alteração no estoque).")
        else:
            med.update_stock(-med.daily_intake)
    save_medications(medications)
    print("Estoque atualizado para os outros medicamentos.")

# Main Menu
def main():
    medications = load_medications()
    while True:
        print("\nGerenciador de Medicamentos:")
        print("1 - Listar medicamentos")
        print("2 - Adicionar medicamento")
        print("3 - Editar medicamento")
        print("4 - Ver previsões de término")
        print("5 - Pular dia de medicamento para dormir")
        print("6 - Sair")
        choice = input("Escolha uma opção: ").strip()
        if choice == '1':
            list_medications(medications)
        elif choice == '2':
            add_medication(medications)
        elif choice == '3':
            edit_medication(medications)
        elif choice == "4":
            remove_medication(medications)
        elif choice == '5':
            view_predictions(medications)
        elif choice == '6':
            skip_sleeping_medication(medications)
        elif choice == '7':
            save_medications(medications)
            print("Alterações salvas. Saindo.")
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()
