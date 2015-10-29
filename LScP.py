#LScrawler for PYTHON!!
import requests

#gGet all possible photo webpages
seed = 160000
while seed <= 200000:
	staticAdd = 'http://www.lschs.org/uploaded/_assets/images/portraits/students/2015-16/'
	suffix = ".jpg"
	finalAdd = staticAdd + str(seed) + suffix
	try:
		r = requests.head(finalAdd)
		statusCode = r.status_code #gets the response code from the webpage
	except requests.ConnectionError:
		print("failed to connect")
	
	if statusCode == 200: # if the webpage succesfully connected...
		print "LsFetcher: [hit] 1 target..." # print that it hit a valid webpage...
		print "\rLsFetcher: [h][cos]" + str(seed) + '\r' # and print the webpage number
		print finalAdd + "\n"
		#write to file
		file = open('lscrawler.log', 'a')
		file.write(finalAdd + '\n') # write to the file "lscrawler.log" the full webpage addresses of the valid webpages
		file.close
	else:
		print "\rLsFetcher: [n][cos]" + str(seed) + "\r" # print webpages that failed as well
	seed += 1
