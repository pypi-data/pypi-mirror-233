<img src="assets/images/logo_with_text.png" style="max-width: 600px">

Formulaic is a high-performance implementation of Wilkinson formulas for Python,
which are very useful for transforming dataframes into a form suitable for
ingestion into various modelling frameworks (especially linear regression).

- **Source Code**: [https://github.com/matthewwardrop/formulaic](https://github.com/matthewwardrop/formulaic)
- **Issue tracker**: [https://github.com/matthewwardrop/formulaic/issues](https://github.com/matthewwardrop/formulaic/issues)

!!! note
    This documentation is a work in process, and is far from complete. This
    documentation is currently a scaffold, and more documentation is being added
    over time. In the mean time, please feel free to reach out via the issue
    tracker if you have any questions.

!!! warning
    While this project is now fully functional, the API is still subject to
    change between major versions (`0.<major>.<minor>`) as we continue to
    improve things. If you are going to depend on it in another project, it is
    advisable to pin formulaic to within a major version, for example:
    `formulaic>=0.5.0,<0.6`.

It provides:

- high-performance dataframe to model-matrix conversions.
- support for reusing the encoding choices made during conversion of one data-set on other datasets.
- extensible formula parsing.
- extensible data input/output plugins, with implementations for:
  - input:
    - `pandas.DataFrame`
    - `pyarrow.Table`
  - output:
    - `pandas.DataFrame`
    - `numpy.ndarray`
    - `scipy.sparse.CSCMatrix`
- support for symbolic differentiation of formulas (and hence model matrices).

with more to come!
