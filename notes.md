# Learning goals
- MILP rolling horizon (done)
- Newly trained RL operation

# Goals of the day for thesis
1. Finish methodology section with the current assumption
2. Run all the case study scenarios
3. Create or import all the figures, tables, equations I want to add
4. Finish the level 1 and level 2 comparison section of chapter 4
5. Submit tonight

## Notes
- Maybe I can also automate table creation with agent?


### Methodology

•	This comparison will be done in two steps: 
o	Joint operational dispatch and sizing methodology comparison:
	The innerloop operational decision is fixed as an oemof problem, 
	Co-optimization of using investment block (IB) vs Bilevel Optimization of Bayesian Optimization (BO)
	This outerloop comparison is to pinpoint which approach results in the best layout both under linear and non-linear economic of scale assumptiom, and other parameters.
	A sensitivity analysis will be conducted for the MILP by varying the methanol price assumption in the beginning since full MILP framework can’t optimize for non linear LCOM, rather only total cost
•	There are four case studies for each step to be analyzed (For the outerloop comparison):
o	Economic assumption: Linear and non-linear economic of scale
o	Weather Variability:
	Stable solar and wind input
	Extreme weather volatility
o	Market Conditions:
	Current and forecasted 2030
•	For each of the steps, stages, and case studies, there are some predetermined KPIs to be examined:
o	Techno-economic level:
	LCOM
	Annualized CAPEX & OPEX
	Carbon intensity
	Clipped Energy
o	Framework level:
	Simulation time
 
o	Operational dispatch optimization methodology comparison
	MILP vs RL
	Stage 1: Using the best linear layout from Joint operational dispatch and sizing methodology comparison result, we fixed the layout now for the operational dispatch optimization methodology comparison.  
•	Linear model reconstruction and validation in RL step-function based environment with imposed control
•	RL control attached to 5 key components based on the Imposed control findings. The linear model reconstruction will tell us which components need to be imposed in order to validate 1-to-1 system design between the MILP and RL framework
	Stage 2: Non-Linear Model with RL  
•	The imposed control from stage 1 will be operated under non-linear high fidelity system representation of the BPtMeOH
•	Train RL to run with the high fidelity non-linear system of the BPtMeOH
•	Compare the results between high-fidelity BPtMeOH system with imposed control and RL t
