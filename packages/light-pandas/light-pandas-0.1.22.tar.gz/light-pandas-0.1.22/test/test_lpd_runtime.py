import sys
import time
sys.path.append('../')
import lightpandas as lpd
import random
import pandas as pd


def main():
    start_ts = time.time()
    col1 = ['i1' for _ in range(10000)] + ['i2' for _ in range(10000)] + ['i3' for _ in range(10000)]
    col2 = [idx for idx in range(30000)]
    df = lpd.DataFrame({'item1': col1, 'item2': col2})
    # df = pd.DataFrame(columns=['item1', 'item2'])
    # for idx in range(30000):
    #     if idx < 10000:
    #         df = df.append({'item1': 'i1', 'item2': idx}, ignore_index=True)
    #     else:
    #         df = df.append({'item1': 'i2', 'item2': idx}, ignore_index=True)
    created_ts = time.time()
    print('Create in {}'.format((created_ts - start_ts)))
    tmp_df = df[df['item1'] == 'i2']
    print(len(tmp_df))
    end_ts = time.time()
    print('Scan in {}'.format((end_ts - created_ts)))


if __name__ == '__main__':
    main()
