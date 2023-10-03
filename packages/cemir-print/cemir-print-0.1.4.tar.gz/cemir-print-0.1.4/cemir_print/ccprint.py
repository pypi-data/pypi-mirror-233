# 4 Color https://talyian.github.io/ansicolors/
color_codes_types = {
    'str': '\033[92m',
    'dict': '\033[91m',
    'list': '\033[96m',
    'int': '\x1b[35m',
    'float': '\x1b[38;5;203m',
    'bool': '\033[95m'
}

color_codes = {
    'key': '\033[93m',
    'reset': '\033[0m'  # Sıfırla
}


def ccprint(data, depth=0):
    data_type = type(data).__name__  # Veri tipinin adını alır
    if not data_type in color_codes_types:
        print(data)
    try:
        if data_type == 'dict':
            for key, value in data.items():
                key_output = f"{color_codes['key']}{key}{color_codes['reset']}"
                if isinstance(value, (dict, list)):
                    print(f"\t" * depth + f"{key_output} ({type(value).__name__}):")
                    ccprint(value, depth + 1)
                else:
                    if isinstance(value, (str, int, bool, float)):
                        value_output = f"{color_codes_types[type(value).__name__.lower()]}{value}{color_codes['reset']}"
                    else:
                        value_output = str(value)
                    print(f"\t" * depth + f"{key_output}: {value_output} ({type(value).__name__})")
        elif data_type == 'list':
            for i, item in enumerate(data):

                item_output = f"{color_codes_types[type(item).__name__.lower()]}{item}{color_codes['reset']}"
                print(f"\t" * depth + f"{color_codes['key']}{i}:{color_codes['reset']} {item_output} ({type(item).__name__})")
                if isinstance(item, (dict, list)):
                    ccprint(item, depth + 1)

        else:
            if data_type in color_codes_types:
                color_code = color_codes_types[data_type]
                print(f"\t" * depth + f"{color_code}{data}{color_codes['reset']} ({data_type})")
            else:
                print(f"\t" * depth + f"{data} ({data_type})")

    except: ## typeerror vs oluşrsa direk print
        print(data)
