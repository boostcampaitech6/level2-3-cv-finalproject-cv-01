import tkinter as tk
import csv
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class DrawingApp:
    def __init__(self, root, stock_path):
        self.root = root
        self.root.title("Drawing Pattern")

        self.stock_data_path = stock_path
        self.run_path = os.path.dirname(os.path.realpath(__file__)) 
        self.save_dir = os.path.join(self.run_path, 'data', 'drawing_pattern.csv')
        
        main_frame = tk.Frame(self.root)
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 캔버스 설정
        self.canvas = tk.Canvas(main_frame, bg='white', width=600, height=400)
        self.canvas.grid(row=0, column=0, columnspan=2)

        # 저장 버튼 설정
        self.save_button = tk.Button(main_frame, text="Save Patterns", command=self.save_and_analyze_patterns)
        self.save_button.grid(row=1, column=0, sticky="ew")  # ew는 동서(좌우)로 스트레치

        # 리셋 버튼 설정
        self.reset_button = tk.Button(main_frame, text="Reset", command=self.reset_canvas_and_graph)
        self.reset_button.grid(row=1, column=1, sticky="ew")

        
        # 패턴 데이터 초기화
        self.drawing_data = []
        self.last_x, self.last_y = None, None

        self.canvas.bind('<Button-1>', self.start_drawing)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.stop_drawing)

        # 그래프 플롯 초기화
        plot_frame = tk.Frame(self.root)
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.figure, self.ax = plt.subplots(figsize=(7, 5))
        self.graph = FigureCanvasTkAgg(self.figure, master=plot_frame)
        self.graph.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

    def start_drawing(self, event):
        self.drawing_data = []
        self.last_x = event.x
        self.last_y = event.y
        self.drawing_data.append((event.x, event.y))

    def draw(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, width=2)
            self.drawing_data.append((event.x, event.y))
        self.last_x = event.x
        self.last_y = event.y

    # 그리기 중단
    def stop_drawing(self, event):
        self.last_x, self.last_y = None, None
        print("Drawing completed.")
        # print("Drawing completed. Data:", self.drawing_data)

    # 패턴 저장 및 분석
    def save_and_analyze_patterns(self):
        if self.drawing_data:
            
            save_dir = self.save_dir
            with open(save_dir, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['x', 'y'])
                writer.writerows(self.drawing_data)
            print("Pattern saved to 'drawing_pattern.csv'")
            
            self.analyze_and_visualize_pattern()

    
    def normalize_pattern(self, pattern, stock_data):
        pattern_min, pattern_max = min(pattern), max(pattern)
        stock_min, stock_max = stock_data.min(), stock_data.max()
        pattern_scaled = (pattern - pattern_min) / (pattern_max - pattern_min)
        pattern_normalized = pattern_scaled * (stock_max - stock_min) + stock_min
        return pattern_normalized - np.mean(pattern_normalized)


    def rolling_pattern_match(self, stock_data, pattern, window_size):
        pattern = (pattern - np.mean(pattern)) / np.std(pattern)
        pattern_len = len(pattern)
        match_scores = []
        start_indices = []
        for i in range(len(stock_data) - window_size + 1):
            window = stock_data[i:i + window_size]
            window_normalized = (window - np.mean(window)) / np.std(window)
            if np.std(window_normalized) != 0:
                resized_pattern = np.interp(np.linspace(0, pattern_len, window_size), np.arange(pattern_len), pattern)
                score = np.dot(window_normalized, resized_pattern)
                match_scores.append(score)
                start_indices.append(i)
        match_scores_df = pd.DataFrame({'Start Index': start_indices, 'Match Score': match_scores})
        match_scores_df.sort_values('Match Score', ascending=False, inplace=True)
        match_scores_df.reset_index(drop=True, inplace=True)
        return match_scores_df

    def reset_canvas_and_graph(self):

        # 캔버스 리셋
        self.canvas.delete("all")
        self.drawing_data = []
        
        # 그래프 리셋
        self.ax.clear()
        self.ax.set_title('Stock Price')
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Price (in KRW)')
        self.graph.draw()

    def analyze_and_visualize_pattern(self):
        stock_data = pd.read_csv(self.stock_data_path) 
        stock_data['Date'] = pd.to_datetime(stock_data['Date'])
        
        window_size = 20
        drawing_pattern_path = self.save_dir
        provided_pattern_df = pd.read_csv(drawing_pattern_path)

        provided_pattern_df['y'] = max(provided_pattern_df['y']) - provided_pattern_df['y']
        provided_pattern_df['x'] = np.linspace(0, window_size, len(provided_pattern_df))
        normalized_drawing_pattern = self.normalize_pattern(provided_pattern_df['y'].values, stock_data['Close'])
        match_scores_df = self.rolling_pattern_match(stock_data['Close'], normalized_drawing_pattern, window_size=20)

        top_10_matches = match_scores_df.head(10)
        print(top_10_matches)


        top_match_index = int(top_10_matches.iloc[0]['Start Index'])
        top_match_score = top_10_matches.iloc[0]['Match Score']

        self.ax.clear()
        self.ax.plot(stock_data['Date'], stock_data['Close'], label='Samsung Stock Price', alpha=0.5)
        self.ax.plot(stock_data['Date'][top_match_index:top_match_index + window_size], 
                stock_data['Close'][top_match_index:top_match_index + window_size], 
                label='Top Matching Window', linewidth=2, color='orange')
        self.ax.legend()
        self.ax.set_title('Stock Price with Top Matching Pattern Highlighted')
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Price (in KRW)')
        self.graph.draw()

if __name__ == "__main__":
    
    run_path = os.path.dirname(os.path.realpath(__file__))
    stock_data = 'SK_Hynix_10y_1d_data.csv'
    stock_path = os.path.join(run_path, 'data', stock_data)
    root = tk.Tk()
    app = DrawingApp(root, stock_path)
    root.mainloop()
