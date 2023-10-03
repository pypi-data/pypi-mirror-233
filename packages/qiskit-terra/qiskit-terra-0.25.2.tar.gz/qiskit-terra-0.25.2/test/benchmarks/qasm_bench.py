# This code is part of Qiskit.
#
# (C) Copyright IBM 2023
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# pylint: disable=no-member,invalid-name,missing-docstring,no-name-in-module
# pylint: disable=attribute-defined-outside-init,unsubscriptable-object

from qiskit.compiler import transpile
from qiskit import QuantumCircuit
from qiskit.providers.fake_provider import FakeTorontoV2


class QASMBenchTranspileBenchmarks:
    params = [0, 1]
    param_names = ["transpiler optimization level"]
    timeout = 600

    def setup(self, _):
        self.backend = FakeTorontoV2()
        self.circuit = QuantumCircuit.from_qasm_file(
            "/home/computertreker/git/qiskit/qiskit-terra/bwt_n21.qasm"
        )

    def time_bwt_n21(self, transpiler_level):
        if transpiler_level == 0:
            transpile(
                self.circuit,
                self.backend,
                layout_method="sabre",
                routing_method="sabre",
                seed_transpiler=123456789,
                optimization_level=transpiler_level,
            )

        else:
            transpile(
                self.circuit,
                self.backend,
                optimization_level=transpiler_level,
                seed_transpiler=123456789,
            )
