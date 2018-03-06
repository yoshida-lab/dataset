# Copyright 2017 TsumiNa. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from pathlib import Path

import pandas as pd


if __name__ == '__main__':
    db_path = Path(__file__).parent
    data = pd.read_csv(str(db_path / 'completed.csv'))
    data = data.rename(lambda i: data.loc[i, 'symbol']).drop('symbol', axis=1)
    data.to_pickle(str(db_path / 'elements_completed.pkl'))
