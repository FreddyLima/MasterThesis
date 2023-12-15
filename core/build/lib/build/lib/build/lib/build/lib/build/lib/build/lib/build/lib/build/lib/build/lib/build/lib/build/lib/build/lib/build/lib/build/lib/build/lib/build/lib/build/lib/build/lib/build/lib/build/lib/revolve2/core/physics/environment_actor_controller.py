"""Contains EnvironmentActorController, an environment controller for an environment with a single actor that uses a provided ActorController."""

from revolve2.actor_controller import ActorController
from revolve2.core.physics.running import ActorControl, EnvironmentController
import matplotlib.pyplot as plt

class EnvironmentActorController(EnvironmentController):
    """An environment controller for an environment with a single actor that uses a provided ActorController."""

    actor_controller: ActorController
    graph = [[], [], [], [], [], [], [], []]

    def __init__(self, actor_controller: ActorController) -> None:
        """
        Initialize this object.

        :param actor_controller: The actor controller to use for the single actor in the environment.
        """
        self.actor_controller = actor_controller

    def control(self, dt: float, actor_control: ActorControl, loop, results, joints_off) -> None:
        """
        Control the single actor in the environment using an ActorController.

        :param dt: Time since last call to this function.
        :param actor_control: Object used to interface with the environment.
        """
        if loop == 'closed':
            self.actor_controller.set_sensors(results)

        self.actor_controller.step(dt)
        dof_targets = self.actor_controller.get_dof_targets()

        for i in range(len(joints_off)):
            dof_targets[i] *= joints_off[i]
            self.graph[i].append(dof_targets[i])

        actor_control.set_dof_targets(0, dof_targets)
        print("CLKNWEFNEFNEFNEFNELFNWELJFNEWLFNWELFNWEFNNWNFOENFINFO2NFLENFLKWENFLEWNFLKWNEKLFNWEKLFNNL")

        if len(self.graph[-1]) == 50:
            for i, inner_list in enumerate(self.graph):
                plt.plot(inner_list)
                plt.xlabel('X-axis')
                plt.ylabel('Y-axis')
                plt.title(f'Plot for Inner List {i + 1}')

                # Save the plot to a file (change the filename as needed)
                plt.savefig(f'plot_{i + 1}.png')

                # Clear the current plot to prepare for the next one
                plt.clf()


