import json
from typing import Union, Set
import llm
import time
import common

AUTO: bool = True

def get_avaliable_cribs_at_position(data, position: int) -> list[str]:
    cribs_at_position = set()
    for _, results in data.items():
        for result in results:
            if result['position'] == position:
                cribs_at_position.add(result['crib'])
    return list(cribs_at_position)

def predict_crib(key: str, cribs: list[str]) -> str:
    prediction = llm.predict(key, cribs)
    sorted_predictions = sorted(prediction.items(), key=lambda x: x[1])
    for s in sorted_predictions:
        print(s)
    return sorted_predictions[0][0]

def select_crib(key: str, cribs: list[str]):
    if len(key) > 0 and key[-1] != ' ' and ' ' in cribs:
        print("Space added.")
        return ' '
    else:
        if AUTO and len(key) > 0:
            # Make prediction using LLM
            return predict_crib(key, cribs)
        else:
            # Display user interaction
            return interactive_selection(cribs)

def interactive_selection(cribs: list[str]) -> str:
    # List cribs
    for i, crib in enumerate(cribs, start=1):
        s = f"{i}. {key}"
        s += "_" if crib == ' ' else crib
        print(s)
    # Interactive selection
    while True:
        try:
            selection_input = input(f"Select crib: ")
            if selection_input.lower() in ['q', 'quit', 'exit']:
                quit()
            selected_crib = cribs[int(selection_input) - 1]
            return selected_crib
        except:
            # Selection failed, will let user try again
            print(f"User input error! Select between 1 and including {len(cribs)} or type 'q' to quit.")
            time.sleep(0.5)  # Otherwise i cannot ctrl + c

if __name__ == "__main__":
    with open(common.CRIBRESULTFILE, 'r') as file:
        print(f"Loading {common.CRIBRESULTFILE}, please wait...")
        data = json.load(file)
    if data:
        key: str = ""
        next_sub_key: Union[str, None] = "#"
        while next_sub_key:
            # Get cribs avaliable at the key's current postition
            next_position = len(key)
            avaliable_cribs = get_avaliable_cribs_at_position(data, next_position)
            if not avaliable_cribs:
                # There are no cribs avaliable at this postition, the crib drag might be completed or this is an unexpected error
                print("No cribs avaliable")
                next_sub_key = None
            else:
                # There are cribs avaliable, make a selection
                next_sub_key = select_crib(key, avaliable_cribs)
                key += next_sub_key
            print(f"Key:{key}")
        print(f"Done")
        quit()