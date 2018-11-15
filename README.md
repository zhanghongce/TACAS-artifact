Installation
==================

1. Please first download the zip archive `ILAng.zip` from the link we provided. (You should have completed this step)

2. Unzip the archive. You can either (a) double click the archive in the file explorer (namely nautilus) and click "Extract" on the top left corner of the window to unzip or (b) using command line `unzip ILAng.zip` with an optionaly `[-d <destination_path>]` argument to specify the destination. We suggest you create a new folder for this purpose, and unzip to its path.

3. Open a terminal and change directory to the folder that contains the unzip files. You can do this by first using the file explorer to navigate to the folder and right clicking in the blank space of the file explorer and select `Open in Terminal`.

4. Install dependent packages and ILAng: in the terminal just opened in the previous step, run 

    ```
    cd ILAng
    source INSTALL.sh
    ```
   
   This will invoke the installation process. When prompted for password, please type your password (`a` for this VM) and press <Enter> to grant root permission. 
 
 
   
Reproduce Results of Case Studies
====================================


Section 3.1 Advanced Encryption Standard (AES)
------------------------------------------------------

#### Overview ####

The artifect is to showcase
   
   1. Synthesis capabiblity (Section 2.2)
   2. Verification capability -- ILA vs. ILA verification utilities (Section 2.3)
  
By following the instructions, you will be able to reproduce the following results
reported in the paper

   1. ILA synthesis result (sizes of design and template & time to synthesis)
   2. ILA vs. ILA verification result (verification time)


#### Instructions ####

   1. After sucessfully installing ILAng, open a new terminal and run the following command  
      ```
      cd $ILAROOT/examples/AES-RTL-C
      ```

      This will land you in the directory of the AES case study.
      There is a README.md in this directory, which gives an overview of the design,
      explain the files under this directory, introduces behaviorial equivalence 
      checking and talks about the basics of how to write refinement relations.
       
      NOTE:
         * For the template for ILA-C (block-level), you can look into `CTemplate.py`
         * For the template for ILA-C (round-level), you can refer to `CRound.py` 
         * The refinement relations is rewritten in `CSimRfRelation.py`
           It is similar for ILA-V. 
         * If you have further questions about how to write a template, 
           you can refer to the following documentation: 
           `$ILAROOT\docs\ILA_Tutorial_Template_Synthesis_Verification.pdf` and
           `$ILAROOT\docs\ILA_User_Manual.pdf`.
    
   2. To synthesize ILA from a Verilog implementation, first run:
      ```
      cd Verilog
      make
      ```
        
      This will build a simulator from the Verilog design provided in the `Verilog` 
      directory, the simulator is an executable named `AESsim`. 
        
      Then start ILA synthesis using the following commands:
      
      ```
      cd $ILAROOT/examples/AES-RTL-C
      time ./syn_Vlg.py
      ```
        
      The synthesis algorithm will query the simulator and use the outcome to figure
      out the holes in the template. The generated ILA intemediate representation (IR)
      will be stored under folder `vILA`.
        
   3. Next, let's synthesize ILA from a C implementation (under folder `C`). Run
      ```  
      time ./syn_C.py
      ```
            
      To start synthesis. The synthesis process will automatically instrument the C
      code to generate a simulator. After synthesis complete, the ILA-IR will be stored
      in folder `cILA`.
    
   4. Behavioral equivalence checking. With the ILA-IR generated, run
      ```
      time ./IlaEqcheck.py
      ```
            
      This script will use the ILA equivalence checking utilities to check for equivalence.
      If no discrepency between the two models is found, the tool will report that 
      the equivalence holds.
       


Section 3.2  Arithmetic Logic Unit (ALU)
------------------------------------------------------

#### Overview ####

The artifect is to showcase
   
   1. Manually defined ILA and ILA programming interface (Section 2.2)
   2. Verification capability -- ILA vs. FSM verification utilities (Section 2.3)
  
By following the instructions, you will be able to reproduce the following results
reported in the paper

   1. Statistics of ILA definition (sizes of the design and ILA definition)
   2. ILA vs. Verilog verification result (verification time)


#### Instructions ####

   1. After sucessfully installing ILAng, open a new terminal. Run  
      ```
      cd $ILAROOT/examples/toy_alu
      ```
        
      This will land you in the directory of the ALU case study.
      In this directory, there is a README.md that gives an overview of this case
      study. 
       
      NOTE:
         * The example, despite it is small, is more than just a module 
           that performs arithmetic and logic operations. It is intended
           to mimic the execution unit of an in-order pipeline of a processor.
           This (dummy) execution unit contains 3 stages and there are also 
           forwarding network implemented as shown below. To aid forwarding, 
           there is also a tiny scoreboard implemented.
       

ILA and ILAng Documentation
====================================

In this section, we'd like to point to more ILA documentations if you would like
to have a further understanding.





