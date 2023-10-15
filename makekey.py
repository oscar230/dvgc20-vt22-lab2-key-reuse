import json
from typing import Union, Set
import llm
import time
import common

def get_cribs_at_position(data, position: int) -> Set[str]:
    cribs_at_position = set()
    for _, results in data.items():
        for result in results:
            if result['position'] == position:
                cribs_at_position.add(result['crib'])
    return cribs_at_position

def display_cribs_with_predictions(key: str, cribs: list[str]):
    prediction = llm.complete(key, cribs)
    print(prediction)
    
    for i, crib in enumerate(cribs, start=1):
        s = f"{i}. {key}"
        s += "_" if crib == ' ' else crib
        if crib in prediction:
            s += f" {prediction[crib]}"
        print(s)

def user_select_crib(cribs: list[str]) -> str:
    while True:
        try:
            selection_input = input(f"Select crib: ")
            if selection_input.lower() in ['q', 'quit', 'exit']:
                print("Exiting the program...")
                quit()  # This will exit the entire program
            selected_crib = cribs[int(selection_input) - 1]
            return selected_crib
        except:
            print(f"Nope! Select between 1 and including {len(cribs)} or type 'q' to quit.")
            time.sleep(0.5)  # Otherwise i cannot ctrl + c


def select_crib(key, data, position: int) -> Union[None, str]:
    cribs_at_position = list(get_cribs_at_position(data, position))
    
    if not cribs_at_position:
        return None

    display_cribs_with_predictions(key, cribs_at_position)
    selected_crib = user_select_crib(cribs_at_position)
    print(f"Selected: {selected_crib}")
    return selected_crib

def main():
    json_path = common.CRIBRESULTFILE
    with open(json_path, 'r') as file:
        data = json.load(file)
        key = ""
        while True:
            position = len(key)
            key_part = select_crib(key, data, position)
            if not key_part:
                print(key)
                quit()
            else:
                key += key_part

if __name__ == "__main__":
    main()
