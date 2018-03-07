def sha256(fname):
    from hashlib import sha256
    hasher = sha256()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def refresh(fname, records='sha256.json'):
    import json
    with open(records, 'r') as f:
        sha_ = json.load(f)
    sha_ = dict(sha_, **{k: v for k, v in ((fname, sha256(fname)), )})
    with open(records, 'w') as f:
        json.dump(sha_, f, indent=4, sort_keys=True)
