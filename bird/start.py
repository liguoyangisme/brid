from scrapy.cmdline import execute

# execute("scrapy crawl line -o line.json".split())

execute("scrapy crawl flight -o datas/flight.json".split())