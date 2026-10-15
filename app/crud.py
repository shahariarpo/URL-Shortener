from app.utils import now_iso, generate_code

def row_to_dict(row, include_stats: bool = False):
    data = {
        "id": str(row["id"]),
        "url": row["url"],
        "shortCode": row["short_code"],
        "createdAt": row["created_at"],
        "updatedAt": row["updated_at"]
    }
    if include_stats:
        data["accessCount"] = row["access_count"]
    return data

def get_by_code(conn, code: str):
    return conn.execute("SELECT * FROM urls WHERE short_code = ?", (code,)).fetchone()


def create_url(conn, url: str):
    code = generate_code(conn)
    now = now_iso()
    conn.execute("INSERT INTO urls (url, short_code, created_at, updated_at)"
                "VALUES (?, ?, ?, ?)",
                (url, code, now, now),
                )
    conn.commit()
    return get_by_code(conn, code)

def increment_access(conn, code: str):
    conn.execute("UPDATE urls SET access_count = access_count + 1 WHERE short_code = ?", (code,))
    conn.commit()

def update_url(conn, code:str, url: str):
    now = now_iso()
    conn.execute("UPDATE urls SET url = ?, updated_at = ? WHERE short_code = ?", (url, now, code,))
    conn.commit()
    return get_by_code(conn, code)

def delete_url(conn, code: str):
    conn.execute("DELETE FROM urls WHERE short_code = ?", (code,))
    conn.commit()