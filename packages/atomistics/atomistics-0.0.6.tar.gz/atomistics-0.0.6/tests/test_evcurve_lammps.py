import os

from ase.build import bulk
import numpy as np
import unittest

from atomistics.workflows.evcurve.workflow import EnergyVolumeCurveWorkflow


try:
    from atomistics.calculators.lammps import (
        evaluate_with_lammps, get_potential_dataframe
    )

    skip_lammps_test = False
except ImportError:
    skip_lammps_test = True


@unittest.skipIf(
    skip_lammps_test, "LAMMPS is not installed, so the LAMMPS tests are skipped."
)
class TestEvCurve(unittest.TestCase):
    def test_calc_evcurve(self):
        potential = '1999--Mishin-Y--Al--LAMMPS--ipr1'
        resource_path = os.path.join(os.path.dirname(__file__), "static", "lammps")
        structure = bulk("Al", a=4.05, cubic=True)
        df_pot = get_potential_dataframe(
            structure=structure,
            resource_path=resource_path
        )
        df_pot_selected = df_pot[df_pot.Name == potential].iloc[0]
        calculator = EnergyVolumeCurveWorkflow(
            structure=structure,
            num_points=11,
            fit_type='polynomial',
            fit_order=3,
            vol_range=0.05,
            axes=['x', 'y', 'z'],
            strains=None,
        )
        structure_dict = calculator.generate_structures()
        result_dict = evaluate_with_lammps(
            task_dict=structure_dict,
            potential_dataframe=df_pot_selected,
        )
        fit_dict = calculator.analyse_structures(output_dict=result_dict)
        self.assertTrue(np.isclose(fit_dict['volume_eq'], 66.43019853103964))
        self.assertTrue(np.isclose(fit_dict['bulkmodul_eq'], 77.7250135953191))
        self.assertTrue(np.isclose(fit_dict['b_prime_eq'], 1.279502459079921))
