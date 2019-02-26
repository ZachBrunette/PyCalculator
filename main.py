# original idea for calculator gui:
# https://medium.com/@adeyinkaadegbenro/project-build-a-python-gui-calculator-fc92bddb744d

from tkinter import *
from decimal import Decimal


class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Python Calculator")

        # create screen widget
        self.screen = Text(master, state='disabled', width=30, height=3, background="yellow", foreground="blue")

        # position screen in window
        self.screen.grid(row=0, column=0, columnspan=4, padx=5, pady=5)
        self.screen.configure(state='normal')

        # initialize screen value as empty
        self.equation = ''

        # create buttons using method createButton
        b1 = self.create_button(7)
        b2 = self.create_button(8)
        b3 = self.create_button(9)
        b4 = self.create_button(u"\u232B", None)
        b5 = self.create_button(4)
        b6 = self.create_button(5)
        b7 = self.create_button(6)
        b8 = self.create_button(u"\u00F7")
        b9 = self.create_button(1)
        b10 = self.create_button(2)
        b11 = self.create_button(3)
        b12 = self.create_button('*')
        b13 = self.create_button('.')
        b14 = self.create_button(0)
        b15 = self.create_button('+')
        b16 = self.create_button('-')
        b17 = self.create_button('=', None, 34)

        # buttons stored in list
        buttons = [b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15, b16, b17]

        # initialize counter
        count = 0
        # arrange buttons with grid manager
        for row in range(1, 5):
            for column in range(4):
                buttons[count].grid(row=row, column=column)
                count += 1
        # arrange last button '=' at the bottom
        buttons[16].grid(row=5, column=0, columnspan=4)

    def create_button(self, val, write=True, width=7):
        # this function creates a button, and takes one compulsory argument, the value that should be on the button
        return Button(self.master, text=val, command=lambda: self.click(val, write), width=width)

    def click(self, text, write):
        # this function handles what happens when you click a button
        # 'write' argument if True means the value 'val' should be written on screen,
        # if None, should not be written on screen
        if write is None:
            # only evaluate code when there is an equation to be evaluated
            if text == '=' and self.equation:
                # replace the unicode value of division ./. with python division symbol / using regex
                self.equation = re.sub(u"\u00F7", '/', self.equation)
                print(self.equation)
                answer = self.evaluate(self.equation)
                self.clear_screen()
                self.insert_screen(answer, newline=True)
            elif text == u"\u232B":
                self.clear_screen()
        else:
            # add text to screen
            self.insert_screen(text)

    def clear_screen(self):
        # to clear screen
        # set equation to empty before deleting screen
        self.equation = ''
        self.screen.configure(state='normal')
        self.screen.delete('1.0', END)

    def insert_screen(self, value, newline=False):
        self.screen.configure(state='normal')
        self.screen.insert(END, value)
        # record every value inserted in screen
        self.equation += str(value)
        self.screen.configure(state='disabled')

    def evaluate(self, equation):
        termslist = []
        termslist = self.find_terms(termslist, equation)
        print(termslist)
        answer = self.solve_equation(termslist)
        return answer

    def find_terms(self, termslist, equation):
        index = 0
        while equation is not None:
            if len(equation) == index:
                termslist.append(equation[:index])
                return termslist
            if equation[index] == '*' or equation[index] == "/" or equation[index] == "+" or equation[index] == "-":
                if index == 0:
                    termslist.append(equation[index])
                    equation = equation[(index+1):]
                else:
                    termslist.append(equation[:index])
                    equation = equation[index:]
                index = -1
            index += 1

    def solve_equation(self, termslist):
        newlist = []
        index = 0
        while index < len(termslist):
            if termslist[index] == '*' or termslist[index] == '/':
                if termslist[index] == '*':
                    newlist.append(Decimal(newlist.pop()) * Decimal(termslist[index+1]))
                    index += 1
                if termslist[index] == '/':
                    newlist.append(Decimal(newlist.pop()) / Decimal(termslist[index + 1]))
                    index += 1
            else:
                newlist.append(termslist[index])
            index += 1
        index = 0
        finallist = []
        while index < len(newlist):
            if newlist[index] == '+' or newlist[index] == '-':
                if newlist[index] == '+':
                    finallist.append(Decimal(finallist.pop()) + Decimal(newlist[index+1]))
                    index += 1
                if newlist[index] == '-':
                    finallist.append(Decimal(finallist.pop()) - Decimal(newlist[index + 1]))
                    index += 1
            else:
                finallist.append(newlist[index])
            index += 1
        print(finallist)
        if len(finallist) != 1:
            return self.solve_equation(finallist)
        else:
            return str(finallist[0])


root = Tk()
my_gui = Calculator(root)
root.mainloop()
