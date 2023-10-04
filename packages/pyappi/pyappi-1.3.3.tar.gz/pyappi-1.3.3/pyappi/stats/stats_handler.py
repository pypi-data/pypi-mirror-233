from pyappi.stats.stats import StatsRecord
from pyappi.document.enumeration import lookup_document_id

def stats_handler(target_id, metric, serial_id=None):
    if serial_id:
        # Require global tallies on the user object
        if not target_id.startswith("user."):
            return

        target_id = lookup_document_id(serial_id)

    # Translate between first and third person.
    match metric:
        case "following":
            metric = "followers"
        case "subscriptions":
            metric = "subscribers"
        case "views":
            metric = "view"

    match metric:
        case "likes" | "comments" | "reviews" | "followers" | "subscribers" | "favorites" | "view" | "time":
            with StatsRecord(target_id) as record:
                record[metric] += 1
        case _:
            pass