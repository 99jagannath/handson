
class Notation:
    def __init__(self):
        self.precedence = {
            '+' : 1,
            '-' : 1,
            '*' : 2,
            '/' : 2,
            '^' : 3
        }

    def convertInfixToPostFix(self, notation_string):
        stack = []
        ans = ""

        for ch in notation_string:
            if ch == '(':
                stack.append(ch)

            elif ch == ')':
                while len(stack) > 0 and stack[-1] != '(':
                    ans += stack.pop()

                if len(stack) > 0 and stack[-1] =='(':
                    stack.pop()

            elif ch.isdigit():
                ans += ch
            
            else:
                while len(stack) > 0 and stack[-1] != '(' and self.precedence[stack[-1]] >= self.precedence[ch]:
                    ans += stack.pop()
                stack.append(ch)

        while len(stack) > 0:
            ans += stack.pop()
        return ans
    
    def convertInfixToPrefix(self, notation_string):

        cur = list(notation_string[::-1])
        for i in range(len(cur)):
            if cur[i] == '(':
                cur[i] = ')'
            
            elif cur[i] == ')':
                cur[i] = '('

        postfix = self.convertInfixToPostFix(''.join(cur))

        return postfix[::-1]
    
    def operate(self, num1, num2, operator):
        if operator == '+':
            return num1 + num2
        elif operator == '-':
            return num1 - num2
        elif operator == '*':
            return num1 * num2
        elif operator =='/':
            return num1 / num2
        else:
            return num1 ^ num2
    
    def calculate(self, notation_string):
        operator_stack = []
        operand_stack = []
        for ch in notation_string:
            if ch == '(':
                operator_stack.append(ch)
            elif ch == ')':
                while len(operand_stack) > 2 and len(operator_stack) > 0 and operator_stack[-1] !='(':
                    top1 = operand_stack.pop()
                    top2 = operand_stack.pop()
                    operator = operator_stack.pop()
                    operand_stack.append(self.operate(top2, top1, operator))
                if len(operator_stack) > 0 and operator_stack[-1] =='(':
                    operator_stack.pop()

            elif ch.isdigit():
                operand_stack.append(int(ch))
            else:
                while len(operator_stack) > 0 and operator_stack[-1] != '(' and self.precedence[operator_stack[-1]] >= self.precedence[ch] and len(operand_stack) > 2:
                    top1 = operand_stack.pop()
                    top2 = operand_stack.pop()
                    operator = operator_stack.pop()
                    operand_stack.append(self.operate(top2, top1, operator))
                operator_stack.append(ch)

        while operator_stack:
            operator = operator_stack.pop()
            top1 = operand_stack.pop()
            top2 = operand_stack.pop()
            operand_stack.append(self.operate(top2, top1, operator))

        return operand_stack
                    

    

notation = Notation()

print(notation.convertInfixToPostFix("3+5*(2-6)^4"))

print(notation.convertInfixToPrefix("3+5*(2-6)^4"))
print(notation.calculate("3+5*(2-6)+4"))
