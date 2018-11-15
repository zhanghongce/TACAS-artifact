 
Handwritten ILA model using ILA APIs and ILA vs FSM Verification
=====================================================================


Overview
--------------

The example, despite it is small, is more than just a module 
that performs arithmetic and logic operations. It is intended
to mimic the execution unit of an in-order pipeline of a processor
(although we simply call it ALU). The design contains a register 
file with 4 registers.

The input of the module contains an 8-bit instruction field. This
is to mimic the output from the dispatch unit of the processor. 
The fields of the 8-bit inputs is define as following:

|------------------------------------------------------------|
|   op (2 bits) | rs1 (2 bits) | rs2 (2 bits) | rd (2 bits)  |
|------------------------------------------------------------|

This (dummy) execution unit contains 3 stages and there is also 
a forwarding network implemented as shown below.

|----------------------------------------|
|                                        |
|  input -- ID --|-- EX --|-- WB         |
|           ^         |       |          |
|           |         |       |          |
|           -------------------          |
|                                        |
|----------------------------------------|

To aid forwarding, there is also a tiny scoreboard implemented
to track future updates of the instructions in the pipeline. 
Based on the record in the scoreboard, the forwarding network 
decides when and where to forward a value.

As a small tutorial example, we focus more on the structure 
of the design. The operations of the execution unit is 
only a set of 3 operations (ADD/SUB/AND) and a NOP (do nothing). 


File Content
----------------
        
* ref-rel       : Folder for refinement relations
    * ref-rel-var-map.json : The variable mapping btw Verilog and ILA states
    * ref-rel-verilog.json : The start and ready conditions of instructions
    * instrument-map.json  : 
    
* vlg-verify.py : The script for parsing JSON 


ALU model
----------------

Refinement Relations
--------------------


Verification Toolchain
----------------------



