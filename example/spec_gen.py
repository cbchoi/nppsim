import contexts

from NPP.process_spec import ProcessSpec
from NPP.code_generator import CodeGen
from NPP.additional_info import AdditionalInfo
'''
 Model Parameters
'''
alpha = 1
beta = 1
gamma = 1

bp_atomic = ProcessSpec("a")

bp_atomic.insert_shared_variables("bool", "ICN_ERR")
bp_atomic.insert_shared_variables("bool", "__MW3_0")

bp_atomic.insert_state("Heartbeat", alpha)
bp_atomic.insert_state("RESET", beta)
bp_atomic.insert_state("ATIP_Mon", gamma)
bp_atomic.insert_state("Func_End")

bp_atomic.set_init_state("Heartbeat")

'''
def guarded_insert_external_transition(self, pre_state, event, post_state, condition, actions):
	pass
'''
bp_atomic.insert_guarded_internal_transition("Heartbeat", None, "RESET", "ICN_ERR == True", [])
bp_atomic.insert_guarded_internal_transition("Heartbeat", None, "ATIP_Mon", "Else", [])
bp_atomic.insert_guarded_internal_transition("RESET", None, "ATIP_Mon", "True", ["HB_BP2ATIP = 0"])
bp_atomic.insert_guarded_internal_transition("ATIP_Mon", None, "Func_End", "True", ["__MW3_0 = HB_BP2ATIP"])

addition = AdditionalInfo()
addition.insert_temp_variables("bool", "HB_BP2ATIP")

cg = CodeGen(bp_atomic, addition)Í
print(cg.generate())