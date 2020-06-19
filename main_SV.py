# 0_Executing Program ============================================================================
import sys
import getopt
import re

args = sys.argv[1:]
opts, args = getopt.getopt(args, "i:b:h")

i_opt = './sample/sample_1.wav'
b_opt = "black"

for opt, arg in opts:
    if opt == "-i":
        i_opt = arg
        x = re.findall("\d", i_opt)
        o_opt = "output_" + x[0] + ".png"

    elif opt == "-b":
        if arg == "0":
            b_opt = "black"
        elif arg == "1":
            b_opt = "white"
        else:
            raise ValueError("")

    elif opt == "-h":
        print("-i : Input audio file path. Default path is './sample/sample_1.wav'")
        print("-b : Background color. 0 is black, 1 is white. Default value is 0(black)")


# 1_Importing Modules and Packages ================================================================

import librosa
import librosa.display
import numpy as np

from bokeh.plotting import figure
from bokeh.io import export_png

from bokeh.palettes import Blues8
from bokeh.palettes import Greens8
from bokeh.palettes import Inferno256


# 2_Loading Audio Files ===========================================================================

audio_data = i_opt
sig, sr = librosa.load(audio_data, sr = 44100)


# 3_Extacting Datas From Audio ====================================================================

# 3-1.Onset Envelope | 3-2.Beats | 3-3.Onsets -----------------------------------------------------
onset_frames = librosa.onset.onset_detect(sig, sr = sr)
onsets = librosa.frames_to_time(onset_frames, sr = sr)
onset_env = librosa.onset.onset_strength(sig, sr = sr, aggregate = np.median)
tempo = librosa.beat.tempo(onset_envelope = onset_env, sr = sr)
tempo, beats = librosa.beat.beat_track(onset_envelope = onset_env, sr = sr, units = 'time')

# 3-4.Frequency & Magnitude -----------------------------------------------------------------------
fft = np.fft.fft(sig)
magnitude = np.abs(fft)
magnitude_dB = librosa.amplitude_to_db(magnitude)
frequency = np.linspace(0, sr, len(magnitude_dB))

left_magnitude_dB = magnitude_dB[:len(magnitude_dB)/2]   # certain magnitude(dB)
left_frequency = frequency[:len(magnitude_dB)/2]         # certain frequency


# 4_Preprocessing Datas for Visualization =========================================================

# 4-1.Onset Envelope(propotional to audio length) -------------------------------------------------
E = len(onset_env)
x1 = np.random.rand(E) * E
y1 = np.random.rand(E) * E
n1 = 50
radii_1 = np.random.rand(E) * E / n1
colors_1 = ["#%02x%02x%02x" % (int(r), int(g), 180) for r, g in zip(x1, y1)]   # 255,100,37

# 4-2.Beats ---------------------------------------------------------------------------------------
B = len(beats)
x2 = [x1[i] for i in range(B)]
y2 = [y1[i] for i in range(B)]
n2 = 13
radii_2 = np.random.rand(B) * E / n2
colors_2 = Blues8[2]

# 4-3.Onsets --------------------------------------------------------------------------------------
O = len(onsets)
x3 = [x1[-(i+1)] for i in range(O)]
y3 = [y1[-(i+1)] for i in range(O)]
n3 = 8
size_3 = np.random.rand(O) * E / n3
colors_3 = Greens8[2]

# 4-4.Frequency & Magnitude -----------------------------------------------------------------------
left_magnitude_dB_max = max(left_magnitude_dB)
left_frequency_max = max(left_frequency)
x_ratio = left_magnitude_dB_max / (0.5 * E)    # for modifying max value = E
y_ratio = left_frequency_max / (0.5 * E)       # for modifying max value = E

F = len(left_frequency)
x_4 = left_magnitude_dB / x_ratio              # certain magnitude(dB)
y_4 = left_frequency / y_ratio                 # certain frequency
n4 = 100
colors_4 = Inferno256[-10]

x4_1 = [x_4[n4 * i] + 0.5 * E for i in range(F / n4)]
y4_1 = [y_4[n4 * i] for i in range(F / n4)]

x4_2 = [-x_4[n4 * i] + 0.5 * E for i in range(F / n4)]
y4_2 = [y_4[n4 * i] for i in range(F / n4)]

x4_3 = [x_4[n4 * i] + 0.5 * E for i in range(F / n4)]
y4_3 = [-y_4[n4 * i] + E for i in range(F / n4)]

