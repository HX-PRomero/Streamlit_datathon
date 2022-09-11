import os
from time import sleep

while True:
    os.system('cmd /k "git add . & git commit -m "Actualización" & git push origin main"')
    sleep(900)