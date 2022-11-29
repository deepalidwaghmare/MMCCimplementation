import math
import numpy
import random
import matplotlib.pyplot as plt
from matplotlib import figure
loop=int(0)

class QueueSystem:
    def __init__(self, totalProcess, mean_interArrival_Time, mean_ServiceTime):
        self.mean_interarrival = mean_interArrival_Time  # 1/λ
        self.mean_service = mean_ServiceTime  # 1/µ
        self.sim_time = 0.0
        self.C_servers = 16
        self.num_event = self.C_servers + 1
        self.num_customers = 0
        self.num_customers_required = totalProcess
        self.next_event_type = 0
        self.server_status = numpy.zeros(self.C_servers + 1)
        self.area_server_status = numpy.zeros(self.C_servers)
        self.time_next_event = numpy.zeros(self.C_servers + 1)
        self.time_next_event[0] = self.sim_time + self.expon(self.mean_interarrival)
        for i in range(1, self.C_servers + 1):
            self.time_next_event[i] = math.inf
        self.server_idle = 0
        self.server_utilization = numpy.zeros(self.C_servers)
        self.total_server_utilization = 0
        self.Total_Loss = 0

    def main(self):
        while self.num_customers < self.num_customers_required:
            self.timing()
            self.update_time_avg_stats()
            if self.next_event_type == 0:
                self.arrive()  ## next event is arrival
            else:
                self.j = self.next_event_type
                self.depart()
        self.report()

    def timing(self):
        self.min_time_next_event = math.inf

        for i in range(0, self.num_event):
            if (self.time_next_event[i] <= self.min_time_next_event):
                self.min_time_next_event = self.time_next_event[i]
                self.next_event_type = i

        self.time_last_event = self.sim_time

        self.sim_time = self.time_next_event[self.next_event_type]

    def update_time_avg_stats(self):
        self.time_past = self.sim_time - self.time_last_event
        for i in range(1, self.C_servers + 1):
            self.area_server_status[i - 1] += self.time_past * self.server_status[i]

    def arrive(self):
        ix = 0
        self.server_idle = 0

        self.time_next_event[0] = self.sim_time + self.expon(self.mean_interarrival)

        while (self.server_idle == 0 and ix <= self.C_servers):
            if (self.server_status[ix] == 0):
                self.server_idle = ix
            ix += 1

        if (self.server_idle != 0):  ## Someone is IDLE
            self.server_status[self.server_idle] = 1
            self.time_next_event[self.server_idle] = self.sim_time + self.expon(self.mean_service)

        else:  ## server is BUSY
            self.Total_Loss += 1
        self.num_customers += 1

        ###########################   Define DEPARTURE() function

    def depart(self):
        # if (self.num_in_q == 0): ## queue empty
        self.server_status[self.j] = 0
        self.time_next_event[self.j] = math.inf

    def expon(self, mean):
        return (-1 * mean * math.log(random.random()))
        #############################################################   Define REPORT() function

    def report(self):
        for i in range(0, self.C_servers): #0...16
            self.server_utilization[i] = self.area_server_status[i] / self.sim_time
            self.total_server_utilization += self.area_server_status[i]
        self.total_server_utilization = self.total_server_utilization / (self.sim_time * self.C_servers)
        print('***Simulation Report from this Simulation***')
        print('')
        µ = 1 / self.mean_service
        λ = 1 / self.mean_interarrival
        print('                        λ = ', λ)
        print('                        µ = ', µ)
        print('total_server_utilization =', self.total_server_utilization)
        print('        Loss Probability =', self.Total_Loss / self.num_customers_required)
        print('')
        print('')
        print('***Sumulation Report from Validation Formula***')
        Temp1 = 0
        Temp2 = 0
        # Loss Probability Calculation:
        for k in range(0, self.C_servers + 1):
            Temp1 += ((λ / µ) ** k) / (math.factorial(k))
        self.Pc = (((λ / µ) ** self.C_servers) / (math.factorial(self.C_servers))) / Temp1
        self.SU = λ / (self.C_servers * µ)
        print()
        print('    Total Server Utilization =', self.SU * (1 - self.Pc))
        print('            Loss Probability =', self.Pc)


myObject = QueueSystem(totalProcess=200000, mean_interArrival_Time=5 , mean_ServiceTime=100)  #mean_interarrival_time = 0.01..0.1
myObject.main()
