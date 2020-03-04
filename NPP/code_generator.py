import contexts

from evsim.definition import Infinite
from NPP.process_spec import ProcessSpec

from collections import deque

class CodeGen(object):
	def __init__(self, spec, additional):
		self.spec = spec
		self.additional_info = additional

	def attach(self, prefix, res, postfix):
		res = prefix + res
		res += postfix
		return res

	def generate(self):
		result = self.attach("", "// Code Generated", "\n")
		
		'''
		definition of shared variables
		'''
		result += self.attach("\n", "// Definitions of Shared Variables", "\n")
		for var in self.spec.retrieve_shared_variables():
			res = self.attach("", "external", "")
			res += self.attach(" ", var[0], " ")
			res += self.attach("", var[1], ";")
			result += self.attach("", res, "\n")

		'''
		Task function generation
		static void prvSpecNameTask( void *pvParameters );
		'''

		result += self.attach("\n", "static void prv{0}Task( void* pvParameters ){", "")

		'''
		definition of temporary variables
		'''
		result += self.attach("\n", "// Definitions of Temporary Variables", "\n")

		for var in self.additional_info.retrieve_temp_variables():
			res = self.attach("\t", var[0], " ")
			res += self.attach("", var[1],";")
			result += self.attach("", res, "\n")

		result += self.attach("", self.traverse_internal_transitions(self.spec.retrieve_init_state(), 1), "\n}")
		return result

	'''
	def traverse_internal_transitions(self):
		traverse_q = deque()
		traverse_q.append(self.spec.retrieve_init_state())
		_visit = []

		while(traverse_q):
			_state = traverse_q.popleft()
					
			if self.spec.retr0ieve_states()[_state] == Infinite:
				pass
			elif _state in _visit:
				pass
			else:
				print(_state)
				_visit.append(_state)
				for in_trans in self.spec.retrieve_g_internal_transition(_state):
					traverse_q.append(in_trans[2])
					print(in_trans[0])
					for act in in_trans[3]:
						print("\t" + act)

		'''		

	def gen_if_stmt_begin(self, cond, level):
		tabbed = "\t" * level
		result = tabbed + "if({0})".format(cond)
		result += "\n" + tabbed +"{"
		return result

	def gen_else_stmt_begin(self, level):
		tabbed = "\t" * level
		result = "\n" + tabbed + "else{"
		return result

	def condition_stmt_end(self, level):
		result = "\t" * level + "}"
		return result

	def traverse_internal_transitions(self, _state, level):
		result = ""
		if self.spec.retrieve_states()[_state] == Infinite:
			return ""
		else:
			tabbed = '\t' * level
			result += self.attach(tabbed, "Sleep({0});".format(self.spec.retrieve_states()[_state]), "\n")
			
			#print(result + str(self.spec.retrieve_g_internal_transition(_state)))
			for in_trans in self.spec.retrieve_g_internal_transition(_state):
				'''
				in_trans[0] : condition
				in_trans[1] : event
				in_trans[2] : post state
				in_trans[3] : actions
				'''
				if in_trans[0] is None or in_trans[0] == "True":
					for act in in_trans[3]:
						result += self.attach(tabbed, act, ";\n")
					result += self.attach("", self.traverse_internal_transitions(in_trans[2], level), "")
				else:
					if in_trans[0] != "Else":
						result += self.attach("", self.gen_if_stmt_begin(in_trans[0], level), "\n")
					else:
						result += self.attach("", self.gen_else_stmt_begin(level), "\n")

					for act in in_trans[3]:
						result += self.attach("\t"*(level+1), act, ";\n")
						
			
					result += self.traverse_internal_transitions(in_trans[2], level+1)
					result += self.condition_stmt_end(level)

		return result