def changes_since(document, tsx):

    return changes_since_dict(document.__dict__["__document"], tsx)


def changes_since_dict(document, tsx):
    result = {}

    def _recursive_changes(current):
        cmt,vmt = (current.get("_cmt",-1),current.get("_vmt",-1))

        if cmt <= tsx and vmt <= tsx:
            return None

        delta = {}

        if cmt > tsx:
            for key,value in current.items():
                if not isinstance(value,dict):
                    continue

                _delta = _recursive_changes(value)
                if _delta:
                    delta[key] = _delta

        if vmt > tsx:
            for key,value in current.items():
                if isinstance(value,dict):
                    continue

                delta[key] = value
            
        return delta

    result = _recursive_changes(document)

    return result

