Installation
==================

1. Please first download the zip archive from the link we provided. (You should have completed this step)

2. Unzip the archive. You can either (a) double click the archive in the file explorer (namely nautilus) and click "Extract" on the top left corner of the window to unzip or (b) using command line `unzip master.zip`. The unzipping process will automatically create a folder named `TACAS-artifact-master`, within which there are the directory of the artifact: `ILAng`, the license and this readme.

3. Open a terminal and change directory into the `TACAS-artifact-master` folder. You can do this by first using the file explorer to navigate into the `TACAS-artifact-master` folder and right clicking in the blank space of the file explorer and select "Open in Terminal".

4. Install dependent packages and ILAng: in the terminal just opened in the previous step, run 

    ```
    cd ILAng
    source INSTALL.sh
    ```
   
   This will start the installation process. When prompted for password, please type your password (a single letter "a" for this VM) and press `<Enter>` to grant root permission. 
 
 
   
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
       


Section 3.2  A Simple Execution Pipeline
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
         * This pipeline case is a simple version of the
           back-end of an in-order processor pipeline. It contains 3 
           pipeline stages and there is also a forwarding network. 
           To aid forwarding, there is also a tiny scoreboard implemented. 
           (See `$ILAROOT/examples/Simple-Pipe/README.md` for details)

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
      

ILAng BMC Engine Demo
----------------------------

#### Overview ####

The artifect in this section is to showcase
   
   1. Verification capability -- Unrolling and Bounded Model Checking (Section 2.3)

It constructs the ILA models for two FIFOs. One has a counter that counts
the number of elements currently in the fifo and does not enqueue any new element
when full, neither dequeue when empty. The other design has no such protection. 

The BMC here is to check if the non-overflow/underflow property holds on the 
two designs respectively.
  
#### Instructions ####

  1. Change directory to the folder that contains the design. In a terminal, type
     ```
     cd $ILAROOT/examples/FIFO-BMC
     ```
     There is `README.md` in the directory that further discusses the designs and properties to be checked.

  2. Compile the code, run
     ```
     make
     ```
     This will create an executable named `fifo-bmc`

  3. Run BMC to check the property. Run 
     ```
     ./fifo-bmc N
     ```
     where `N` is the bound, and it should be a positive integer, for example.
     ```
     ./fifo-bmc 20
     ```
     You will find that, if you set `N` to be smaller than or equal to the configured FIFO depth (which is 16 by default), BMC will not find that the `FIFO without protection` can overflow, though it can always find it can underflow. This is understandable, because to trigger the overflow, there has to be at least #Depth+1 (ie. 17) Enqueue operations whereas underflow can be triggered just be a Dequeue operation in the first step, when the FIFO is initiallly empty.

              

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




