



from timer_tic_toc import TIMER_TIC_TOC as timer


timerForLooping = timer() # to compute elapsed time for a process.
timerForWholeProcess = timer() # to compute elapsed time for all state machine algorithm.

# define the necessary states for state-machine pacer
INIT    = 0
PROCESS = 1
UPDATE  = 2
WAIT    = 3
FINISH  = 4
END     = 5

#---------------------------------------------------------
# Alkim GOKCEN, University of Izmir Katip Celebi
# Control Systems Lab - PhD.
# alkim.gokcen@outlook.com
# --------------------------------------------------------
# This code is to provide a script-based 
# simulink-like simulation environment.
#---------------------------------------------------------
#                          EXPLANATION
# - A real-time pacer is implemented to force the 
#   simulation run in real-time.
# - Usage: Real Time Pacer computes the necessary length
#   of iteration for the given parameters by calculatin
#   the (SimulationTime / SamplingTime)
#   i.e. SimulationTime = 10 sec, SamplingTime = 0.01
# - "OVERRUN case":
#   If an iteration execution time (elapsedTime) exceeds
#   the samplingTime, iteration counter is increased by
#   a value of  ceil((executionTime / samplingTime)) which
#   defines that how many iteration it took the execute
#   the simulation. In such cases, program displays an
#   error message to user to increase the sampling time
#   i.e. Please increase your samplingTime 
#        Smaller sampling frequency
#---------------------------------------------------------

class REAL_TIME_PACER:
    
    # Variable          Definition                                          Defaults
    # ==============    ==================================================  ============================
    # SimulationTime => defines the simulation duration in seconds.         (Default = 1 seconds)
    # samplingTime   => defines the sampling period for solver in seconds.  (Default = 0.01 seconds)
    # sampleLength   => defines the necessary iteration number for sim.     (Default = 100 iteration)
    # ==================================================================================================
    def __init__(self, simulationTime = 1, samplingTime = 1e-2):
        
        self.SoftwareVersion = "1.0.0"
        
        if simulationTime <= 0:
            print("Simulation time must be positive!")
            return
        
        if samplingTime <= 0:
            print("Sampling period must be positive!")

        self.simulationTime = simulationTime
        self.samplingTime = samplingTime
        self.INITIALIZATION = INIT
        self.PROCESS = PROCESS
        self.UPDATE = UPDATE
        self.WAIT = WAIT
        self.FINISH = FINISH
        
        # Initialization phase starts
        STATE = INIT
    
    def someFunction(self): # temporary function to mimic the env. to simulate.
        timerForLooping.delay(0.1) # assume that the env. process takes 0.53 seconds.
    
    def Pacer(self, STATE):
        
        match STATE:
            
            case self.INITIALIZATION:
                # compute the necessary iterion number to complete the simulation
                self.sampleLength = self.simulationTime / self.samplingTime
                # initialize the timer vars
                self.processCounter = 0     # defines the iteration counter
                self.elapsedTime = 0        # defines the elapsed time during the process.
                self.waitTime = 0           # defines the remaining time to reach the sampling time.
                self.totalRunTime = 0       # defines the total executed time (wait time is not included)
                self.totalSimulatedTime = 0 # defines the total simulation time including NOPs.
                self.overrunCounter = 0     # defines the total iteration number where the overrun occurs.
                
                STATE = PROCESS # start the process.
                timerForWholeProcess.tic() # start the timer after initialization is performed.
                return STATE
            
            case self.PROCESS:
                self.processCounter += 1 # count up the value to get how many times process is executed.
                timerForLooping.tic() # timer is initialized to compute the elapsed time for each iteration.
                # Calls some function. @TODO: simulation environment runs in this function.
                # to do that, I must learn how to input a user-defined function for this calss.
                self.someFunction()
                
                self.elapsedTime = timerForLooping.toc() # find the elapsed time.
                print(self.elapsedTime)
                self.waitTime = self.samplingTime - self.elapsedTime # determines the wait time.(samplingTime - elapsedTime) 
                # => overrun cases not taken into account yet
                
                STATE = WAIT # after process is executed, program should wait 
                return STATE
            
            case self.UPDATE:
                # update the simulation related parameters
                self.totalRunTime = self.totalRunTime + self.elapsedTime # total run time is integrated.
                # Parameters are updated. Detect if the simulation is over
                
                # if simulation is over
                if self.processCounter >= self.sampleLength:
                    STATE = FINISH
                else:
                    # if simulation should continue
                    STATE = PROCESS
                return STATE
            
            case self.WAIT:
                # @TODO: do not forget to take precautions for OVERRUN cases. 
                # For that cases, update the necessary iteration number by an appropriate number
                # i.e. if the execution time is 0.245 seconds, and sampling time is 0.1 seconds,
                # program should wait 0.055 seconds for the next iteration, and elpasedIteration 
                # should be increased by 3 = ceil((executionTime / samplingTime)), 
                # and return a warning message
                
                timerForLooping.delay(self.waitTime) # wait for the t(n+1) - t(n) is elapsed.
                # wait process is done!, now it is time to update simulation parameters
                STATE = UPDATE
                return STATE
            
            case self.FINISH:
                self.totalSimulatedTime = timerForWholeProcess.toc()
                print("============================================================================")
                print(" => Simulation is over!")
                # @TODO: Output the simulation related parameters
                # @TODO: Close timers if necessary!
                # @TODO: return the output parameters
                print(" => Total simulated time: ", self.totalSimulatedTime, " seconds.")
                print(" => Total Run Time: ", self.totalRunTime, " seconds.")
                print(" => # of iteration that Overrun detected: ", self.overrunCounter, " iteration")
                print("============================================================================")
                STATE = END
                return STATE
            case _:
                pass
    
    def pacerDriver(self):
        # this function is employed to run pacer state machine.
        stateInLoop = INIT
        while True:
            
            stateInLoop = self.Pacer(stateInLoop) # loop the paceer with state
            
            if stateInLoop is END:
                break # leave the pacer.
            
            
SIMULATION_TIME = 60 #seconds
SAMPLING_PERIOD = 1 #seconds
rtp = REAL_TIME_PACER(SIMULATION_TIME, SAMPLING_PERIOD)
rtp.pacerDriver()