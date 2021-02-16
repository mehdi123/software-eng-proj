import time

def strToTime(sdate):
    ''' Converts a string date in \'yyyy-mm-dd\' format to
a floating point time. '''
    
    if(type(sdate)==type(0.0)):
        return sdate

    date=sdate.split('-')
    return time.mktime((int(date[0]), int(date[1]), int(date[2]), 0, 0, 0, 0, 0, 0))

def timeToStr(ftime):
    ''' Converts a floating point time to a string date in
format \'yyyy-mm-dd\' '''
    t=time.localtime(ftime)
    return '%d-%02d-%02d'%(t[0], t[1], t[2])

g_days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
j_days_in_month = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]

def gregorian_to_jalali(g_y, g_m, g_d):
    ''' Converts a Gregorian date to Jalali date.

Example:        gregorian_to_jalali(2002, 12, 21) -> (1381, 9, 30) '''

    gy = g_y-1600
    gm = g_m-1
    gd = g_d-1

    g_day_no = 365*gy+(gy+3)/4-(gy+99)/100+(gy+399)/400
    for i in range(gm):
        g_day_no += g_days_in_month[i]
    if (gm>1 and ((gy%4==0 and gy%100!=0) or (gy%400==0))):
        # leap and after Feb
        g_day_no+=1
    g_day_no += gd

    j_day_no = g_day_no-79

    j_np = j_day_no / 12053
    j_day_no %= 12053

    jy = 979+33*j_np+4*(j_day_no/1461)
    j_day_no %= 1461

    if (j_day_no >= 366):
        jy += (j_day_no-1)/365
        j_day_no = (j_day_no-1)%365

    i=0
    while j_day_no >= j_days_in_month[i]:
        j_day_no -= j_days_in_month[i]
        i+=1
    jm = i+1
    jd = j_day_no+1
    return (jy, jm, jd)

def jalali_to_gregorian(j_y, j_m, j_d):
    ''' Converts a Jalali date to Gregorian date.

Example:        jalali_to_gregorian(1381, 9, 30) -> (2002, 12, 21) '''

    jy = j_y-979
    jm = j_m-1
    jd = j_d-1

    j_day_no = 365*jy + (jy/33)*8 + (jy%33+3)/4
    for i in range(jm):
        j_day_no += j_days_in_month[i]

    j_day_no += jd

    g_day_no = j_day_no+79

    gy = 1600 + 400*(g_day_no / 146097)  # 146097 = 365*400 + 400/4 - 400/100 + 400/400
    g_day_no = g_day_no % 146097

    leap = 1
    if g_day_no >= 36525: # 36525 = 365*100 + 100/4 
        g_day_no-=1
        gy += 100*(g_day_no / 36524) # 36524 = 365*100 + 100/4 - 100/100
        g_day_no = g_day_no % 36524

        if g_day_no >= 365:
            g_day_no+=1
        else:
            leap = 0

    gy += 4*(g_day_no / 1461) # 1461 = 365*4 + 4/4
    g_day_no %= 1461

    if (g_day_no >= 366):
        leap = 0

        g_day_no-=1
        gy += g_day_no / 365
        g_day_no = g_day_no % 365

    i=0
    while g_day_no >= g_days_in_month[i] + (i == 1 and leap):
        g_day_no -= g_days_in_month[i] + (i == 1 and leap)
        i+=1
    gm = i+1;
    gd = g_day_no+1;
    return (gy, gm, gd)
