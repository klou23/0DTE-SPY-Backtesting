from SPYData import SPYData


def main():
    print("hello world")
    spd = SPYData(11)
    spd.get_market_days()


if __name__ == '__main__':
    main()

'''
.AAPL261218C200

https://demo.dxfeed.com/webservice/rest/events.json?events=Trade,Quote&symbols=SPY&fromTime=20190114&toTime=201901014&timeout=60&indent

https://demo.dxfeed.com/webservice/rest/events.json?events=Trade,Quote&symbols=.AAPL261218C200&fromTime=20240601&toTime=20240614&timeout=60&indent

https://demo.dxfeed.com/webservice/rest/events.json?events=Trade,Quote&symbols=.SPY240628C500&fromTime=20240601&toTime=20240614&timeout=60&indent

https://demo.dxfeed.com/webservice/rest/events.json?events=Candle&symbols=.AAPL261218C200{=h}&fromTime=20240601&toTime=20240614&timeout=60&indent

https://demo.dxfeed.com/webservice/rest/events.json?events=Candle&symbols=.SPY240628C540{=h}&fromTime=20240601&toTime=20240614&timeout=60&indent

https://demo.dxfeed.com/webservice/rest/events.json?events=Candle&symbols=.SPY240627C540{=h}&fromTime=20240627&toTime=20240628&timeout=60&indent

https://demo.dxfeed.com/webservice/rest/events.json?events=Candle&symbols=SPY{=d}&fromTime=20240601&toTime=20240614&timeout=60&indent

'''