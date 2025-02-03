# Feature extraction example
#%%
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

#%% Celda
# Cargar un archivo de ejemplo actualizado
audio_path = librosa.example("trumpet")
y, sr = librosa.load(audio_path)
plt.figure(figsize=(12, 8))

#%%
D = librosa.amplitude_to_db(librosa.stft(y), ref=np.max)

#%%
plt.subplot(4, 2, 1)
librosa.display.specshow(D, y_axis='linear', x_axis='time', sr=sr)
plt.colorbar(format='%+2.0f dB')
plt.title('Linear-frequency power spectrogram')
plt.show()
# %%
