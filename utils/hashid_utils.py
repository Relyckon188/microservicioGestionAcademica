from app import hashids

def encode_id(id_num: int) -> str:
    return hashids.encode(id_num)

def decode_id(hashid: str) -> int | None:
    ids = hashids.decode(hashid)
    return ids[0] if ids else None
