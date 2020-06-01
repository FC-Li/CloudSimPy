# CloudSimPy data center job scheduling simulation framework

* CloudSimPy * is based on the discrete event simulation framework [SimPy] (https://simpy.readthedocs.io/en/latest/contents.html), implemented using *Python* language;
The scientific computing, deep learning, and machine learning ecology of the *Python* language is more complete than other programming languages. *CloudSimPy* works well with deep learning frameworks with *Python* support (such as *TensorFlow*, *PyTorch*) The combination helps to study resource management methods based on machine learning or deep learning.

The data center job scheduling algorithm based on deep reinforcement learning in `CloudSimPy / playground / Non_DAG / algorithm / DeepJS / DRL.py` is implemented by *TensorFlow*, and it is inferred and trained in its *eager* mode.

## CloudSimPy
As a data center job scheduling simulation framework *CloudSimPy* contains two *Python* packages `core` and` playground`.
#### Core
`core` abstracts and models each entity (*entity*) in the data center job scheduling problem. The` core` package contains the following modules:

+ `TaskInstanceConfig`,` TaskConfig` and `JobConfig` in` config` give the configuration of task instances, tasks and jobs (resource requirements, duration, etc.)
+ `TaskInstance`,` Task` and `Job` in` job` are the modeling of task instances, tasks and jobs respectively
+ `machine` is to model the machine
+ `cluster` is a model for computing clusters, the class`Cluster` maintains a list of machines in the cluster
+ The interface of the scheduling algorithm is defined in `alogrithm`. The user-defined scheduling algorithm must implement this interface, which is the key to the realization of **strategic mode**
+ `scheduler` is the modeling of the scheduler. Through the design pattern of strategy mode, different` Scheduler` instances can be scheduled using different scheduling algorithms
+ `broker` implements the class` Broker`, `Broker` replaces users to submit jobs to the computing cluster
+ `Monitor` implements the class` Monitor`, which is used to monitor and record the state of the simulation during the simulation process
+ `simulation` is the modeling of a simulation. A simulation must construct a cluster` Cluster` instance; construct a series of job configuration `JobConfig` instances, and use these job configuration instances to construct a` Broker` instance;
Construct a scheduler `Scheduler` instance. In a simulation, you can choose whether to use a `Monitor` instance to monitor the simulation process
! [CloudSimPy] (images / cloudsimpy-arch.png)

#### Playground
The `playground` package is designed to be convenient for software package users to conduct experiments. It mainly includes the` DAG` package and the `Non_DAG` package (supports simulation experiments when considering dependencies between tasks and without considering dependencies between tasks), and auxiliary package.
Both `DAG` and` Non_DAG` pre-implement some heuristic job scheduling algorithms and job scheduling algorithms based on deep reinforcement learning.
For example, the data center job scheduling algorithm based on deep reinforcement learning implemented in `Non_DAG / algorithm / DeepJS`:
+ agent agent, which realizes *strategy gradient* in reinforcement learning
+ brain *TensorFlow* implemented neural network structure
+ DRL data center job scheduling algorithm based on deep reinforcement learning
+ reward_giver reinforcement learning reward function

The auxiliary package provides some auxiliary classes and functions:
+ The `Episode` class in` episode` is used for **episodic** simulation experiments
+ `multiprocessing_run` in` tools` is used for training in **multi-process mode**; `average_slowdown` and` average_completion` are used to extract calculation statistics from an object of class `Episode`

## High-performance simulation
In the data center, the task instance `TaskInstance` is the actual resource consumer and the executor of the actual business logic, so conceptually the` TaskInstance` in the `core` package` job module is designed as a * SimPy * Process (`Process`),
The class `Task` is designed as a collection of` TaskInstance`, and the class `Job` is designed as a collection of` Task`. The running status of `Job` and` Task` is implemented using the `property` feature under *Python*,
And use the information transmission mechanism shown in the following figure to realize the synthesis of `Task` and` Job` states.

! [msg_pass] (images / msg.png)

When we ask about the status of a `Job`, the` Job` instance will ask about the status of its `Task` instances, and the` Task` instance will ask about the status of their respective `TaskInstance` instances,
The `Task` instance synthesizes its own state according to the state of the respective` TaskInstance` instances, and then the `Job` instance synthesizes its own state according to the state of its` Task` instances, that is, the state information backpropagates and finally returns to the `Job` `Examples.
This design can not only ensure the accuracy and consistency of the status information of `Job` and` Task`, but more importantly, it does not actively maintain the status information of `Job` and` Task` at every simulation time step.
Instead, the acquisition of the status of `Job` and` Task` is postponed to the passive inquiry of the status of `Job` and` Task`, which allows us to turn off the monitoring function (that is, not to query the status of `Job` and` Task`) Let the simulation run quickly and efficiently.
Passive query replaces active maintenance, and **hotpath** is optimized during the simulation process, so that the operations performed on **hotpath** are as few and fast as possible.

In addition to `TaskInstance` being conceptually designed as a *SimPy* process,` Broker`, `Scheduler`, and` Monitor` are also designed as *SimPy* processes.
The `Broker` process continuously submits the jobs described in the job configuration list to the cluster` Cluster` instance according to the job submission time. Until all jobs are submitted, `Broker` stops submitting and destroying them.
The `Scheduler` is continuously scheduled according to the scheduling time step until the simulation` Simulation` is marked as ended (when `Broker` is destroyed (ie no new jobs will arrive) and all submitted jobs are executed,
`Simulation` is marked as end). `Monitor` continuously monitors and records the simulation status according to the monitoring time step until the simulation` Simulation` is marked as end.

In addition, the entities `Simulation`,` Cluster`, `Machine`,` Task`, and `Job` in the job scheduling problem of the data center are common class concepts, and serve only as managers of related information.

## Strategy Mode
The strategy pattern is a behavioral design pattern. A series of algorithms are defined in the strategy pattern, each algorithm is placed in a separate class, and objects of these classes are interchangeable.
In the strategy mode, we have a class that can perform specific operations in different ways, such as the scheduler `Scheduker` class here. It can perform scheduling with different scheduling algorithms (scheduling strategies), we can extract all these Into individual classes called strategies. The original class (called the context) holds a reference to the strategy and delegates the work to the strategy instead of directly performing the work on its own. The original class is not responsible for selecting the appropriate algorithm, instead, the user passes the required strategy to it. In fact, the original class knows very little about strategy, it calls all strategies through the same common interface.
In this way, the context becomes independent of the specific strategy, and we can add new algorithms or modify existing algorithms without changing the code of the original class or other strategies.

By using the strategy design pattern, the implementation of `Scheduler` and the implementation of the scheduling algorithm used by` Scheduler` are separated in *CloudSimPy*,
And put them in the `core` package and the` playground / DAG / algorithm` and `playground / Non_DAG / algorithm` packages respectively.

The strategy mode is also used in `layground / DAG / algorithm / DeepJS / reward_giver.py` to provide different reward calculation methods for job scheduling models based on deep reinforcement learning with different optimization goals:
+ MakespanRewardGiver gives rewards for optimizing completion time (Makespan)
+ AverageSlowDownRewardGiver gives the reward for optimizing the average SlowDown
+ AverageCompletionRewardGiver gives rewards for optimizing average completion time

## Papers using CloudSimPy
1. [DeepJS: Job Scheduling Based on Deep Reinforcement Learning in Cloud Data Center] (./ playground / paper / F0049-4.19.pdf)

## Run examples
#### Requirements
1. Python 3.6
2. SimPy 3.0.11
3. TensorFlow 1.12.0
4. Numpy 1.15.3
5. Pandas 0.23.4
#### Install and run
1. `git clone git@github.com: RobertLexis / CloudSimPy.git`
2. Add the path to directory cloudsimpy to system environment ** PYTHONPATH **
3. `cd cloudsimpy / playground / Non_DAG / launch_scripts`
4. `python main-makespan.py`