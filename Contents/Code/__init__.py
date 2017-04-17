import urllib
from Common import *

TITLE = '4Tube'
NAME = L(TITLE)
ART = 'art-default.jpg'
ICON = 'icon-default.png'

BASE_URL = "http://www.4tube.com"
PAGINATION_REGEX = "//ul[contains(@class, 'pagination')]/li/a[not(contains(@class, 'btn-simple'))]/@data-page"

#####################################################################
# This (optional) function is initially called by the PMS framework to
# initialize the plug-in. This includes setting up the Plug-in static
# instance along with the displayed artwork.

def Start(): # Initialize the plug-in

	Log('Starting 4Tube Plugin')

	Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
	Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

# Setup the default attributes for the ObjectContainer
ObjectContainer.title1 = TITLE
ObjectContainer.view_group = 'List'
ObjectContainer.art = R(ART)

# Setup the default attributes for the other objects
DirectoryObject.thumb = R(ICON)
DirectoryObject.art = R(ART)
VideoClipObject.thumb = R(ICON)
VideoClipObject.art = R(ART)

#####################################################################
@handler('/video/4tube', TITLE)
def MainMenu():

	oc = ObjectContainer()
	
	oc.add(DirectoryObject(
		key =	Callback(StartPage, title="Most Viewed Today"),
		title =	"Most Viewed Today",
	))
	
	oc.add(DirectoryObject(
		key =	Callback(ListLatestVideos, title="Latest Videos"),
		title =	"Latest Videos",
	))
	
	oc.add(DirectoryObject(
		key =	Callback(BrowseCategories, title="Categories"),
		title =	"Categories",
	))
	
	oc.add(DirectoryObject(
		key =	Callback(BrowsePornStars, title="Porn Stars"),
		title =	"Porn Stars",
	))
	
	oc.add(DirectoryObject(
		key =	Callback(BrowseFavorites, title="Favorites"),
		title =	"Favorites",
	))
	
	oc.add(InputDirectoryObject(
		key = Callback(Search),
		title = "Search",
		prompt = "Search for...",
		summary = "Enter Search Terms"
	))
	

	return oc
	
@route('/video/4tube/start')
def StartPage(title=""):
	
	oc = ObjectContainer(title2=title)
	
	page = HTML.ElementFromURL("http://www.4tube.com")

	divs = page.xpath("//div[contains(@class, 'container')]/div[contains(@class, 'colspan3')]/div[contains(@class, 'thumb_video')]")
	for videodiv in divs:
		url = BASE_URL + videodiv.xpath('./a/@href')[0] 
		title = videodiv.xpath('./a/@title')[0] 
		thumbUrl = videodiv.xpath('./a/div[contains(@class, "thumb")]/img/@data-master')[0]
		
		oc.add(DirectoryObject(
			key =	Callback(LaunchVideoPage, url=url, thumbUrl=thumbUrl),
			title =	title,
			summary =	title,
			thumb =	thumbUrl
		))

		

	return oc
	
@route('/video/4tube/launch')
def LaunchVideoPage(title="Play", url = "", thumbUrl = ""):
	oc = ObjectContainer(title2=title)
	
	oc.add(VideoClipObject(
		url = url,
		thumb = thumbUrl,
		title = title,
		summary = 'summary'
	))
		
	return oc
	
@route('/video/4tube/categories')
def BrowseCategories(title="Categories"):

	oc = ObjectContainer(title2=title)
	
	page = HTML.ElementFromURL(BASE_URL)
	
	for categoryLink in page.xpath("//li[contains(@class, 'categories-button')]/ul/li/a"):
		
		title = categoryLink.xpath("./@title")[0]
		url = BASE_URL + categoryLink.xpath("./@href")[0]
		
		oc.add(DirectoryObject(
			key = Callback(ListVideosForCategory, title=title, url=url),
			title = title
		))
	
	
	return oc
	
@route('/video/4tube/pornstars')
def BrowsePornStars(title="Porn Stars"):

	oc = ObjectContainer(title2=title)
	
	page = HTML.ElementFromURL(BASE_URL)
	
	for letter in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]:

		url = BASE_URL + "/pornstars/" + letter
		oc.add(DirectoryObject(
			key = Callback(ListPornStarsForLetter, title=letter, url=url),
			title = letter
		))
	
	
	return oc
	
