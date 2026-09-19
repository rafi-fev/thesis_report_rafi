# List of Abbreviations

*Generated from comprehensive scan of `Thesis Rafi Draft Complete.docx`*

---

## 1. Master Alphabetical List (Thesis Ready)

| Abbreviation | Full Name / Description |
| :--- | :--- |
| **A2C** | Advantage Actor-Critic |
| **A3C** | Asynchronous Advantage Actor-Critic |
| **AC** | Alternating Current |
| **AD** | Anaerobic Digestion / Anaerobic Digester |
| **AI** | Artificial Intelligence |
| **ASU** | Air Separation Unit |
| **ATR** | Autothermal Reformer / Autothermal Reforming |
| **AUX** | Auxiliary (Balance of Plant Components / Loads) |
| **AWE** | Alkaline Water Electrolysis / Alkaline Water Electrolyzer |
| **BESS** | Battery Energy Storage System |
| **BGSS** | Biogas Storage System |
| **BO** | Bayesian Optimization |
| **BOP** | Balance of Plant |
| **BPtMeOH** | Biomass Power-to-Methanol |
| **CAPEX** | Capital Expenditure |
| **CBC** | COIN-OR Branch and Cut (Solver) |
| **CCDC** | Chinese Control and Decision Conference |
| **CCS** | Carbon Capture and Storage |
| **CGH2** | Compressed Gas Hydrogen (Storage) |
| **CO** | Carbon Monoxide |
| **CO₂ / CO2** | Carbon Dioxide |
| **COIN-OR** | Computational Infrastructure for Operations Research |
| **CPLEX** | IBM ILOG CPLEX Optimization Studio |
| **DDPG** | Deep Deterministic Policy Gradient |
| **DENSYS** | Decentralized Smart Energy Systems (Erasmus Mundus) |
| **DEPS** | Direct Environment and Policy Search |
| **DHI** | Diffuse Horizontal Irradiance ($W/m^2$) |
| **DNI** | Direct Normal Irradiance ($W/m^2$) |
| **DP** | Dynamic Programming |
| **DQN** | Deep Q-Network |
| **DRL** | Deep Reinforcement Learning |
| **DRM** | Dry Reforming of Methane |
| **FEV** | FEV Europe GmbH |
| **GA** | Genetic Algorithm |
| **GHG** | Greenhouse Gas |
| **GmbH** | Gesellschaft mit beschränkter Haftung |
| **GP** | Gaussian Process |
| **GPSampler** | Gaussian Process Sampler (Optuna) |
| **Gurobi** | Gurobi Optimizer |
| **H₂ / H2** | Hydrogen Gas |
| **H2SS** | Hydrogen Storage System |
| **IB** | Investment Block (oemof-solph) |
| **IC** | Ideal Controller (LP-Derived Global Optimum Benchmark) |
| **IEEE** | Institute of Electrical and Electronics Engineers |
| **ISGT** | Innovative Smart Grid Technologies (IEEE Conference) |
| **KOH** | Potassium Hydroxide |
| **KPI / KPIs** | Key Performance Indicator(s) / Key Performance Indices |
| **L2** | Level 2 (Decoupled BO-LP Formulation / Linear Environment) |
| **L3** | Level 3 (High-Fidelity Model Formulation / Environment) |
| **LCA** | Life Cycle Assessment |
| **LCB** | Lower Confidence Bound |
| **LCOM** | Levelized Cost of Methanol (\$/ton) |
| **LP** | Linear Programming |
| **MARL** | Multi-Agent Reinforcement Learning |
| **MDP / MDPs** | Markov Decision Process(es) |
| **MDPI** | Multidisciplinary Digital Publishing Institute |
| **MeOH** | Methanol ($CH_3OH$) |
| **MILP** | Mixed-Integer Linear Programming |
| **MINLP** | Mixed-Integer Non-Linear Programming |
| **MlpPolicy** | Multi-Layer Perceptron Policy (Neural Network Architecture) |
| **MPCE** | Journal of Modern Power Systems and Clean Energy |
| **MW** | Megawatt ($10^6\text{ W}$) |
| **MWh** | Megawatt-Hour |
| **NP-hard** | Non-Deterministic Polynomial-Time Hard |
| **O₂ / O2** | Oxygen Gas |
| **oemof** | Open Energy Modelling Framework |
| **OPEX** | Operational Expenditure |
| **Optuna** | Open-Source Hyperparameter and Black-Box Optimization Framework |
| **PEM** | Proton Exchange Membrane |
| **PES** | Power & Energy Society (IEEE PES) |
| **PPO** | Proximal Policy Optimization |
| **PSO** | Particle Swarm Optimization |
| **PtX / P2X** | Power-to-X |
| **PV** | Solar Photovoltaic |
| **Pyomo** | Python Optimization Modeling Objects |
| **RBC** | Rule-Based Controller / Rule-Based Control |
| **RDF** | Refuse-Derived Fuel |
| **RL** | Reinforcement Learning |
| **RWGS** | Reverse Water-Gas Shift |
| **SAC** | Soft Actor-Critic |
| **SMR** | Steam Methane Reforming |
| **SOC / SoC** | State of Charge |
| **SOEC / SOECs** | Solid Oxide Electrolyzer Cell(s) / Solid Oxide Electrolysis |
| **TD3** | Twin Delayed Deep Deterministic Policy Gradient |
| **TES** | Thermal Energy Storage |
| **TPE / TPEsampler** | Tree-Structured Parzen Estimator (Optuna) |
| **TRL** | Technology Readiness Level |
| **WT** | Wind Turbine |

