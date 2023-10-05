import teradatasql

from genpypress import session


def get_stats(
    spec: str,
) -> str:
    try:
        database, table = spec.split(".")
    except ValueError:
        return spec

    stats = _stats_from_tera(database, table)
    if not stats:
        return spec
    return stats


def _stats_from_tera(
    database: str,
    table: str,
) -> str | None:
    sql = f"show stats on {database}.{table};"
    print("--", sql)
    print(f"-- user:     {session.DEFAULT_USER}")
    print(f"-- password: {session.DEFAULT_PASSWORD[0:3]}**************")
    print(f"-- logmech:  {session.DEFAULT_LOGMECH}")
    try:
        with session.connect_teradata() as sess:
            with sess.cursor() as cur:
                rows = ["\n".join(r[0].splitlines()) for r in cur.execute(sql)]
    except teradatasql.DatabaseError as err:
        print("/*", err, "*/")
        return None

    return "".join(rows)
