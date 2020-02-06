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
	print("4. Atualizar DataFrame")
	print("\n0. Sair")
	option = to_int(input("\nEscolha uma opção: "))
	while option not in range(5):
		print(f"{Fore.RED}ERRO - Esse opção não é válida. Tente novamente.{Style.RESET_ALL}")
		option = to_int(input("\nEscolha uma opção: "))
	clear_screen()
	return option

def set_name():
	name = input("Digite o seu primeiro nome: ").capitalize()
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
	for col in list(df)[:12]:
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
	for index, row in df.iterrows():
		if not pd.isna(row[NAME]):
			print_row(row)

def calculate_debits_per_person():
	debits = [0]*len(NAMES)
	for index, row in df.iterrows():
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
	for index, row in df.iterrows():
		if row["Quem pagou"] == NAME:
			print_row(row)

def calculate_credits_per_person():
	credits = [0]*len(NAMES)
	for index, row in df.iterrows():
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

def update_df():
	return pd.read_csv("https://docs.google.com/spreadsheets/d/1dCYfYqVfgioZQ5YXxrmSPXuiudIbfHvW4jj9tQQBq20/export?gid=0&format=csv")
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

df = update_df()
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
		df = update_df()
	clear_screen()
	option = print_menu()