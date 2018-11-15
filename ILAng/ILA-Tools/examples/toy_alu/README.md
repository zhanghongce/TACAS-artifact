 
Handwritten ILA model using ILA APIs & ILA vs. FSM Equivalence Checking
=====================================================================


Overview
--------------

It is intended to mimic the execution unit of an in-order pipeline 
of a processor (although we simply call it ALU). The design contains 
a register file with 4 registers.

The input of the module contains an 8-bit instruction field. This
is to mimic the output from the dispatch unit of a processor. 
The fields of the 8-bit inputs are define as following:

<pre>
|------------------------------------------------------------|
|   op (2 bits) | rs1 (2 bits) | rs2 (2 bits) | rd (2 bits)  |
|------------------------------------------------------------|
</pre>

This (dummy) execution unit contains 3 stages and there is also 
a forwarding network implemented as shown below.

<pre>                                    
  input -- ID --|-- EX --|-- WB         
           ^         |       |          
           |         |       |          
           -------------------                                                  
</pre>

To aid forwarding, there is also a tiny scoreboard implemented
to track register updates of the instructions in the pipeline. 
Based on the record in the scoreboard, the forwarding network 
decides when and where to forward a value.

As a small tutorial example, we focus more on the structure 
of the design. The operations of the execution unit is 
only a set of 3 operations (ADD/SUB/AND) and a NOP (do nothing). 


File Content
----------------

* ila                      
    * main.cc              : The C++ source code that constructs the ILA
* verilog
    * simple_alu.v         : A pipelined Verilog implementation
* ref-rel                  : Folder for refinement relations
    * ref-rel-var-map.json : The variable mapping btw Verilog and ILA states
    * ref-rel-verilog.json : The start and ready conditions of instructions
    * instrument-map.json  : The list of Verilog signals that needs to be pull to the top level (automatically by code instrumenting)
* vlg-verify.py : The script for parsing JSON 


Behaviorial Equivalence
-------------------------
The ILA model in `ila/main.cc` does not contain the information of
the pipeline, scoreboard or forwarding logic. This is intended 
as it is a _specification_, while an implementation is free to choose 
its way of performing the operations, whether pipelined or not. So 
the equivalence between the ILA model and the Verilog model is not 
combinational or sequential equivalence. It is _behaviorial_ equivalence.

For more information about the equivalence checking, you can refer to our
previous [paper](https://arxiv.org/abs/1801.01114) on arXiv.

Refinement Relations
--------------------
The refinement relations for checking behaviorial equivalence between
the ILA model and the Verilog implementation is specified under directory
`ref-rel`. The refinement relations specify how to apply an instruction,
the commit point of instructions and the variable mapping between ILA state
variables and RTL variables.

In the design, there is the need to (a)


Verification Toolchain
----------------------

The verification uses Yosys + Z3. Yosys parses input verilog and generate 
SMT-LIB2 output to work with Z3. A python script provided along with Yosys 
(under `~/yosys/yosys-smtbmc.py`) is capable of assembling SMT assertions 
from the a generated SMT-LIB2 file. As its name suggested, it is capable of
performaing Bounded Model Checking (BMC).




