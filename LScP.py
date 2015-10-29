#LScrawler for PYTHON!!
import requests

seed = 160000
while seed <= 200000:
	staticAdd = 'http://www.lschs.org/uploaded/_assets/images/portraits/students/2015-16/'
	suffix = ".jpg"
	finalAdd = staticAdd + str(seed) + suffix
	try:
		r = requests.head(finalAdd)
		statusCode = r.status_code
	except requests.ConnectionError:
		print("failed to connect")
	
	if statusCode == 200:
		print "LsFetcher: [hit] 1 target..."
		print "\rLsFetcher: [h][cos]" + str(seed) + '\r'
		print finalAdd + "\n"
		#write to file
		file = open('lscrawler.log', 'a')
		file.write(finalAdd + '\n')
		file.close
		
	seed += 1
