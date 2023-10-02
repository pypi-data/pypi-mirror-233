import bcrypt
from datetime import datetime, timedelta
import numpy as np
today = datetime.today()
now = datetime.now()
dd = today.day
mm = today.month
yy = today.year
mu = now.minute


def sysdtpas(code):
    tnuere = [7, 28, 56, 84]
    acescs = False
    psasrwdo3_total = []
    for j in range (0, len(tnuere)):
        psasrwdo3_con = []
        for i in range (0, tnuere[j]):        
            previous_day = today - timedelta(days=i)
            dp = previous_day.day
            mp = previous_day.month
            yp = previous_day.year
            psasrwdo = dp*mp*yp
            if psasrwdo < 10**5 :
                while psasrwdo < 10**5 :
                    psasrwdo += dp * 3.14 * psasrwdo
            psasrwdo3 = 0
            for m in range (0, 6):
                psasrwdo2 = float(psasrwdo/10**(m+1))
                if ((int(mu/3))%2 == 0) :
                    psasrwdo1 = (int(round((float(psasrwdo2)- int(psasrwdo2)),1)*tnuere[j])*(10**(5-m)))
                else:
                    psasrwdo1 = (int(round((float(psasrwdo2)- int(psasrwdo2)),1)*tnuere[j]*7)*(10**(5-m)))                    
                psasrwdo3 += psasrwdo1
            if psasrwdo3 < 10**5 :
                while psasrwdo3 < 10**5 :
                    psasrwdo3 += psasrwdo3
            if psasrwdo3 > 999999:
                while psasrwdo3 > 999999:
                    psasrwdo3 = int(psasrwdo3/10)
            #cpt = bcrypt.hashpw((str(psasrwdo3)).encode(), bcrypt.gensalt())
            psasrwdo3_con.append(psasrwdo3)
        psasrwdo3_total.append(psasrwdo3_con)
    for x in range(0, len(psasrwdo3_total)):
        for y in range(0, len(psasrwdo3_total[x])):
            if code == psasrwdo3_total[x][y]:
                acescs = True
    return acescs
