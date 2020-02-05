import os
from SigProfilerMatrixGenerator import install as genInstall
genInstall.install(os.environ['REF'], bash=True)
print(os.environ['REF'])
print(f'{os.environ["REF"]} has been installed.')