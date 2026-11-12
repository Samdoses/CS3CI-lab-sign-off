import pandas as pd
from novel import tsp
from novel import cs3ci

tsp_instance, ulysses16_coords = tsp.load_tsp_data('cities15_13.csv')
TIME_LIMIT = 5

print('Running an EA for {} seconds'.format(
  TIME_LIMIT))

ea_route, ea_route_cost = cs3ci.ea.solve_tsp(
  tsp_instance,
  pop_size = 10,
  plot_fitness=True,
  time_limit = TIME_LIMIT
)

tsp.display_route(
  tsp_instance,ea_route, city_coords=ulysses16_coords,
  title="EA-generated route on the Ulysses16 TSP Instance.\n" +
    "Cost: {}".format(ea_route_cost)
)