x4_4 = [-x_4[n4 * i] + 0.5 * E for i in range(F / n4)]
y4_4 = [-y_4[n4 * i] + E for i in range(F / n4)]

# 4-5.Adjusting Values ----------------------------------------------------------------------------
np.set_printoptions(precision = 0)


# 5_Creating Plots ================================================================================

p = figure(x_range = (0, E), y_range = (0, E), plot_width = E, plot_height = E)


# 6_Adding Renderers ==============================================================================

# 6-1.Onset Envelope(propotional to audio length) -------------------------------------------------
p.circle(x1, y1, radius = radii_1, fill_color = colors_1, fill_alpha = 0.15, line_color = None)
p.circle(x1, y1, color = "white", size = 1, alpha = 0.15)
p.line(
       x1, y1, line_color = "white", line_width = 0.3, line_dash = "dashdot", line_alpha = 0.25)

# 6-2.Beats ---------------------------------------------------------------------------------------
p.circle(
         x2, y2, radius = radii_2, fill_color = colors_2, fill_alpha = 0.1,
         line_color = colors_2, line_width = 1, line_dash = "dotted", line_alpha = 0.8)
p.circle(
         x2, y2, radius = radii_2 / 2, fill_color = colors_2, fill_alpha = 0.1,
         line_color = colors_2, line_width = 1, line_dash = "dotted", line_alpha = 0.8)
p.circle(
         x2, y2, radius = radii_2 / 4, fill_color = colors_2, fill_alpha = 0.1,
         line_color = colors_2, line_width = 1, line_dash = "dotted", line_alpha = 0.8)
p.cross(x2, y2, color = colors_2, size = 10, alpha = 1)
p.line(
       x2, y2, line_color = colors_2, line_width = 1, line_dash = "dotted", line_alpha = 0.8)

# 6-3.Onsets --------------------------------------------------------------------------------------
p.square(
         x3, y3, size = size_3, angle = 45, fill_color = colors_3, fill_alpha = 0.1,
         line_color = colors_3, line_width = 1, line_dash = "4 4", line_alpha = 0.8)
p.square(
         x3, y3, size = size_3 / 2, angle = 45, fill_color = colors_3, fill_alpha = 0.1,
         line_color = colors_3, line_width = 1, line_dash = "4 4", line_alpha = 0.8)
p.square(
         x3, y3, size = size_3 / 4, angle = 45, fill_color = colors_3, fill_alpha = 0.1,
         line_color = colors_3, line_width = 1, line_dash = "4 4", line_alpha = 0.8)
p.cross(x3, y3, angle = 45, color = colors_3, size = 10, alpha = 1)
p.line(
       x3, y3, line_color = colors_3, line_width = 1, line_dash = "dashed", line_alpha = 0.8)

# 6-4.Frequency & Magnitude -----------------------------------------------------------------------
p.line(x4_1, y4_1, line_color = colors_4, line_dash = "dotted", line_width = 0.6, line_alpha = 0.4)
p.line(x4_2, y4_2, line_color = colors_4, line_dash = "dotted", line_width = 0.6, line_alpha = 0.4)
p.line(x4_3, y4_3, line_color = colors_4, line_dash = "dotted", line_width = 0.6, line_alpha = 0.4)
p.line(x4_4, y4_4, line_color = colors_4, line_dash = "dotted", line_width = 0.6, line_alpha = 0.4)
p.line(y4_1, x4_1, line_color = colors_4, line_dash = "dotted", line_width = 0.6, line_alpha = 0.4)
p.line(y4_2, x4_2, line_color = colors_4, line_dash = "dotted", line_width = 0.6, line_alpha = 0.4)
p.line(y4_3, x4_3, line_color = colors_4, line_dash = "dotted", line_width = 0.6, line_alpha = 0.4)
p.line(y4_4, x4_4, line_color = colors_4, line_dash = "dotted", line_width = 0.6, line_alpha = 0.4)


# 7_Setting Plot Properties =======================================================================

# Background Properties
p.background_fill_color = b_opt
p.background_fill_alpha = 1

# Outline Properties
p.outline_line_width = 0
p.outline_line_alpha = 0
p.outline_line_color = "black"

# Border Properties
p.min_border_left = 0
p.min_border_right = 0
p.min_border_top = 0
p.min_border_bottom = 0

# Grid / Axes Properties
p.grid.visible = False
p.xaxis.visible = False
p.yaxis.visible = False

# Toolbar Properties
p.toolbar.logo = None
p.toolbar_location = None


# 8_Exporting Output Files =======================================================================

# Output to PNG file
export_png(p, filename = o_opt)
