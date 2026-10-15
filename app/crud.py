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
    return conn.execute("SELECT FROM urls WHERE short_code = ?", (code,))