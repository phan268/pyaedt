# %%
"""
------------
PWM Spectrum
------------

This notebook illustrates the impact of switching rise and fall
time on the spectrum of a pulse-width modulated (PWM) signal.

"""
# %%
import numpy as np
import matplotlib.pyplot as plt

# %% [markdown]
# Define basic input parameters

# %%
freq = 150  # Electrical frequency (Hz)
pwm_freq = 3000  # PWM frequency (Hz)
t_pwm = 1.0 / pwm_freq  # PWM period
dt = 1E-8  # Smallest sampling time step
mod_index = 0.9  # Modulation index
n_cycles = 2  # Number of electrical cycles
t_tot = n_cycles / freq  # Total time

# %% [markdown]
# Update the time series so each PWM cycle is fully sampled.  This simplifies the creation of the PMW
# signal if the number of electrical cycles is not an integer multiple of the number of PWM cycles.
#
# The total number of time samples will be updated.

# %%
n_pwm_cycles = int(np.ceil(t_tot * pwm_freq))
n_samples = int(n_pwm_cycles * np.ceil(1 / (dt * pwm_freq)))
t_tot = n_samples * dt
t = np.linspace(0, t_tot, num=n_samples)
print(f"Number of total samples: {n_samples}")
print(f"Number of PWM cycles: {n_pwm_cycles}")
print(f"Total time has been updated to {t_tot * 1E3:.1f} ms")

# %%
# Time-axis samples
n_pwm_cycles = int(np.max(t) * pwm_freq)
print(f"Number of PWM cycles: {n_pwm_cycles}")
print(f"Total time has been updated to {t_tot * 1E3:.1f} ms")

# %% [markdown]
# ### PWM Signal
#
# Build the PWM signal from the sinusoidal signal, `f(_freq, _t)`.

# %%
f = lambda _freq, _t: 0.5 * (1 + np.sin(2 * np.pi * _freq * _t))  # Sinusoidal signal

pwm = np.zeros(t.shape)  # Initialize the pwm data.
t0 = 0.0  # t0 is the start time for the current PWM cycle.
for m in range(n_pwm_cycles):  # Build the transient PWM signal.
    t_index = (t >= t0) & (t < t0 + t_pwm)
    fraction_on = (1 - mod_index) / 2 + mod_index * np.average(f(freq, t[t_index]))
    pwm[(t >= t0) & (t < t0 + fraction_on * t_pwm)] = 1.0
    t0 += t_pwm  # Update the PWM cycle number.

# %% [markdown]
# ### Apply rise-time and FFT
#
# - ``lpf(_w, _f)`` applies a window function `_w` to the time-series data in `_f`
# - ``spectrum(_f)`` returns the FFT of the data series in `_f`
#

# %%
lpf = lambda _w, _f: np.convolve(_w / _w.sum(), _f, mode="valid")
spectrum = lambda _f: np.fft.fft(_f, norm="forward")

# %% [markdown]
# ## Visualize the PWM Signal
#
# - Apply the windowing function ``lpf()`` to realize the rise/fall time in ``trf``.
# - Plot the resulting signal and spectrum.

# %%
trf = np.array([50, 500, 5000]) * 1e-9  # Rise/Fall times of pulse.

fig = plt.figure(figsize=(5.6, 6.9))
# axs = fig.subplots(nrows=2, sharex=False)
axs = fig.subplot_mosaic([["all_time"], ["t_fine"], ["spectrum"]])

# Plot electrical sinusiod.
axs["all_time"].plot(t * 1E3, f(freq, t), color="grey", linestyle="--")

# Plot PWM for all rise/file time values.
for trise in trf:
    w = np.hanning(int(2 * trise / dt))  # Window LPF function.
    pwm_filt = lpf(w, pwm)  # PWM with finite rise and fall time.
    nplot = len(pwm_filt)  # update number of data points in time series.
    label = f"$t_r = {trise * 1E6:.1f} \mu s$"
    # Update time-axis for plotting
    dn = n_samples - nplot
    t_plot = np.linspace(dt * dn / 2, dt * (n_samples - dn / 2), nplot)
    axs["all_time"].plot(t_plot * 1E3, pwm_filt, linewidth=.5, label=label)
    t_select = (t_plot > 0.98 / pwm_freq) & (t_plot < 1.02 / pwm_freq)
    axs["t_fine"].plot((t_plot[t_select] - 0.99 / pwm_freq) * 1E6,
                       pwm_filt[t_select], linewidth=1, label=label)

    pwm_spectrum = spectrum(pwm_filt)  # Calculate spectrum
    fplot = np.linspace(0, (nplot - 1) / (nplot * dt), num=nplot)
    axs["spectrum"].loglog(fplot[1:int(nplot / 2)] * 1e-3,
                           np.abs(pwm_spectrum[1:int(nplot / 2)]),
                           label=label)
axs["all_time"].set_xlabel("Time (ms)")
axs["t_fine"].set_xlabel("Time ($\mu s$)")
axs["spectrum"].set_xlabel("Freq (kHz)")
axs["spectrum"].set_ylim(1E-6, 1)
axs["spectrum"].legend(loc="best")
axs["t_fine"].legend(loc="best")
plt.show()

# %%
