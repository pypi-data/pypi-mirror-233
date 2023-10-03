import sys
import re
from .enums import PromiseState
from .types_pb2 import AgentSpec, Promise

def parse_promise(promise_string: str):
    result = re.search("Promise\(\s*([-\w]+)\s+as\s+([-\w]+)\s+from\s+([-\w]+)\s*\)", promise_string)
    if result == None:
        result = re.search("^Promise", promise_string)
        if result != None:
            raise Exception(f"possible Promise detected '{promise_string}'; please check name, type, and source for spelling")
        else:
            return
    
    p = Promise(name=result.group(1),
                type=result.group(2),
                source=result.group(3),
                state=PromiseState.PENDING,
                data=None)
    
    return p

def parse_promises(spec: AgentSpec):
    promises = {}

    # Iterate over attributes, extracting promises and saving
    for attr in spec.attributes:
        attr_val = spec.attributes[attr]
        p = parse_promise(attr_val)

        if p == None:
            continue
        
        promises[attr]= p
    
    return promises

class PromiseSet():
    
    promises = {}
    
    def __init__(self, spec: AgentSpec):
        self.promises = parse_promises(spec)
        
    def all_fulfilled(self):
        for name, promise in self.promises.items():
            if promise.state == PromiseState.PENDING:
                return False

        return True

    def contains(self, promise):
        for name, curr_prom in self.promises.items():
            data_id_match = (promise.name == curr_prom.name)
            data_type_match = (promise.type == curr_prom.type)
            source_match = (promise.source == curr_prom.source)

            if data_type_match and data_id_match and source_match:
                return (name, True)

        return ("", False)
    
if __name__ == "__main__":

    spec = AgentSpec(attributes = {
        "second": "Promise( hello as hellotype from   silly_goose )",
        "notpromise":"10"})
    
    promise_set = PromiseSet(spec)
    if promise_set.all_fulfilled():
        print("FAIL: promises are not fulfilled")

    if len(promise_set.promises) > 1:
        print("FAIL: too many promises")

    # "fulfill" the promise
    promise_set.promises["second"].state = PromiseState.FULFILLED

    if not promise_set.all_fulfilled:
        print("FAIL: promises should be fulfilled")
