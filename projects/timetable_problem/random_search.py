from random import shuffle
import numpy as np
from collections import defaultdict


def read_tutorial_file(filename):
  participant_tutorials = []
  with open(filename) as infile:
    for line in infile.readlines():
      try:
        tutorials = map(int, line.split()[1:])
      except Exception:
        continue
      participant_tutorials.append(tutorials)
  return participant_tutorials

def tutorial_count(x):
  count = defaultdict(int)
  for participant in x:
    for tutorial in participant:
      count[tutorial] += 1
  return count

def filter_tutorials(x, n):
  
  count = tutorial_count(x)
  tutorial_index = list(count.keys())
  # tutorial_index = reversed(sorted(tutorial_index, key=lambda x: count[x]))
  # tutorial_index = list(tutorial_index)[:n]
  result = []
  for participant in x:
    tutorials = [tutorial for tutorial in participant if tutorial in tutorial_index]
    if len(tutorials) > 0:
      result.append(tutorials)
  assert len(set(tutorial_index)) == len(tutorial_index)
  return result, tutorial_index

def gen_random_schedule(indices, nslots, nsessions):
  shuffle(indices)
  indices = indices[:(nslots*nsessions)]
  indices = np.array(indices, np.int)
  indices = indices.reshape((nslots, nsessions))
  return indices 


class CostFunction(object):

  def __init__(self, participant_tutorials):
    self._participant_tutorials = participant_tutorials

  def __call__(self, schedule):
    session_slot_lookup = {}
    for j in range(schedule.shape[0]):
      for i in range(schedule.shape[1]):
        session_slot_lookup[schedule[j,i]] = j

    cost =  0
    for participant in self._participant_tutorials:
      slots = []
      for tutorial in participant:
        if tutorial in session_slot_lookup:
          slot = session_slot_lookup[tutorial]
          if slot is not None:
            slots.append(slot)
      cost += (len(set(slots)) - len(participant))**2
    return cost

def sort_schedule(schedule):
  schedule.sort(axis=1)
  v = [schedule[j,0] for j in range(schedule.shape[0])]
  index = sorted(range(len(v)), key=lambda x: v[x])
  result = schedule.copy()
  for j in range(schedule.shape[0]):
    for i in range(schedule.shape[1]):
      k = index[j]
      result[j,i] = schedule[k,i] 
  return result

if __name__ == '__main__':
  
  n_tutorials = 15
  n_sessions = 3
  n_slots = 5
  
  participant_tutorials = read_tutorial_file("data/timetable_selection.txt")
  participant_tutorials, tutorial_index = filter_tutorials(participant_tutorials, 15)
  n_participants = len(participant_tutorials)

  compute_cost = CostFunction(participant_tutorials)

  min_cost = None
  best_schedule = None
  try:
    for num_iter in range(1000000):
      schedule = gen_random_schedule(tutorial_index, n_slots, n_sessions)
      cost = compute_cost(schedule)
      if best_schedule is None or cost < min_cost:
        min_cost = cost
        best_schedule = schedule
      print i, min_cost
      if cost == 0:
        break
  except KeyboardInterrupt:
    print ""

  print "Num iterations: ", num_iter

  best_schedule = sort_schedule(best_schedule)
  print ""
  print "Best Schedule:"
  print best_schedule
  print "Cost: ", compute_cost(best_schedule)

  # print "People per tutorial:"
  # count = tutorial_count(participant_tutorials)
  # for key, value in count.iteritems():
  #   print key, value

  print ""
  print "Participant sessions"
  session_slot_lookup = {}
  for j in range(best_schedule.shape[0]):
    for i in range(best_schedule.shape[1]):
      session_slot_lookup[best_schedule[j,i]] = j

  for participant in participant_tutorials:
    slots = []
    for tutorial in participant:
      if tutorial in session_slot_lookup:
        slot = session_slot_lookup[tutorial]
        if slot is not None:
          slots.append(slot)
    print len(participant) - (len(set(slots))), participant

  

