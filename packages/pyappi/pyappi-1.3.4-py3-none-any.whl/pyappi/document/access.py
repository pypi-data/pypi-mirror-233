from pyappi.api_base import get_document_type as dt
from fastapi import Response


def document_with_write_access(document_id, session, callback):
    user = session["user"]
    try:
        with dt()(document_id, user, who_id=session["id"]) as doc:
            permissions = doc._perm.unwrap()

            if not len(permissions):
                doc._perm[user] = "owner"
                return callback(doc)

            if user in permissions:
                level = permissions[user]
            elif "_inherit" in permissions:
                level = lookup_inherited_permissions(permissions["_inherit"], user) or permissions.get("public",None)
            else:
                level = permissions.get("public",None)
                
            match session.get("type",""):
                case "comments":
                    return callback(doc.comments_type_log) if permissions.get("comments","") == "enable" else Response(status_code=403)
                case _:
                    pass	

            match level:
                case "write" | "owner":
                    return callback(doc)
                case "blind_write":
                    return callback(doc["mail~log"])
                case _: 
                    return Response(status_code=409)
    except Exception as e:
        return Response(status_code=422)
    
def document_with_owner_access(document_id, session, callback):
    user = session["user"]
    try:
        with dt()(document_id, user) as doc:
            permissions = doc._perm.unwrap()

            if not len(permissions):
                return callback(doc)

            level = permissions.get("public",None)

            if user in permissions:
                level = permissions[user]

            match level:
                case "owner":
                    return callback(doc)
                case _: 
                    return Response(status_code=409)
    except Exception as e:
        return Response(status_code=422)

def lookup_inherited_permissions(inherited, user):
    for document_id, control_level in inherited.items():
        with dt()(document_id, "server", read_only = True) as base:
            permissions = base._perm.unwrap()

            if user in permissions:
                return control_level if control_level else permissions[user]
        

def document_with_read_access(document_id, session):
    user = session["user"]
    try:
        
        with dt()(document_id, user) as base, dt()(document_id, user, session=session) as doc:
            permissions = base._perm.unwrap()

            match session.get("type",""):
                case "stats":
                    return doc.unwrap() if permissions.get("stats","") == "enable" else {}
                case "comments":
                    return {"comments~log":doc.comments_type_log.unwrap()} if permissions.get("comments","") == "enable" else {}
                case _:
                    pass
                
            level = None

            if user in permissions:
                level = permissions[user]
            elif "_inherit" in permissions:
                level = lookup_inherited_permissions(permissions["_inherit"], user) or permissions.get("public",None)
            else:
                level = permissions.get("public",None)

            match level:
                case "read" | "write" | "owner" | "unlisted":
                    return doc.unwrap()
                case  "blind_write":
                    return {}
                case _: 
                    return {}
    except Exception as e:
        return None

    """			std::string Get(std::string_view _real_id, const Session& session)
			{
				auto [real_id, query] = d8u::util::split_pair(_real_id, "@");

				auto *record = GetRecord(real_id);
				std::string_view p_cap;

				if (record)
				{
					auto permissions = record->index("_perm");
					if (session.requested_permission.starts_with("child_"))
					{
						// Proxy to child resource
						auto child_resource_name = std::string_view(session.requested_permission.data() + 6, session.requested_permission.size() - 6);
						d8u::util::replace_char(child_resource_name, ',', '.');

						//auto children = record->index("_children");
						//auto child_id = children[child_resource_name];
						auto* child = GetRecord(child_resource_name);

						if (!child)
							return "";

						if (child->index("_perm")[real_id] != "inherit")
							p_cap = std::string_view(child->index("_perm")[real_id]);

						//TODO Fix query by replacing real_id@query with child_id@query
						record = child;
					}
					else if (real_id[0] == '_')
					{
						auto nid = std::stoull(real_id.data()+1);
						auto* parent = GetRecord(std::string("!") + std::to_string(nid));

						if (!parent)
							return "";

						if (!session.HaveReadAccess(parent->index("_perm")))
							return "";

						return record->data;
					}
					else
					{
						switch (switch_t(session.requested_permission)) {
						case switch_t("member"):
							if (session.app != "APPIUSERS")
								return "";

							return "{}"; // TODO SHARE RELEVANT USER DATA WITH MEMBER APPS
						case switch_t("public"):
						{
							auto _public = record->index("~public");

							// Return the public region if it exists
							if (_public.Valid())
								return std::string(_public.Json());

							// Check if this is a public resource and return that
							if (session.HaveReadAccess(permissions))
								return record->data;

							return "";
						}
						case switch_t("share"):
						{
							auto share = record->index("~share");
							auto user_mask = share("access")(session.user);
							auto public_mask = share("access")("public");

							if (user_mask.Valid())
								return Mask(share("data"), user_mask);
							else if (public_mask.Valid())
								return Mask(share("data"), public_mask);

							return "";
						}
						default:
							break;
						}
					}

					if (!session.HaveReadAccess(permissions, p_cap))
						return "";

					if (query.size())
						return provider.Get(_real_id);

					return record->data;
				}

				return "";
			}"""