use pyo3::prelude::*;
use num_bigint::BigUint;

/// gives the Fibonacci number. 
#[pyfunction]
fn fib(x: BigUint) -> BigUint {
    let mut last1: BigUint = (1 as u32).into();
    if x == (1 as u32).into() {return  last1;}
    let mut last2: BigUint = (0 as u32).into();
    if x == (0 as u32).into() {return  last2;}
    let mut count: BigUint = (1 as u32).into();
    while x > count {
        let tmp: BigUint = &last1 + last2;
        last2 = last1;
        last1 = tmp;
        count += 1 as u32;
    }
    return last1;
}

/// A Python module implemented in Rust.
#[pymodule]
fn basic_rust_fib_py(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fib, m)?)?;
    Ok(())
}