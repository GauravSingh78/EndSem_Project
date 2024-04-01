import matplotlib.pyplot as plt
import pandas as pd
from itertools import count
from matplotlib.animation import FuncAnimation
import pickle
import numpy as np

data = pd.read_csv(r"C:\Users\Admin\Desktop\forthSem\test\fastnfastp_3.6V_45.csv")

x_data_input = []
pdd = []
vdd = []
vinp = []
temperature = []
process = []

index = count()

def calculate_metrics(y_data, vinn):
    rmse = np.sqrt(((y_data - vinn) ** 2).mean())
    mae = np.abs(y_data - vinn).mean()
    noise = y_data - vinn
    signal_power = np.mean(y_data ** 2)
    noise_power = np.mean(noise ** 2)
    snr = 10 * np.log10(signal_power / noise_power)
    return rmse, mae, snr

def animate_input(i):
    if next(index) < len(data):
        x = data['time'].iloc[next(index)]
        p = data['pd'].iloc[next(index)]
        vin = data['vinp'].iloc[next(index)]
        vd = data['vdd'].iloc[next(index)]
        temp = data['temperature'].iloc[next(index)]
        pro = data['process'].iloc[next(index)]

        x_data_input.append(x)
        pdd.append(p)
        vinp.append(vin)
        vdd.append(vd)
        temperature.append(temp)
        process.append(pro)
        
        ax1.clear()
        ax1.plot(x_data_input, pdd, label='pdd')
        ax1.plot(x_data_input, vinp, label='vinp')
        ax1.plot(x_data_input, vdd, label='vdd')
        ax1.plot(x_data_input, temperature, label='temperature')
        ax1.plot(x_data_input, process, label='process')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Voltage')
        ax1.set_title('Real-time Waveform Plot (Input)')
        ax1.legend()

x_data_output = []
y_data = []
vinn = []
rmse_values = []
mae_values = []
snr_values = []

def animate_output(i):
    if next(index) < len(data):
        x = data['time'].iloc[next(index)]
        y = data['vinn'].iloc[next(index)]
        vin = prediction[next(index)]
        
        x_data_output.append(x)
        y_data.append(y)
        vinn.append(vin)
        
        rmse, mae, snr = calculate_metrics(np.array(y_data), np.array(vinn))
        rmse_values.append(rmse)
        mae_values.append(mae)
        snr_values.append(snr)
        
        ax2.clear()
        ax2.plot(x_data_output, y_data, label='Actual', color='b')
        ax2.plot(x_data_output, vinn, label='Predicted', color='red')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Voltage')
        ax2.set_title('Real-time Waveform Plot (Output) \n(RMSE: {:.4f}, MAE: {:.4f}, SNR: {:.4f})'.format(rmse, mae, snr))
        ax2.legend()

with open('Random_Forest_20.pkl', 'rb') as file:
    model_data = pickle.load(file)
 
loaded_model = model_data['model']
feature_names = model_data['feature_names']
label_encoder = model_data['label_encoder']

new_data = data[['vdd', 'pd', 'vinp', 'temperature','process']]
new_df = pd.DataFrame(new_data, columns=['vdd', 'pd', 'vinp', 'temperature','process'])
new_df['process'] = label_encoder.transform(new_df['process'])
prediction = loaded_model.predict(new_df)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,10))
ax1.set_title('Title 1', pad=20)  
ax2.set_title('Title 2', pad=20)
ax1.set_xlabel('X-axis label', labelpad=10) 
ax1.set_ylabel('Y-axis label', labelpad=10) 
ax2.set_xlabel('X-axis label', labelpad=10) 
ax2.set_ylabel('Y-axis label', labelpad=10)

ani_input = FuncAnimation(fig, animate_input, interval=50, cache_frame_data=False)
ani_output = FuncAnimation(fig, animate_output, interval=50, cache_frame_data=False)

plt.tight_layout()
plt.show()
print("Graphs plotted")
