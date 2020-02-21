from colorama import Fore, Style
import os
import pandas as pd


def clear_screen():
	os.system('cls' if os.name == 'nt' else 'clear')

def to_int(s):
	try:
		return int(s)
	except:
		return float("INF")

def print_menu():
	clear_screen()
	print(f"Olá, {NAME}! Escolha uma opção\n\n")
	print("1. Trocar nome")
	print("2. Quanto devo para cada um?")
	print("3. Quem e quanto me devem?")
	print("4. Pagar alguém")
	print("5. Roda de pagamento")
	print("6. Atualizar DataFrame")
	print("\n0. Sair")
	option = to_int(input("\nEscolha uma opção: "))
	while option not in range(6):
		print(f"{Fore.RED}ERRO - Esse opção não é válida. Tente novamente.{Style.RESET_ALL}")
		option = to_int(input("\nEscolha uma opção: "))
	clear_screen()
	return option

def set_name(mes="Digite o seu primeiro nome"):
	name = input(mes + ": ").capitalize()
	while name not in NAMES:
		print(f"{Fore.RED}ERRO - Esse nome não está cadastrado. Tente novamente.{Style.RESET_ALL}")
		name = input("Digite o seu primeiro nome: ").capitalize()
	clear_screen()
	return name

def get_data(d):
	if d == '2' or d == '2.0':
		return "Pagou"
	elif d == '1' or d == '1.0':
		return "Não Pagou"
	elif d == 'nan':
		return "  -  "
	return d

def print_cols():
	for col in list(gastos)[:12]:
		if len(col) < 8:
			print(col[:15], end="\t\t")
		else:
			print(col[:15], end="\t")
	print()

def print_row(row):
	for data in row[:12]:
		data = get_data(str(data))
		if len(data) < 8:
			print(data[:15], end="\t\t")
		else:
			print(data[:15], end="\t")
	print()

def print_rows_that_you_used():
	for index, row in gastos.iterrows():
		if not pd.isna(row[NAME]):
			print_row(row)

def calculate_debits_per_person():
	debits = [0]*len(NAMES)
	for index, row in gastos.iterrows():
		if row[NAME] == 1:
			idx = NAMES.index(row["Quem pagou"])
			debits[idx] += float(row["Preço por pessoa"].split()[-1].replace(",", "."))
	return debits

def print_debits_per_person(debits):
	total = 0
	for idx, name in enumerate(NAMES):
		if name == NAME: continue
		total += debits[idx]
		if len(name) < 7:
			print(f"{name}:\t  R${'%.2f' % debits[idx]}")
		elif len(name) < 8:
			print(f"{name}:  R${'%.2f' % debits[idx]}")
		else:
			print(f"{name}: R${'%.2f' % debits[idx]}")
	print(f"\nTOTAL:\t  R${'%.2f' % total}")

def debits():
	print(f"{NAME}, aqui estão seus débitos: ")
	print_cols()
	print_rows_that_you_used()

	print("\nQuanto você deve para cada um:\n")
	debits = calculate_debits_per_person()
	print_debits_per_person(debits)

	input("\n\nPress ENTER to return to menu")

def print_rows_that_you_paid():
	for index, row in gastos.iterrows():
		if row["Quem pagou"] == NAME:
			print_row(row)

def calculate_credits_per_person():
	credits = [0]*len(NAMES)
	for index, row in gastos.iterrows():
		if row["Quem pagou"] == NAME:
			for idx, name in enumerate(NAMES):
				if row[name] == 1:
					credits[idx] += float(row["Preço por pessoa"].split()[-1].replace(",", "."))
	return credits

def print_credits_per_person(credits):
	total = 0
	for idx, name in enumerate(NAMES):
		if name == NAME: continue
		total += credits[idx]
		if len(name) < 7:
			print(f"{name}:\t  R${'%.2f' % credits[idx]}")
		elif len(name) < 8:
			print(f"{name}:  R${'%.2f' % credits[idx]}")
		else:
			print(f"{name}: R${'%.2f' % credits[idx]}")
	print(f"\nTOTAL:\t  R${'%.2f' % total}")

