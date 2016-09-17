# -------------------------------
# Projet: Puissance 4
# Rôle: Contient le moteur de jeu
# Auteur:	kadeseb
# Crée le:	17/07/2016
# -------------------------------
from math import sqrt
from random import randrange
from configuration import *

#===============|
# Moteur de jeu | 
#===============|
class Engine:
	##
	# Constructeur
	##
	def __init__( self ):
		self.player = 1
		self.cursor = 0
		self.grid = [[0 for line in range( CONFIGURATION.GRID['LINE'] )] for column in range( CONFIGURATION.GRID['COLUMN'] )]

	##
	# Remplis la grille aléatoirement
	##
	def randomGrid( self ):
		self.emptyGrid()
		pawnNumber = randrange( CONFIGURATION.GRID['MINRANDOMPAWN'], CONFIGURATION.GRID['LINE']*CONFIGURATION.GRID['COLUMN'] )

		for i in range( 0, pawnNumber ):
			while True:
				owner = randrange( 0, 2+1 )
				column = randrange( 0, CONFIGURATION.GRID['COLUMN'] )
			
				if self.dropPlayerPawnAt( column, owner ):
					break;

	##
	# Vide la grille
	##
	def emptyGrid( self ):
		for column in range( 0, CONFIGURATION.GRID['COLUMN'] ):
			for line in range( 0, CONFIGURATION.GRID['LINE'] ):
				self.grid[column][line] = 0

	##
	# Retourne l'appartenance de la case spécifié
	#
	# -?-
	# x 		[int] Position x
	# y 		[int] Position y 
	#
	# -!-
	# [int] Engine.PLAYER
	##
	def getCaseOwner( self, column, line ):
		return self.grid[column][line]

	##
	# Place un pion du joueur spécifié dans la colonne spécifié 
	#
	# -?-
	# line 		[int] Colonne de la grille
	# player 	[int] Pion du joueur 
	#
	# -!-
	# [bool]	True si le pion a été placé, False si un paramètre est incorrect ou si la colonne ciblé est pleine 
	##
	def dropPlayerPawnAt( self, column, player ):
		if (player != 1 and player != 2 and player != 0) or (column >= CONFIGURATION.GRID['COLUMN'] and column < 0):
			return False

		for line in range( 0, CONFIGURATION.GRID['LINE'] ):
			if not self.grid[column][line] and ((line == (CONFIGURATION.GRID['LINE']-1)) or self.grid[column][line+1]):
				self.grid[column][line] = player
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
		if self.player == 1:
			self.player = 2
		elif self.player == 2:
			self.player = 1

	##
	# Recupère le joueur courrant
	##
	def getPlayer( self ):
		return self.player

	##
	# Déplace le curseur dans le sens spécifié
	#
	# -?-
	# direction		[int] Sens de déplacement
	#
	# -!-
	# [bool]		Retourne False si direction est incorrect   
	##
	def moveCursor( self, direction ):
		if direction != CONFIGURATION.DIRECTION['LEFT'] and direction != CONFIGURATION.DIRECTION['RIGHT']:
			return False

		if direction == CONFIGURATION.DIRECTION['LEFT']:
			if (self.cursor+1) >= CONFIGURATION.GRID['COLUMN']:
				self.cursor = 0
			else:
				self.cursor += 1
		else:
			if (self.cursor-1) < 0:
				self.cursor = CONFIGURATION.GRID['COLUMN'] - 1
			else:
				self.cursor -= 1

		return True

	##
	# Retourne la colonne ciblé par le curseur
	#
	# -!-
	# [int]		Curseur 
	def getCursor( self ):
		return self.cursor

	##
	# Détermine si un joueur à gagné
	#
	# -!-
	# [int]		Retourne le numéro du joueur gagnant, 0 si aucun
	##
	def findWiner( self, canvas = False ):
		pawnCount  = { 
			'line': 0, 
			'column': 0, 
			'diagonal': 0 
		}

		for column in range( 0, CONFIGURATION.GRID['COLUMN'] ):
			for line in range( 0, CONFIGURATION.GRID['LINE'] ):
				currentPawnOwnner = self.grid[column][line]

				pawnCount['line'] = 0
				pawnCount['column'] = 0
				pawnCount['diagonal'] = 0

				if currentPawnOwnner == 0:
					continue

				for pawnOffset in range( 0, 4 ):
					pawnCount['line'] += int( (line+pawnOffset) < CONFIGURATION.GRID['LINE'] and currentPawnOwnner == self.grid[column][line + pawnOffset] )
					pawnCount['column'] += int( (column+pawnOffset) < CONFIGURATION.GRID['COLUMN'] and currentPawnOwnner == self.grid[column + pawnOffset][line] )
					pawnCount['diagonal'] += int( ((line+pawnOffset) < CONFIGURATION.GRID['LINE']) and ((column+pawnOffset) < CONFIGURATION.GRID['COLUMN']) and (currentPawnOwnner == self.grid[column + pawnOffset][line + pawnOffset]) )

				# Segment pour débuguage
				"""
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
					if ((column+pawnOffset) < Engine.GRIDSIZE) and ((line+pawnOffset) <= Engine.GRIDSIZE):
						size = 2 + int(pawnCount['diagonal'] == 4)*3
						canvas.create_line( self.calculateMidleOfPawn( line, column ), self.calculateMidleOfPawn( line + pawnOffset, column + pawnOffset ), width=size, fill='orange' )

				"""
				if pawnCount['line'] == 4 or pawnCount['column'] == 4 or pawnCount['diagonal'] == 4:
					"""
					if CONFIGURATION._EXEC_['DEBUG_MODE']:
						print( '[OUI] L:', pawnCount['line'], 'C:', pawnCount['column'], 'D:', pawnCount['diagonal'] )
					"""
					return currentPawnOwnner

		return False

	def calculateMidleOfPawn( self, line, column ):
		displayX = CONFIGURATION.GRID['XGAP'] + (CONFIGURATION.PAWN['INCREMENT'])*line + CONFIGURATION.PAWN['SIZE']//2
		displayY = CONFIGURATION.GRID['YGAP'] + (CONFIGURATION.PAWN['INCREMENT'])*column + CONFIGURATION.PAWN['SIZE']//2

		return displayX, displayY