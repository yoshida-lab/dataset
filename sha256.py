# Copyright 2019 TsumiNa. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


def sha256(fname):
    from hashlib import sha256
    hasher = sha256()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def refresh(*fname, records='sha256.json'):
    import json
    with open(records, 'r') as f:
        sha_ = json.load(f)
    for n in fname:
        sha_ = dict(sha_, **{k: v for k, v in ((n, sha256(n)),)})
    with open(records, 'w') as f:
        json.dump(sha_, f, indent=4, sort_keys=True)
