# CurveMaker 🚀

A professional web application for creating advanced data visualizations with live preview, inspired by LiveGap Charts. Generate beautiful charts and curves using Python's scientific computing libraries with an intuitive web interface.

## ✨ Features

### 📊 Chart Types
- **Basic Charts**: Line, Bar, Pie, Area
- **Smooth Curves**: Spline, Bezier, LOWESS/LOESS, Moving Average
- **Mathematical Curves**: Polynomial Regression, Exponential, Sigmoid, Gompertz
- **Area & Volume**: Stacked Area, Streamgraph, Step Charts

### 🎨 Design Features
- **Dark Theme**: Professional black and dark blue color scheme
- **Neon Accents**: Eye-catching neon blue, purple, green, pink, and orange highlights
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Interactive UI**: Smooth animations and hover effects
- **Multiple Color Schemes**: Neon, Ocean, Sunset, Forest, Monochrome

### 🔧 Technical Features
- **Real-time Preview**: See your chart as you configure it
- **Data Validation**: Smart input validation for various data formats
- **Export Options**: Download charts as PNG or SVG
- **Sample Data**: Quick sample data buttons for testing
- **Backend Integration**: Python Flask API with matplotlib and scipy
- **Value Labels**: Data values displayed on charts for better readability
- **Axis Control**: Toggle X and Y axes visibility

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Node.js (optional, for development)

### Backend Setup
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Plotmaker
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask backend**
   ```bash
   python app.py
   ```
   The backend will start on `http://localhost:5000`

### Frontend Setup
The frontend is pure HTML/CSS/JavaScript, so you can simply:
1. Open `index.html` in your web browser
2. Or serve it using a local server:
   ```bash
   # Using Python
   python -m http.server 8000
   
   # Using Node.js
   npx serve .
   ```

## 📖 Usage

### 1. Select Chart Type
Choose from the dropdown menu:
- **Basic Charts**: Perfect for simple data visualization
- **Smooth Curves**: For elegant, continuous data representation
- **Mathematical Curves**: For scientific and statistical analysis
- **Area & Volume**: For cumulative and flow data

### 2. Configure Chart
- **Title**: Give your chart a descriptive title
- **Axis Labels**: Add meaningful labels for X and Y axes
- **Data Input**: Enter your data in JSON or CSV format
- **Color Scheme**: Choose from 5 beautiful color schemes
- **Grid Style**: Select grid appearance (Neon, Subtle, or None)
- **Axis Control**: Show or hide X and Y axes as needed

### 3. Data Format Examples

#### JSON Format
```json
{
  "years": [2020, 2021, 2022, 2023, 2024, 2025],
  "sales": [100, 250, 450, 612, 800, 950],
  "profit": [20, 50, 90, 122, 160, 190]
}
```

#### CSV Format
```
years,2020,2021,2022,2023,2024,2025
sales,100,250,450,612,800,950
profit,20,50,90,122,160,190
```

### 4. Generate and Export
- Click "Generate Curve" to create your visualization
- Download as PNG or SVG
- Share your chart with others

## 🎯 Chart Type Guide

### Line Chart
- **Best for**: Time series data, trend analysis
- **Example**: Sales over time, temperature trends

### Spline Curve
- **Best for**: Smooth trend visualization
- **Example**: Elegant presentations, continuous data

### Bar Chart
- **Best for**: Categorical comparisons
- **Example**: Survey results, performance metrics

### Pie Chart
- **Best for**: Parts of a whole
- **Example**: Market share, budget allocation

### Area Chart
- **Best for**: Cumulative data, volume emphasis
- **Example**: User growth, revenue accumulation

### Polynomial Regression
- **Best for**: Complex relationships, predictive analysis
- **Example**: Scientific modeling, trend prediction

### Exponential Curve
- **Best for**: Rapid growth patterns
- **Example**: Population growth, viral spread

### Sigmoid Curve
- **Best for**: Saturation behavior
- **Example**: Learning curves, market adoption

## 🔧 API Endpoints

### Generate Chart
```
POST /api/generate-chart
Content-Type: application/json

{
  "curve_type": "line",
  "title": "My Chart",
  "x_axis_label": "Time",
  "y_axis_label": "Value",
  "data": {...},
  "color_scheme": "neon",
  "grid_style": "neon"
}
```

### Health Check
```
GET /api/health
```

## 🎨 Customization

### Color Schemes
- **Neon**: Bright, eye-catching colors
- **Ocean**: Professional blue tones
- **Sunset**: Warm orange and red hues
- **Forest**: Natural green palette
- **Monochrome**: Clean grayscale

### Grid Styles
- **Neon**: Bright grid lines with glow effect
- **Subtle**: Soft, unobtrusive grid
- **None**: Clean, grid-free design

## 🚀 Deployment

### Local Development
1. Start the Flask backend: `python app.py`
2. Open `index.html` in your browser
3. Update the API endpoint in `script.js` if needed

### Production Deployment
1. Use a production WSGI server like Gunicorn
2. Configure CORS for your domain
3. Set up proper error handling and logging
4. Consider using a CDN for static assets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Matplotlib**: For powerful chart generation
- **SciPy**: For scientific computing functions
- **Flask**: For the web framework
- **Google Fonts**: For beautiful typography

---

**CurveMaker** - Transform your data into stunning visualizations! 🎨📊

**Made by Ummay Maimona Chaman**

If you encounter any issues or have suggestions to share, please feel free to let me know. 😊
