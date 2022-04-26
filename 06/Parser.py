"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from SymbolTable import *
from Code import *


class Parser:
    """Encapsulates access to the input code. Reads and assembly language 
    command, parses it, and provides convenient access to the commands 
    components (fields and symbols). In addition, removes all white space and 
    comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        self.input_lines = input_file.read().splitlines()
        self.commands_arr = []
        for line in self.input_lines:
            if ' ' in line:
                line = line.replace(' ', "")
            line = line.split('//')[0]
            if len(line) < 1 or line[0] == '\n':
                continue
            self.commands_arr.append(line)
        self.var_address = 16
        self.curr_line = 0
        self.num_of_L_comm = 0
        self.curr_command = self.commands_arr[self.curr_line]
        self.symbol_table = SymbolTable()
        self.first_run()
        self.second_run()

    def get_binary_code(self) -> str:
        """
        Returns the binary version of a line
        """
        symbol = self.symbol()
        if self.command_type() == "C_COMMAND":
            a = "1"
            if ">>" in self.curr_command or "<<" in self.curr_command:
                a = "0"
            return "1" + a + "1" + self.comp() + self.dest() + self.jump()
        elif self.command_type() == "A_COMMAND":
            if self.symbol_table.contains(symbol):
                return bin(int(self.symbol_table.get_address(symbol)))[
                       2:].zfill(16)
            elif symbol.isdigit():
                return bin(int(symbol))[2:].zfill(16)
        else:
            return ""

    def first_run(self):
        while self.has_more_commands():
            self.advance()
            if self.command_type() == "L_COMMAND":
                symbol = self.symbol()
                if self.symbol_table.contains(symbol):
                    continue
                else:
                    self.num_of_L_comm += 1
                    self.symbol_table.add_entry(symbol,
                                                self.curr_line - self.num_of_L_comm + 1)

    def second_run(self):
        self.curr_line = 0
        self.curr_command = self.commands_arr[0]
        while self.has_more_commands():
            self.advance()
            if self.command_type() == "A_COMMAND":
                symbol = self.symbol()
                if self.symbol_table.contains(symbol) or symbol.isdigit():
                    continue
                else:
                    self.symbol_table.add_entry(symbol, self.var_address)
                    self.var_address += 1

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self.curr_line < len(self.commands_arr) - 1

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        self.curr_line += 1
        self.curr_command = self.commands_arr[self.curr_line]

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        curr = self.curr_command
        if curr[0] == "@":
            return "A_COMMAND"
        elif curr[0] == "(":
            return "L_COMMAND"
        else:
            return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        curr = self.curr_command
        if self.command_type() == "A_COMMAND":
            return curr[1:]
        elif self.command_type() == "L_COMMAND":
            return curr[1: len(curr) - 1]
        return ""

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        curr = self.curr_command
        if self.command_type() == "C_COMMAND":
            if "=" in curr:
                return Code.dest(curr.split('=')[0])
            else:
                return Code.dest("")

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        curr = self.curr_command
        curr = curr.split(';')[0]
        if self.command_type() == "C_COMMAND":
            if "=" in curr:
                curr = curr.split('=')[1]
            return Code.comp(curr)

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # todo - there is some bug at the binary code
        curr = self.curr_command
        if self.command_type() == "C_COMMAND":
            if ";" in curr:
                return Code.jump(curr.split(';')[1])
            else:
                return Code.jump("")
