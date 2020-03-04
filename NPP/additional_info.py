
class AdditionalInfo(object):
	def __init__(self):
		self.temporary_variables = []

	def insert_temp_variables(self, _type, _name):
		self.temporary_variables.append((_type, _name))
		pass

	def retrieve_temp_variables(self):
		return self.temporary_variables
