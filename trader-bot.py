import requests
import datetime
import pytz
import schedule
import time


#these parameters will come from config file
unit = "MINUTES"
period = "5"
pair = "BTC_EUR"
rsi_range = "14"

#-----------------------------------------
#set the time delta according to rsi range and unit of time. 
#E.g.: RSI = 14, unit = 5 minutes will give us 14*5=70 candles


#def job():
#    print("I'm working...")

#	while 1:
#    	schedule.run_pending()
#    	get_candles()
#    	print(get_rsi)

raw_current_time = datetime.datetime.utcnow()

def get_candles(sample_range):
	time_frame_minutes = int(sample_range) * int(period) 
	delta = datetime.timedelta(minutes=time_frame_minutes)
	raw_initial_time = (raw_current_time - delta)

	t0 = raw_initial_time.replace(microsecond=0).isoformat()
	t1 = raw_current_time.replace(microsecond=0).isoformat()
	
	api_url = "https://api.exchange.bitpanda.com/public/v1/candlesticks/"+pair+"?unit="+unit+"&period="+period+"&from="+t0+"Z&to="+t1+"Z"
	ret = requests.get(api_url).json()
	print(ret)
	return ret

def get_rsi(range):
	ret_val = 0
	variation_pct = 0
	sum_gain = 0
	sum_loss = 0
	avg_loss = 0
	avg_gain = 0

	step = 1
	for x in get_candles(range):
		open_f = float(x['open'])
		close_f = float(x['close'])
		print ("Step " + str(step))
		print ("open_f " + str(open_f))
		print ("close_f " + str(close_f))
		print ("==============")
	
		variation_pct = 100*(close_f/open_f)-100
		#print ("variation_pct " + str(variation_pct))
		#print(x)

		if variation_pct > 0:
			sum_gain += variation_pct 
		else:
			sum_loss += variation_pct * -1

		avg_gain = sum_gain / range - (range - step)
		avg_loss = sum_loss / range - (range - step)
		step += 1

	if avg_gain == avg_loss: 
		#the below will prevent 0/0
		ret_val = 50
	elif avg_loss == 0:
		#the below will prevent /0
		ret_val = 100
	else:
		#RSI formula source: https://www.investopedia.com/terms/r/rsi.asp
		#ret_val = 100 - (100/(1+(avg_gain * (range - step)/avg_loss * (range - step))))
		ret_val = 100 - (100/(1+(avg_gain/avg_loss)))


	print(avg_loss)
	print(avg_gain)
	print(ret_val)

get_rsi(18)
print(raw_current_time)

# Parei tentando descobrir porque nao pega as ultimas 5 velas (25% ??).