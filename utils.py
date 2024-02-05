def search_entry(entry, query):
    for key, value in entry.items():
        if isinstance(value, str) and query.lower() in value.lower():
            return True
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    if search_entry(item, query):  # Recursive search in nested dictionaries
                        return True
    return False
