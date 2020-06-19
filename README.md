<img src = "https://raw.githubusercontent.com/MYEONGJOONIL/Sound_Visualization/master/thumbnail/thumbnail.jpg" width = "350">

## 1. Overview
- **Project Name : Sound Visualization**
- **Project starts from one simple question.**  
*"What would **sound look like**, if we  could **see sound**?"*

## 2. Dependency
- **macOS** : Catalina 10.15
- **Python** : ver. 2.7.16
- [Librosa](https://librosa.github.io/librosa/) : ver. 0.7.2  
(librosa 0.7 will be last version to support Python 2)
- [Bokeh](https://docs.bokeh.org/en/1.3.4/) : ver. 1.3.4

## 3. Usage
- **0. Executing Program :**  
  ```python
  # 0-1.Basic Code Line
  > python main_sv.py -i "./sample/sample_1.wav" -b "0"
  ```
  ```python
  # 0-2.Option Description
  > python main_sv.py -h
    -i : Inout audio file path. Default path is './sample/sample_1.wav'
    -b : background color. 0 is black, 1 is white. Default value is 0(black)
  ```
- **1. Importing Libraries / Color Palettes :**  
  ```python
  import librosa
  import numpy as numpy
  from bokeh.plotting import figure
  from bokeh.io import export_png
  from bokeh.palettes import Inferno256
  ```
- **2. Loading Audio File :**  
  ```python
  audio_data = i_opt    # Default path is './sample/sample_1.wav'
  sig, sr = librosa.load(audio_data, sr = 44100)
  ```
- **3. Extracting Datas from Audio File :**  
  ```python
  # 3-1.Onset Envelope | 2.Beats | 3.Onsets
  onset_frames = librosa.onset.onset_detect(sig, sr = sr)
  onsets = librosa.frames_to_time(onset_frames, sr = sr)
  onset_env = librosa.onset.onset_strength(sig, sr = sr, aggregate = np.median)
  tempo = librosa.beat.tempo(onset_envelope = onset_env, sr = sr)
  tempo, beats = librosa.beat.beat_track(onset_envelope = onset_env, sr = sr, units = 'time')
  ```
  ```python
  # 3-4.Frequency & Magnitude
  fft = np.fft.fft(sig)
  magnitude = np.abs(fft)
  magnitude_dB = librosa.amplitude_to_db(magnitude)
  frequency = np.linspace(0, sr, len(magnitude_dB))
  left_magnitude_dB = magnitude_dB[:len(magnitude_dB)/2]
  left_frequency = frequency[:len(magnitude_dB)/2]
  ```

- **4. Preprocessing Datas for Visualization :**  
  ```python
  # 4-1.Onset Envelope
  E = len(onset_env)            
  x1 = np.random.rand(E) * E
  y1 = np.random.rand(E) * E
  n1 = 50
  radii_1 = np.random.rand(E) * E / n1
  ```
  ```python
  # 4-2.Beats
  B = len(beats)
  x2 = [x1[i] for i in range(B)]
  y2 = [y1[i] for i in range(B)]
  n2 = 13
  radii_2 = np.random.rand(B) * E / n2
  ```
  ```python
  # 4-3.Onsets
  O = len(onsets)
  x3 = [x1[-(i+1)] for i in range(O)]
  y3 = [y1[-(i+1)] for i in range(O)]
  n3 = 8
  size_3 = np.random.rand(O) * E / n3
  ```
  ```python
  # 4-4.Frequency & Magnitude
  F = len(left_frequency)
  x_4 = left_magnitude_dB / x_ratio
  y_4 = left_frequency / y_ratio
  n4 = 100

  x4_1 = [x_4[n4 * i] + 0.5 * E for i in range(F / n4)]
  y4_1 = [y_4[n4 * i] for i in range(F / n4)]

  x4_2 = [-x_4[n4 * i] + 0.5 * E for i in range(F / n4)]
  y4_2 = [y_4[n4 * i] for i in range(F / n4)]

  x4_3 = [x_4[n4 * i] + 0.5 * E for i in range(F / n4)]
  y4_3 = [-y_4[n4 * i] + E for i in range(F / n4)]

  x4_4 = [-x_4[n4 * i] + 0.5 * E for i in range(F / n4)]
  y4_4 = [-y_4[n4 * i] + E for i in range(F / n4)]
  ```

- **5. Creating Plots :**  
  ```python
  p = figure(x_range = (0, E), y_range = (0, E), plot_width = E, plot_height = E)
  ```

- **6. Adding Renderers :**  
  ```python
  # 6-1.Onset Envelope
  p.circle(x1, y1, radius = radii_1, fill_color = colors_1, fill_alpha = 0.15, line_color = None)
  ```
  ```python
  # 6-2.Beats
  p.circle(
  x2, y2, radius = radii_2, fill_color = colors_2, fill_alpha = 0.1,
  line_color = colors_2, line_width = 1, line_dash = "dotted", line_alpha = 0.8)
  ```
  ```python
  # 6-3.Onsets
  p.square(
  x3, y3, size = size_3, angle = 45, fill_color = colors_3, fill_alpha = 0.1,
  line_color = colors_3, line_width = 1, line_dash = "4 4", line_alpha = 0.8)
  ```
  ```python
  # 6-4.Frequency & Magnitude
  p.line(x4_1, y4_1, line_color = colors_4, line_dash = "dotted", line_width = 0.6, line_alpha = 0.4)
  ```

- **7. Setting Plot Properties :**  
  ```python
  # Background Properties
  p.background_fill_color = b_opt   # Default value is "black"
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
  ```
- **8. Exporting Output Files :**  
  ```python
  # Output to PNG file
  export_png(p, filename = o_opt)   # According to input file name
  ```

## 4. Version
- version of sound visualization project : SV 1.0

