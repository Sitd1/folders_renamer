from renamer import Renamer
from utils import get_config
from time import sleep

rn = Renamer(get_config('config.yaml'))
rn.rename()

print('done!')
sleep(10)
print('closing')
for i in range(5,1):
    print(i)
    sleep(1)

