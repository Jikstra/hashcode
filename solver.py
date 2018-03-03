from pprint import pprint
import time

from parser import Parser, calcDistance, generatorPossibleStarts

class Solver(Parser):
    def __init__(self, f):
        super().__init__(f)
        print('Parsed')
        print(self.latest_finishs)
        #pprint(self.timeline_earliest_start)
        self.findAllPossibleNextPassengers()
        #pprint(self.passengers)
        #self.solve()
   
    def findAllPossibleNextPassengers(self):
        i = 0
        last_time = time.time()
        for passenger in self.passengers:
            pid = passenger['id']
            self.findPossibleNextPassengers(pid)
            if i % 100 == 0:
                now = time.time()
                print(i, now - last_time)
                last_time = now
            if i > 5000:
                break
            i += 1

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
        for step in self.latest_finishs:
            if step < passenger['earliest_finish']:
                continue
            for next_pid in self.timeline_latest_finish[step]:
                if next_pid == pid:
                        continue
                next_passenger = self.passengers[next_pid]
                distance_between = calcDistance(passenger['end_point'], next_passenger['start_point'])
                if next_passenger['latest_start'] - distance_between < passenger['earliest_finish']:
                    continue
                arrival_range = (
                    passenger['earliest_finish'] + distance_between,
                    passenger['latest_start'] + distance_between
                )
                passenger['possible_next_passengers'][next_pid] = arrival_range

    def solve(self):
        for carId in self.config['cars']:
            pass



if __name__ == '__main__':
    sovler = Solver('data/c_no_hurry.in')



