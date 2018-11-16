Installation
==================

1. Please first download the zip archive `ILAng.zip` from the link we provided. (You should have completed this step)

2. Unzip the archive. You can either (a) double click the archive in the file explorer (namely nautilus) and click "Extract" on the top left corner of the window to unzip or (b) using command line `unzip ILAng.zip` with an optionaly `[-d <destination_path>]` argument to specify the destination. We suggest you create a new folder for this purpose, and unzip to its path.

3. Open a terminal and change directory to the folder that contains the unzipped files. You can do this by first using the file explorer to navigate to the folder and right clicking in the blank space of the file explorer and select "Open in Terminal".

4. Install dependent packages and ILAng: in the terminal just opened in the previous step, run 

    ```
    cd ILAng
    source INSTALL.sh
    ```
   
   This will invoke the installation process. When prompted for password, please type your password (a single letter "a" for this VM) and press `<Enter>` to grant root permission. 
 
 
   
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

   1. ILA synthesis result (sizes of the design and template & time to synthesis)
   2. ILA vs. ILA verification result (verification time)


#### Instructions ####

   1. After sucessfully installing ILAng, open a new terminal and run the following command  
      ```
      cd $ILAROOT/examples/AES-RTL-C
      ```

      This will land you in the directory of the AES case study.
      There is a README.md in this directory, which gives an overview of the design,
      explains the files under this directory, introduces behaviorial equivalence 
      checking and talks about the basics of how to write refinement relations.
       
      NOTE:
         * For the template for AES_C (block-level), you can look into `CTemplate.py`
         * For the template for AES_C (round-level), you can refer to `CRound.py` 
         * The refinement relations is rewritten in `CSimRfRelation.py`
           It is similar for AES_V, except the file names start with a letter `V`. 
         * If you have further questions about how to write a template, 
           you can refer to the following documentation: 
           `$ILAROOT/docs/ILA_Tutorial_Template_Synthesis_Verification.pdf` and
           `$ILAROOT/docs/ILA_User_Manual.pdf`.
    
   2. To synthesize ILA from a Verilog implementation, first run:
      ```
      cd Verilog
      make
      ```
        
      This will build a simulator from the Verilog design provided in the `Verilog` 
      directory, the simulator is an executable named `AESsim` 
        
      Then start ILA synthesis using the following commands:
      
      ```
      cd $ILAROOT/examples/AES-RTL-C
      time python syn_Vlg.py
      ```
        
      The synthesis algorithm will query the simulator and use the outcome to figure
      out the holes in the template. The generated ILA intemediate representation (IR)
      will be stored under folder `vILA`.
        
   3. Next, let's synthesize ILA from a C implementation (under folder `$ILAROOT/examples/AES-RTL-C/C`). Run
      ```  
      time python syn_C.py
      ```
            
      To start synthesis. The synthesis process will automatically instrument the C
      code to generate a simulator. After synthesis completes, the ILA-IR will be stored
      in folder `cILA`.
    
   4. Behavioral equivalence checking. With the ILA-IR for both AES_V and AES_C generated, run
      ```
      time python IlaEqcheck.py -v vILA -c cILA
      ```
            
      This script will use the ILA equivalence checking utilities to check for behavioral equivalence.
      If no discrepency between the two models is found, the tool will report that 
      the equivalence holds.
       


Section 3.2  A Simple Execution Pipelines
------------------------------------------------------

#### Overview ####

The artifect is to showcase
   
   1. Manually defined ILA and ILA programming interface (Section 2.2)
   2. Verification capability -- Verfication Targets Generation (Section 2.4), ILA vs. FSM equivalence checking (Section 2.3)
  
By following the instructions, you will be able to reproduce the following results
reported in the paper

   1. Statistics of ILA definition (sizes of the design and ILA definition)
   2. ILA vs. Verilog verification result (verification time)


