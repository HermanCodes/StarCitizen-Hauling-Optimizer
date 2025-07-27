from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpInteger, LpStatus, value


class ContainerSolver:
    """Handles the optimization logic for container allocation"""
    
    def __init__(self):
        pass
    
    def solve(self, requirements, available, locations, materials, sizes):
        """
        Solve the container allocation problem
        
        Args:
            requirements: Dict of {location: {material: amount}}
            available: Dict of {material: {size: count}}
            locations: List of location names
            materials: List of material names
            sizes: List of container sizes
            
        Returns:
            Dict with 'success' flag and solution data
        """
        try:
            # Create the optimization problem
            prob = LpProblem("ContainerAllocation", LpMinimize)

            # Decision variables: x[location, material, size] = number of containers
            x = {
                (loc, mat, size): LpVariable(f"x_{loc}_{mat}_{size}", 0, None, LpInteger)
                for loc in locations
                for mat in materials
                for size in sizes
            }

            # Objective: minimize total containers used
            prob += lpSum(x.values())

            # Constraints: meet requirements at each location
            for loc in locations:
                for mat in materials:
                    prob += lpSum(x[(loc, mat, s)] * s for s in sizes) == requirements[loc][mat]

            # Constraints: don't exceed container availability
            for mat in materials:
                for size in sizes:
                    prob += lpSum(x[(loc, mat, size)] for loc in locations) <= available[mat][size]

            # Solve the problem
            result = prob.solve()

            if LpStatus[result] == "Optimal":
                return {
                    'success': True,
                    'variables': x,
                    'total_containers': sum(int(value(var)) for var in x.values())
                }
            else:
                return {
                    'success': False,
                    'status': LpStatus[result]
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }