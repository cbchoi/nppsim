from collections import OrderedDict

from evsim.behavior_model import BehaviorModel
from evsim.system_message import SysMessage
from evsim.definition import *

from config import *

class ProcessSpec(BehaviorModel):
    def __init__(self, name):
        BehaviorModel.__init__(self, name)
        self.init_state = None
        self.shared_variables = []
        self.search_structure_external = {}
        self.search_structure_internal = {}

    def set_init_state(self, _state):
        self.init_state = _state

    def retrieve_init_state(self):
        return self.init_state

    def insert_shared_variables(self, _type, _name):
        self.shared_variables.append((_type, _name))

    def retrieve_shared_variables(self):
        return self.shared_variables
    
    def insert_guarded_internal_transition(self, pre_state, event, post_state, condition, actions):

        self.internal_transition_map_tuple[(pre_state, event, condition)]  = (actions, post_state, actions)
        
        if (pre_state, condition) in self.internal_transition_map_state:
            self.internal_transition_map_state[(pre_state, condition)].append(event, post_state)
        else:
            self.internal_transition_map_state[(pre_state, condition)] = [(event, post_state, actions)]
            
        if pre_state in self.search_structure_internal:
            self.search_structure_internal[pre_state].append((condition, event, post_state, actions))
        else:
            self.search_structure_internal[pre_state] = [(condition, event, post_state, actions)]

        pass

    def insert_guarded_external_transition(self, pre_state, event, post_state, condition, actions):
        self.external_transition_map_tuple[(pre_state, event, condition)] = (actions, post_state)
        if (pre_state, condition) in self.external_transition_map_state:
            self.external_transition_map_state[(pre_state, condition)].append(event, post_state, actions)            
        else:
            self.external_transition_map_state[(pre_state, condition)] = [(event, post_state, actions)]

        if pre_state in self.search_structure_external:
            self.search_structure_external[pre_state].append((condition, event, post_state, actions))
        else:
            self.search_structure_external[pre_state] = [(condition, event, post_state, actions)]

    def retrieve_g_external_transition(self, pre_state):
        return self.search_structure_external[pre_state]

    def retrieve_g_internal_transition(self, pre_state):
        return self.search_structure_internal[pre_state]

    def serialize(self):
        json_obj = OrderedDict()
        json_obj["name"] = self._name
        json_obj["states"] = self._states
        json_obj["input_ports"] = self.retrieve_input_ports()
        json_obj["output_ports"] = self.retrieve_output_ports()
        json_obj["shared_variables"] = self.shared_variables
        json_obj["external_trans"] = self.external_transition_map_state
        json_obj["internal_trans"] = self.internal_transition_map_state
        return json_obj

    def deserialize(self, json):
        self._name = json["name"]
        for k, v in json["states"].items():
            self.insert_state(k, v)

        # Handle In ports
        for port in json["input_ports"]:
            self.insert_input_port(port)

        # Handle out ports
        for port in json["output_ports"]:
            self.insert_output_port(port)

        # Handle out ports
        for var in json["shared_variables"]:
            self.insert_shared_variables(var)

        # Handle External Transition
        for k, v in json["external_trans"].items():
            print(v)
            for ns in v:
                self.insert_guarded_external_transition(k[0], ns[0], ns[1], k[1], ns[2])

        # Handle Internal Transition
        for k, v in json["internal_trans"].items():
            for ns in v:
                self.insert_guarded_internal_transition(k[0], ns[0], ns[1], k[1], ns[2])