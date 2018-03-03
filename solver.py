from pprint import pprint

from parser import Parser, calcDistance, generatorPossibleStarts

class Solver(Parser):
    def __init__(self, f):
        super().__init__(f)
        self.findAllPossibleNextPassengers()
        #pprint(self.passengers)
        #self.solve()
   
    def findAllPossibleNextPassengers(self):
        for passenger in self.passengers:
            pid = passenger['id']
            self.findPossibleNextPassengers(pid)

    def findPossibleNextPassengers(self, pid):
        """
        Finds all possible passengers we could pick up after we delivered passenger with pid.
        Saves all possible next passengers into self.passengers[pid]['possible_next_passengers']
        where key is next possible passenger id and value is an array of possible start times.
        Those start times are the times where the car would need to start getting to the next passenger
        not when the car would arrive at the next passengers place.
        """
        passenger = self.passengers[pid]
        passenger['possible_next_passengers'] = {}
        for next_pids in self.timeline_latest_finish[passenger['earliest_finish']:]:
            for next_pid in next_pids:
                if next_pid == pid:
                    continue
                next_passenger = self.passengers[next_pid]
                distance_between = calcDistance(passenger['end_point'], next_passenger['start_point'])
                start_times = [i for i in range(passenger['earliest_finish'], next_passenger['latest_start'] - distance_between + 1)]
                if len(start_times) > 0:
                    passenger['possible_next_passengers'][next_pid] = start_times

    def solve(self):
        for carId in self.config['cars']:
            pass



if __name__ == '__main__':
    sovler = Solver('data/c_no_hurry.in')