---

## 2. Chemical Compounds & Physical Units

### Chemical Species
| Formula / Symbol | Name | Role in Process |
| :--- | :--- | :--- |
| **CH₄** | Methane | Upgraded biogas component reformed in ATR |
| **CH₃OH / MeOH** | Methanol | Desired liquid energy carrier product |
| **CO** | Carbon Monoxide | Syngas component for catalytic methanol synthesis |
| **CO₂ / CO2** | Carbon Dioxide | Biogas byproduct converted via RWGS |
| **H₂ / H2** | Hydrogen Gas | Produced via AWE; adjusts stoichiometric syngas ratio |
| **KOH** | Potassium Hydroxide | Liquid alkaline electrolyte in AWE stack |
| **O₂ / O2** | Oxygen Gas | Byproduct of AWE; supplied to ATR for partial oxidation |

### Physical Units & Symbols
| Symbol | Unit | Dimension / Notes |
| :--- | :--- | :--- |
| **bar** | Bar | Pressure ($1\text{ bar} = 10^5\text{ Pa}$) |
| **kg** | Kilogram | Mass ($10^3\text{ g}$) |
| **kt** | Kilotonne | Mass ($10^3\text{ metric tons} = 10^6\text{ kg}$) |
| **kW** | Kilowatt | Electrical / Thermal Power ($10^3\text{ W}$) |
| **kWh** | Kilowatt-Hour | Energy ($3.6\times 10^6\text{ J}$) |
| **kWp** | Kilowatt-Peak | Nominal PV panel DC peak rating under STC |
| **m³** | Cubic Meter | Volumetric capacity (methanol / gas storage) |
| **MW** | Megawatt | Power capacity ($10^6\text{ W}$) |
| **MWh** | Megawatt-Hour | Energy ($10^6\text{ W}\cdot\text{h}$) |
| **ton / t** | Metric Ton | Mass ($1,000\text{ kg}$) |
| **$ / USD** | United States Dollar | Economic currency base for CAPEX, OPEX, LCOM |

---

## 3. Thematic Classification

### Energy Systems & Process Engineering
- **AD**: Anaerobic Digestion / Anaerobic Digester
- **ASU**: Air Separation Unit
- **ATR**: Autothermal Reformer / Autothermal Reforming
- **AUX**: Auxiliary (Balance of Plant Components / Loads)
- **AWE**: Alkaline Water Electrolysis / Alkaline Water Electrolyzer
- **BESS**: Battery Energy Storage System
- **BGSS**: Biogas Storage System
- **BOP**: Balance of Plant
- **BPtMeOH**: Biomass Power-to-Methanol
- **CCS**: Carbon Capture and Storage
- **CGH2**: Compressed Gas Hydrogen Storage
- **DRM**: Dry Reforming of Methane
- **H2SS**: Hydrogen Storage System
- **PEM**: Proton Exchange Membrane
- **PtX**: Power-to-X
- **PV**: Solar Photovoltaic
- **RDF**: Refuse-Derived Fuel
- **RWGS**: Reverse Water-Gas Shift
- **SMR**: Steam Methane Reforming
- **SOC**: State of Charge
- **SOEC**: Solid Oxide Electrolyzer Cell
- **TES**: Thermal Energy Storage
- **WT**: Wind Turbine

### Optimization, Control & Machine Learning
- **A2C**: Advantage Actor-Critic
- **A3C**: Asynchronous Advantage Actor-Critic
- **AI**: Artificial Intelligence
- **BO**: Bayesian Optimization
- **DDPG**: Deep Deterministic Policy Gradient
- **DEPS**: Direct Environment and Policy Search
- **DP**: Dynamic Programming
- **DQN**: Deep Q-Network
- **DRL**: Deep Reinforcement Learning
- **GA**: Genetic Algorithm
- **GP**: Gaussian Process
- **GPSampler**: Gaussian Process Sampler
- **IC**: Ideal Controller (LP-derived benchmark)
- **LCB**: Lower Confidence Bound
- **LP**: Linear Programming
- **MARL**: Multi-Agent Reinforcement Learning
- **MDP**: Markov Decision Process
- **MILP**: Mixed-Integer Linear Programming
- **MINLP**: Mixed-Integer Non-Linear Programming
- **MlpPolicy**: Multi-Layer Perceptron Policy
- **PPO**: Proximal Policy Optimization
- **PSO**: Particle Swarm Optimization
- **RBC**: Rule-Based Controller
- **RL**: Reinforcement Learning
- **SAC**: Soft Actor-Critic
- **TD3**: Twin Delayed Deep Deterministic Policy Gradient
- **TPE**: Tree-Structured Parzen Estimator

