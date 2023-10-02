import bcrypt
from datetime import datetime, timedelta
import numpy as np
today = datetime.today()
now = datetime.now()
dd = today.day
mm = today.month
yy = today.year
mu = now.minute

def sysdtpasshw(end_date):
    today_date = datetime.now().date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    time_difference = end_date - today_date
    days_difference = abs(time_difference.days)
    tnuere = [7, 28, 56, 84]
    psasrwdo3_total = []
    psasrwdo4_total = []
    for j in range (0, len(tnuere)):
        psasrwdo3_con = []
        psasrwdo4_con = []
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
            psasrwdo4 = 0
            for m in range (0, 6):
                psasrwdo2 = float(psasrwdo/10**(m+1))
                psasrwdo11 = (int(round((float(psasrwdo2)- int(psasrwdo2)),1)*tnuere[j])*(10**(5-m)))
                psasrwdo12 = (int(round((float(psasrwdo2)- int(psasrwdo2)),1)*tnuere[j]*7)*(10**(5-m)))
                
                psasrwdo3 += psasrwdo11
                psasrwdo4 += psasrwdo12
            if psasrwdo3 < 10**5 :
                while psasrwdo3 < 10**5 :
                    psasrwdo3 += psasrwdo3
            if psasrwdo3 > 999999:
                while psasrwdo3 > 999999:
                    psasrwdo3 = int(psasrwdo3/10)
            if psasrwdo4 < 10**5 :
                while psasrwdo4 < 10**5 :
                    psasrwdo4 += psasrwdo4
            if psasrwdo4 > 999999:
                while psasrwdo4 > 999999:
                    psasrwdo4 = int(psasrwdo4/10)
            psasrwdo3_con.append(psasrwdo3)
            psasrwdo4_con.append(psasrwdo4)
        psasrwdo3_total.append(psasrwdo3_con)
        psasrwdo4_total.append(psasrwdo4_con)
        
    if (days_difference <= 84):
        ind = (84 - days_difference)
        actv_key1 = psasrwdo3_total[3][ind]
        actv_key2 = psasrwdo4_total[3][ind]
    else:
        print ("tenure must be less than 3 months")
        
    return actv_key1, actv_key2
