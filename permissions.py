class Tree(object):
    "Generic tree node."
    def __init__(self, name='root', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    
    def __repr__(self):
        return self.name
    
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

    def print_tree_aux(self, tree):
        for child in tree.children:
            print(child)
            self.print_tree_aux(child)

    def print_tree(self):
        print(self)
        self.print_tree_aux(self)

    def get_subtree_aux(self, tree, node):
        for child in tree.children:
            print(child)
            if child.name == node:
                return child
            else:
                res = self.get_subtree_aux(child, node)
                if res is not None:
                    return res
        return None

    def get_subtree(self, node):
        if self.name == node:
            return self
        else:
            return self.get_subtree_aux(self, node)


    def is_in_subtree_aux(self, tree, node):
        for child in tree.children:
            if child.name == node:
                return True
            else:
                res = self.is_in_subtree_aux(child, node)
                if res is not False:
                    return res
        return False

    def is_in_subtree(self, node):
        if self.name == node:
            return True
        else:
            return self.is_in_subtree_aux(self, node)


resources = Tree("All")
resource_A = Tree("A")
resource_B = Tree("B")
resource_C = Tree("C")
resource_A1 = Tree("A1")
resource_A11 = Tree("A1.1")
resource_A12 = Tree("A1.2")
resource_B1 = Tree("B1")
resource_C1 = Tree("C1")
resource_A2 = Tree("A2")
resource_B2 = Tree("B2")
resource_C2 = Tree("C2")
resources.add_child(resource_A)
resources.add_child(resource_B)
resources.add_child(resource_C)
resource_A.add_child(resource_A1)
resource_A.add_child(resource_A2)
resource_A1.add_child(resource_A11)
resource_A1.add_child(resource_A12)
resource_B.add_child(resource_B1)
resource_B.add_child(resource_B2)
resource_C.add_child(resource_C1)
resource_C.add_child(resource_C2)

#resources.print_tree()

# subtree = resources.get_subtree("D")
# if subtree is not None:
#     subtree.print_tree()
#     print("")
# else:
#     print(subtree)

subtree = resources.get_subtree("B")
# if subtree is not None:
#     subtree.print_tree()
#     print("")
# #    print(subtree.is_in_subtree("A1.2"))
# else:
#     print(subtree)

# subtree = resources.get_subtree("B1")
# if subtree is not None:
#     subtree.print_tree()
#     print("")
# else:
#     print(subtree)






#resources.is_in_subtree("A1.1", "A")
#resources.is_in_subtree("A1.1", "A")

#print_tree(resources)
#print(resources)

payload_data2 = {
    "sub": "4242",
    "access": [
        {
            "role": "admin",
            "resource": "all"
        },
        {
            "role": "admin",
            "resource": "A"
        }
    ]
}

#https://www.openpolicyagent.org/
json_access_scheme = {
    "role":
        { "admin" :
             [{
                "read_write" : 
                [
                    { 
                        "read" : "read"
                    },
                    {
                        "write" : "write"
                    }
                ]
            },
            {
                "delete" : "delete"
            }]    
        }
    }


access_scheme = { "admin": 
                    {"read_write": 
                        {"read": "true",
                        "write": "true"
                        }
                    },
                    "delete": "true",
                    "update": "true",
                    "create": "true"
                }


#print(access_scheme.get("read_write"))

resource_scheme = {
    "all": ["A", "B", "C"]
}