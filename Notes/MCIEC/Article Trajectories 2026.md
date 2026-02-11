Related papers:
- Does the Mass Public Transport System Cover the Social Transport Needs? Targeting SDG 11.2 in Guadalajara, Mexico : https://www.mdpi.com/2076-3417/11/16/7709

### **Introduction:**
**General Background Information**

Public transportation systems serve as the backbone of sustainable urban development, facilitating economic growth and social equity by providing essential mobility to the population. As cities expand, the challenge of maintaining an efficient, accessible, and sustainable transport network becomes increasingly complex. Global studies emphasize that effective public transport must not only reduce reliance on private vehicles to lower emissions but also ensure equitable access to opportunities for all socioeconomic groups [1]. However, in many developing metropolitan areas, these systems struggle to meet the dual goals of sustainability and efficiency. Reviews of sustainable transportation concepts highlight that despite the clear environmental and social benefits of public transit, the practical implementation often faces significant hurdles related to planning, funding, and adapting to rapid urban sprawl [1].

**Specific Background Information**

In the context of Mexico, and specifically the Guadalajara Metropolitan Area (GMA), these challenges are acute. The public transport system, including the main bus lines and the SITEUR (Sistema de Tren Eléctrico Urbano) network, plays a critical role in the daily lives of millions. However, recent analyses indicate that the current infrastructure is often insufficient to cover the "transport social needs" of the population effectively. For instance, studies targeting Sustainable Development Goal 11.2 in Guadalajara have found that approximately 50.3% of inhabitants reside in areas with very high social transport needs, yet the coverage remains uneven [2]. Furthermore, historical reviews of public transport in Guadalajara from 1960 to 2020 reveal that the system's efficiency has been hampered by issues related to ownership structure, fare policies, and a lack of focus on social justice in route planning [3]. The result is a system often characterized by slow transportation times, poor accessibility, and insufficient coverage, which directly diminishes the quality of life for a significant percentage of inhabitants [3].


**A Description of the Gap in Our Knowledge**

While existing literature has extensively documented the sustainability deficits [1] and social exclusion caused by the current transport layout in Guadalajara [2][3], there is a lack of research focusing on the dynamic, data-driven optimization of these specific routes. Most studies evaluate the _status quo_ or propose policy-level changes, but few utilize advanced computational methods to reimagine the physical routing of buses based on actual passenger flow. Specifically, the application of bio-inspired optimization algorithms—which mimic the efficiency found in biological systems—combined with graph theory to model the complex connectivity of Guadalajara's urban fabric remains an underexplored avenue. There is a need to understand how these advanced algorithms can be applied to existing infrastructure to mathematically optimize connectivity and reduce travel times.

**Study Objective**

Consequently, this study was designed to fill this gap by analyzing and proposing improvements to the routing of main bus lines in the Guadalajara Metropolitan Area. The primary objective is to utilize bio-inspired optimization algorithms and graph theory to simulate the passenger flow (affluence) through the city's transport network. By modeling the city as a graph where nodes represent stops and edges represent routes, this research aims to determine if the current network configuration is fit to cover the mobility demand and to demonstrate how rearranging routes can improve efficiency, accessibility, and ultimately, the quality of life for users.

Existing literature has extensively documented the sustainability deficits [1] and social exclusion caused by the current transport layout in Guadalajara [2][3], there is a lack of research focusing on the dynamic and data-driven optimization of these specific routes that this research aims to tackle. The primary objective is to utilize bio-inspired optimization algorithms and graph theory to simulate the passenger flow (affluence) through the city's transport network. By modeling the city as a graph where nodes represent stops and edges represent routes, this research aims to determine if the current network configuration is fit to cover the mobility demand and to demonstrate how rearranging routes can improve efficiency, accessibility, and ultimately, the quality of life for users.

---

#### **References**

