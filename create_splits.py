import os
import argparse
import numpy as np

def main(args):
    audstems = ''.join([str(a) for a in args.files])[1:-1]
    print(audstems)
    audstems = [int(item) for item in audstems.split(',')]
    with open(os.path.join(args.folder, args.filename), 'r') as f:
        data = f.read()
    data = data.split('\n')
    data = [d.split(',') for d in data if len(d)>0]
    mismatch = np.array([d for d in data if d[1] == '2'][:args.num_mismatch])[:, 0].tolist()
    correct = np.array([d for d in data if d[1] == '1'][:args.num_correct])[:, 0].tolist()
    completed_ids = np.array(data)[:, 0]
    remaining_ids = [a for a in audstems if a not in completed_ids][:50]
    common_ids = remaining_ids[:args.num_common]
    remaining_ids = np.array(remaining_ids[args.num_common:])
    splits = np.array_split(remaining_ids, args.num_splits)
    print(mismatch)
    print(correct)
    print(common_ids)
    splits = [np.append(split, mismatch+correct+common_ids) for split in splits]
    for idx, split in enumerate(splits):
        with open(args.folder+str(idx)+'.txt', 'w') as f:
            f.writelines([s+'\n' for s in split])

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Process some integers.')
  parser.add_argument('--folder', required=True, help='Folder name for the data')
  parser.add_argument('--num_mismatch', default=20)
  parser.add_argument('--num_common', default=20)
  parser.add_argument('--num_correct', default=20)
  parser.add_argument('--filename', default='verified_output.csv')
  parser.add_argument('--files', required=True, type=str, nargs='+')
  parser.add_argument('--num_splits', default=3, help='number of validators')
  args = parser.parse_args()
  main(args)
