import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv

class DSPSandbox:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced DSP Analyzer")
        self.root.geometry("1300x900")
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.fs = 30000 
        self.duration = 10.0
        self.t = np.linspace(0, self.duration, int(self.fs * self.duration), endpoint=False)
        
        self.freq_var = tk.DoubleVar(value=1.0)
        self.cycles_var = tk.IntVar(value=1)
        self.phase_var = tk.DoubleVar(value=0.0)
        self.noise_var = tk.DoubleVar(value=0.0)
        self.waveform_var = tk.StringVar(value="Sine")
        self.window_var = tk.BooleanVar(value=False)
        self.log_scale_var = tk.BooleanVar(value=False)
        self.view_mode_var = tk.StringVar(value="Magnitude") 

        self.fig, (self.ax_time, self.ax_freq) = plt.subplots(2, 1, figsize=(10, 8))
        self.fig.subplots_adjust(hspace=0.4, left=0.1, right=0.95, top=0.92, bottom=0.1)

        self.setup_ui()
        self.update_plots()

    def setup_ui(self):
        control_frame = ttk.Frame(self.root, padding="15")
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(control_frame, text="Signal Generator", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        self.create_slider(control_frame, "Frequency (Hz)", self.freq_var, 1, 1000)
        self.create_slider(control_frame, "Cycles to Display", self.cycles_var, 1, 50, is_int=True)
        self.create_slider(control_frame, "Phase (Deg)", self.phase_var, 0, 360)
        self.create_slider(control_frame, "Noise Level", self.noise_var, 0, 1)

        ttk.Label(control_frame, text="Waveform Type").pack(anchor="w", pady=(10, 0))
        wave_cb = ttk.Combobox(control_frame, textvariable=self.waveform_var, values=["Sine", "Square", "Sawtooth"], state="readonly")
        wave_cb.pack(fill=tk.X, pady=5)
        wave_cb.bind("<<ComboboxSelected>>", self.update_plots)

        ttk.Separator(control_frame, orient='horizontal').pack(fill='x', pady=20)

        ttk.Label(control_frame, text="Analysis & Metrics", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        self.thd_label = ttk.Label(control_frame, text="THD: 0.00%", font=("Courier", 10, "bold"), foreground="#e67e22")
        self.thd_label.pack(anchor="w", pady=5)

        ttk.Checkbutton(control_frame, text="Apply Hann Window", variable=self.window_var, command=self.update_plots).pack(anchor="w", pady=2)
        ttk.Checkbutton(control_frame, text="Log Scale (dB)", variable=self.log_scale_var, command=self.update_plots).pack(anchor="w", pady=2)

        mode_cb = ttk.Combobox(control_frame, textvariable=self.view_mode_var, values=["Magnitude", "Phase"], state="readonly")
        mode_cb.pack(fill=tk.X, pady=10)
        mode_cb.bind("<<ComboboxSelected>>", self.update_plots)

        ttk.Button(control_frame, text="Export CSV", command=self.export_csv).pack(fill=tk.X, pady=20)

        plot_frame = ttk.Frame(self.root)
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def create_slider(self, parent, label, var, start, end, is_int=False):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)
        ttk.Label(frame, text=label).pack(anchor="w")
        fmt = "{:.0f}" if is_int else "{:.1f}"
        val_lbl = ttk.Label(frame, text=fmt.format(var.get()), font=("Arial", 9, "bold"))
        val_lbl.pack(anchor="e")
        s = ttk.Scale(parent, from_=start, to=end, variable=var, command=lambda v: [val_lbl.config(text=fmt.format(float(v))), self.update_plots()])
        s.pack(fill=tk.X)

    def generate_signal(self):
        f = self.freq_var.get()
        p = np.radians(self.phase_var.get())
        noise_amp = self.noise_var.get()
        waveform = self.waveform_var.get()

        if waveform == "Sine":
            sig = np.sin(2 * np.pi * f * self.t + p)
        elif waveform == "Square":
            sig = np.sign(np.sin(2 * np.pi * f * self.t + p))
        elif waveform == "Sawtooth":
            sig = 2 * (f * self.t + p/(2*np.pi) - np.floor(f * self.t + p/(2*np.pi) + 0.5))
        
        return sig + np.random.normal(0, noise_amp, size=len(self.t))

    def calculate_thd(self, mags, freqs):
        idx = np.argmax(mags[1:]) + 1
        fundamental_mag = mags[idx]
        if fundamental_mag < 0.01: return 0.0
        harmonics_mag_sq = np.sum(mags[idx+1:]**2)
        return (np.sqrt(harmonics_mag_sq) / fundamental_mag) * 100

    def compute_fft(self, signal):
        N = len(signal)
        if self.window_var.get():
            signal = signal * np.hanning(N)
            acf = 2.0 
        else:
            acf = 1.0
        fft_raw = np.fft.rfft(signal)
        freqs = np.fft.rfftfreq(N, d=1/self.fs)
        mag = np.abs(fft_raw) * (2.0 / N) * acf
        mag[0] = mag[0] / 2.0 
        phase = np.where(mag > 0.05, np.angle(fft_raw, deg=True), 0)
        return freqs, mag, phase

    def update_plots(self, event=None):
        signal = self.generate_signal()
        freqs, mags, phases = self.compute_fft(signal)
        target_f = self.freq_var.get()
        num_cycles = self.cycles_var.get()

        self.thd_label.config(text=f"THD: {self.calculate_thd(mags, freqs):.2f}%")

        self.ax_time.clear()
        self.ax_time.plot(self.t, signal, color='#2ecc71', linewidth=1)
        self.ax_time.set_title(f"Time Domain (Showing {num_cycles} Cycle(s))")
        
        display_limit = num_cycles / target_f
        self.ax_time.set_xlim(0, min(display_limit, self.duration))
        self.ax_time.grid(True, alpha=0.3)

        self.ax_freq.clear()
        if self.view_mode_var.get() == "Magnitude":
            y_data = 20 * np.log10(mags + 1e-12) if self.log_scale_var.get() else mags
            self.ax_freq.plot(freqs, y_data, color='#e74c3c', linewidth=1.5)
            peak_idx = np.argmax(mags[1:]) + 1
            peak_f, peak_m = freqs[peak_idx], y_data[peak_idx]
            self.ax_freq.plot(peak_f, peak_m, 'ro')
            self.ax_freq.annotate(f'{peak_f:.1f}Hz', (peak_f, peak_m), textcoords="offset points", xytext=(0,10), ha='center', color='red')
            self.ax_freq.set_ylim(-60, 10) if self.log_scale_var.get() else self.ax_freq.set_ylim(0, 1.2)
        else:
            self.ax_freq.scatter(freqs, phases, s=5, color='#3498db')
            self.ax_freq.set_ylim(-180, 180)

        self.ax_freq.set_xlim(0, max(10, target_f * 6))
        self.ax_freq.grid(True, alpha=0.3)
        self.canvas.draw()

    def export_csv(self):
        signal = self.generate_signal()
        freqs, mags, _ = self.compute_fft(signal)
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if path:
            with open(path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Freq_Hz", "Mag_Linear"])
                for i in range(len(freqs)):
                    if freqs[i] > 2000: break
                    writer.writerow([freqs[i], mags[i]])

    def on_close(self):
        plt.close(self.fig)
        self.root.destroy()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    DSPSandbox(root)
    root.mainloop()