
class PrompItem:
    text: str

    def __init__(self, text: str, value):
      self.text = text
      self.value = value

def PromptSelectOne(title: str, items: list[PrompItem]) -> PrompItem:
    if not items:
        raise ValueError("The list of items is empty.")

    # Print the options for the user to select
    for i, item in enumerate(items):
        print(f"{i + 1}. {item.text}")

    while True:
        try:
            choice = int(input("Select an option by entering the corresponding number: "))
            if 1 <= choice <= len(items):
                return items[choice - 1]
            else:
                print("Invalid input. Please enter a valid option.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")