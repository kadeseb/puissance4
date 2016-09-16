#!/usr/bin/python3
# -*- coding: utf8 -*-
# =================================
# Programme:	Puissance 4
# Auteur:		BINARD Sébastien
# =================================
DEBUGMODE = True

from time import sleep
from random import randrange
try:
	from tkinter import *
	from tkinter import messagebox
except ImportError:
	print( "-> ERREUR: La dépendance Tkinter n'a pas pu être chargé" )
	exit(1)


#===============|
# Moteur de jeu | 
#===============|
class Engine:
	GRIDSIZE = 6
	LEFT, RIGHT = 1, 2
	PLAYER1, PLAYER2 = 1, 2
	PAWNCOLOR = { 0 : "white", 1: "yellow", 2: "red" }
	PAWNSIZE = 50
	PAWNGAP = 10
	RANDOMPAWNMIN = 20
	GRIDBASEX, GRIDBASEY = 10, 50

	def __init__( self ):
		self.player = Engine.PLAYER1
		self.cursor = 0

		self.emptyGrid()

	##
	# Remplis la grille aléatoirement
	##
	def randomGrid( self ):
		self.emptyGrid()
		pawnNumber = randrange( Engine.RANDOMPAWNMIN, Engine.GRIDSIZE**2 )

		for i in range( 0, pawnNumber ):
			while True:
				owner = randrange( 0, Engine.PLAYER2+1 )
				column = randrange( 0, Engine.GRIDSIZE )
			
				if self.dropPlayerPawnAt( column, owner ):
					break;

	##
	# Vide la grille
	##
	def emptyGrid( self ):
		self.grid = [ [],[],[],[],[],[] ]

		for i in range( 0, 6 ):
			self.grid[i] = [0,0,0,0,0,0]

	##
	# Retourne l'appartenance de la case spécifié
	# -?-
	# x 		[int] Position x
	# y 		[int] Position y 
	# -!-
	# [int] Engine.PLAYER
	##
	def getCaseOwner( self, x, y ):
		return self.grid[y][x]

	##
	# Place un pion du joueur spécifié dans la colonne spécifié 
	# -?-
	# line 		[int] Colonne de la grille
	# player 	[int] Pion du joueur 
	# -!-
	# [bool]	True si le pion a été placé
	# 			False si un paramètre est incorrect ou si la colonne ciblé est pleine 
	##
	def dropPlayerPawnAt( self, column, player ):
		if (player != Engine.PLAYER1 and player != Engine.PLAYER2 and player != 0) or (column >= 6 and column < 0):
			return False

		for line in range( 0, self.GRIDSIZE ):
			if (line == 5 or self.grid[line+1][column]) and not self.grid[line][column]:
				self.grid[line][column] = player
				return True

		return False

	##
	# Place un pion avec les paramètres courants
	##
	def dropPawn( self ):
		return self.dropPlayerPawnAt( self.cursor, self.player )

	##
	# Change le joueur courant
	##
	def changePlayer( self ):
		if self.player == Engine.PLAYER1:
			self.player = Engine.PLAYER2
		elif self.player == Engine.PLAYER2:
			self.player = Engine.PLAYER1

	##
	# Recupère le joueur courrant
	##
	def getPlayer( self ):
		return self.player

	##
	# Déplace le curseur dans le sens spécifié
	# -?-
	# direction		[int] Sens de déplacement
	# -!-
	# [bool]		Retourne False si direction est incorrect   
	##
	def moveCursor( self, direction ):
		if direction != Engine.LEFT and direction != Engine.RIGHT:
			return False


		if direction == Engine.LEFT:
			if (self.cursor+1) >= self.GRIDSIZE:
				self.cursor = 0
			else:
				self.cursor += 1
		else:
			if (self.cursor-1) < 0:
				self.cursor = self.GRIDSIZE - 1
			else:
				self.cursor -= 1

		return True

	##
	# Retourne la colonne ciblé par le curseur
	# -!-
	# [int]		Curseur 
	def getCursor( self ):
		return self.cursor

	##
	# Détermine si un joueur à gagné
	# -!-
	# [int]		Retourne le numéro du joueur gagnant, 0 si aucun
	##
	def findWiner( self, canvas = False ):
		pawnCount  = { 'line': 0, 'column': 0, 'diagonal': 0 }

		for column in range( 0, Engine.GRIDSIZE ):
			for line in range( 0, Engine.GRIDSIZE ):
				currentPawnOwnner = self.grid[column][line]

				pawnCount['line'] = 0
				pawnCount['column'] = 0
				pawnCount['diagonal'] = 0

				if currentPawnOwnner == 0:
					continue

				for pawnOffset in range( 0, 4 ):
					# Ligne
					if (line+pawnOffset) < Engine.GRIDSIZE and currentPawnOwnner == self.grid[column][line + pawnOffset]:
						pawnCount['line'] += 1

					# Column
					if (column+pawnOffset) < Engine.GRIDSIZE and currentPawnOwnner == self.grid[column + pawnOffset][line]:
						pawnCount['column'] += 1

						canvas.create_line( self.calculateMidleOfPawn( line, column ), self.calculateMidleOfPawn( line, column + pawnOffset ), width=2, fill='blue' )

					# Diagonal
					if ((line+pawnOffset) < Engine.GRIDSIZE) and ((column+pawnOffset) < Engine.GRIDSIZE) and (currentPawnOwnner == self.grid[column + pawnOffset][line + pawnOffset]):
						pawnCount['diagonal'] += 1

				# Segment pour débuguage
				if DEBUGMODE and canvas != False:
					# > Ligne
					if (line+pawnOffset) < Engine.GRIDSIZE:
						size = 2 + int(pawnCount['line'] == 4)*3
						canvas.create_line( self.calculateMidleOfPawn( line, column ), self.calculateMidleOfPawn( line + pawnOffset, column ), width=size, fill='purple' )

					# > Colonne
					if (column+pawnOffset) < Engine.GRIDSIZE:
						size = 2 + int(pawnCount['column'] == 4)*3
						canvas.create_line( self.calculateMidleOfPawn( line, column ), self.calculateMidleOfPawn( line, column + pawnOffset ), width=size, fill='blue' )

					# > Diagonale
					if ((column+pawnOffset) < Engine.GRIDSIZE) and ((line+pawnOffset) < Engine.GRIDSIZE):
						size = 2 + int(pawnCount['diagonal'] == 4)*3
						canvas.create_line( self.calculateMidleOfPawn( line, column ), self.calculateMidleOfPawn( line + pawnOffset, column + pawnOffset ), width=size, fill='orange' )


					if pawnCount['line'] == 4 or pawnCount['column'] == 4 or pawnCount['diagonal'] == 4:
						print( '[OUI] L:', pawnCount['line'], 'C:', pawnCount['column'], 'D:', pawnCount['diagonal'] )
						return True
		return False

	def calculateMidleOfPawn( self, line, column ):
		displayX = Engine.GRIDBASEX + (Engine.PAWNSIZE+Engine.PAWNGAP)*line + Engine.PAWNSIZE//2
		displayY = Engine.GRIDBASEY + (Engine.PAWNSIZE+Engine.PAWNGAP)*column + Engine.PAWNSIZE//2

		return displayX, displayY
