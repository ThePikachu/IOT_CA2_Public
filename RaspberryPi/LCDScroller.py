from rpi_lcd import LCD
import time

class LCDScroller:
	def __init__(self):
		self.lcd = LCD(rows = 2)
		self.lcd.clear()
		self.internalclear()
		self.update_time = time.time()

	def text(self, text, line):
		print(text)
		self.lcd.text(text,line)
		line -= 1
		self.index[line] = 0
		self.texts[line] = text

	def update(self):
		if time.time() - self.update_time < 0.5:
			return
		self.update_time = time.time()
		line = 0
		for txt in self.texts:
			text_len = len(txt)
			if text_len > 16:
				self.index[line] += 1
				new_text = txt[self.index[line] : self.index[line] + 16]
				if self.index[line] + 17 > text_len:
					if len(new_text) <= 0:
						self.index[line] = 0
						new_text = txt[0 : 16 - len(new_text)]
					else:
						new_text += ' ' + txt[0 : 16 - len(new_text)]
				self.lcd.text(new_text,line + 1)
			line += 1

	def clear(self):
		self.lcd.clear()
		self.texts
		self.internalclear()

	def internalclear(self):
		self.texts = ['','']
		self.index = [0,0]