[1] Miller, P., de Barros, A. G., Kattan, L., & Wirasinghe, S. C. (2016). Public transportation and sustainability: A review. _KSCE Journal of Civil Engineering_, 20(3), 1076–1083. [https://doi.org/10.1007/s12205-016-0705-0](https://doi.org/10.1007/s12205-016-0705-0)

[2] Obregón-Biosca, S. A. (2021). Does the Mass Public Transport System Cover the Social Transport Needs? Targeting SDG 11.2 in Guadalajara, Mexico. _Applied Sciences_, 11(16), 7709. [https://doi.org/10.3390/app11167709](https://doi.org/10.3390/app11167709)

[3] Villalvazo, P., & Corona, J. P. (2023). Movilidad urbana y justicia social: transporte público en la zona metropolitana de Guadalajara, México. _Journal of Transport and Management Studies_, 68. [https://doi.org/10.56294/tms202368](https://www.google.com/search?q=https://doi.org/10.56294/tms202368)

### Methodology
Describe the research methods you use, including tools, materials and techniques. If necessary, this section must be enough to allow others to repeat their process. This enhances the reliability and transparency of your study.

In order to assess alternative public bus routes that enhance time efficiency and accessibility a compound cost function that takes in account the public bus transportation operation's costs and the user's time traversing from several starting locations A to locations B within our weighted directed multi graph.

$$
J = (C_{operator} \cdot \beta) + (C_{operator} \cdot \alpha)
$$
Where the bus operations cost is calculated based on route duration and operational expenses such as maintenance, equipment lifespan, and wages.
$$
C_{operator} \approx \text{Route Duration} \times \text{Cost per minute}
$$
The time invested by passengers traveling is mesure by adding the total of time spend by passengers per segment travel in bus.
$$
C_{user} = \sum (\text{Passengers in segment} \times \text{Travel time})
$$
Other parameters such as $\alpha$ and $\beta$ define the algorithm's tendency:
$\beta$: Short routes, low operational cost, lower coverage.
$\alpha$: Long routes, high coverage, lower waiting time for the user.

This paper employs a Genetic Algorithm to optimize the routing of public transport. This method was selected for its robustness in handling multi-objective optimization problems where traditional deterministic methods fail to converge.

For the genetic algorithm application, each solution (individual) is represented as an array of lists composed by nodes, each node links to a connection within the weighted directed multi graph hence each node represents a junction within the city street layout. Since there are multiple adjacent nodes, the stops do not necessarily follow a strict geographic linear order, allowing flexibility during the exploration of the solution space.

## Gemini output
**1. Network Modeling and Representation** To model the complex street network of the Guadalajara Metropolitan Area, this study utilizes graph theory, specifically representing the city as a Weighted Directed Multigraph. The foundational graph was extracted from real-world OpenStreetMap (OSM) data. In this model, nodes represent street intersections or specific locations (such as transit stops), while directed edges represent the navigable street segments connecting them.

A critical component of this network is the assignment of weights to the edges, which symbolize the travel time (impedance) required to traverse a segment. Travel time is calculated as a function of the street segment length and an estimated traversal speed. To better reflect real-world urban dynamics, a dynamic traffic noise multiplier was introduced to the edge weights, simulating variable congestion patterns across the network.

Simultaneously, passenger affluence is modeled using a demand matrix. This matrix maps the origin-destination (O-D) flow of passengers across the network. To represent urban focal points—such as commercial centers, universities, and historical districts—specific high-traffic nodes were designated as "hotspots". The demand matrix artificially inflates the passenger volume traveling to and from these hotspots, providing a realistic baseline of public transport demand.

**2. Cost Function Formulation** In order to assess alternative public bus routes that enhance time efficiency and accessibility, a compound cost function was formulated. This function evaluates both the operational expenses of the transit provider and the travel time incurred by users traversing from various origins ($A$) to destinations ($B$) within the multigraph. The objective function $J$ is defined to be minimized:

$$J = (C_{operator} \cdot \beta) + (C_{user} \cdot \alpha)$$

The operator cost ($C_{operator}$) is determined by the total temporal duration of the proposed routes and an associated operational expense rate (e.g., maintenance, fuel, and wages). It is approximated as:

$$C_{operator} \approx \text{Route Duration} \times \text{Cost per minute}$$

Conversely, the user cost ($C_{user}$) quantifies the total time investment of the passengers. It is calculated by aggregating the travel time of all passengers across their respective route segments:

$$C_{user} = \sum (\text{Passengers in segment} \times \text{Travel time})$$

The parameters $\alpha$ and $\beta$ serve as scaling factors to steer the algorithm's optimization tendency:

- Prioritizing $\beta$: Favors shorter routes with lower operational costs, potentially at the expense of network coverage.
    
- Prioritizing $\alpha$: Favors longer, more comprehensive routes that provide high coverage and reduce user travel time.
    

The computational evaluation of this fitness function requires calculating the shortest paths for all passengers using the proposed transit network. Below is the pseudo-code illustrating the evaluation process:

Plaintext

```
Algorithm 1: Compound Cost Function Evaluation
Input: Candidate routes (R), City Graph (G), Passenger Demand Matrix (D), Hotspots (H)
Output: Total Cost (J)

1: Initialize OperatorCost = 0
2: Initialize UserCost = 0
3: Initialize TransitGraph = Copy(G)

// Step 1: Calculate Operator Cost & Update Transit Graph
4: FOR EACH route in R:
5:     FOR EACH segment (u, v) in route:
6:         TravelTime = GetEdgeWeight(G, u, v)
7:         OperatorCost += (TravelTime * BusSpeedMultiplier) * CostPerMinute
8:         UpdateEdgeWeight(TransitGraph, u, v, TravelTime * BusSpeedMultiplier)
9:     END FOR
10: END FOR

// Step 2: Calculate User Cost via Shortest Paths
11: FOR EACH source in H:
12:     IF source has departing passengers in D:
13:         ShortestPaths = Dijkstra(TransitGraph, source)
14:         FOR EACH destination, passenger_count in D[source]:
15:             IF destination is reachable in ShortestPaths:
16:                 UserCost += passenger_count * ShortestPaths[destination]
17:             ELSE:
18:                 UserCost += passenger_count * UnservedPenalty
19:             END IF
20:         END FOR
21:     END IF
22: END FOR

// Step 3: Apply Tendency Parameters
23: J = (OperatorCost * β) + (UserCost * α)
24: RETURN J
```

**3. Bio-Inspired Optimization via Genetic Algorithm** Due to the NP-Hard nature of the transit routing problem and the non-differentiable characteristics of the proposed cost function over a massive urban graph, traditional deterministic optimization methods are computationally prohibitive. Therefore, this study employs a Genetic Algorithm (GA) to navigate the vast solution space. GAs have been extensively validated in literature as highly robust mechanisms for solving multi-objective transport routing problems where local optima trap standard algorithms.

+2

The GA implementation relies on a specific chromosomal representation. Each candidate solution (individual) is represented as an array of lists, where each list defines a specific bus route. The elements within these lists are integer node IDs corresponding to junctions in the city graph. Because nodes represent intersections with multiple adjacent connections, the algorithm permits flexibility in route generation; routes are constructed via random walks through the graph's topology rather than strict linear geographic constraints.

The evolutionary process is driven by the following operators:

- **Initialization:** The initial population is generated by creating random viable paths (random walks) originating from arbitrary nodes.
    
- **Fitness Evaluation:** The compound cost function ($J$) is applied. Because the GA is designed to maximize fitness, the cost is inverted (e.g., $Fitness = 1 / J$).
    
- **Selection:** A tournament selection method is utilized to choose parent chromosomes, favoring individuals with lower overall network costs.
    
- **Crossover:** A single-point crossover mechanism swaps entire routes between two parent solutions to generate offspring.
    
- **Mutation:** To maintain genetic diversity and prevent premature convergence, offspring undergo mutation with a specified probability. Mutation operators include extending a route to an adjacent node, trimming the final stop, or entirely regenerating a route within the chromosome.
    

The algorithm iteratively evolves the population, continuously plotting the most fit routes against the spatial data of Guadalajara until a maximum generation threshold is reached, yielding the optimized transit network configuration.

---

### **References**

[1] User Context (2026). Provided Python Codebase for Genetic Algorithm and Graph Simulation (`main.py`, `map_gdl.py`, `optimized_route_evaluator.py`, `city_environment.py`, `genetic_algoritm.py`).

[2] User Context (2026). Provided LaTeX Document (`p_2.tex`).

[3] Farahani, R. Z., Miandoabchi, E., Szeto, W. Y., & Rashidi, H. (2013). A review of urban transportation network design problems. _European Journal of Operational Research_, 229(2), 281-302. [https://doi.org/10.1016/j.ejor.2013.01.001](https://doi.org/10.1016/j.ejor.2013.01.001)

[4] Kepaptsoglou, K., & Karlaftis, M. G. (2009). The transit route network design problem: review, methodology and applications. _Public Transport_, 1(4), 291-325. [https://doi.org/10.1007/s12469-009-0014-9](https://doi.org/10.1007/s12469-009-0014-9)

#### Related Papers
