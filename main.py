import math

#WORK IN PROGRESS
class ParseError(Exception):
  pass

class ParsedExpression:
  def __init__(self, expression_list, variables):
    self.expression_list = expression_list
    self.result = None
    self.variables = variables
    self.constants = {'pi': 3.141592, 'e': 2.71828}
    self.math_functions = ['+', '-', '*', '/', '÷', '(', ')', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'log', 'abs', 'ceil', 'floor', 'round', 'exp']
    self.math_symbols = ['+', '-', '*', '/', '÷', '(', ')']
    self.variables_and_constants = {**self.variables, **self.constants}
    expression_string = ''
    for letter in expression_list:
      expression_string += ' '
      expression_string += str(letter)
    self.expression = expression_string.strip()
  
  @property
  def parsed_expression(self):
    return self.expression

  def calculate_expression(self):
    expression_list = self.expression_list
    i = 0
    current_calculated = 0
    for letter in expression_list:
      if str(letter).isdigit():
        if not i >= len(expression_list):
          i += 1
          math_function = expression_list[i]
          if math_function == '+':
            i += 1
            number = expression_list[i]
        else:
          break
      i += 1

  @property
  def calculate_result(self):
    self.calculate_expression()
    return self.result

class Parser:
  def __init__(self, expression, variables):
    if not type(variables) is dict:
      raise ParseError('Please pass in your variables as a dictionary.')
    self.variables = variables
    self.expression_list = list(expression.replace('π', 'pi').replace(' ', ''))
    self.characters = list('abcdefghijklmnopqrstuvwyxz')
    self.math_functions = ['+', '-', '*', '/', '÷', '(', ')', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'log', 'abs', 'ceil', 'floor', 'round', 'exp']
    self.math_symbols = ['+', '-', '*', '/', '÷', '(', ')']
    self.variables_names_list = list(variables.keys())
    self.variables_value_list = list(variables.values())
  
  def parse(self):
    variables = self.variables
    expression_list = self.expression_list
    characters = self.characters
    math_functions = self.math_functions
    math_symbols = self.math_symbols
    variables_names_list = self.variables_names_list
    variables_value_list = self.variables_value_list
    #check if there is an overlapping math symbol
    i = 0
    for variable in variables_names_list:
      if variable in math_functions:
        raise ParseError(f"Please name your {variable} variable a name that isn't any math symbol, such as +, -, * and ÷.")
      if not str(variables_value_list[i]).isdigit():
        if variables_names_list[i] in variables_value_list:
          variables_value_list[i + 1] = variables[variable]
      if variable.isdigit():
        raise ParseError(f"Please do not name the {variable} variable a number.")
      i += 1
    i = 0
    #part 1 of formatting the expression: 2X turns into 2 * X. also replaces the variables with their values
    for letter in expression_list:
      if letter in characters and not letter in variables:
        function_list = []
        i2 = i
        while True:
          if not i2 > 5 and not expression_list[i2] in math_symbols and not str(expression_list[i2]).isdigit():
            try:
              function_list.append(expression_list[i2])
            except:
              break
          else:
            break
          i2 += 1
        i += 1
        function = ''
        for letter in function_list:
          function += str(letter)
        i = i2
        if function in math_functions or len(function_list) == 0:
          if expression_list[i] == '(' or len(function_list) == 0:
            pass
          else:
            raise ParseError(f'Unexpected variable: {function}')
        else:
          raise ParseError(f'Unexpected variable: {function}')
      else:
        if str(letter).isdigit() or letter in variables_names_list:
          if not i > len(expression_list) - 2:
            if expression_list[i + 1] in variables_names_list:
              expression_list[i + 1] = variables[expression_list[i + 1]]
              expression_list.insert(i + 1, '*')
      i += 1
    i = 0
    #part 2 of formatting: ['1', '0', '0'] turns into '100' and etc.
    expression_formatted = []
    number_list = []
    while True:
      if not i > len(expression_list) - 1:
        if str(expression_list[i]).isdigit():
          number_list = []
          while True:
            if i > len(expression_list) - 1:
              break
            else:
              if not expression_list[i] in math_symbols and not expression_list[i] in characters and str(expression_list[i]).isdigit():
                number_list.append(expression_list[i])
                i += 1
              else:
                break
          add_formatted = ''
          for number in number_list:
            add_formatted += str(number)
          expression_formatted.append(add_formatted)
      else:
        break
      i += 1
    print(expression_formatted)
    #done formatting; now, begin calculating
    return ParsedExpression(expression_formatted, self.variables)

parsed_object = Parser('tan(100)+atan(200)+2x+3b+3b', {'x': 69420, 'b': 100}).parse()
print(parsed_object.expression)
print(parsed_object.calculate_result)