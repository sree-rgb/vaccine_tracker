import mailer
import datetime

message_template = """\
Subject: {l_string} Vaccine available

{l_string}
pincode: {pincode}
"""

class user:
	def __init__(self,pincodes):
		self.pincodes = pincodes
		self.pin_dict = {}
		for pincode in pincodes:
			self.pin_dict[pincode] = 'Unavailable'

	def notify(self,pincode_availability):
		for pincode in pincode_availability.keys():
			if pincode in self.pincodes:
				if pincode_availability[pincode] and self.pin_dict[pincode] == 'Unavailable':
					l_string = self.get_location(pincode_availability[pincode])
					print('Notify')
					self.send_mail(pincode=pincode, l_string=l_string)
					self.pin_dict[pincode] = 'Notified'
				if not pincode_availability[pincode] and self.pin_dict[pincode] == 'Notified':
					print(f'Marked Unavailable:{pincode}')
					self.pin_dict[pincode] = 'Unavailable'
	def get_location(self, pin_dict):
		outputlist = []
		for key in pin_dict.keys():
			outputlist.append(f'{key}:{pin_dict[key]}')
		return ' | '.join(outputlist)
	def send_mail(self, pincode, l_string):
		t1 = datetime.datetime.now()
		mailer.mailer(message_template.format(pincode=pincode, l_string=l_string))

if __name__ == '__main__':
	usr_1 = user([682305, 682314, 682312])
	usr_1.send_mail(682305,'Kuttampuzha FHC:0')