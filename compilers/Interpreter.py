
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
from myTypes import *
import sys

sys.setrecursionlimit(10000)

class Interpreter(object):
    def __init__(self):
        self.memory = MemoryStack(Memory("global"))

    @staticmethod
    def isNumber(number):
        return number is Number

    @staticmethod
    def isMatrix(matrix):
        return matrix is Matrix or matrix is Array

    @staticmethod
    def wrapNumber(number):
        return Integer(number) if number is int else Float(number)

    @staticmethod
    def wrapMatrix(rawMatrix):
        x = len(rawMatrix)
        y = len(rawMatrix[0]) 
        matrixType = type(rawMatrix[0][0])
        return Matrix(x, y, matrixType, rawMatrix)

    @on('node')
    def visit(self, node):
        pass

    @when(AST.BinaryExpression)
    def visit(self, node):
        print("Interpret bin expr")
        left = node.left.accept(self)
        right = node.right.accept(self)
        operator = node.op
        numberOperation = { 
            '+': lambda x, y: wrapNumber(x + y),
            '-': lambda x, y: wrapNumber(x - y),
            '*': lambda x, y: wrapNumber(x * y),
            '/': lambda x, y: wrapNumber(x / y)
        }
        matrixOperation = {
            '+': lambda x, y: #define this operation in Matrix class in myTypes
        }
        if operator in ['+', '-', '*', '/']:
            if isNumber(left):
                return numberOperation[operator](left, right)
            elif isMatrix(left):
                return matrixOperation[operator](left, right)
        if operator in ['+=', '-=', '*=', '/=']:
            if isNumber(left):
                value = numberOperation[operator[0]](left, right)
                self.memory.set(node.left.name, value)
                return value
            elif isMatrix(left):
                value = matrixOperation[operator[0]](left, right)
                self.memory.set(node.left.name, value)
                return value
            else:
                #string or array? what then?
                pass
        if operator in ['.+', '.-', '.*', './']:
            value = matrixDotOperation[operator](left, right)
            return value
        if operator in ['==', '<', '>', '<=', '>=', '!=']:
            return booleanOperation[operator](left, right)
        if operator == '=':
            self.memory.insert(node.left.name, right)
            return right
        
        

            



    @when(AST.UnaryExpression)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        op = node.op
        pass

    @when(AST.Return)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        op = node.op
        pass

    @when(AST.Block)
    def visit(self, node):
        print("Interpret block")
        for expression in node.body:
            expression.accept(self)

        


