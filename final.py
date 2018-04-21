# _*_ coding: utf-8 _*_


from selenium import webdriver
from bs4 import BeautifulSoup
import csv


driver = webdriver.PhantomJS('phantomjs.exe')

def DownloadPageHtml(url):
	print 'Downloading : ' + url
	driver.get(url)
	html = driver.page_source
	return html

cd = 283
start_page = 1
end_page = 1

for x in xrange(start_page,end_page + 1):
	url = 'http://www.amarbooks.com/cat.php?cd={}&pg={}'.format(cd,x)

	file_name = str(cd) + '_' + str(x) + '.csv'

	soup = BeautifulSoup(DownloadPageHtml(url),'lxml')
	bookcontainer = soup.find('div',class_ = 'col-lg-9 col-md-9 col-sm-9 col-xs-12 left')
	allbooks = bookcontainer.find_all('div',class_ ='bookDiv')
	base_url = 'http://www.amarbooks.com/'

	data = [['post_type','post_status','post_title','post_content','post_category','post_thumbnail','download_link']]
	f = open(file_name,'a+')
	with f:
		writer = csv.writer(f)
		writer.writerows(data)



	for book in allbooks:
		html = DownloadPageHtml(base_url + book.find('a')['href'])
		soup = BeautifulSoup(html,'lxml')

		post_type = 'post'
		post_status = 'publish'

		post_title = soup.find('div',{'id':'StateFeeder'}).find_all('h3')[1].text.replace('Book : ','').replace('.pdf','')
		post_category = soup.find('div',{'id':'StateFeeder'}).find_all('h3')[0].text.replace('Category : ','')
		post_thumbnail = soup.find('div',{'id':'StateFeeder'}).find_all('img')[1]['src']
		download_link = 'http://www.amarbooks.com/FreeDownload.php?w={}&f={}.pdf'.format(post_category,post_title).replace(' ','%20')
		last_part = soup.find('div',class_ = 'col-lg-9 col-md-9 col-sm-9 col-xs-12 left').text.rsplit('Thanks',1)[-1]
		first_part = soup.find('div',class_ = 'col-lg-9 col-md-9 col-sm-9 col-xs-12 left').text.rsplit('!!!',1)[-1]
		post_content = first_part.replace(last_part,'').replace('\n','').replace('\t','')

		data = [[post_type,post_status,post_title,post_content,post_category,post_thumbnail,download_link]]

		f = open(file_name,'a+')

		with f:
			writer = csv.writer(f)
			writer.writerows(data)


	print 'Finish'


driver.close()
f.close()