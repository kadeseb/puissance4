#!/usr/bin/python3
# -*- coding: utf8 -*-
# ------------------------
# Projet:		Puissance4
# Auteur:		kadeseb
# Créer le:		15/07/2016
# Version:		1.1
# ------------------------
from engine import *
from display import *
from display import *
from event import *
from configuration import *
import time

if __name__ == "__main__":
	engine = Engine()
	event = Event( engine )
	application = Application( event )
	canvas = GameCanvas( application, engine )

	event.associateApplication( application )

	while True:
		if CONFIGURATION._EXEC_['CONTINUE_PROGRAM']:
			canvas.displayContent()

			if not CONFIGURATION._EXEC_['DEBUG_MODE'] and not CONFIGURATION._EXEC_['HELP_SHOWED']:
				application.showHelp()
				CONFIGURATION._EXEC_['HELP_SHOWED'] = True

			winner = engine.findWiner( canvas )
			if winner:
				if CONFIGURATION._EXEC_['DEBUG_MODE']:
					print( '-> Joueur', winner, 'gagne !' )
				else:
					if application.showVictoryMessage( winner ):
						engine.emptyGrid()
					else:
						CONFIGURATION._EXEC_['CONTINUE_PROGRAM'] = False

			application.update()
		else:
			application.destroy()
			exit( 0 )