#### Instructions ####

   1. After sucessfully installing ILAng, open a new terminal. Run  
      ```
      cd $ILAROOT/examples/Simple-Pipe
      ```
        
      This will land you in the directory of the simple pipeline case study.
      In this directory, there is a README.md that gives an overview of this case
      study. 
       
      NOTE:
         * This example is intended to mimic the execution unit in the 
           back-end of an in-order processor pipeline. It contains 3 
           pipeline stages and there are also forwarding network 
           implemented as shown below. To aid forwarding, there is also 
           a tiny scoreboard implemented. (See 
           `$ILAROOT/examples/Simple-Pipe/README.md` for details)

      To learn about the size of the ILA constructing code, run
      ```
      wc -l ila/main.cc
      ```
      Similiarly, you can run
      ```
      wc -l verilog/simple_pipe.v
      ```
      to count lines of code of the Verilog design. 

   2. Construct the ILA and generate Verilog model from ILA. Run
      ```
      make
      ./main
      ```
      
      This will compile the C++ code under `ila` directory. This piece
      of C++ code constructs ILA-IR by calling its C++ API and use the
      ILAng functionality to generate a Verilog module (`vlg-gen/pipe.v`) 
      for equivalence checking.

      The ILA constructed by C++ code does not contain the 
      information of microarchitectural details (e.g., # of pipeline stages,
      scoreboard or forwarding network), because these are micro-architectural.
      The ILA constructed here, is a specification that only requires
      the correct execution of instructions according to the state update
      functions definitions. So is the Verilog code (`vlg-gen/pipe.v`),
      which also contains no pipelines. The behavior equivalence checking
      is to check functional equivalence while allowing flexibility in 
      specific implementations.
      
      To reproduce the result of equivalence checking, run
      ```
      time python vlg-verif.py -v verilog/simple_pipe.v -i vlg-gen/pipe.v
      ```
      
      The equivalence checking will first parse in the refinement relations,
      and decides the verification tasks. For each verification task, it
      will first generate a verification wrapper (`vlg-gen/all.v`), and calls
      yosys to parse the wrapper and produce a SMT-LIB2 file for SMT queries.
      The verification tasks contains (a) verifying the given inductive invariants,
      and (b) verifying the equivalence of each instruction assuming the invariants
      given are valid. A more detailed explanantion of what the inductive
      invariants specify can be found in `$ILAROOT/examples/Simple-Pipe/README.md`.
      If the verification failed, a waveform named `trace.vcd` showing the failing
      trace will be generated.
      
      We also provide an incorrectly implemented design `verilog/simple_pipe_wrong.v`,
      where the only difference from `verilog/simple_pipe.v` is around Line 162-163,
      about the bypassing network. In this wrong design, the designer wanted to 
      save some typing by copying the code of bypassing `rs1` and use it for bypassing
      `rs2`, but carelessly forgot to change the name of a signal from `1` to `2`, to 
      adapt it for rs2. You can check for the equvialence also between this Verilog
      implementation and the ILA specification using the following command:
      ```
      time python vlg-verif.py -v verilog/simple_pipe_wrong.v -i vlg-gen/pipe.v      
      ```

      The checking should fail and the trace that manifests this problem is generated and
      saved as `trace.vcd` in the same folder, which can be viewed using GtkWave:
      ```
      gtkwave trace.vcd &
      ```
      
      
              

ILA and ILAng Documentation
====================================

In this section, we'd like to point you to more ILA documentations (available online) 
if you would like to have a further understanding of ILA and ILAng. 

   1. User manual for writing a synthesis template: 
      * https://github.com/Bo-Yuan-Huang/ILA-Tools/blob/master/docs/ILA_User_Manual.pdf 
      * https://github.com/Bo-Yuan-Huang/ILA-Tools/blob/master/docs/ILA_Tutorial_Template_Synthesis_Verification.pdf 
   2. The API for manually constructing ILAs:
      * https://rawgit.com/Bo-Yuan-Huang/ILA-Tools/master/docs/api-html/namespaceila.html 
   3. The API for verification utilities and documentation for ILAng implementation:
      * https://rawgit.com/Bo-Yuan-Huang/ILA-Tools/master/docs/impl-html/namespaceila.html 




