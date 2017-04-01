def GenerateMenu(title, menuItems, no_cache=False):
	# Create the object to contain the menu items
	oc = ObjectContainer(title2=title, no_cache=no_cache)
	
	# Loop through the menuItems dictionary
	for menuTitle, menuData in menuItems.items():
		# Create empty dictionaries to hold the arguments for the Directory Object and the Function
		directoryObjectArgs =	{}
		functionArgs =		{}
		
		# See if any Directory Object arguments are present in the menu data
		if ('directoryObjectArgs' in menuData):
			# Merge dictionaries
			directoryObjectArgs.update(menuData['directoryObjectArgs'])
		
		# Check to see if the menu item is a search menu item
		if ('search' in menuData and menuData['search'] == True):
			directoryObject = InputDirectoryObject(title=menuTitle, **directoryObjectArgs)
		# Check to see if the menu item is a next page item
		elif ('nextPage' in menuData and menuData['nextPage'] == True):
			directoryObject = NextPageObject(title=menuTitle, **directoryObjectArgs)
		# Otherwise, use a basic Directory Object
		else:
			directoryObject = DirectoryObject(title=menuTitle, **directoryObjectArgs)
			functionArgs['title'] = menuTitle
		
		# See if any Function arguments are present in the menu data
		if ('functionArgs' in menuData):
			# Merge dictionaries
			functionArgs.update(menuData['functionArgs'])
		
		# Set the Directory Object key to the function from the menu data, passing along any additional function arguments
		directoryObject.key =	Callback(menuData['function'], **functionArgs)
		
		# Add the Directory Object to the Object Container
		oc.add(directoryObject)
	
	return oc