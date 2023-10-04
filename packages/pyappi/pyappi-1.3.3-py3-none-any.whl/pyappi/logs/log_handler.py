def log_handler(serial_id, path, key, time_group, value, parent):
    log_id = f'_{serial_id}.{time_group}'
    doc_type = parent.get_document_type()
    user = parent.get_user()
    user_id = parent.get_user_id()

    with doc_type(log_id,user, who_id=user_id) as doc:
        doc._perm[parent.get_id()] = "inherit"
        doc[path][key] = value