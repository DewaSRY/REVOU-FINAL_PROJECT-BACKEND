


from dataclasses import dataclass,field

@dataclass 
class MockData:
    id:int= field(init=False)
    name:str
    
    def halloo():
        print("hallo")