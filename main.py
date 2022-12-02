import math
import numpy
import random
import matplotlib.pyplot as plt
import pandas as pd

class QueueSystem:
    def __init__(self, totalIterations, mean_arrival_time, mean_ServiceTime):
        self.mean_interarrival = mean_arrival_time
        self.mean_service = mean_ServiceTime
        self.simulator_time = 0.0                #Simmulation Clock
        self.C_Cells = 16                        # Total Number of Cells
        self.num_event = self.C_Cells + 1
        self.num_calls = 0
        self.num_call_required = totalIterations
        self.next_event_type = 0
        self.server_status = numpy.zeros(self.C_Cells + 1)
        self.area_server_status = numpy.zeros(self.C_Cells)
        self.time_next_event = numpy.zeros(self.C_Cells + 1)
        self.time_next_event[0] = self.simulator_time + self.expon(self.mean_interarrival)  # determine next arrival
        for i in range(1, self.C_Cells + 1):
            self.time_next_event[i] = math.inf;
        self.server_idle = 0  # determine next departure.
        self.server_utilization = numpy.zeros(self.C_Cells)
        self.total_server_utilization = 0                #variable to Store Server Utilization
        self.Total_Loss = 0

    def main(self):
        while (self.num_calls < self.num_call_required):
            self.timing()
            self.update_time_avg_stats()
            if (self.next_event_type == 0):
                self.arrive()  ## next event is arrival
            else:
                self.j = self.next_event_type
                self.depart()  ## next event is departure
        self.report()


    def timing(self):
        self.min_time_next_event = math.inf
        ##Determine the event type of the next events to occur
        for i in range(0, self.num_event):
            if (self.time_next_event[i] <= self.min_time_next_event):
                self.min_time_next_event = self.time_next_event[i]
                self.next_event_type = i

        self.time_last_event = self.simulator_time
        ##advance the simulation clock
        self.simulator_time = self.time_next_event[self.next_event_type]

    ########################  Define UPDATE_TIME_AVG_STATS() function
    def update_time_avg_stats(self):
        self.time_past = self.simulator_time - self.time_last_event
        for i in range(1, self.C_Cells + 1):
            self.area_server_status[i - 1] += self.time_past * self.server_status[i]

    #########################   Define ARRIVAL() function
    def arrive(self):
        ix = 0
        self.server_idle = 0

        ##Schedule next arrival
        self.time_next_event[0] = self.simulator_time + self.expon(self.mean_interarrival)

        while (self.server_idle == 0 and ix <= self.C_Cells):
            if (self.server_status[ix] == 0):
                self.server_idle = ix
            ix += 1

        if (self.server_idle != 0):  ## Someone is IDLE
            self.server_status[self.server_idle] = 1
            self.time_next_event[self.server_idle] = self.simulator_time + self.expon(self.mean_service)

        else:  ## server is BUSY
            self.Total_Loss += 1
        self.num_calls += 1

        ###########################   Define DEPARTURE() function

    def depart(self):
        # if (self.num_in_q == 0): ## queue empty
        self.server_status[self.j] = 0
        self.time_next_event[self.j] = math.inf

    def expon(self, mean):
        return (-1 * mean * math.log(random.random()))
        #############################################################   Define REPORT() function

    def report(self):
        for i in range(0, self.C_Cells):
            self.server_utilization[i] = self.area_server_status[i] / self.simulator_time
            self.total_server_utilization += self.area_server_status[i]
        self.total_server_utilization = self.total_server_utilization / (self.simulator_time * self.C_Cells)
        print('-----Simulation Report-----')
        µ = 1 / self.mean_service
        λ = 1 / self.mean_interarrival
        print('λ = ', λ)
        print('µ = ', µ)
        print('total_server_utilization =', self.total_server_utilization)
        print('Loss Probability =', self.Total_Loss / self.num_call_required)
        print('')
        print('')
        print('-----Validation-----')
        Temp1 = 0
        Temp2 = 0
        # Loss Probability Calculation:
        for k in range(0, self.C_Cells + 1):
            Temp1 += ((λ / µ) ** k) / (math.factorial(k))
        self.Pc = (((λ / µ) ** self.C_Cells) / (math.factorial(self.C_Cells))) / Temp1
        self.SU = λ / (self.C_Cells * µ)
        print('Total Server Utilization =', self.SU * (1 - self.Pc))
        print('Loss Probability =', self.Pc)


myObject = QueueSystem(totalIterations=100000, mean_arrival_time=10, mean_ServiceTime=100)
myObject.main()
# 100 total_server_utilization = 0.062164797250383666 Loss Probability = 0.0
# 50 total_server_utilization = 0.12429448923403205 Loss Probability = 0.0
# 30 total_server_utilization = 0.2083747192442803 Loss Probability = 0.0
# 25 total_server_utilization = 0.25095895475555247 Loss Probability = 0.0
# 20 total_server_utilization = 0.3121959902531711 Loss Probability = 9e-05
# 15 total_server_utilization = 0.4184205145719484 Loss Probability = 0.00097
# 14 total_server_utilization = 0.44544368466785494 Loss Probability = 0.00151
# 12 total_server_utilization = 0.5209342792432314 Loss Probability = 0.00704
# 11 total_server_utilization = 0.5609819607776643 Loss Probability = 0.0118
# 10 total_server_utilization = 0.6106726701044084 Loss Probability = 0.02176
data = {'Total Server Utilization': [0.06, 0.12, 0.20, 0.25, 0.31, 0.41, 0.44, 0.52, 0.56, 0.61],
        'Blocking Probability': [0.0, 0.0, 0.0, 0.0, 9e-05, 0.00097, 0.00151, 0.00704, 0.0118, 0.02176],
        'Arrival Rate': [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
       }
df = pd.DataFrame(data)
plt.plot(df['Arrival Rate'], df['Blocking Probability'], color='red', marker='o')
plt.xlabel('Arrival Rate', fontsize=14)
plt.ylabel('Blocking Probability', fontsize=14)
plt.show()
plt.plot(df['Arrival Rate'], df['Total Server Utilization'], color='green', marker='o')
plt.xlabel('Arrival Rate', fontsize=14)
plt.ylabel('Total Server Utilization', fontsize=14)
plt.show()