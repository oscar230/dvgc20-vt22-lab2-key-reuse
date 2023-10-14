import json
from typing import Union

def select_crib(data, position: int) -> Union[None, str]:
    cribs_at_position = set()  # Using a set to automatically remove any duplicates

    for _, results in data.items():
        for result in results:
            if result['position'] == position:
                cribs_at_position.add(result['crib'])
    
    cribs = list(cribs_at_position)
    if len(cribs) == 0:
        return None
    else:
        for i, crib in enumerate(cribs, start=1):
            if crib == ' ':
                print(f"{i}. _SPACE_")
            else:
                print(f"{i}. {crib}")

        selected_crib: str = ''
        while selected_crib not in cribs:
            try:
                selection_input: str = input(f"Select: ")
                selected_crib = cribs[int(selection_input) - 1]
            except:
                print(f"Nope! Select between 1 and including {len(cribs)}")

        print(f"Selected: {selected_crib}")
        return selected_crib

if __name__ == "__main__":
    json_path = "crib_drag_results.json"
    with open(json_path, 'r') as file:
        data = json.load(file)
        key: str = ""
        while True:
            position: int = len(key)
            print(f"\tKey:\t{key}\n\tPos:\t{position + 1}")
            key_part: Union[None, str] = select_crib(data, position)
            if not key_part:
                print(key)
                quit()
            else:
                key += key_part
