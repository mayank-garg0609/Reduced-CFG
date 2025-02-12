from os import remove
def read_symbols(symbol_type):
  while True:
    input_string = input(f"Enter {symbol_type} separated by spaces: ")
    symbols = input_string.split()

    if all(len(char) == 1 for char in symbols):
      print(f"{symbol_type} entered:", symbols)
      return symbols
    else:
      print("Invalid input: Each entry should be a single character.")

def handle_common_elements(vars, const):

  common_elements = set(vars) & set(const)
  if common_elements:
    print("There are common characters in both Terminal and Non-terminal")
    choice = input("Do you want to change Terminal(enter 't') or Non-terminal variables(enter anything else) ? ").lower()
    if choice == 't':
      const = read_symbols("Terminal variables")
    else:
      vars = read_symbols("Non-terminal variables ")

    return handle_common_elements(vars, const)
  else:
    return vars, const

def read_starting_terminal(vars):
  while True:
    char = input("Enter Starting Terminal for grammar: ")
    if len(char) == 1 and char in vars:
      start = char
      break
    elif len(char) != 1:
      print("Please enter only one character.")
    else:
      print("Enter a character from Non-terminal only.")

  print("Starting Non-terminal entered:", start)
  return start

def read_production_rules(vars, all_elements):
  prod = []
  while True:
    string = input("Enter production rule (Aa means A->a) (or type 'done' to finish): ")
    if string == 'done':
      break
    if len(string) > 0 and string[0] in vars:
      if all(char in all_elements for char in string[1:]):
        prod.append(string)
      else:
        print("The production rule of " + str(string[0]) + " must contain only terminal and non-terminals.")
    elif len(string) == 0:
      print("You entered an empty string.")
    else:
      print("1st char should be a Non-terminal.")
  for string in prod:
    print(string[0] + '->' + string[1:])
  return prod

def remove_duplicate_strings(input_list):

  seen_strings = set()
  result_list = []
  for string in input_list:
    if string not in seen_strings:
      seen_strings.add(string)
      result_list.append(string)
  return result_list

vars = read_symbols("Non-terminal variables ")
const = read_symbols("Terminal variables")

vars, const = handle_common_elements(vars, const)
all_elements = set(vars) | set(const)

productions = read_production_rules(vars, all_elements)
productions=remove_duplicate_strings(productions)

start = read_starting_terminal(vars)

def remove_non_generating_values(productions, const):
  print("Removal of non generating value \n")
  gen = []
  i = 1
  for string in productions:
    if all(char in const for char in string[1:]):
      gen.append(string[0])
      const.append(string[0])
  if len(gen)==0:
    print("There are no generating variable in production rule")
    return [],[]
  else:
    print("Generating variables" + str(i) + str(gen))

  while True:
    j = 0
    for string in productions:
      if string[0] not in gen:
        if all(char in const for char in string[1:]):
          gen.append(string[0])
          const.append(string[0])
          j += 1
    if j == 0:
      break
    i += 1
    print("Generating variables" + str(i) + str(gen))

  prod = []
  for string in productions:
    if string[0] in gen:
      prod.append(string)
      print(string[0] + '->' + string[1:])

  return prod , gen

def remove_non_reachable_states(productions, start_symbol):
  print("\nRemoval of non reachable state \n")
  reachable = [start_symbol]
  i = 1
  print(f"Reach{i}-{reachable}")

  while True:
    j = 0
    for string in productions:
      if string[0] in reachable:
        for char in string[1:]:
          if char not in reachable:
            reachable.append(char)
            j += 1
    if j == 0:
      break
    i += 1
    print(f"Reach{i}-{reachable}")

    prod=[]
    for string in productions:
      if all(char in reachable for char in string[0:]):
            prod.append(string)
            print(string[0] + '->' + string[1:])

  return reachable , prod


productions , vars = remove_non_generating_values(productions, const)
reach , productions = remove_non_reachable_states(productions, start)

final_vars = set(vars) & set(reach)
final_const = set(const) & set(reach)