@route('/video/4tube/favorites')
def BrowseFavorites(title="Favorites", url = "", sortOrders = ""):

	oc = ObjectContainer(title2=title)
	
	page = HTML.ElementFromURL(BASE_URL)
	
	fav1 = {"name": "Allie Haze", "url": "allie-haze"}
	fav2 = {"name": "Riley Reid", "url": "riley-reid"}
	fav3 = {"name": "Rachel James", "url": "rachel-james"}
	fav4 = {"name": "Veronica Radke", "url": "veronica-radke"}
	fav5 = {"name": "Casi James", "url": "casi-james"}
	fav6 = {"name": "Peachy", "url": "margarita-c-peachy"}
	fav7 = {"name": "Stoya", "url": "stoya"}
	fav8 = {"name": "Sativa Rose", "url": "sativa-rose"}
	favorites = [fav1, fav2, fav3, fav4, fav5, fav6, fav7, fav8]
	
	for fav in favorites:

		url = BASE_URL + "/pornstars/" + fav["url"]
		oc.add(DirectoryObject(
			key =	Callback(ListVideosForCategory, title =	fav["name"], url=url),
			title =	fav["name"]
		))
	
	
	return oc
	
@route('/video/4tube/pornstars/list')
def ListPornStarsForLetter(title="A", url = ""):

	oc = ObjectContainer(title2="Starts with "+title)
	
	baseUrlForLetter = url
	page = HTML.ElementFromURL(url)

	links = page.xpath("//div/a[contains(@class, 'thumb-link')]")
	for starlink in links:
		url = starlink.xpath('./@href')[0] 
		name = starlink.xpath("./@title")[0] 
		thumbUrl = starlink.xpath("./div[contains(@class, 'thumb')]/img/@data-original")[0]
		
		oc.add(DirectoryObject(
			key =	Callback(ListVideosForCategory, title=name, url=url),
			title =	name,
			thumb =	thumbUrl
		))

	pages = page.xpath(PAGINATION_REGEX)
	for pageNumber in pages:
		if int(pageNumber) > 1:
			page = HTML.ElementFromURL(baseUrlForLetter+"?p="+pageNumber)

			links = page.xpath("//div/a[contains(@class, 'thumb-link')]")
			for starlink in links:
				url = starlink.xpath('./@href')[0] 
				name = starlink.xpath("./@title")[0] 
				thumbUrl = starlink.xpath("./div[contains(@class, 'thumb')]/img/@data-original")[0]
				
				oc.add(DirectoryObject(
					key =	Callback(ListVideosForCategory, title=name, url=url),
					title =	name,
					thumb =	thumbUrl
				))
		

	return oc
	
@route('/video/4tube/categories/list')
def ListVideosForCategory(title="List for Category", url = "", params = {}, sortOrders = ""):

	oc = ObjectContainer(title2=title)
	
	categoryBaseUrl = url
	page = HTML.ElementFromURL(categoryBaseUrl + "?" + urllib.urlencode(params))

	divs = page.xpath("//div[contains(@class, 'thumb_video')]")
	for videodiv in divs:
		url = "http://www.4tube.com" + videodiv.xpath('./a/@href')[0] 
		title = videodiv.xpath('./a/@title')[0] 
		thumbUrl = videodiv.xpath('./a/div[contains(@class, "thumb")]/img/@data-master')[0]
		
		oc.add(DirectoryObject(
			key =	Callback(LaunchVideoPage, url=url, thumbUrl=thumbUrl),
			title =	title,
			summary =	title,
			thumb =	thumbUrl
		))
	
	pages = page.xpath(PAGINATION_REGEX)
	for pageNumber in pages:
		if int(pageNumber) > 1:
			params["p"] = pageNumber
			page = HTML.ElementFromURL(categoryBaseUrl+ "?" + urllib.urlencode(params))
			divs = page.xpath("//div[contains(@class, 'thumb_video')]")
			for videodiv in divs:
				url = "http://www.4tube.com" + videodiv.xpath('./a/@href')[0] 
				title = videodiv.xpath('./a/@title')[0] 
				thumbUrl = videodiv.xpath('./a/div[contains(@class, "thumb")]/img/@data-master')[0]
				
				oc.add(DirectoryObject(
					key =	Callback(LaunchVideoPage, url=url, thumbUrl=thumbUrl),
					title =	title,
					summary =	title,
					thumb =	thumbUrl
				))
		

	return oc
	
@route('/video/4tube/latest/list')
def ListLatestVideos(title="Latest Videos"):

	oc = ObjectContainer(title2=title)
	
	url = BASE_URL + "/videos?sort=date"
	page = HTML.ElementFromURL(url)

	divs = page.xpath("//div[contains(@class, 'thumb_video')]")
	for videodiv in divs:
		url = "http://www.4tube.com" + videodiv.xpath('./a/@href')[0] 
		title = videodiv.xpath('./a/@title')[0] 
		thumbUrl = videodiv.xpath('./a/div[contains(@class, "thumb")]/img/@data-master')[0]
		
		oc.add(DirectoryObject(
			key =	Callback(LaunchVideoPage, url=url, thumbUrl=thumbUrl),
			title =	title,
			summary =	title,
			thumb =	thumbUrl
		))

		

	return oc

@route('/video/4tube/search')
def Search(query):
	params = {"q" : query}
	url = BASE_URL + "/search" 
	return ListVideosForCategory(title="Search Result", url=url, params=params)