import fire

def testfn():
  print('in test.py with fire.Fire')

if __name__ == '__main__':
  fire.Fire(testfn)