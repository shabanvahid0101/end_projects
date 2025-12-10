import pyshorteners as sh

#insert long url
long_url = input("enter long url to shorten: ")

#make shortner function
type_tiny=sh.Shortener()
short_url = type_tiny.tinyurl.short(long_url)

print("the shorten url is : "+short_url)