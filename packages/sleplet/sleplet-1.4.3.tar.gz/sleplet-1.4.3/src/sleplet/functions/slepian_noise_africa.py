"""Contains the `SlepianNoiseAfrica` class."""
import numpy as np
import numpy.typing as npt
import pydantic.v1 as pydantic

import sleplet._string_methods
import sleplet._validation
import sleplet.functions.slepian_africa
import sleplet.noise
import sleplet.slepian.region
from sleplet.functions.fp import Fp


@pydantic.dataclasses.dataclass(config=sleplet._validation.Validation, kw_only=True)
class SlepianNoiseAfrica(Fp):
    """
    Creates a noised Slepian region on the topographic map of the Earth of
    the Africa region.
    """

    SNR: float = -10
    """A parameter which controls the level of signal-to-noise in the noised
    data."""

    def __post_init_post_parse__(self) -> None:
        super().__post_init_post_parse__()
        if (
            isinstance(self.region, sleplet.slepian.region.Region)
            and self.region.name_ending != "africa"
        ):
            raise RuntimeError("Slepian region selected must be 'africa'")

    def _create_coefficients(self) -> npt.NDArray[np.complex_ | np.float_]:
        sa = sleplet.functions.slepian_africa.SlepianAfrica(
            self.L,
            region=self.region,
            smoothing=self.smoothing,
        )
        noise = sleplet.noise._create_slepian_noise(
            self.L,
            sa.coefficients,
            self.slepian,
            self.SNR,
        )
        sleplet.noise.compute_snr(sa.coefficients, noise, "Slepian")
        return noise

    def _create_name(self) -> str:
        return (
            f"{sleplet._string_methods._convert_camel_case_to_snake_case(self.__class__.__name__)}"
            f"{sleplet._string_methods.filename_args(self.SNR, 'snr')}"
        )

    def _set_reality(self) -> bool:
        return False

    def _set_spin(self) -> int:
        return 0

    def _setup_args(self) -> None:
        if isinstance(self.extra_args, list):
            num_args = 1
            if len(self.extra_args) != num_args:
                raise ValueError(f"The number of extra arguments should be {num_args}")
            self.SNR = self.extra_args[0]
