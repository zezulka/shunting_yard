from anytree import Node, RenderTree

PRECEDENCE_TABLE = [['('], ['+', '-'], ['*', '/'], [')']]

def get_precedence(op):
    for (precedence, ops) in enumerate(PRECEDENCE_TABLE):
        if op in ops:
            return precedence
        else:
            "Op {} is not in {}, continuing further...".format(op, ops)
    raise ValueError("Unknown operator {}".format(op))

def can_push_op_to_stack(stack, op):
    if len(stack) == 0:
        return True
    precedence_cand = get_precedence(op)
    precedence_curr = get_precedence(stack[-1])
    return precedence_curr < precedence_cand

def shunting_yard_postfix(infix_string):
    """ Return an postfix representation of the infix input
expression (containing constants only)."""
    ops = []
    output = []
    for c in infix_string:
        if c.isnumeric() and int(c) in range(0,10):
            output.append(c)
        elif c != ' ':
            # We have an operator
            while not can_push_op_to_stack(ops, c):
                output.append(ops.pop())
            ops.append(c)

    # Remove all the remaining operations
    for op in ops[::-1]:
        output.append(op)
    return output

def shunting_yard_ast(infix_string):
    """ Return an AST representation (more specifically, a root of instance
 anytree.Node of the infix input
 expression (containing constants only). """
    root = None
    ops = []
    unprocessed = []
    for c in infix_string:
        if c.isnumeric():
            unprocessed.append(Node(c))
        elif c != ' ':
            # We have an operator
            while not can_push_op_to_stack(ops, c):
                root = Node(ops.pop())
                secondNode = unprocessed.pop()
                firstNode  = unprocessed.pop()
                firstNode.parent = root
                secondNode.parent = root
                unprocessed.append(root)
            ops.append(c)

    # Remove all the remaining operations
    for op in ops[::-1]:
        root = Node(ops.pop())
        secondNode = unprocessed.pop()
        firstNode  = unprocessed.pop()
        firstNode.parent = root
        secondNode.parent = root
        unprocessed.append(root)
    return root    

input_expression = input("Input a valid infix expression: ")
#print("Result for {} -> ".format(input_expression) 
#    + str(shunting_yard(input_expression)))
for pre, fill, node in RenderTree(shunting_yard_ast(input_expression)):
    print("%s%s" % (pre, node.name))
