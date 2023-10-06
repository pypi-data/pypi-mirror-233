import dataclasses
import logging

import numpy as np
import numpy.typing as npt
import pydantic.v1 as pydantic

import sleplet._integration_methods
import sleplet._validation
import sleplet.harmonic_methods
from sleplet.meshes.mesh_slepian import MeshSlepian

_logger = logging.getLogger(__name__)


@pydantic.dataclasses.dataclass(config=sleplet._validation.Validation)
class MeshSlepianDecomposition:
    mesh_slepian: MeshSlepian
    _: dataclasses.KW_ONLY
    mask: bool = False
    u_i: npt.NDArray[np.complex_ | np.float_] | None = None
    u: npt.NDArray[np.complex_ | np.float_] | None = None

    def __post_init_post_parse__(self) -> None:
        self._detect_method()

    def decompose(self, rank: int) -> float:
        """Decompose the signal into its Slepian coefficients via the given method."""
        self._validate_rank(rank)

        match self.method:
            case "harmonic_sum":
                return self._harmonic_sum(rank)
            case "integrate_mesh":
                return self._integrate_mesh(rank)
            case "integrate_region":
                return self._integrate_region(rank)
            case _:
                raise ValueError(f"'{self.method}' is not a valid method")

    def decompose_all(self, n_coefficients: int) -> npt.NDArray[np.float_]:
        """Decompose all ranks of the Slepian coefficients."""
        coefficients = np.zeros(n_coefficients)
        for rank in range(n_coefficients):
            coefficients[rank] = self.decompose(rank)
        return coefficients

    def _integrate_region(self, rank: int) -> float:
        r"""
        F_{p} =
        \frac{1}{\lambda_{p}}
        \int\limits_{R} \dd{x}
        f(x) \overline{S_{p}(x)}.
        """
        s_p = sleplet.harmonic_methods.mesh_inverse(
            self.mesh_slepian.mesh,
            self.mesh_slepian.slepian_functions[rank],
        )
        integration = sleplet._integration_methods.integrate_region_mesh(
            self.mesh_slepian.mesh.region,
            self.mesh_slepian.mesh.vertices,
            self.mesh_slepian.mesh.faces,
            self.u,
            s_p,
        )
        return integration / self.mesh_slepian.slepian_eigenvalues[rank]

    def _integrate_mesh(self, rank: int) -> float:
        r"""
        F_{p} =
        \int\limits_{x} \dd{x}
        f(x) \overline{S_{p}(x)}.
        """
        s_p = sleplet.harmonic_methods.mesh_inverse(
            self.mesh_slepian.mesh,
            self.mesh_slepian.slepian_functions[rank],
        )
        return sleplet._integration_methods.integrate_whole_mesh(
            self.mesh_slepian.mesh.vertices,
            self.mesh_slepian.mesh.faces,
            self.u,
            s_p,
        )

    def _harmonic_sum(self, rank: int) -> float:
        r"""
        F_{p} =
        \sum\limits_{i=0}^{K}
        f_{i} (S_{p})_{i}^{*}.
        """
        return (self.u_i * self.mesh_slepian.slepian_functions[rank]).sum()

    def _detect_method(self) -> None:
        """Detects what method is used to perform the decomposition."""
        if self.u_i is not None:
            _logger.info("harmonic sum method selected")
            self.method = "harmonic_sum"
        elif self.u is not None:
            if self.mask:
                _logger.info("integrating a region on the mesh method selected")
                self.method = "integrate_region"
            else:
                _logger.info("integrating the whole mesh method selected")
                self.method = "integrate_mesh"
        else:
            raise RuntimeError(
                "need to pass one off harmonic coefficients, real pixels "
                "or real pixels with a mask",
            )

    def _validate_rank(self, rank: int) -> None:
        """Checks the requested rank is valid."""
        if not isinstance(rank, int):
            raise TypeError("rank should be an integer")
        if rank < 0:
            raise ValueError("rank cannot be negative")
        if rank >= self.mesh_slepian.mesh.number_basis_functions:
            raise ValueError(
                "rank should be less than "
                f"{self.mesh_slepian.mesh.number_basis_functions}",
            )