### Techno-Economics & Performance Metrics
- **CAPEX**: Capital Expenditure
- **DHI**: Diffuse Horizontal Irradiance
- **DNI**: Direct Normal Irradiance
- **GHG**: Greenhouse Gas
- **KPI**: Key Performance Indicator
- **L2**: Level 2 (Linear System / Decoupled Framework)
- **L3**: Level 3 (High-Fidelity Nonlinear Environment)
- **LCA**: Life Cycle Assessment
- **LCOM**: Levelized Cost of Methanol
- **OPEX**: Operational Expenditure
- **TRL**: Technology Readiness Level

### Computational Frameworks & Solvers
- **CBC**: COIN-OR Branch and Cut
- **COIN-OR**: Computational Infrastructure for Operations Research
- **CPLEX**: IBM ILOG CPLEX Optimization Studio
- **Gurobi**: Gurobi Optimizer
- **IB**: Investment Block (oemof-solph)
- **oemof**: Open Energy Modelling Framework
- **Optuna**: Hyperparameter Optimization Framework
- **Pyomo**: Python Optimization Modeling Objects

---

## 4. LaTeX Acronym Environment Snippet

For easy copy-pasting if compiling a LaTeX version of the report:

```latex
\usepackage{acronym}

\begin{acronym}[BPtMeOH]
    \acro{A2C}{Advantage Actor-Critic}
    \acro{A3C}{Asynchronous Advantage Actor-Critic}
    \acro{AC}{Alternating Current}
    \acro{AD}{Anaerobic Digestion}
    \acro{AI}{Artificial Intelligence}
    \acro{ASU}{Air Separation Unit}
    \acro{ATR}{Autothermal Reformer}
    \acro{AUX}{Auxiliary}
    \acro{AWE}{Alkaline Water Electrolysis}
    \acro{BESS}{Battery Energy Storage System}
    \acro{BGSS}{Biogas Storage System}
    \acro{BO}{Bayesian Optimization}
    \acro{BOP}{Balance of Plant}
    \acro{BPtMeOH}{Biomass Power-to-Methanol}
    \acro{CAPEX}{Capital Expenditure}
    \acro{CBC}{COIN-OR Branch and Cut}
    \acro{CCS}{Carbon Capture and Storage}
    \acro{CGH2}{Compressed Gas Hydrogen}
    \acro{DDPG}{Deep Deterministic Policy Gradient}
    \acro{DHI}{Diffuse Horizontal Irradiance}
    \acro{DNI}{Direct Normal Irradiance}
    \acro{DP}{Dynamic Programming}
    \acro{DQN}{Deep Q-Network}
    \acro{DRL}{Deep Reinforcement Learning}
    \acro{DRM}{Dry Reforming of Methane}
    \acro{FEV}{FEV Europe GmbH}
    \acro{GA}{Genetic Algorithm}
    \acro{GHG}{Greenhouse Gas}
    \acro{GP}{Gaussian Process}
    \acro{H2SS}{Hydrogen Storage System}
    \acro{IB}{Investment Block}
    \acro{IC}{Ideal Controller}
    \acro{KPI}{Key Performance Indicator}
    \acro{LCA}{Life Cycle Assessment}
    \acro{LCB}{Lower Confidence Bound}
    \acro{LCOM}{Levelized Cost of Methanol}
    \acro{LP}{Linear Programming}
    \acro{MARL}{Multi-Agent Reinforcement Learning}
    \acro{MDP}{Markov Decision Process}
    \acro{MeOH}{Methanol}
    \acro{MILP}{Mixed-Integer Linear Programming}
    \acro{MINLP}{Mixed-Integer Non-Linear Programming}
    \acro{oemof}{Open Energy Modelling Framework}
    \acro{OPEX}{Operational Expenditure}
    \acro{PEM}{Proton Exchange Membrane}
    \acro{PPO}{Proximal Policy Optimization}
    \acro{PSO}{Particle Swarm Optimization}
    \acro{PtX}{Power-to-X}
    \acro{PV}{Photovoltaic}
    \acro{Pyomo}{Python Optimization Modeling Objects}
    \acro{RBC}{Rule-Based Controller}
    \acro{RDF}{Refuse-Derived Fuel}
    \acro{RL}{Reinforcement Learning}
    \acro{RWGS}{Reverse Water-Gas Shift}
    \acro{SAC}{Soft Actor-Critic}
    \acro{SMR}{Steam Methane Reforming}
    \acro{SOC}{State of Charge}
    \acro{SOEC}{Solid Oxide Electrolyzer Cell}
    \acro{TD3}{Twin Delayed Deep Deterministic Policy Gradient}
    \acro{TES}{Thermal Energy Storage}
    \acro{TPE}{Tree-Structured Parzen Estimator}
    \acro{TRL}{Technology Readiness Level}
    \acro{WT}{Wind Turbine}
\end{acronym}
```
