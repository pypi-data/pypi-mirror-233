from uuid import uuid4 as uuid

def generate_randon_hash() -> str:
    """Generate a random hash"""
    return str(hash())