#===
# Gère l'affichage 
#==
class Application( Tk ):
	WINDOWSIZEW, WINDOWSIZEH = 370, 410
	BACKGROUNDCOLOR = "green"

	def __init__( self ):
		Tk.__init__( self )
		self.exiting = False

		self.title( "Puissance 4" )
		self.bind( '<Key>', self.key )
		self.resizable( width=False, height=False )

		self.canvas = Canvas( self, width = Application.WINDOWSIZEW, height = Application.WINDOWSIZEH )
		self.canvas.pack( fill = BOTH, expand = True )

		self.engine = Engine()

		self.displayEngine( self.engine )
		self.displayHelp()

	def displayEngine( self, grille ):
		#self.canvas.delete( ALL )
		self.canvas.create_rectangle( 0, 0, Application.WINDOWSIZEW, Application.WINDOWSIZEH, fill=Application.BACKGROUNDCOLOR )

		increment = Engine.PAWNSIZE + Engine.PAWNGAP

		displayY = Engine.GRIDBASEY
		for column in range( 0, 6 ):
			displayX = Engine.GRIDBASEX

			for line in range( 0, 6 ):
				case = grille.getCaseOwner( line, column )
				self.canvas.create_rectangle( displayX, displayY, displayX + Engine.PAWNSIZE, displayY + Engine.PAWNSIZE, fill=Engine.PAWNCOLOR[ case ])

				displayX += increment
			displayY += increment

		# Affichage du curseur
		cursor = self.engine.getCursor()
		cursorX = Engine.GRIDBASEX + increment*cursor
		cursorY = 20
		self.canvas.create_rectangle( cursorX, cursorY, cursorX + Engine.PAWNSIZE, cursorY + 10, fill=Engine.PAWNCOLOR[ self.engine.getPlayer() ] )

		self.engine.findWiner( self.canvas )

	def displayHelp( self ):
		helpMessage = "Bienvenue sur Puissance 4 !\n\n"

		helpMessage += '[F1] \tAfficher l\'aide\n'
		helpMessage += '[<] [>] \tDéplacer le curseur\n'
		helpMessage += '[ENTRE] \tPlacer un pion\n'
		helpMessage += '[DEL] \tRéinitialiser\n'
		helpMessage += '[ECHAP] \tQuitter\n'

		messagebox.showinfo( 'Aide', helpMessage, parent=self )	

	def exitingStatus( self ):
		return self.exiting

	###
	# Gestion des évenements
	##

	# $ Clavier
	#------------
	def key( self, event ):
		keylist = { 'ENTER': 36, 'DEL': 22, 'F1': 67, 'ESCAPE': 9, 'LEFT': 114, 'RIGHT': 113, 'R': 27 }
		key = event.keycode

		# Placement d'un pion
		if key == keylist['ENTER']:
			if self.engine.dropPawn():
				self.engine.changePlayer()

		elif key == keylist['F1']:
			self.displayHelp()

		# Arrêt du programme 
		elif key == keylist['ESCAPE']:
			self.exiting = True

		# Déplacement du curseur
		elif key == keylist['LEFT']:
			self.engine.moveCursor( Engine.LEFT )
		elif key == keylist['RIGHT']:
			self.engine.moveCursor( Engine.RIGHT )

		# Vide la grille
		elif key == keylist['DEL']:
			self.engine.emptyGrid()

			if self.engine.getPlayer() != 1:
				self.engine.changePlayer()

		# Remplissage aléatoire de la grille
		elif DEBUGMODE and key == keylist['R']:
			self.engine.randomGrid()


		self.displayEngine( self.engine )

if __name__ == '__main__':
	application = Application()

	while True:
		if not application.exitingStatus():
			application.update()
		else:
			exit(0)