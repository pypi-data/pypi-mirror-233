# mypy: disable-error-code="import"
"""Defines the API for Gaussian diffusion.

This is largely take from `here <https://github.com/tonyduan/diffusion>`_.

This module can be used to train a Gaussian diffusion model as follows.

.. code-block:: python

    # Instantiate the beta schedule and diffusion module.
    betas = get_diffusion_beta_schedule("linear", 1000)
    diff = GaussianDiffusion(betas)

    # Pseudo-training loop.
    for _ in range(1000):
        images = ds[index]  # Get some image from the dataset
        loss = diff.loss(images, model)
        loss.backward()
        optimizer.step()

    # Sample from the model.
    init_noise = torch.randn_like(images)
    generated = diff.sample(model, init_noise)
    show_image(generated[-1])

Choices for the beta schedule are:

- ``"linear"``: Linearly increasing beta.
- ``"quad"``: Quadratically increasing beta.
- ``"warmup"``: Linearly increasing beta with a warmup period.
- ``"const"``: Constant beta.
- ``"cosine"``: Cosine annealing schedule.
- ``"jsd"``: Jensen-Shannon divergence schedule.
"""

import math
from typing import Callable, Literal, cast, get_args

import torch
from torch import Tensor, nn

DiffusionPredMode = Literal["pred_x_0", "pred_eps", "pred_v"]
SigmaType = Literal["upper_bound", "lower_bound"]
DiffusionBetaSchedule = Literal["linear", "quad", "warmup", "const", "cosine", "jsd"]


def _warmup_beta_schedule(
    beta_start: float,
    beta_end: float,
    num_timesteps: int,
    warmup: float,
    dtype: torch.dtype = torch.float32,
) -> Tensor:
    betas = beta_end * torch.ones(num_timesteps, dtype=dtype)
    warmup_time = int(num_timesteps * warmup)
    betas[:warmup_time] = torch.linspace(beta_start, beta_end, warmup_time, dtype=dtype)
    return betas


def _cosine_beta_schedule(
    num_timesteps: int,
    offset: float = 0.008,
    dtype: torch.dtype = torch.float32,
) -> Tensor:
    rng = torch.arange(num_timesteps, dtype=dtype)
    f_t = torch.cos((rng / (num_timesteps - 1) + offset) / (1 + offset) * math.pi / 2) ** 2
    bar_alpha = f_t / f_t[0]
    beta = torch.zeros_like(bar_alpha)
    beta[1:] = (1 - (bar_alpha[1:] / bar_alpha[:-1])).clip(0, 0.999)
    return beta


def cast_beta_schedule(schedule: str) -> DiffusionBetaSchedule:
    assert schedule in get_args(DiffusionBetaSchedule), f"Unknown schedule type: {schedule}"
    return cast(DiffusionBetaSchedule, schedule)


def get_diffusion_beta_schedule(
    schedule: DiffusionBetaSchedule,
    num_timesteps: int,
    *,
    beta_start: float = 0.0001,
    beta_end: float = 0.02,
    warmup: float = 0.1,
    dtype: torch.dtype = torch.float32,
) -> Tensor:
    """Returns a beta schedule for the given schedule type.

    Args:
        schedule: The schedule type.
        num_timesteps: The total number of timesteps.
        beta_start: The initial beta value.
        beta_end: The final beta value.
        warmup: The fraction of timesteps to use for warmup.
        dtype: The dtype of the returned tensor.

    Returns:
        The beta schedule, a tensor with shape ``(num_timesteps)``.
    """
    match schedule:
        case "linear":
            return torch.linspace(beta_start, beta_end, num_timesteps, dtype=dtype)
        case "quad":
            return torch.linspace(beta_start**0.5, beta_end**0.5, num_timesteps, dtype=dtype) ** 2
        case "warmup":
            return _warmup_beta_schedule(beta_start, beta_end, num_timesteps, warmup, dtype=dtype)
        case "const":
            return torch.full((num_timesteps,), beta_end, dtype=dtype)
        case "cosine":
            return _cosine_beta_schedule(num_timesteps, dtype=dtype)
        case "jsd":
            return torch.linspace(num_timesteps, 1, num_timesteps, dtype=dtype) ** -1.0
        case _:
            raise NotImplementedError(f"Unknown schedule type: {schedule}")


