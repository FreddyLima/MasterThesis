import multineat
import random

from ._genotype import Genotype


def mutate_v1(
    genotype: Genotype,
    multineat_params: multineat.Parameters,
    innov_db: multineat.InnovationDatabase,
    rng: multineat.RNG, joints_off,
) -> Genotype:
    """
    Mutate a CPPNWIN genotype.

    The genotype will not be changed; a mutated copy will be returned.

    :param genotype: The genotype to mutate. This object is not altered.
    :param multineat_params: Multineat parameters. See Multineat library.
    :param innov_db: Multineat innovation database. See Multineat library.
    :param rng: Random number generator.
    :returns: A mutated copy of the provided genotype.
    """
    new_genotype = genotype.genotype.MutateWithConstraints(
        False,
        multineat.SearchMode.BLENDED,
        innov_db,
        multineat_params,
        rng,
    )

    for ind in joints_off:
        idx = random.randint(0, len(ind) - 1)
        if ind[idx] == 0:
            ind[idx] = 1
        else:
            ind[idx] = 0

    return Genotype(new_genotype), joints_off

