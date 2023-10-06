import mpmath as mpm
import numpy as np
import numpy.typing as npt
import scipy.stats as stats
from scipy.special import gamma

mpm.mp.dps = 25


def get_ergodic_rate(k: float, m: float, theta: float, omega: float) -> float:
    r"""Computes the ergodic rate of the system.
        .. math::
            \mathcal{R(k,m,\theta,\Omega)}=\frac{1}{{\log (2) \Gamma (k+m) B(k,m)}}{G_{3,3}^{3,2}\left(\frac{\Omega }{\theta }|\begin{array}{c}0,1-m,1 \\0,0,k \\\end{array}\right)}

    Args:
        k: The shape parameter of the numerator Gamma distribution.
        m: The shape parameter of the denominator Gamma distribution.
        theta: The scale parameter of the numerator Gamma distribution.
        omega: The scale parameter of the denominator Gamma distribution.

    Returns:
        The rate of the system.
    """
    assert not isinstance(k, np.ndarray), "mpmath does not operate on numpy arrays"
    return (1 / (mpm.log(2) * mpm.beta(k, m) * mpm.gamma(k + m))) * mpm.meijerg(
        [[0, 1 - m], [1]], [[0, 0, k], []], mpm.mpf(omega) / mpm.mpf(theta)
    )


def get_outage_lt(
    k: float, m: float, theta: float, omega: float, lambda_th: float
) -> float:
    r"""Computes the probability of the received SNR being less than the threshold.
         .. math::
            Pr(\lambda_{r}\lt\lambda_{th})=\frac{1}{{k B(k,m)}}{\left(\frac{2^{\lambda_{th} /10} \Omega}{\theta }\right)^k{_2F_1\left(k,k+m;k+1;-\frac{2^{\lambda_{th} /10} \Omega }{\theta}\right)}}

    , where :math:`\lambda_{r}=10\ln(x)`, with :math:`x \sim \beta'(k, m, \theta / \Omega)`.

    Args:
        k: The shape parameter of the numerator Gamma distribution.
        m: The shape parameter of the denominator Gamma distribution.
        theta: The scale parameter of the numerator Gamma distribution.
        omega: The scale parameter of the denominator Gamma distribution.
        lambda_th: The threshold of the received SNR.

    Returns:
        The outage probability of the system.
    """
    assert not isinstance(k, np.ndarray), "mpmath does not operate on numpy arrays"
    return (
        (((2 ** (lambda_th / 10) * omega) / theta) ** k)
        * mpm.hyp2f1(k, m + k, k + 1, -((2 ** (lambda_th / 10) * omega) / theta))
        / (k * mpm.beta(k, m))
    )


def get_outage_clt(
    k_a: float,
    m_a: float,
    theta_a: float,
    omega_a: float,
    k_b: float,
    m_b: float,
    theta_b: float,
    omega_b: float,
    lambda_th_a: float,
    lambda_th_b: float,
):
    r"""Computes the probability of the received SNR being greater than one threshold, but less than another.
        .. math::
            Pr(\lambda_{a}\gt\lambda_{th_a}, \lambda_{b}\lt\lambda_{b})=\frac{1}{k_b \Gamma\left(m_a\right) B\left(k_b,m_b\right)}{\left(\frac{2^{\gamma /10} \Omega _b}{\theta_b}\right){}^{k_b} {_2F_1\left(k_b,k_b+m_b;k_b+1;-\frac{2^{\gamma /10} \Omega_b}{\theta _b}\right)}} \\
            {\left(\Gamma \left(m_a\right)-\Gamma\left(k_a+m_a\right) \left(\frac{2^{\lambda /10} \Omega_a}{\theta _a}\right){}^{k_a} {_2\tilde{F}_1\left(k_a,k_a+m_a;k_a+1;-\frac{2^{\lambda /10}\Omega _a}{\theta _a}\right)}\right)}

    Args:
        k_a: The shape parameter of the numerator Gamma distribution of the first threshold.
        m_a: The shape parameter of the denominator Gamma distribution of the first threshold.
        theta_a: The scale parameter of the numerator Gamma distribution of the first threshold.
        omega_a: The scale parameter of the denominator Gamma distribution of the first threshold.
        k_b: The shape parameter of the numerator Gamma distribution of the second threshold.
        m_b: The shape parameter of the denominator Gamma distribution of the second threshold.
        theta_b: The scale parameter of the numerator Gamma distribution of the second threshold.
        omega_b: The scale parameter of the denominator Gamma distribution of the second threshold.
        lambda_th_a: The first threshold of the received SNR.
        lambda_th_b: The second threshold of the received SNR.

    Returns:
        The outage probability between two thresholds.
    """
    return (
        (((2 ** (lambda_th_a / 10) * omega_b) / theta_b) ** k_b)
        * mpm.hyp2f1(
            k_b,
            m_b + k_b,
            k_b + 1,
            -((2 ** (lambda_th_a / 10) * omega_b) / theta_b),
        )
        / (k_b * mpm.beta(k_b, m_b))
    ) * (
        (
            gamma(m_a)
            - (
                gamma(m_a + k_a)
                * (((2 ** (lambda_th_b / 10) * omega_a) / theta_a) ** k_a)
                * (
                    (
                        mpm.hyp2f1(
                            k_a,
                            m_a + k_a,
                            k_a + 1,
                            -((2 ** (lambda_th_b / 10) * omega_a) / theta_a),
                        )
                    )
                    / (gamma(k_a + 1))
                )
            )
        )
        / (gamma(m_a))
    ) + (
        (((2 ** (lambda_th_b / 10) * omega_a) / theta_a) ** k_a)
        * mpm.hyp2f1(
            k_a,
            m_a + k_a,
            k_a + 1,
            -((2 ** (lambda_th_b / 10) * omega_a) / theta_a),
        )
        / (k_a * mpm.beta(k_a, m_a))
    )


__all__ = [
    "get_ergodic_rate",
    "get_outage_lt",
    "get_outage_clt",
]
