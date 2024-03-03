from fltk import *
import random
import os
'''
		self.flag_image_path = os.path.join(os.path.dirname(__file__), 'flag.png')
		self.bomb_image_path = os.path.join(os.path.dirname(__file__), 'bomb.png')
		self.bomb_wrong_image_path = os.path.join(os.path.dirname(__file__), 'bombwrong.png')
'''
class button(Fl_Button):
	def __init__(self,bomb,window,count,tileX,tileY,boolbomb,x,y,w,h,l=''):
		self.flag_image_path = os.path.join(os.path.dirname(__file__), 'flag.png')
		self.boolbomb = boolbomb
		self.count = count
		self.window = window
		self.tileX = tileX
		self.tileY = tileY
		self.bomb = bomb
		if boolbomb == True:
			self.visit = True
		else:
			self.visit = False
		self.flagged = False
		self.flaggable = True
		self.firstturn = 0
		super().__init__(x,y,w,h)
		self.x = 0		

	def handle(self,event):
		r = super().handle(event)
		rep = 0

		if event == FL_PUSH and Fl.event_button() == FL_LEFT_MOUSE:
			self.x = 1
			return 1
		elif event == FL_RELEASE and Fl.event_button() == FL_LEFT_MOUSE:
			if self.flagged == False:
				if self.x == 1 and self.boolbomb == False:
					self.x = 0
					self.window.reveal(self.tileX, self.tileY)
					self.window.wincheck()
					
				if self.boolbomb == True:
					self.window.lose = True
					for x in self.bomb:
						self.window.losefunc(x)
					for y in range(10):
						for x in range(10):
							self.window.reveal(x,y)	
					fl_message('You Lose')
			return 1
			
		if event == FL_PUSH and Fl.event_button() == FL_RIGHT_MOUSE and self.window.lose == False and self.flaggable == True:
			if self.flagged == False:
				pic = Fl_PNG_Image(self.flag_image_path)
				pic = pic.copy(75,75)
				self.flagged = True
				self.image(pic)
				self.redraw()
			elif self.flagged == True:
				self.image(None)
				self.redraw()
				self.flagged = False
			return 1
				
		else:
			return r
			
class app(Fl_Window):
	def __init__(self,x,y,w,h,l=''):
		super().__init__(x,y,w,h,l)
		self.begin()
		self.bomb_image_path = os.path.join(os.path.dirname(__file__), 'bomb.png')
		self.bomb_wrong_image_path = os.path.join(os.path.dirname(__file__), 'bombwrong.png')
		self.firstturn = True
		self.seconds = 0
		self.minutes=0
		self.timer = '0:00'
		self.lose = False
		self.bomb = (random.sample(range(0,100),10))
		count = 0
		boolbomb = False
		self.LB = []
		
		for y in range(10):
			for x in range(10):
				for n in self.bomb:
					if n == count:
						boolbomb = True
				self.LB.append(button(self.bomb,self,count,x,y,boolbomb,x*300//4,y*300//4+75,75,75))
				boolbomb = False
				count+=1
				
		self.box1 = Fl_Box(0,0,w,75,'0:00')
		
		self.end()

	def tofunc(self):
		self.box1.label(self.timer)
		self.seconds+=1
		if self.seconds%60 == 0:
			self.minutes+=1
			self.seconds = 0
		if self.seconds<=9:
			self.timer = (str(self.minutes)+':0'+str(self.seconds))
		else:
			self.timer = (str(self.minutes)+':'+str(self.seconds))
		Fl.repeat_timeout(1.0,self.tofunc)
	
	def wincheck(self):
		win = True
		for x in self.LB:
			if x.visit == False:
				win = False
				
		if win == True and self.lose == False:
			Fl.remove_timeout(self.tofunc)
			h = open('MinesweeperSc.txt','r')
			highscore = h.read()
			prev = self.gettime(highscore)
			newscore = self.gettime(self.timer)
			
			for x in self.bomb:
				if self.LB[x].flagged == False:
					self.losefunc(x)
					
			if newscore<prev:
				fl_message('You got a new high score! Please write your name in the terminal')
				usrinp = input('Write Your Name: ')
				outf = open('MinesweeperSc.txt','w')
				outf.write(f'{usrinp} {self.timer}')
				outf.close()

			fl_message(f'You Win! It took you {self.timer} to win')


	def char(self,times):
		for x in range(10): #checks if it is an int or str
			if str(x) == times:
				return True
		return False
		
	def gettime(self,hs):
		minutes = ''
		for times in str(hs):
			charcheck = self.char(times)
			if times == ':':
				break
			if charcheck == True:
				minutes=minutes+times
		minutes = int(minutes)
		seconds = hs[-2:]
		minutes*=60
		return (minutes+int(seconds))
		
	def losefunc(self,x):
		Fl.remove_timeout(self.tofunc)
		pic = Fl_PNG_Image(self.bomb_image_path)
		pic = pic.copy(75,75)
		self.LB[x].image(pic)
		self.LB[x].redraw()
		
	def getTileButton(self,tileX,tileY):
		return self.LB[tileY*10+tileX]

	def reveal(self,tileX,tileY):
		self.visited={}
		self.revealNums(tileX,tileY)
		if self.firstturn == True:
			Fl.add_timeout(0.1,self.tofunc)
			self.firstturn=False
			
	def revealNums(self,tileX,tileY):
		tileKey = str(tileX)+str(tileY)
		if tileKey in self.visited.keys():
			return

		self.visited[tileKey] = True

		minX = max(tileX-1, 0)
		maxX = min(tileX+2, 10)
		minY = max(tileY-1, 0)
		maxY = min(tileY+2, 10)
		
		bombCount = 0
		for y in range(minY,maxY):
			for x in range(minX,maxX):
				tileButton = self.getTileButton(x, y)
				if tileButton.boolbomb:
					bombCount += 1


		mc = self.getTileButton(tileX, tileY)
		
		if mc.flagged == True and self.lose == False:
			mc.image(None)
			mc.flagged == False
			
		if mc.boolbomb == False and self.lose == True and mc.flagged == True:
			mc.image(None)
			pic = Fl_PNG_Image(self.bomb_wrong_image_path)
			pic = pic.copy(75,75)
			mc.image(pic)

		if bombCount>0 and mc.boolbomb == False:
			mc.label(str(bombCount))
		
		winCheck = 0
		mc.flaggable = False
		mc.visit = True
		
		
		if bombCount == 0:
			mc.deactivate()
			for y in range(minY,maxY):
				for x in range(minX,maxX):
					self.revealNums(x, y)


win = app(0,0,750,825,'Minesweeper')
win.resizable(win)
win.show()
Fl.scheme('plastic')
Fl.run()
