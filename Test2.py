import matplotlib.pyplot as plt
import pandas as pd
from itertools import count
from matplotlib.animation import FuncAnimation
import pickle
import numpy as np
import concurrent.futures

with open('Random_Forest_20.pkl', 'rb') as f:
    m = pickle.load(f)

label_encoder = m['label_encoder']

def import_set(file_path):
    with open(file_path, 'rb') as file:
        my_set = pickle.load(file)
    return my_set

def evaluate_all_conditions(**kwargs):
    results = []

    function_file_path = r"TreeFunction.py"

    with open(function_file_path, 'r') as file:
        functions_code = file.read()

    for i in range(1, 21):
        function_name = f"decision_tree_rule_{i}"
        exec(functions_code)
        function = locals()[function_name]
        result = function(**kwargs) or 0
        results.append(result)

    return results

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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 10))
ax1.set_title('Input', pad=20)
ax2.set_title('Output', pad=20)
ax1.set_xlabel('TIme', labelpad=10)
ax1.set_ylabel('Voltage', labelpad=10)
ax2.set_xlabel('Time', labelpad=10)
ax2.set_ylabel('Voltage', labelpad=10)

x_data_output = []
y_data = []
prediction = []

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

def animate_output(i):
    if next(index) < len(data):
        x = data['time'].iloc[next(index)]
        y = data['vinn'].iloc[next(index)]

        input_values = data[['vdd', 'pd', 'vinp', 'temperature', 'process']].iloc[next(index)].to_dict()

        input_values['process'] = label_encoder.transform([input_values['process']])[0]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(evaluate_all_conditions, **input_values)
            pred = future.result()

        prediction.append(np.average(pred))  
        x_data_output.append(x) 
        y_data.append(y)  

        rmse, mae, snr = calculate_metrics(np.array(y_data), np.array(prediction))

        ax2.clear()
        ax2.plot(x_data_output, y_data, label='Actual', color='b')
        ax2.plot(x_data_output, np.array(prediction).flatten(), label='Predicted', color='red')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Voltage')
        ax2.set_title('Real-time Waveform Plot (Output) \n(RMSE: {:.4f}, MAE: {:.4f}, SNR: {:.4f})'.format(rmse, mae, snr))
        ax2.legend()

ani_input = FuncAnimation(fig, animate_input, interval=1000, cache_frame_data=False)
ani_output = FuncAnimation(fig, animate_output, interval=1000, cache_frame_data=False)

plt.tight_layout()
plt.show()
print("Graphs plotted")
