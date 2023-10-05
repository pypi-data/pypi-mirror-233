from lal import gpstime
import numpy as np

#Would normally input these from our previous sun sign calculation + the gracedb coalesence time
sun_sign = 'cancer'
coal_datetime_gps = gpstime.gps_time_now()

#Convert given gps time to form EST-hour.minute
coal_time_utc = gpstime.gps_to_utc(coal_datetime_gps).time()
hour = str(coal_time_utc).split(':')[0]
hour = int(hour) - 5
coal_time_utc = hour + int(str(coal_time_utc).split(':')[1])/100
print(coal_time_utc)

#Arrange rising signs in order according to your sun sign
sun_signs = ['aries','taurus','gemini','cancer','leo','virgo','libra','scorpio','sagittarius','capricorn','aquarius','pisces']
sun_sign_index = sun_signs.index(sun_sign)

rising_signs=[""]*len(sun_signs)
for index in range(0,len(sun_signs)):
	rising_signs[index-sun_sign_index+2] = sun_signs[index]
print(rising_signs)

#Find index of your rising sign based on your time of birth
rising_sign_index = int(coal_time_utc)//2
print(rising_signs[rising_sign_index])
