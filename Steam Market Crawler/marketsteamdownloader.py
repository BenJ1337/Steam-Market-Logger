# -*- coding: utf-8 -*-

import os, json, urllib.request, time, random, datetime, traceback


def createResourceFolder( data_folder ):
	if not os.path.exists(data_folder):
		os.makedirs(data_folder)
	else:
		print("# Resource folder already exits.")

def createGameFolder( game_data_folder ):
	if not os.path.exists(game_data_folder):
		os.makedirs(game_data_folder)
	else:
		print("# Game folder already exits.")

def createRawDataFolder( raw_data_folder):
	id = 0
	content_of_gamefolder = os.listdir( raw_data_folder )

	if ( len( content_of_gamefolder ) == 0):
		path = os.path.join( raw_data_folder, str(id) )
		os.makedirs(path)
		return 0
	else:
		path = os.path.join( raw_data_folder, str( len( content_of_gamefolder ) ) )
		os.makedirs(path)

		return len( content_of_gamefolder )

def downloadMarketResources( raw_data_folder, folder_id, game_id, number_of_items_in_one_json, start_item ):

	content_of_gamefolder = os.path.join(raw_data_folder, str( folder_id ))

	number_of_sites = 1000

	index = 0
	i = 1
	while( i < number_of_sites ):
		down_link = 'https://steamcommunity.com/market/search/render/?query=&norender=1&start=' + str( i ) + '&count=' + str( number_of_items_in_one_json ) + '&search_descriptions=0&sort_column=price&sort_dir=asc&appid=' + str( game_id )

		try:	
			response 				= urllib.request.urlopen( down_link )
			data 					= json.load(response)  	

			number_of_sites = data["total_count"]
			print( "Items in market: " + str( number_of_sites ) )
			print( "Iteration: " + str( i ) )

			content_of_gamefolder 	= os.path.join(raw_data_folder, str( folder_id ), "items" + str( index ) + ".json")	

			datei_out = open(content_of_gamefolder, "w")
			datei_out.write(json.dumps(data))
			datei_out.close()	
			i += 100

		except Exception:
			print( traceback.format_exc() )
			traceback.print_exc()

		index += 1
		time.sleep( random.randint(10,15)  )
	

def createList( game_data_folder, raw_game_data_folder, game_id, id ):
		listfile_folder = os.path.join( raw_game_data_folder, str( id ) )

		zusammenfassung_folder = os.path.join( game_data_folder, game_name + str(id) + ".csv")
		datei_out = open(zusammenfassung_folder , "w", encoding='utf8')
		datei_out.close()

		datei_out = open(zusammenfassung_folder , "a", encoding='utf8')

		items = os.listdir( listfile_folder )

		datei_out.write( "Name;Price;CPrice;Number;Type;Restriction,PicUrl\n" )
		for item in items:
			items_data = os.path.join(listfile_folder, item)

			datei_in 	= open( items_data , "r")
			data 		= datei_in.read()
			data 		= json.loads(data)

			ausgabe = outputCSV( data['results'] )
			print( ausgabe )
			datei_out.write( ausgabe )

		datei_out.close()

def outputCSV( items ):
	ausgabe = ""
	for entry in items:
		ausgabe += entry['name'] + ";" + entry['sell_price_text'] + ";" + str(entry['sale_price_text']) + ";" + str(entry['sell_listings']) \
					+ ";" + str(entry['asset_description']['type']) + ";" + str(entry['asset_description']['market_tradable_restriction']) \
					 + ";" + "https://steamcommunity-a.akamaihd.net/economy/image/" + str(entry['asset_description']['icon_url_large']) + "\n"

	return ausgabe

def outputFile( items ):		
	abstandNachName = 75
	abstandNachPreis = 20

	ausgabe = ''
	for entry in items:
		ausgabe += 'Name: '
		ausgabe += entry['name']
		index = len( entry['name'] )
		while( index < abstandNachName ):
			ausgabe += ' '
			index += 1
		ausgabe += entry['sell_price_text']
		index = len( entry['sell_price_text'] )
		while( index < abstandNachPreis ):
			ausgabe += ' '
			index += 1
		ausgabe += "#" + str(entry['sell_listings']) + "\n"
	
	return ausgabe


def setup( data_folder, game_data_folder, raw_game_data_folder ):
	if ( os.path.isdir( data_folder ) == False ):
		createResourceFolder( data_folder )

	if ( os.path.isdir( game_data_folder ) == False ):
		createGameFolder( game_data_folder )

	if ( os.path.isdir( raw_game_data_folder ) == False ):
		createGameFolder( raw_game_data_folder )

if __name__ == "__main__":

	programm_folder 	 				= os.path.abspath(".")
	resource_folder_name 				= "Resources"
	#game_name 	 						= "PLAYERUNKNOWN'S BATTLEGROUNDS"
	#game_id 	 						= "578080"
	game_name 	 						= "CSGO"
	game_id 	 						= "730"
	number_of_items_in_one_json 		= 100
	start_item 							= 0
	
	data_folder 			= os.path.join(programm_folder, resource_folder_name)
	game_data_folder 		= os.path.join( data_folder , game_name)
	raw_game_data_folder 	= os.path.join( game_data_folder, 'raw_data')

	setup( data_folder, game_data_folder, raw_game_data_folder )

	folder_id = createRawDataFolder( raw_game_data_folder )	

	folder_id = 1

	startzeitpunkt = time.localtime()
	print( "starttime: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n" )

	#downloadMarketResources( raw_game_data_folder, folder_id, game_id, number_of_items_in_one_json, start_item )


	endzeitpunkt = time.localtime()
	diffenenz = time.mktime( endzeitpunkt ) - time.mktime( startzeitpunkt )
	print( "endtime: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n" + "Dauer: " + str( diffenenz/60 ) + " min" )



	createList( game_data_folder, raw_game_data_folder, game_id, folder_id )
