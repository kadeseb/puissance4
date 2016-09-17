#!/usr/bin/python3
# -*- coding: utf8 -*-
# -----------------------------------
# Projet: 	Puissance4
# Rôle: 	Contient le moteur de jeu
# Auteur: 	kadeseb
# Crée le:	17/07/2016
# -----------------------------------
from event import *
from engine import *
from configuration import *
from tkinter import *
from tkinter import messagebox
from time import sleep
from random import randrange

#----------------------------|
# Gère le canvas d'affichage |
#----------------------------|
class GameCanvas( Canvas ):
	##
	# Constructeur
	#
	# -?-
	# parent 	[~Frame] Conteneur parent
	# engine 	[Engine] Instance d'engine
	#
	# -/!\-
	# {TypeError} 	Si engine n'est pas une instance d'Engine
	## 
	def __init__( self, parent, engine ):
		Canvas.__init__( self,  width = CONFIGURATION.DISPLAY['WIDTH'], height = CONFIGURATION.DISPLAY['HEIGHT'] )
		self.pack( fill = BOTH, expand = True )

		if isinstance( engine, Engine ):
			self.engine = engine
		else:
			raise TypeError

	##
	# Affiche la grille et le curseur
	##
	def displayContent( self ):
		self.clear()

		# Affiche la grille
		for column in range( 0, CONFIGURATION.GRID['COLUMN'] ):
			for line in range( 0, CONFIGURATION.GRID['LINE'] ):
				caseOwner = self.engine.getCaseOwner( column, line )

				self.create_rectangle( self.calculatePawnPosition( line, column ), fill = CONFIGURATION.PAWN['COLOR'][ caseOwner ] )

		# Affiche le curseur
		cursor = self.engine.getCursor()
		self.create_rectangle( self.calculateCursorPosition( cursor ), fill = CONFIGURATION.PAWN['COLOR'][ self.engine.getPlayer() ] )

	##
	# Calcule la position des pions
	#
	# -?-
	# line		[int] Ligne dans la grille
	# column	[int] Colonne dans la grille
	#
	# -!-
	# [int],[int],[int],[int]	Retourne les angles opposés des pions
	##
	def calculatePawnPosition( self, line, column ):
		x1 = CONFIGURATION.GRID['XGAP'] + CONFIGURATION.PAWN['INCREMENT']*column 
		y1 = CONFIGURATION.GRID['YGAP'] + CONFIGURATION.PAWN['INCREMENT']*line

		x2 = x1 + CONFIGURATION.PAWN['SIZE']
		y2 = y1 + CONFIGURATION.PAWN['SIZE']

		return x1, y1, x2, y2

	##
	# Calcule la position du curseur
	#
	# -?-
	# cursor 	[int] Position du curseur en colonne sur la grille
	#
	# -!-
	# [int],[int],[int],[int]	Retourne les angles opposés du curseur
	##
	def calculateCursorPosition( self, cursor ):
		x1 = CONFIGURATION.GRID['XGAP'] + CONFIGURATION.PAWN['INCREMENT']*cursor
		y1 = CONFIGURATION.CURSOR['YGAP']
		
		x2 = x1 + CONFIGURATION.CURSOR['WSIZE']
		y2 = y1 + CONFIGURATION.CURSOR['HSIZE']

		return x1, y1, x2, y2

	##
	# Supprime le contenu du canvas
	##
	def clear( self ):
		self.delete( ALL )
		self.create_rectangle( 0, 0, CONFIGURATION.DISPLAY['WIDTH'], CONFIGURATION.DISPLAY['HEIGHT'], fill=CONFIGURATION.BACKGROUNDCOLOR )


#-----------------------------------------|
# Gère la fenêtre principale du programme |
#-----------------------------------------|
class Application( Tk ):
	def __init__( self, event ):
		Tk.__init__( self )
		self.event = event
		self.bind( '<Key>', event.keyboard ) 
		self.title( "Puissance 4" )
		self.resizable( width=False, height=False )

	##
	# Affiche le message d'aide
	##
	def showHelp( self ):
		helpMessage = "Bienvenue sur Puissance 4 !\n\n"

		helpMessage += '[F1] \tAfficher l\'aide\n'
		helpMessage += '[<] [>] \tDéplacer le curseur\n'
		helpMessage += '[ENTRE] \tPlacer un pion\n'
		helpMessage += '[DEL] \tRéinitialiser\n'
		helpMessage += '[ECHAP] \tQuitter\n'

		messagebox.showinfo( 'Aide', helpMessage, parent=self )

	##
	# Affiche une confirmation de réinitialisation de la partie
	#
	# -!-
	# [bool] 	L'utilisateur confirme vouloir réin
	##
	def showResetConfirmation( self ):
		return messagebox.askyesno( 'Réinitialiser la partie ?', 'Vous êtes sur le point de réinitialiser la partie, voulez vous continuer ?', parent=self )

	##
	# Affiche le message de victoire et propose une nouvelle partie
	#
	# -?-
	# player 	[int] Joueur victorieux
	#
	# -!-
	# [bool]	L'utilisateur veux faire une nouvelle partie
	##
	def showVictoryMessage( self, player ):
		return messagebox.askyesno( 'Victoire', 'Le joueur ' + str( player ) + ' gagne !\n Souhaitez-vous rejouer ?', parent=self )