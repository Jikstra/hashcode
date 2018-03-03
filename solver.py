from pprint import pprint
import time
from bisect import bisect_left

from parser import Parser, calcDistance, generatorPossibleStarts

class Solver(Parser):
    def __init__(self, f):
        super().__init__(f)
        #print(self.timeline_latest_start)
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
        for next_pid in self.generatorPassengersStartingAfter(passenger['earliest_finish']):
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

    def generatorPassengersStartingAfter(self, after):
        start_pos = find_ge_pos(self.latest_starts, after)
        if start_pos == -1:
            return
        for step in self.latest_starts[start_pos:]:
            for pid in self.timeline_latest_start[step]:
                yield pid

def find_ge_pos(a, x):
    'Find leftmost item greater than or equal to x'
    i = bisect_left(a, x)
    return(-1 if i >= len(a) else i)


if __name__ == '__main__':
    solver = Solver('data/c_no_hurry.in')
    #solver = Solver('data/b_should_be_easy.in')
    #print(find_ge([1,2,3,4,6,7], 5))