def credits():
	print(f"{NAME}, aqui estão seus créditos: \n")
	print_cols()
	print_rows_that_you_paid()

	print("\nQuanto cada um te deve:\n")
	credits = calculate_credits_per_person()
	print_credits_per_person(credits)

	input("\n\nPress ENTER to return to menu")

def pay():
	receiver = set_name("Digite o nome de quem você quer pagar")
	idx = NAMES.index(receiver)
	credits = calculate_credits_per_person()
	debits = calculate_debits_per_person()
	if credits[idx]-debits[idx] >= 0:
		print(f"Que maravilha, {NAME}! Você não deve nada para {receiver}.")
	else:
		debit = debits[idx]-credits[idx]
		print(f"Pelos nossos calculos, você deve R${'%.2f' % debit} para {receiver}.\n")
		print("Para pagar, basta enviar esse valor para a conta abaixo:")
		for index, row in dados_bancarios.iterrows():
			if len(row["Dado"]) < 7:
				print(row["Dado"] + ": \t\t" + str(row[receiver]))
			else:
				print(row["Dado"] + ": \t" + str(row[receiver]))
	input("\n\nPress ENTER to return to menu")

def roda_de_gastos():
	global NAME
	old_name = NAME
	all_debits = []
	for name in NAMES:
		NAME = name
		credits = calculate_credits_per_person()
		debits = calculate_debits_per_person()
		diff = []
		for i in range(len(credits)):
			diff.append(debits[i]-credits[i])
		all_debits.append([sum(diff), NAME])

	all_debits = sorted(all_debits)[::-1]
	while(len(all_debits) > 1):
		print(f"{all_debits[0][1]} paga R${'%.2f' % all_debits[0][0]} ao {all_debits[-1][1]}")
		all_debits[-1][0] += all_debits[0][0]
		all_debits = sorted(all_debits[1:])[::-1]
	
	input("\n\nPress ENTER to return to menu")
	NAME = old_name

def update_gastos():
	gastos = pd.read_csv("https://docs.google.com/spreadsheets/d/1dCYfYqVfgioZQ5YXxrmSPXuiudIbfHvW4jj9tQQBq20/export?gid=0&format=csv")
	dados_bancarios = pd.read_csv("https://docs.google.com/spreadsheets/d/1dCYfYqVfgioZQ5YXxrmSPXuiudIbfHvW4jj9tQQBq20/export?gid=1968442958&format=csv")
	return gastos, dados_bancarios

clear_screen()

print(" ___________________________________________________")
print(f"/      {Fore.WHITE}Sejam bem-vindos, meus nobres puladores!{Style.RESET_ALL}     \\")
print(f"\\ {Fore.WHITE}Hora de contar quantos pulos cada um está devendo{Style.RESET_ALL} /")
print(" ---------------------------------------------------")
print("     \\")
print("      \\")
print(f"{Fore.GREEN}         oO)-.                       .-(@@\\")
print("         /__  _\                     /_  __\\")
print("         \  \(  |     ()~()         |  )/  /\\")
print("          \__|\ |    (-___-)        | /|__/\\")
print("          '  '--'    ==`-'==        '--'  '\\")
print(f"{Style.RESET_ALL}\n\n")


input("Press ENTER to continue")

clear_screen()

gastos, dados_bancarios = update_gastos()
NAMES = ["Breno", "Bruno", "Caio", "Emanuel", "Henrique", "Pedro", "Rafael"]

NAME = set_name()
option = print_menu()

while option:
	clear_screen()
	if option == 1:
		NAME = set_name()
	elif option == 2:
		debits()
	elif option == 3:
		credits()
	elif option == 4:
		pay()
	elif option == 5:
		roda_de_gastos()
	elif option == 6:
		gastos, dados_bancarios = update_gastos()
	clear_screen()
	option = print_menu()
