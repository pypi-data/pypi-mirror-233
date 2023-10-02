import bcrypt
from datetime import datetime, timedelta
import numpy as np
today = datetime.today()
now = datetime.now()
dd = today.day
mm = today.month
yy = today.year
mu = now.minute


from .sdprotchk import sysdtpas
from .sdprotgen import sysdtpasshw
