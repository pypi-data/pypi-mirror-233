use pyo3::{pyfunction, pymodule, PyResult, Python, wrap_pyfunction};
use pyo3::types::PyModule;
use dc_converter_tof;

#[pyfunction]
fn convert_file(source_file: String, alpha: f64, beta: f64) {
    dc_converter_tof::convert_depth_infrared(source_file, false, alpha, beta);
}

#[pyfunction]
fn convert_depth_file(source_file: String, target_file: String) {
    dc_converter_tof::convert_depth_named(source_file, target_file);
}

#[pyfunction]
fn read_raw_file(source_file: String)-> (Vec<u16>, Vec<u16>, u8, u8, u32) {
    let tof_image = dc_converter_tof::read_image_to_buffer(source_file);

    (tof_image.depth_image, tof_image.infrared_image,
     tof_image.meta.t_int, tof_image.meta.t_ext, tof_image.meta.exposure_time)
}
#[pymodule]
fn dc_converter(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(convert_file, m)?)?;
    m.add_function(wrap_pyfunction!(read_raw_file, m)?)?;
    m.add_function(wrap_pyfunction!(convert_depth_file, m)?)?;

    Ok(())
}
