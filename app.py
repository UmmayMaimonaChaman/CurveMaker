from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from scipy.interpolate import make_interp_spline, UnivariateSpline
from scipy.stats import linregress
from scipy.optimize import curve_fit
import io
import base64
import json
import seaborn as sns
from matplotlib.patches import Polygon
import warnings
warnings.filterwarnings('ignore')

# Set matplotlib to use non-interactive backend
matplotlib.use('Agg')

app = Flask(__name__)
CORS(app)

# Configure matplotlib for professional white theme
plt.style.use('default')
sns.set_palette("husl")

class CurveGenerator:
    def __init__(self):
        self.color_schemes = {
            'neon': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'],
            'ocean': ['#1e3a8a', '#3b82f6', '#06b6d4', '#0891b2', '#0e7490', '#155e75'],
            'sunset': ['#f97316', '#ea580c', '#dc2626', '#b91c1c', '#991b1b', '#7f1d1d'],
            'forest': ['#166534', '#16a34a', '#22c55e', '#4ade80', '#86efac', '#bbf7d0'],
            'monochrome': ['#000000', '#404040', '#808080', '#c0c0c0', '#e0e0e0', '#f0f0f0']
        }
        
        self.grid_styles = {
            'neon': {'alpha': 0.3, 'color': '#cccccc', 'linewidth': 0.8},
            'subtle': {'alpha': 0.2, 'color': '#dddddd', 'linewidth': 0.5},
            'none': None
        }

    def generate_chart(self, curve_type, title, x_axis_label, y_axis_label, data, color_scheme='neon', grid_style='neon', show_x_axis=True, show_y_axis=True):
        """Main method to generate charts based on curve type"""
        try:
            # Parse data
            if isinstance(data, str):
                data = json.loads(data)
            
            # Set up the plot
            fig, ax = plt.subplots(figsize=(12, 8))
            colors = self.color_schemes.get(color_scheme, self.color_schemes['neon'])
            
            # Apply grid style
            if grid_style != 'none':
                grid_config = self.grid_styles.get(grid_style, self.grid_styles['neon'])
                if grid_config:
                    ax.grid(True, **grid_config)
                    ax.set_axisbelow(True)  # Put grid behind data
            
            # Generate chart based on type
            if curve_type == 'line':
                self.create_line_chart(ax, data, colors, x_axis_label, y_axis_label)
            elif curve_type == 'bar':
                self.create_bar_chart(ax, data, colors, x_axis_label, y_axis_label)
            elif curve_type == 'pie':
                self.create_pie_chart(ax, data, colors, title)
            elif curve_type == 'area':
                self.create_area_chart(ax, data, colors, x_axis_label, y_axis_label)
            elif curve_type == 'spline':
                self.create_spline_chart(ax, data, colors, x_axis_label, y_axis_label)
            elif curve_type == 'bezier':
                self.create_bezier_chart(ax, data, colors, x_axis_label, y_axis_label)
            elif curve_type == 'lowess':
                self.create_lowess_chart(ax, data, colors, x_axis_label, y_axis_label)
            elif curve_type == 'moving_average':
                self.create_moving_average_chart(ax, data, colors, x_axis_label, y_axis_label)
            elif curve_type == 'polynomial':
                self.create_polynomial_chart(ax, data, colors, x_axis_label, y_axis_label)
            elif curve_type == 'exponential':
                self.create_exponential_chart(ax, data, colors, x_axis_label, y_axis_label)
            elif curve_type == 'sigmoid':
                self.create_sigmoid_chart(ax, data, colors, x_axis_label, y_axis_label)
            elif curve_type == 'gompertz':
                self.create_gompertz_chart(ax, data, colors, x_axis_label, y_axis_label)
            elif curve_type == 'stacked_area':
                self.create_stacked_area_chart(ax, data, colors, x_axis_label, y_axis_label)
            elif curve_type == 'streamgraph':
                self.create_streamgraph_chart(ax, data, colors, x_axis_label, y_axis_label)
            elif curve_type == 'step':
                self.create_step_chart(ax, data, colors, x_axis_label, y_axis_label)
            else:
                raise ValueError(f"Unsupported curve type: {curve_type}")
            
            # Set title and labels
            ax.set_title(title, fontsize=16, fontweight='bold', color='#000000', pad=20)
            if x_axis_label and curve_type != 'pie' and show_x_axis:
                ax.set_xlabel(x_axis_label, fontsize=12, color='#000000')
            if y_axis_label and curve_type != 'pie' and show_y_axis:
                ax.set_ylabel(y_axis_label, fontsize=12, color='#000000')
            
            # Style the plot
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(show_y_axis)
            ax.spines['bottom'].set_visible(show_x_axis)
            ax.spines['left'].set_color('#000000')
            ax.spines['bottom'].set_color('#000000')
            ax.tick_params(colors='#000000')
            
            # Show/hide axis ticks and labels
            if not show_x_axis:
                ax.set_xticks([])
                ax.set_xticklabels([])
            if not show_y_axis:
                ax.set_yticks([])
                ax.set_yticklabels([])
            
            # Ensure axis ticks are visible and properly formatted
            if show_x_axis:
                ax.tick_params(axis='x', which='major', labelsize=10, colors='#000000')
            if show_y_axis:
                ax.tick_params(axis='y', which='major', labelsize=10, colors='#000000')
            
            plt.tight_layout()
            
            # Convert to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return f"data:image/png;base64,{image_base64}"
            
        except Exception as e:
            raise Exception(f"Error generating chart: {str(e)}")

    def create_line_chart(self, ax, data, colors, x_label, y_label):
        """Create a line chart"""
        if 'years' in data and 'sales' in data:
            years = data['years']
            sales = data['sales']
            ax.plot(years, sales, marker='o', linewidth=3, markersize=8, 
                   color=colors[0], label='Sales')
            
            if 'profit' in data:
                profit = data['profit']
                ax.plot(years, profit, marker='s', linewidth=3, markersize=8, 
                       color=colors[1], label='Profit')
                ax.legend()
            
            # Ensure axis values are displayed
            ax.set_xticks(years)
            ax.set_xticklabels(years, fontsize=10, fontweight='bold')
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
            ax.tick_params(axis='both', which='major', labelsize=10)
        else:
            # Generic line chart
            keys = list(data.keys())
            x_data = data[keys[0]] if len(keys) > 0 else []
            for i, key in enumerate(keys[1:]):
                y_data = data[key]
                ax.plot(x_data, y_data, marker='o', linewidth=3, markersize=8, 
                       color=colors[i % len(colors)], label=key)
            ax.legend()
            
            # Ensure axis values are displayed for generic data
            if len(x_data) > 0:
                ax.set_xticks(x_data)
                ax.set_xticklabels(x_data, fontsize=10, fontweight='bold')
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
            ax.tick_params(axis='both', which='major', labelsize=10)

    def create_bar_chart(self, ax, data, colors, x_label, y_label):
        """Create a bar chart"""
        if 'categories' in data and 'revenue' in data:
            categories = data['categories']
            revenue = data['revenue']
            x_pos = np.arange(len(categories))
            
            bars = ax.bar(x_pos, revenue, color=colors[0], alpha=0.8, 
                         edgecolor=colors[0], linewidth=2)
            
            if 'costs' in data:
                costs = data['costs']
                ax.bar(x_pos, costs, color=colors[1], alpha=0.8, 
                      edgecolor=colors[1], linewidth=2, bottom=revenue)
            
            ax.set_xticks(x_pos)
            ax.set_xticklabels(categories, rotation=0, ha='center')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                       f'{int(height):,}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        else:
            # Generic bar chart - handle multiple series like the Google Colab example
            keys = list(data.keys())
            if 'years' in data:
                years = data['years']
                bar_width = 0.13
                x = np.arange(len(years))
                
                for i, (domain, values) in enumerate(data.items()):
                    if domain != 'years':
                        ax.bar([p + i * bar_width for p in x], values, width=bar_width, 
                              label=domain, color=colors[i % len(colors)], alpha=0.8)
                
                ax.set_xticks([p + 2.5 * bar_width for p in x])
                ax.set_xticklabels(years, rotation=0, ha='center', fontsize=10, fontweight='bold')
                ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                
                # Ensure Y-axis shows proper tick values
                ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
                ax.tick_params(axis='both', which='major', labelsize=10)
                
                # Add value labels on bars
                for i, (domain, values) in enumerate(data.items()):
                    if domain != 'years':
                        for j, value in enumerate(values):
                            ax.text(x[j] + i * bar_width, value + value*0.01,
                                   f'{int(value):,}', ha='center', va='bottom', 
                                   fontsize=8, fontweight='bold', rotation=90)
            else:
                # Fallback for other data formats
                categories = data[keys[0]] if len(keys) > 0 else []
                for i, key in enumerate(keys[1:]):
                    values = data[key]
                    x_pos = np.arange(len(categories))
                    bars = ax.bar(x_pos + i * 0.2, values, color=colors[i % len(colors)], 
                                 alpha=0.8, width=0.2, label=key)
                    
                    # Add value labels
                    for bar in bars:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                               f'{int(height):,}', ha='center', va='bottom', fontsize=8, fontweight='bold')
                
                ax.set_xticks(x_pos + 0.1)
                ax.set_xticklabels(categories, rotation=0, ha='center')
                ax.legend()

    def create_pie_chart(self, ax, data, colors, title):
        """Create a pie chart"""
        if 'labels' in data and 'values' in data:
            labels = data['labels']
            values = data['values']
            
            # Calculate percentages for better labels
            total = sum(values)
            percentages = [f'{(v/total)*100:.1f}%' for v in values]
            
            # Create custom labels with values and percentages
            custom_labels = [f'{label}\n({value:,})' for label, value in zip(labels, values)]
            
            wedges, texts, autotexts = ax.pie(values, labels=custom_labels, 
                                             startangle=90, colors=colors[:len(values)],
                                             textprops={'color': '#000000', 'fontsize': 10, 'fontweight': 'bold'},
                                             autopct=lambda pct: f'{pct:.1f}%')
            
            # Style the percentage text
            for autotext in autotexts:
                autotext.set_color('#000000')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(9)
            
            # Add a legend
            ax.legend(wedges, labels, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            
        else:
            # Generic pie chart
            keys = list(data.keys())
            values = data[keys[0]] if len(keys) > 0 else []
            labels = keys[1:] if len(keys) > 1 else []
            
            if len(values) > 0:
                total = sum(values)
                custom_labels = [f'{label}\n({value:,})' for label, value in zip(labels, values)]
                
                wedges, texts, autotexts = ax.pie(values, labels=custom_labels, 
                                                 startangle=90, colors=colors[:len(values)],
                                                 textprops={'color': '#000000', 'fontsize': 10, 'fontweight': 'bold'},
                                                 autopct=lambda pct: f'{pct:.1f}%')
                
                # Style the percentage text
                for autotext in autotexts:
                    autotext.set_color('#000000')
                    autotext.set_fontweight('bold')
                    autotext.set_fontsize(9)
                
                # Add a legend
                ax.legend(wedges, labels, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    def create_area_chart(self, ax, data, colors, x_label, y_label):
        """Create an area chart"""
        if 'months' in data and 'users' in data:
            months = data['months']
            users = data['users']
            ax.fill_between(months, users, alpha=0.6, color=colors[0])
            ax.plot(months, users, color=colors[0], linewidth=2, marker='o')
            
            if 'premium' in data:
                premium = data['premium']
                ax.fill_between(months, premium, alpha=0.6, color=colors[1])
                ax.plot(months, premium, color=colors[1], linewidth=2, marker='s')
            
            # Ensure axis values are displayed
            ax.set_xticks(range(len(months)))
            ax.set_xticklabels(months, fontsize=10, fontweight='bold')
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
            ax.tick_params(axis='both', which='major', labelsize=10)
        else:
            # Generic area chart
            keys = list(data.keys())
            x_data = data[keys[0]] if len(keys) > 0 else []
            for i, key in enumerate(keys[1:]):
                y_data = data[key]
                ax.fill_between(x_data, y_data, alpha=0.6, color=colors[i % len(colors)])
                ax.plot(x_data, y_data, color=colors[i % len(colors)], linewidth=2)
            
            # Ensure axis values are displayed for generic data
            if len(x_data) > 0:
                ax.set_xticks(x_data)
                ax.set_xticklabels(x_data, fontsize=10, fontweight='bold')
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
            ax.tick_params(axis='both', which='major', labelsize=10)

    def create_spline_chart(self, ax, data, colors, x_label, y_label):
        """Create a spline curve chart"""
        if 'years' in data and 'sales' in data:
            years = np.array(data['years'])
            sales = np.array(data['sales'])
            
            # Create smooth spline
            xnew = np.linspace(years.min(), years.max(), 300)
            spline = make_interp_spline(years, sales, k=3)
            ynew = spline(xnew)
            
            ax.plot(xnew, ynew, color=colors[0], linewidth=3, label='Spline')
            ax.scatter(years, sales, color=colors[0], s=100, zorder=5)
            ax.legend()
        else:
            # Generic spline
            keys = list(data.keys())
            x_data = np.array(data[keys[0]] if len(keys) > 0 else [])
            for i, key in enumerate(keys[1:]):
                y_data = np.array(data[key])
                xnew = np.linspace(x_data.min(), x_data.max(), 300)
                spline = make_interp_spline(x_data, y_data, k=3)
                ynew = spline(xnew)
                ax.plot(xnew, ynew, color=colors[i % len(colors)], linewidth=3, label=f'{key} (Spline)')
                ax.scatter(x_data, y_data, color=colors[i % len(colors)], s=100, zorder=5)
            ax.legend()

    def create_bezier_chart(self, ax, data, colors, x_label, y_label):
        """Create a Bezier curve chart"""
        # Simplified Bezier implementation
        if 'years' in data and 'sales' in data:
            years = np.array(data['years'])
            sales = np.array(data['sales'])
            
            # Create control points for Bezier
            t = np.linspace(0, 1, 100)
            x_bezier = []
            y_bezier = []
            
            for i in range(len(years) - 1):
                p0 = np.array([years[i], sales[i]])
                p1 = np.array([years[i] + (years[i+1] - years[i])/2, sales[i] + (sales[i+1] - sales[i])/2])
                p2 = np.array([years[i+1], sales[i+1]])
                
                for j in t:
                    point = (1-j)**2 * p0 + 2*(1-j)*j * p1 + j**2 * p2
                    x_bezier.append(point[0])
                    y_bezier.append(point[1])
            
            ax.plot(x_bezier, y_bezier, color=colors[0], linewidth=3, label='Bezier')
            ax.scatter(years, sales, color=colors[0], s=100, zorder=5)
            ax.legend()

    def create_lowess_chart(self, ax, data, colors, x_label, y_label):
        """Create a LOWESS smoothed chart"""
        if 'years' in data and 'sales' in data:
            years = np.array(data['years'])
            sales = np.array(data['sales'])
            
            # Add some noise for demonstration
            noise = np.random.normal(0, sales * 0.1)
            noisy_sales = sales + noise
            
            # Simple moving average as LOWESS approximation
            window = 3
            smoothed = np.convolve(noisy_sales, np.ones(window)/window, mode='valid')
            smoothed_x = years[window-1:]
            
            ax.scatter(years, noisy_sales, color=colors[0], alpha=0.6, s=50, label='Original Data')
            ax.plot(smoothed_x, smoothed, color=colors[1], linewidth=3, label='LOWESS Smoothed')
            ax.legend()

    def create_moving_average_chart(self, ax, data, colors, x_label, y_label):
        """Create a moving average chart"""
        if 'years' in data and 'sales' in data:
            years = np.array(data['years'])
            sales = np.array(data['sales'])
            
            # Calculate moving averages
            window_sizes = [3, 5]
            for i, window in enumerate(window_sizes):
                if len(sales) >= window:
                    ma = np.convolve(sales, np.ones(window)/window, mode='valid')
                    ma_x = years[window-1:]
                    ax.plot(ma_x, ma, color=colors[i], linewidth=3, 
                           label=f'{window}-period MA')
            
            ax.plot(years, sales, color=colors[-1], linewidth=2, marker='o', 
                   label='Original Data', alpha=0.7)
            ax.legend()

    def create_polynomial_chart(self, ax, data, colors, x_label, y_label):
        """Create a polynomial regression chart"""
        if 'years' in data and 'sales' in data:
            years = np.array(data['years'])
            sales = np.array(data['sales'])
            
            # Fit polynomial
            coeffs = np.polyfit(years, sales, 2)  # Quadratic
            poly = np.poly1d(coeffs)
            x_poly = np.linspace(years.min(), years.max(), 100)
            y_poly = poly(x_poly)
            
            ax.plot(x_poly, y_poly, color=colors[0], linewidth=3, label='Polynomial Fit')
            ax.scatter(years, sales, color=colors[1], s=100, zorder=5, label='Data Points')
            ax.legend()

    def create_exponential_chart(self, ax, data, colors, x_label, y_label):
        """Create an exponential curve chart"""
        if 'years' in data and 'sales' in data:
            years = np.array(data['years'])
            sales = np.array(data['sales'])
            
            # Fit exponential function
            def exp_func(x, a, b, c):
                return a * np.exp(b * x) + c
            
            try:
                popt, _ = curve_fit(exp_func, years, sales, maxfev=5000)
                x_exp = np.linspace(years.min(), years.max(), 100)
                y_exp = exp_func(x_exp, *popt)
                
                ax.plot(x_exp, y_exp, color=colors[0], linewidth=3, label='Exponential Fit')
                ax.scatter(years, sales, color=colors[1], s=100, zorder=5, label='Data Points')
                ax.legend()
            except:
                # Fallback to simple exponential
                ax.plot(years, sales, color=colors[0], linewidth=3, marker='o')

    def create_sigmoid_chart(self, ax, data, colors, x_label, y_label):
        """Create a sigmoid curve chart"""
        # Generate sigmoid data
        x = np.linspace(-5, 5, 100)
        y = 1 / (1 + np.exp(-x))
        
        ax.plot(x, y, color=colors[0], linewidth=3, label='Sigmoid Function')
        ax.set_xlabel('Input')
        ax.set_ylabel('Output')
        ax.legend()

    def create_gompertz_chart(self, ax, data, colors, x_label, y_label):
        """Create a Gompertz curve chart"""
        # Generate Gompertz data
        x = np.linspace(0, 10, 100)
        y = np.exp(-np.exp(-x + 5))
        
        ax.plot(x, y, color=colors[0], linewidth=3, label='Gompertz Function')
        ax.set_xlabel('Time')
        ax.set_ylabel('Growth')
        ax.legend()

    def create_stacked_area_chart(self, ax, data, colors, x_label, y_label):
        """Create a stacked area chart"""
        if 'years' in data:
            years = data['years']
            bottom = np.zeros(len(years))
            
            for i, (key, values) in enumerate(data.items()):
                if key != 'years':
                    ax.fill_between(years, bottom, bottom + values, 
                                  alpha=0.7, color=colors[i % len(colors)], label=key)
                    bottom += values
            
            ax.legend()

    def create_streamgraph_chart(self, ax, data, colors, x_label, y_label):
        """Create a streamgraph chart"""
        # Simplified streamgraph
        if 'years' in data:
            years = data['years']
            bottom = np.zeros(len(years))
            
            for i, (key, values) in enumerate(data.items()):
                if key != 'years':
                    # Center the stream
                    center = np.sum(values) / 2
                    ax.fill_between(years, bottom - center, bottom + values - center, 
                                  alpha=0.7, color=colors[i % len(colors)], label=key)
                    bottom += values

    def create_step_chart(self, ax, data, colors, x_label, y_label):
        """Create a step chart"""
        if 'years' in data and 'sales' in data:
            years = data['years']
            sales = data['sales']
            
            ax.step(years, sales, where='post', color=colors[0], linewidth=3, 
                   marker='o', markersize=8, label='Step Function')
            ax.legend()

# Initialize the curve generator
curve_generator = CurveGenerator()

@app.route('/api/generate-chart', methods=['POST'])
def generate_chart():
    """API endpoint to generate charts"""
    try:
        data = request.json
        
        # Extract parameters
        curve_type = data.get('curve_type')
        title = data.get('title', 'Generated Chart')
        x_axis_label = data.get('x_axis_label', '')
        y_axis_label = data.get('y_axis_label', '')
        chart_data = data.get('data', {})
        color_scheme = data.get('color_scheme', 'neon')
        grid_style = data.get('grid_style', 'neon')
        show_x_axis = data.get('show_x_axis', True)
        show_y_axis = data.get('show_y_axis', True)
        
        # Generate the chart
        chart_url = curve_generator.generate_chart(
            curve_type, title, x_axis_label, y_axis_label, 
            chart_data, color_scheme, grid_style, show_x_axis, show_y_axis
        )
        
        return jsonify({
            'success': True,
            'chart_url': chart_url,
            'chart_data': data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'CurveMaker Pro API is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 