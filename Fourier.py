# Feature extraction example
#%%
print("fer") 
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
#%% Celda
y, sr = librosa.load(librosa.util.example_audio_file())
plt.figure(figsize=(12, 8))
#%%
D = librosa.amplitude_to_db(librosa.stft(y), ref=np.max)
#%%
plt.subplot(4, 2, 1)
librosa.display.specshow(D, y_axis='linear')
plt.colorbar(format='%+2.0f dB')
plt.title('Linear-frequency power spectrogram')
plt.show()


# %%


# %%
