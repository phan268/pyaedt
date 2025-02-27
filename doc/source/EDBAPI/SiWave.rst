Siwave manager
==============
`Siwave <https://www.ansys.com/products/electronics/ansys-siwave>`_ is a specialized tool
for power integrity, signal integrity, and EMI analysis of IC packages and PCB. This tool
solves power delivery systems and high-speed channels in electronic devices. It can be
accessed from PyAEDT in Windows only. All setups can be implemented through EDB API.

.. image:: ../Resources/siwave.png
  :width: 800
  :alt: Siwave
  :target: https://www.ansys.com/products/electronics/ansys-siwave


.. currentmodule:: pyaedt

.. autosummary::
   :toctree: _autosummary

   siwave.Siwave


.. code:: python

    from pyaedt.siwave import Siwave
    # this call returns the Edb class initialized on 2023 R1
    siwave = Siwave(specified_version="2023.1")
    siwave.open_project("pyproject.siw")
    siwave.export_element_data("mydata.txt")
    siwave.close_project()
    ...