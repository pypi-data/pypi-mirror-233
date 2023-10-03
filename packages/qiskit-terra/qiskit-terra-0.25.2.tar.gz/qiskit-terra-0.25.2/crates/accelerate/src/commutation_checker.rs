// This code is part of Qiskit.
//
// (C) Copyright IBM 2022
//
// This code is licensed under the Apache License, Version 2.0. You may
// obtain a copy of this license in the LICENSE.txt file in the root directory
// of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
//
// Any modifications or derivative works of this code must retain this
// copyright notice, and modified files need to carry a notice indicating
// that they have been altered from the originals.

use hashbrown::{HashMap, HashSet};
use pyo3::prelude::*;
use pyo3::Python;

use approx::AbsDiffEq;
use num_complex::Complex64;
use numpy::ndarray::linalg::kron;
use numpy::ndarray::{Array, Array2, ArrayView2};
use numpy::PyReadonlyArray2;

fn check_commute(
    op_1: ArrayView2<Complex64>,
    qargs_1: &[usize],
    op_2: ArrayView2<Complex64>,
    qargs_2: &[usize],
    num_qubits: usize,
) -> [Array2<Complex64>; 2] {
    let mut op_1: Array2<Complex64> = op_1.into_owned();
    let lenq1 = qargs_1.len();
    let lenq2 = qargs_2.len();
    if lenq1 != lenq2 {
        let extra_qarg2: u32 = (num_qubits - lenq1) as u32;
        if extra_qarg2 > 0 {
            let id_op: Array2<Complex64> = Array::eye(2_usize.pow(extra_qarg2));
            op_1 = kron(&id_op, &op_1);
        }
    }
    let op12 = op_1.dot(&op_2);
    let op21 = op_2.dot(&op_1);
    [op12, op21]
}

#[pyclass(module = "qiskit._accelerate.commutation_checker")]
struct CommutationCheckerRS {
    cache: HashMap<[String; 2], bool>,
}

impl Default for CommutationCheckerRS {
    fn default() -> Self {
        Self::new()
    }
}


#[pymethods]
impl CommutationCheckerRS {
    #[new]
    pub fn new() -> Self {
        CommutationCheckerRS {
            cache: HashMap::new(),
        }
    }

    pub fn commute(
        &mut self,
        op_1: PyReadonlyArray2<Complex64>,
        qargs_1: Vec<usize>,
        node_1_key: String,
        op_2: PyReadonlyArray2<Complex64>,
        qargs_2: Vec<usize>,
        node_2_key: String,
        num_qubits: usize,
    ) -> bool {
        let forward_key = [node_1_key.clone(), node_2_key.clone()];
        match self.cache.get(&forward_key) {
            Some(val) => *val,
            None => {
                let op_out = if qargs_1 == qargs_2 {
                    check_commute(
                        op_1.as_array(),
                        &qargs_1,
                        op_2.as_array(),
                        &qargs_2,
                        num_qubits,
                    )
                } else {
                    check_commute(
                        op_1.as_array(),
                        &qargs_1,
                        op_2.as_array(),
                        &qargs_2,
                        num_qubits,
                    )
                };
                let res = op_out[0].abs_diff_eq(&op_out[1], 1e-8);
                self.cache.insert(forward_key, res);
                self.cache.insert([node_2_key, node_1_key], res);
                res
            }
        }
    }
}

#[pymodule]
pub fn commutation_checker(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<CommutationCheckerRS>()?;
    Ok(())
}
