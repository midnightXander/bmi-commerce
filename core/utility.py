from .models import Item

def parse_id(number):
    if number < 10:
        return f"00{number}"
    elif number <= 100:
        return f"0{number}"
    else:
        return str(number)

def item_ref(item_name:str):
    n_items = len(Item.objects.all())
    decomposed = item_name.split()
    ref = ""
    for name in decomposed:
        ref += name[0]
    ref = ref.upper()

    number_id = parse_id(3)
    ref += f"-{number_id}"
    
    return ref


