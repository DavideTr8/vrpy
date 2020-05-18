from networkx import from_numpy_matrix, relabel_nodes, DiGraph
from numpy import matrix
from data import DISTANCES, PICKUPS_DELIVERIES
import sys

sys.path.append("../../")
sys.path.append("../../../cspy")
from vrpy import VehicleRoutingProblem

# Transform distance matrix to DiGraph
A = matrix(DISTANCES, dtype=[("cost", int)])
G = from_numpy_matrix(A, create_using=DiGraph())

# Set demands and requests
for (u, v) in PICKUPS_DELIVERIES:
    G.nodes[u]["request"] = v
    G.nodes[u]["demand"] = PICKUPS_DELIVERIES[(u, v)]
    G.nodes[v]["demand"] = -PICKUPS_DELIVERIES[(u, v)]

# Relabel depot
G = relabel_nodes(G, {0: "Source", 17: "Sink"})

if __name__ == "__main__":

    prob = VehicleRoutingProblem(
        G, load_capacity=10, pickup_delivery=True, num_stops=6,
    )
    prob.solve(cspy=False)
    print(prob.best_value)
    print(prob.best_routes)
    print(prob.node_load)
