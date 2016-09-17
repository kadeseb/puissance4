#!/usr/bin/python3
# -*- coding: utf8 -*-
# ---------------------------------
# Projet:	Puissance4
# Rôle:		Gère le jeu en lui même
# Auteur:	kadeseb
# Crée le:	17/07/2016
# ---------------------------------
from configuration import *
from engine import *
from display import *

class Event:
	KEYLIST = { 
		'ENTER': 36, 
		'DEL': 22, 
		'F1': 67, 
		'ESCAPE': 9, 
		'LEFT': 114, 
		'RIGHT': 113, 
		'R': 27, 
	}

	##
	# Constructeur
	#
	# -?-
	# engine 	[Engine] Une instance d'Engine
	#
	# -/!\-
	# {TypeError} 	Si engine n'est pas une instance d'engine
	##
	def __init__( self, engine ):
		if not isinstance( engine, Engine ):
			raise TypeError

		self.engine = engine
		self.application = None
		self.callbackList = {
			'pressESCAPE': self.__CB_pressESCAPE,
			'pressENTER': self.__CB_pressENTER,
			'pressARROW': self.__CB_pressARROW,
			'pressF1': self.__CB_pressF1,
			'pressDEL': self.__CB_pressDEL,
			'pressR': self.__CB_pressR
		}

	##
	# Associe une instance d'application
	#
	# -?- 
	# application 	[Application] Application
	#
	# -!-
	# [bool]		Retourne True si l'association a réuissie, False si application n'est pas une instance d'Application 
	##
	def associateApplication( self, application ):
		#if isinstance( application, Application ):
			self.application = application
		#	return True
		#return False

	##
	# Associe les fonctions callbacks
	#
	# -?-
	# callbackList	[dict] Liste des fonctions callbacks
 	##
	def associateCallback( self, callbalList ):
		self.callbalList = callbalList

	##
	# Gère les évenements clavier
	##
	def keyboard( self, event ):
		keycodeList = { v: k for k, v in self.KEYLIST.items() }

		# Tente de retrouver le nom de la touche
		try:
			keyName = keycodeList[ event.keycode ]
		
			if keyName == 'LEFT' or keyName == 'RIGHT':
				keyName = 'ARROW'
		except KeyError:
			return

		callback = self.callbackList[ 'press' + keyName ]

		if callback != None:
			callback( event.keycode )

	#**********************
	# Fonctions Callbacks *
	#**********************
	def __CB_pressARROW( self, keycode ):
		if keycode == self.KEYLIST['LEFT']:
			self.engine.moveCursor( CONFIGURATION.DIRECTION['LEFT'] )

		elif keycode == self.KEYLIST['RIGHT']:
			self.engine.moveCursor( CONFIGURATION.DIRECTION['RIGHT'] )

	def __CB_pressENTER( self, keycode ):
		if self.engine.dropPawn():
			self.engine.changePlayer()

	def __CB_pressDEL( self, keycode ):
		if( CONFIGURATION._EXEC_['DEBUG_MODE'] ):
			reset = True
		else:
			reset = self.application.showResetConfirmation()

		if reset:
			self.engine.emptyGrid()

			if self.engine.getPlayer() != 1:
				self.engine.changePlayer()

	def __CB_pressESCAPE( self, keycode ):
		global CONFIGURATION

		CONFIGURATION._EXEC_['CONTINUE_PROGRAM'] = False

	def __CB_pressR( self, keycode ):
		if CONFIGURATION._EXEC_['DEBUG_MODE']:
			self.engine.randomGrid()

	def __CB_pressF1( self, keyName ):
		#if isinstance( self.application, Application ):
		self.application.showHelp()