class GaussianDiffusion(nn.Module):
    """Defines a module which provides utility functions for Gaussian diffusion.

    Parameters:
        betas: The beta values for each timestep, provided by the function
            :func:`get_diffusion_beta_schedule`.
    """

    __constants__ = ["num_timesteps", "pred_mode", "sigma_type"]

    def __init__(
        self,
        betas: Tensor,
        pred_mode: DiffusionPredMode = "pred_x_0",
        loss_type: Literal["mse", "l1"] = "mse",
        sigma_type: SigmaType = "upper_bound",
    ) -> None:
        super().__init__()

        assert betas.dim() == 1

        self.num_timesteps = betas.shape[0] - 1
        self.pred_mode = pred_mode
        self.sigma_type = sigma_type
        self.loss_fn = nn.MSELoss() if loss_type == "mse" else nn.L1Loss()

        bar_alpha = torch.cumprod(1.0 - betas, dim=0)
        self.register_buffer("bar_alpha", bar_alpha, persistent=False)

    bar_alpha: Tensor

    def loss(self, x: Tensor, func: Callable[[Tensor, Tensor], Tensor]) -> Tensor:
        """Computes the loss for a given sample.

        Args:
            x: The input data, with shape ``(*)``
            func: The model forward process, which takes a tensor with the same
                shape as the input data plus a timestep and returns the
                predicted noise or target, with shape ``(*)``.

        Returns:
            The loss, with shape ``(*)``.
        """
        bsz = x.shape[0]
        t_sample = torch.randint(1, self.num_timesteps + 1, size=(bsz,), device=x.device)
        eps = torch.randn_like(x)
        bar_alpha = self.bar_alpha[t_sample].view(-1, *[1] * (x.dim() - 1)).expand(x.shape)
        x_t = torch.sqrt(bar_alpha) * x + torch.sqrt(1 - bar_alpha) * eps
        pred_target = func(x_t, t_sample)
        match self.pred_mode:
            case "pred_x_0":
                gt_target = x
            case "pred_eps":
                gt_target = eps
            case "pred_v":
                gt_target = torch.sqrt(bar_alpha) * eps - torch.sqrt(1 - bar_alpha) * x
            case _:
                raise NotImplementedError(f"Unknown pred_mode: {self.pred_mode}")
        return self.loss_fn(pred_target, gt_target)

    @torch.no_grad()
    def sample(
        self,
        model: Callable[[Tensor, Tensor], Tensor],
        shape: tuple[int, ...],
        device: torch.device,
        sampling_timesteps: int | None = None,
    ) -> Tensor:
        sampling_timesteps = self.num_timesteps if sampling_timesteps is None else sampling_timesteps
        assert 1 <= sampling_timesteps <= self.num_timesteps

        x = torch.randn(shape, device=device)
        t_start = torch.empty((shape[0],), dtype=torch.int64, device=device)
        t_end = torch.empty((shape[0],), dtype=torch.int64, device=device)

        subseq = torch.linspace(self.num_timesteps, 0, sampling_timesteps + 1).round()
        samples = torch.zeros((sampling_timesteps + 1, *shape), device=device)
        samples[-1] = x

        for idx, (scalar_t_start, scalar_t_end) in enumerate(zip(subseq[:-1], subseq[1:])):
            t_start.fill_(scalar_t_start)
            t_end.fill_(scalar_t_end)
            noise = torch.randn_like(x) if scalar_t_end > 0 else torch.zeros_like(x)

            bar_alpha_start = self.bar_alpha[t_start].view(-1, *[1] * (noise.dim() - 1)).expand(noise.shape)
            bar_alpha_end = self.bar_alpha[t_end].view(-1, *[1] * (noise.dim() - 1)).expand(noise.shape)

            if self.pred_mode == "pred_x_0":
                pred_x_0 = model(x, t_start)
            elif self.pred_mode == "pred_eps":
                pred_eps = model(x, t_start)
                pred_x_0 = (x - torch.sqrt(1 - bar_alpha_start) * pred_eps) / torch.sqrt(bar_alpha_start)
            elif self.pred_mode == "pred_v":
                pred_v = model(x, t_start)
                pred_x_0 = torch.sqrt(bar_alpha_start) * x - torch.sqrt(1 - bar_alpha_start) * pred_v
            else:
                raise AssertionError(f"Invalid {self.pred_mode=}.")

            # Forward model posterior mean given x_0, x_t
            x = (
                torch.sqrt(bar_alpha_end) * (1 - bar_alpha_start / bar_alpha_end) * pred_x_0
                + (1 - bar_alpha_end) * torch.sqrt(bar_alpha_start / bar_alpha_end) * x
            ) / (1 - bar_alpha_start)

            # Forward model posterior noise
            if scalar_t_end == 0:
                pass
            elif self.sigma_type == "upper_bound":
                x += torch.sqrt(1 - bar_alpha_start / bar_alpha_end) * noise
            elif self.sigma_type == "lower_bound":
                x += (
                    torch.sqrt((1 - bar_alpha_start / bar_alpha_end) * (1 - bar_alpha_end) / (1 - bar_alpha_start))
                    * noise
                )
            else:
                raise AssertionError(f"Invalid {self.sigma_type=}.")

            samples[-1 - idx - 1] = x
        return samples


def plot_schedules(*, num_timesteps: int = 1000) -> None:
    """Plots all of the schedules together on one graph.

    Args:
        num_timesteps: The number of timesteps to plot
    """
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError("Please install matplotlib to use this script: `pip install matplotlib`") from e

    plt.figure(figsize=(8, 8))
    time = torch.arange(num_timesteps)
    for schedule in get_args(DiffusionBetaSchedule):
        plt.plot(time, get_diffusion_beta_schedule(schedule, num_timesteps=num_timesteps), label=schedule)
    plt.yscale("log")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # python -m ml.utils.diffusion
    plot_schedules()
