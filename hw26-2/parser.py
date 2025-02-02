import requests
import xml.etree.ElementTree as ET
import pandas as pd


url = "https://scipost.org/atom/publications/comp-ai"

response = requests.get(url)

if response.status_code == 200:
	xml_content = response.text

	namespace = {'atom': 'http://www.w3.org/2005/Atom'}

	root = ET.fromstring(xml_content)

	news_list = []
	for entry in root.findall('atom:entry', namespace):
		title = entry.find('atom:title', namespace).text
		link = entry.find('atom:link', namespace).attrib['href']
		summary = entry.find('atom:summary', namespace).text if entry.find('atom:summary',
		                                                                   namespace) is not None else "No summary available"
		news_list.append({"Title": title, "Link": link, "Summary": summary})

	df_news = pd.DataFrame(news_list)

	print(df_news)
else:
	print(f"Error when loading data: {response.status_code}")
