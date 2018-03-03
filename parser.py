import sys

class Parser:
    def __init__(self, f):
        self.config = None
        self.passengers = []
        self.timeline_latest_finish = []
        self.timeline_earliest_start = []
        self.timeline_latest_start = []
        self.timeline_finishs = []
        self.latest_starts = set()

        self.parse(f)
        print('Parsed')
        self.latest_starts = sorted(self.latest_starts)

    def parse(self, f):
        with open(f, 'r') as infile:
            self.config = parseConfigLine(next(infile))

            self.timeline_earliest_start = [[] for i in range(0, self.config['steps']+1)]
            self.timeline_latest_finish = [[] for i in range(0, self.config['steps']+1)]
            self.timeline_possible_start = [[] for i in range(0, self.config['steps']+1)]
            self.timeline_latest_start = [[] for i in range(0, self.config['steps']+1)]

            id = 0
            for l in infile:
                passenger = parsePassengerLine(l, id)
                if passenger['distance'] > (passenger['latest_finish'] - passenger['earliest_start']):
                    print('Skipping undeliverable passenger %s' %passenger)
                    continue
                self.latest_starts.add(passenger['latest_start'])
                self.timeline_latest_start[passenger['latest_start']].append(id)
                self.passengers.append(passenger)
                id += 1

    def timelineAdd(self, pid):
        passenger = self.passengers[pid]
        self.timeline_earliest_start[passenger['earliest_start']].append(pid)
        self.timeline_latest_finish[passenger['latest_finish']].append(pid)
        print(passenger['latest_start'])
        self.timeline_latest_start[passenger['latest_start']].append(pid)


    def __repr__(self):
        s = 'config: %s\npassengers: %s\ntimeline_latest_finish: %s\ntimeline_earliest_start: %s' % (
                str(self.config),
                str(self.passengers),
                str(self.timeline_latest_finish),
                str(self.timeline_earliest_start)
            )
        return s

def parseConfigLine(line):
    splitted_line = splitLineToInts(line)
    return {
        'grid_size': parseCoordinate(splitted_line[0], splitted_line[1]),
        'num_vehicles': splitted_line[2],
        'num_rides': splitted_line[3],
        'bonus': splitted_line[4],
        'steps': splitted_line[5]
    }


def parsePassengerLine(line, id):
    splitted_line = splitLineToInts(line)
    start_point = parseCoordinate(splitted_line[0], splitted_line[1])
    end_point = parseCoordinate(splitted_line[2], splitted_line[3])
    earliest_start = splitted_line[4]
    latest_finish = splitted_line[5]
    distance = calcDistance(start_point, end_point)
    earliest_finish = earliest_start + distance
    latest_start = latest_finish - distance

    return {
        'id': id,
        'start_point': start_point,
        'end_point': end_point,
        'earliest_start': earliest_start,
        'latest_start': latest_start,
        'earliest_finish': earliest_finish,
        'latest_finish': latest_finish,
        'distance': distance,
    }

def calcDistance(a, b):
    """
    Calculate a distance between two coordinates

    Tests:
        >>> calcDistance((1, 3), (4, 6))
        6
        >>> calcDistance((-1, -1), (-4, -6))
        8
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def parseCoordinate(x, y):
    return (x, y)

def splitLineToInts(l):
    return list(map(lambda s: int(s), l.strip().split(" ")))

def generatorPossibleStarts(passenger):
    for possible_start in range(passenger['earliest_start'], passenger['latest_start']):
        yield possible_start

if __name__ == '__main__':
    parser = Parser('example_in.txt')
    print(parser)
