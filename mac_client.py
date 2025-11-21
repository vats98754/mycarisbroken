#!/usr/bin/env python3
"""
Standalone Mac Client for OBD-II Data Visualization
Connect to your Raspberry Pi OBD server from your Mac
"""

import tkinter as tk
from tkinter import ttk, messagebox
import socketio
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
from collections import deque
import threading


class OBDVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OBD-II Real-Time Visualizer")
        self.root.geometry("1400x900")
        
        # Socket.IO client
        self.sio = socketio.Client()
        self.connected = False
        self.server_url = tk.StringVar(value="http://192.168.1.150:5000")
        
        # Data storage
        self.max_points = 100
        self.timestamps = deque(maxlen=self.max_points)
        self.rpm_data = deque(maxlen=self.max_points)
        self.speed_data = deque(maxlen=self.max_points)
        self.load_data = deque(maxlen=self.max_points)
        self.temp_data = deque(maxlen=self.max_points)
        
        # Current values
        self.current_values = {
            'RPM': '--',
            'SPEED': '--',
            'ENGINE_LOAD': '--',
            'COOLANT_TEMP': '--',
            'THROTTLE_POS': '--',
            'INTAKE_PRESSURE': '--'
        }
        
        self.setup_ui()
        self.setup_socketio()
        
    def setup_ui(self):
        # Top control panel
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Label(control_frame, text="Server URL:").grid(row=0, column=0, padx=5)
        ttk.Entry(control_frame, textvariable=self.server_url, width=30).grid(row=0, column=1, padx=5)
        
        self.connect_btn = ttk.Button(control_frame, text="Connect", command=self.connect_to_server)
        self.connect_btn.grid(row=0, column=2, padx=5)
        
        self.disconnect_btn = ttk.Button(control_frame, text="Disconnect", command=self.disconnect_from_server, state='disabled')
        self.disconnect_btn.grid(row=0, column=3, padx=5)
        
        self.status_label = ttk.Label(control_frame, text="Status: Disconnected", foreground="red")
        self.status_label.grid(row=0, column=4, padx=20)
        
        # Metrics display
        metrics_frame = ttk.LabelFrame(self.root, text="Current Values", padding="10")
        metrics_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        self.metric_labels = {}
        metrics = [
            ('RPM', 'Engine RPM', 'rpm'),
            ('SPEED', 'Speed', 'km/h'),
            ('ENGINE_LOAD', 'Engine Load', '%'),
            ('COOLANT_TEMP', 'Coolant Temp', '°C'),
            ('THROTTLE_POS', 'Throttle', '%'),
            ('INTAKE_PRESSURE', 'Intake Press', 'kPa')
        ]
        
        for idx, (key, label, unit) in enumerate(metrics):
            col = idx % 3
            row = idx // 3
            
            frame = ttk.Frame(metrics_frame)
            frame.grid(row=row, column=col, padx=15, pady=5)
            
            ttk.Label(frame, text=f"{label}:", font=('Arial', 10)).pack()
            value_label = ttk.Label(frame, text="--", font=('Arial', 16, 'bold'), foreground='blue')
            value_label.pack()
            ttk.Label(frame, text=unit, font=('Arial', 8)).pack()
            
            self.metric_labels[key] = value_label
        
        # Charts
        self.setup_charts()
        
    def setup_charts(self):
        # Create figure with subplots
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        self.fig.tight_layout(pad=3.0)
        
        # RPM Chart
        self.ax1.set_title('Engine RPM')
        self.ax1.set_ylabel('RPM')
        self.ax1.grid(True, alpha=0.3)
        self.line1, = self.ax1.plot([], [], 'r-', linewidth=2)
        
        # Speed Chart
        self.ax2.set_title('Vehicle Speed')
        self.ax2.set_ylabel('km/h')
        self.ax2.grid(True, alpha=0.3)
        self.line2, = self.ax2.plot([], [], 'b-', linewidth=2)
        
        # Engine Load Chart
        self.ax3.set_title('Engine Load')
        self.ax3.set_ylabel('Load (%)')
        self.ax3.grid(True, alpha=0.3)
        self.line3, = self.ax3.plot([], [], 'g-', linewidth=2)
        
        # Temperature Chart
        self.ax4.set_title('Coolant Temperature')
        self.ax4.set_ylabel('°C')
        self.ax4.grid(True, alpha=0.3)
        self.line4, = self.ax4.plot([], [], 'm-', linewidth=2)
        
        # Embed in tkinter
        chart_frame = ttk.Frame(self.root)
        chart_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        
    def setup_socketio(self):
        @self.sio.on('connect')
        def on_connect():
            self.connected = True
            self.root.after(0, self.update_connection_status, True)
            self.root.after(100, self.start_monitoring)
            
        @self.sio.on('disconnect')
        def on_disconnect():
            self.connected = False
            self.root.after(0, self.update_connection_status, False)
            
        @self.sio.on('obd_data')
        def on_data(data):
            self.root.after(0, self.update_data, data)
            
        @self.sio.on('status')
        def on_status(data):
            message = data.get('message', '')
            if data.get('error'):
                self.root.after(0, lambda: messagebox.showerror("Error", message))
            else:
                self.root.after(0, lambda: messagebox.showinfo("Info", message))
    
    def connect_to_server(self):
        try:
            url = self.server_url.get()
            self.sio.connect(url)
            messagebox.showinfo("Success", f"Connected to {url}")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
    
    def disconnect_from_server(self):
        try:
            self.sio.emit('stop_monitoring')
            self.sio.disconnect()
            messagebox.showinfo("Disconnected", "Disconnected from server")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to disconnect: {str(e)}")
    
    def start_monitoring(self):
        if self.connected:
            self.sio.emit('start_monitoring')
    
    def update_connection_status(self, connected):
        if connected:
            self.status_label.config(text="Status: Connected", foreground="green")
            self.connect_btn.config(state='disabled')
            self.disconnect_btn.config(state='normal')
        else:
            self.status_label.config(text="Status: Disconnected", foreground="red")
            self.connect_btn.config(state='normal')
            self.disconnect_btn.config(state='disabled')
    
    def update_data(self, data):
        # Update current values
        timestamp = datetime.now()
        self.timestamps.append(timestamp)
        
        for key in self.current_values.keys():
            value = data.get(key)
            if value is not None:
                if isinstance(value, float):
                    display_value = f"{value:.1f}"
                else:
                    display_value = str(round(value)) if isinstance(value, (int, float)) else str(value)
                self.current_values[key] = display_value
                self.metric_labels[key].config(text=display_value)
        
        # Update chart data
        self.rpm_data.append(data.get('RPM', 0) or 0)
        self.speed_data.append(data.get('SPEED', 0) or 0)
        self.load_data.append(data.get('ENGINE_LOAD', 0) or 0)
        self.temp_data.append(data.get('COOLANT_TEMP', 0) or 0)
        
        # Update charts
        self.update_charts()
    
    def update_charts(self):
        if len(self.timestamps) < 2:
            return
        
        times = list(self.timestamps)
        
        # Update RPM chart
        self.line1.set_data(times, list(self.rpm_data))
        self.ax1.relim()
        self.ax1.autoscale_view()
        
        # Update Speed chart
        self.line2.set_data(times, list(self.speed_data))
        self.ax2.relim()
        self.ax2.autoscale_view()
        
        # Update Load chart
        self.line3.set_data(times, list(self.load_data))
        self.ax3.relim()
        self.ax3.autoscale_view()
        
        # Update Temp chart
        self.line4.set_data(times, list(self.temp_data))
        self.ax4.relim()
        self.ax4.autoscale_view()
        
        # Format x-axis
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
            ax.tick_params(axis='x', rotation=45)
        
        self.fig.canvas.draw_idle()


def main():
    root = tk.Tk()
    app = OBDVisualizerApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
