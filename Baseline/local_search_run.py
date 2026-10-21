import pandas as pd
from lib import tsp
from lib import local_search
import copy

# A local search algorithm is composed of:
#  - An initialisation method
#  - A neighbourhood function
#  - A step function
#  - A termination condition
# We also need an evaluation function to guide the search's progress.
#
# Step functions and termination conditions are often not specific to the
# problem being solved. We will use general-purpose functions from
# tsp.step_function and tsp.termination respectively. We therefore need to
# define a problem specific:
#   - initialisation method
#   - neighbourhood function
#   - evaluation function

# Our initialisation method is just to generate a random route
ulysses16_coords = pd.read_csv('ulysses16.csv',header=0).values
ulysses16_tsp_instance = tsp.construct_from_city_coords(ulysses16_coords)
def initializer():
  return tsp.random_route(ulysses16_tsp_instance)

# As per the lab worksheet, our neighbourhood function is based on swapping
# all pairs of cities from its starting solution.
def neighbourhood(soln):
  neighbours = []
  for i in range(1,len(soln)-2):
    for j in range(i+1,len(soln)-1):
      neighbour = copy.deepcopy(soln) # Warning about shallow copies
      neighbour[i], neighbour[j] = neighbour[j], neighbour[i]
      neighbours.append(neighbour)
  return neighbours

# Our evaluation function simply returns the length of a TSP tour on the
# problem at hand.
def evaluate(route):
  return tsp.evaluate(ulysses16_tsp_instance, route)

# We were asked to use a time-based termination condition. As mentioned above,
# This is implemented in tsp.termination. Let's define the time limit (in
# seconds) that we will give our algorithm.
LOCAL_SEARCH_TIME_LIMIT = 3

# With those methods defined, we can run random search (without restart). Note
# that we are passing in the problem-specific functions defined above
# (initializer, evaluate, neighbourhood) and the general purpose methods
# (local_search.termination.Time_Expired,
# local_search.step_function.best_improver).
print('#'*80)
print('Running local search without restart for {} seconds'.format(
  LOCAL_SEARCH_TIME_LIMIT))
print('#'*80 + "\n")
# Now run local search...
local_search_route, local_search_route_cost = local_search.run(
  initializer,
  evaluate,
  local_search.termination.Time_Expired(LOCAL_SEARCH_TIME_LIMIT),
  neighbourhood,
  local_search.step_function.best_improver,
  print_improvements = True
)
#...and display the result.
tsp.display_route(
  ulysses16_tsp_instance,local_search_route,
  city_coords=ulysses16_coords,
  title="Local-search-generated route on the Ulysses16 TSP Instance.\n" +
    "Cost: {}".format(local_search_route_cost)
)

# We were also asked to implement local search with restart. This works in the
# same way as the above, except that we need also to pass in a method to create
# the restart condition. Here we pass in
# local_search.termination.No_Improvement, which creates a restart condition
# that is triggered when local search fails to make an improvement from one
# iteration to the next.
print('#'*80)
print('Running local search with restart for {} seconds'.format(
  LOCAL_SEARCH_TIME_LIMIT))
print('#'*80 + "\n")
local_search_route, local_search_route_cost = local_search.run_with_restart(
  initializer,
  evaluate,
  local_search.termination.No_Improvement,
  local_search.termination.Time_Expired(LOCAL_SEARCH_TIME_LIMIT),
  neighbourhood,
  local_search.step_function.best_improver,
  print_improvements = True
)
tsp.display_route(
  ulysses16_tsp_instance,local_search_route,
  city_coords=ulysses16_coords,
  title="Local-search-generated route on the Ulysses16 TSP Instance.\n" +
    "Cost: {}".format(local_search_route_cost)
)