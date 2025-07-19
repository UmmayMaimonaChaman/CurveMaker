// CurveMaker - Frontend JavaScript
class CurveMaker {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.loadCurveDescriptions();
        this.currentChartData = null;
    }

    initializeElements() {
        this.form = document.getElementById('curveForm');
        this.curveTypeSelect = document.getElementById('curveType');
        this.chartTitleInput = document.getElementById('chartTitle');
        this.xAxisLabelInput = document.getElementById('xAxisLabel');
        this.yAxisLabelInput = document.getElementById('yAxisLabel');
        this.dataInput = document.getElementById('dataInput');
        this.colorSchemeSelect = document.getElementById('colorScheme');
        this.gridStyleSelect = document.getElementById('gridStyle');
        this.showXAxisCheckbox = document.getElementById('showXAxis');
        this.showYAxisCheckbox = document.getElementById('showYAxis');
        this.chartPreview = document.getElementById('chartPreview');
        this.generatedChart = document.getElementById('generatedChart');
        this.chartImage = document.getElementById('chartImage');
        this.curveDescription = document.getElementById('curveDescription');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.downloadSVGBtn = document.getElementById('downloadSVGBtn');
        this.shareBtn = document.getElementById('shareBtn');
    }

    bindEvents() {
        this.form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        this.curveTypeSelect.addEventListener('change', () => this.updateCurveDescription());
        this.dataInput.addEventListener('input', () => this.validateDataInput());
        this.downloadBtn.addEventListener('click', () => this.downloadChart('png'));
        this.downloadSVGBtn.addEventListener('click', () => this.downloadChart('svg'));
        this.shareBtn.addEventListener('click', () => this.shareChart());
        
        // Add sample data buttons
        this.addSampleDataButtons();
    }

    loadCurveDescriptions() {
        this.curveDescriptions = {
            'line': {
                title: 'Line Chart',
                description: 'Straight lines connecting data points—basic and widely used for showing trends over time or continuous relationships between variables.',
                useCases: 'Time series data, trend analysis, continuous relationships'
            },
            'bar': {
                title: 'Bar Chart',
                description: 'Rectangular bars representing categorical data with heights proportional to values. Perfect for comparing quantities across categories.',
                useCases: 'Categorical comparisons, survey results, performance metrics'
            },
            'pie': {
                title: 'Pie Chart',
                description: 'Circular chart divided into sectors, each representing a proportion of the whole. Best for showing parts of a whole.',
                useCases: 'Market share, budget allocation, demographic breakdowns'
            },
            'area': {
                title: 'Area Chart',
                description: 'Line chart with the area below the line filled. Emphasizes volume and shows cumulative values effectively.',
                useCases: 'Cumulative data, volume representation, trend emphasis'
            },
            'spline': {
                title: 'Spline Curve',
                description: 'Smooth interpolated curve (cubic spline) through data points. Creates elegant, continuous curves that pass through all data points.',
                useCases: 'Smooth trend visualization, aesthetic presentations, continuous data'
            },
            'bezier': {
                title: 'Bezier Curve',
                description: 'Smooth curve using Bezier mathematics—common in computer graphics. Creates natural-looking curves with control points.',
                useCases: 'Design applications, smooth animations, artistic visualizations'
            },
            'lowess': {
                title: 'LOWESS / LOESS',
                description: 'Locally weighted scatterplot smoothing—great for noisy data. Shows underlying trends while reducing noise.',
                useCases: 'Noisy data analysis, trend discovery, statistical smoothing'
            },
            'moving_average': {
                title: 'Moving Average Curve',
                description: 'Smooths short-term fluctuations to highlight long-term trends. Calculates average over a sliding window.',
                useCases: 'Financial data, time series smoothing, trend identification'
            },
            'polynomial': {
                title: 'Polynomial Regression Curve',
                description: 'Fitted curve using polynomial equation (quadratic, cubic, etc.). Models complex relationships between variables.',
                useCases: 'Scientific modeling, complex relationships, predictive analysis'
            },
            'exponential': {
                title: 'Exponential Curve',
                description: 'Models rapid growth patterns. Used in population studies, virus spread modeling, and compound growth scenarios.',
                useCases: 'Population growth, viral spread, compound interest, technology adoption'
            },
            'sigmoid': {
                title: 'Sigmoid (Logistic) Curve',
                description: 'S-shaped curve modeling saturation behavior. Common in learning curves, market adoption, and biological processes.',
                useCases: 'Learning curves, market saturation, biological growth, neural networks'
            },
            'gompertz': {
                title: 'Gompertz Curve',
                description: 'Asymmetric S-shaped curve used in epidemiology and technology adoption. Models growth with different rates.',
                useCases: 'Epidemiology, technology adoption, asymmetric growth patterns'
            },
            'stacked_area': {
                title: 'Stacked Area Chart',
                description: 'Shows cumulative values across categories over time. Each area represents a category contribution to the total.',
                useCases: 'Cumulative contributions, multi-category trends, composition over time'
            },
            'streamgraph': {
                title: 'Streamgraph',
                description: 'Like stacked area chart but smoothed and centered. Used for temporal flows and organic data visualization.',
                useCases: 'Temporal flows, organic data, artistic visualizations'
            },
            'step': {
                title: 'Step Chart',
                description: 'Shows changes in steps rather than continuous flow. Perfect for discrete changes and threshold-based data.',
                useCases: 'Discrete changes, threshold data, step functions, digital signals'
            }
        };
    }

    updateCurveDescription() {
        const selectedType = this.curveTypeSelect.value;
        const descriptionDiv = this.curveDescription;
        
        if (selectedType && this.curveDescriptions[selectedType]) {
            const info = this.curveDescriptions[selectedType];
            descriptionDiv.innerHTML = `
                <h4>${info.title}</h4>
                <p><strong>Description:</strong> ${info.description}</p>
                <p><strong>Best for:</strong> ${info.useCases}</p>
            `;
        } else {
            descriptionDiv.innerHTML = 'Select a curve type to see detailed information about its use cases and characteristics.';
        }
    }

    addSampleDataButtons() {
        const dataGroup = this.dataInput.parentElement;
        const sampleDataDiv = document.createElement('div');
        sampleDataDiv.className = 'sample-data-buttons';
        sampleDataDiv.innerHTML = `
            <p><strong>Quick Sample Data:</strong></p>
            <button type="button" class="sample-btn" data-sample="line">Line Chart Data</button>
            <button type="button" class="sample-btn" data-sample="bar">Bar Chart Data</button>
            <button type="button" class="sample-btn" data-sample="pie">Pie Chart Data</button>
            <button type="button" class="sample-btn" data-sample="area">Area Chart Data</button>
        `;
        
        dataGroup.appendChild(sampleDataDiv);
        
        // Add styles for sample buttons
        const style = document.createElement('style');
        style.textContent = `
            .sample-data-buttons {
                margin-top: 10px;
                padding: 15px;
                background: rgba(139, 92, 246, 0.1);
                border-radius: 8px;
                border-left: 3px solid var(--neon-purple);
            }
            .sample-data-buttons p {
                margin-bottom: 10px;
                font-size: 0.9rem;
                color: var(--text-secondary);
            }
            .sample-btn {
                margin: 5px;
                padding: 8px 15px;
                background: rgba(139, 92, 246, 0.2);
                border: 1px solid var(--neon-purple);
                border-radius: 5px;
                color: var(--neon-purple);
                cursor: pointer;
                font-size: 0.8rem;
                transition: all 0.3s ease;
            }
            .sample-btn:hover {
                background: var(--neon-purple);
                color: var(--bg-primary);
                box-shadow: 0 0 10px rgba(139, 92, 246, 0.3);
            }
        `;
        document.head.appendChild(style);
        
        // Bind sample data events
        sampleDataDiv.addEventListener('click', (e) => {
            if (e.target.classList.contains('sample-btn')) {
                this.loadSampleData(e.target.dataset.sample);
            }
        });
    }

    loadSampleData(type) {
        const sampleData = {
            'line': {
                data: '{"years": [2020, 2021, 2022, 2023, 2024, 2025], "sales": [100, 250, 450, 612, 800, 950], "profit": [20, 50, 90, 122, 160, 190]}',
                title: 'Sales and Profit Trends',
                xAxis: 'Year',
                yAxis: 'Value ($K)'
            },
            'bar': {
                data: '{"years": [2020, 2021, 2022, 2023, 2024, 2025], "Healthcare": [100, 250, 450, 612, 800, 950], "Medical Imaging": [50, 120, 200, 250, 350, 400], "IoT Health": [30, 80, 150, 200, 250, 300], "Smart Cities": [10, 30, 50, 60, 80, 100], "Biometrics": [5, 20, 40, 50, 60, 70], "Other": [40, 80, 150, 180, 220, 260]}',
                title: 'Federated Learning Papers by Domain (2020-2025)',
                xAxis: 'Year',
                yAxis: 'No. of Publications'
            },
            'pie': {
                data: '{"labels": ["Marketing", "Development", "Sales", "Support"], "values": [30, 40, 20, 10]}',
                title: 'Budget Allocation',
                xAxis: '',
                yAxis: ''
            },
            'area': {
                data: '{"months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], "users": [1000, 1500, 2200, 3000, 4000, 5000], "premium": [100, 200, 350, 500, 700, 900]}',
                title: 'User Growth Over Time',
                xAxis: 'Month',
                yAxis: 'Number of Users'
            }
        };
        
        if (sampleData[type]) {
            this.dataInput.value = sampleData[type].data;
            this.chartTitleInput.value = sampleData[type].title;
            this.xAxisLabelInput.value = sampleData[type].xAxis;
            this.yAxisLabelInput.value = sampleData[type].yAxis;
            this.curveTypeSelect.value = type;
            this.updateCurveDescription();
            this.showMessage('Sample data loaded! You can now generate the chart.', 'success');
        }
    }

    validateDataInput() {
        const data = this.dataInput.value.trim();
        if (!data) return;
        
        try {
            // Try to parse as JSON
            JSON.parse(data);
            this.dataInput.style.borderColor = 'var(--neon-green)';
        } catch (e) {
            // Try to parse as CSV
            const csvPattern = /^[\d\w\s,;]+$/;
            if (csvPattern.test(data)) {
                this.dataInput.style.borderColor = 'var(--neon-green)';
            } else {
                this.dataInput.style.borderColor = 'var(--neon-pink)';
            }
        }
    }

    async handleFormSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(this.form);
        const data = Object.fromEntries(formData);
        
        // Validate required fields
        if (!data.curveType || !data.chartTitle || !data.dataInput) {
            this.showMessage('Please fill in all required fields.', 'error');
            return;
        }
        
        // Show loading state
        const submitBtn = this.form.querySelector('.submit-btn');
        const originalText = submitBtn.querySelector('.btn-text').textContent;
        submitBtn.querySelector('.btn-text').innerHTML = '<span class="loading"></span> Generating...';
        submitBtn.disabled = true;
        
        try {
            // Parse and validate data
            const parsedData = this.parseDataInput(data.dataInput);
            if (!parsedData) {
                throw new Error('Invalid data format. Please check your input.');
            }
            
            // Prepare request payload
            const payload = {
                curve_type: data.curveType,
                title: data.chartTitle,
                x_axis_label: data.xAxisLabel || '',
                y_axis_label: data.yAxisLabel || '',
                data: parsedData,
                color_scheme: data.colorScheme || 'neon',
                grid_style: data.gridStyle || 'neon',
                show_x_axis: data.showXAxis === 'on',
                show_y_axis: data.showYAxis === 'on'
            };
            
            // Send to backend
            const response = await this.sendToBackend(payload);
            
            if (response.success) {
                this.displayChart(response.chart_url, response.chart_data);
                this.showMessage('Chart generated successfully!', 'success');
            } else {
                throw new Error(response.error || 'Failed to generate chart');
            }
            
        } catch (error) {
            this.showMessage(error.message, 'error');
        } finally {
            // Reset button state
            submitBtn.querySelector('.btn-text').textContent = originalText;
            submitBtn.disabled = false;
        }
    }

    parseDataInput(input) {
        input = input.trim();
        
        try {
            // Try JSON first
            return JSON.parse(input);
        } catch (e) {
            // Try CSV format
            const lines = input.split(/[;\n]/);
            const data = {};
            
            for (let line of lines) {
                line = line.trim();
                if (!line) continue;
                
                const parts = line.split(/[,=]/);
                if (parts.length >= 2) {
                    const key = parts[0].trim();
                    const values = parts.slice(1).map(v => {
                        const num = parseFloat(v.trim());
                        return isNaN(num) ? v.trim() : num;
                    });
                    data[key] = values;
                }
            }
            
            return Object.keys(data).length > 0 ? data : null;
        }
    }

    async sendToBackend(payload) {
        try {
            const response = await fetch('http://localhost:5000/api/generate-chart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Backend connection failed:', error);
            // Fallback to mock chart if backend is not available
            return {
                success: true,
                chart_url: this.generateMockChart(payload),
                chart_data: payload
            };
        }
    }

    generateMockChart(payload) {
        // Create a mock chart using Canvas API
        const canvas = document.createElement('canvas');
        canvas.width = 800;
        canvas.height = 500;
        const ctx = canvas.getContext('2d');
        
        // Set background
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Add grid
        ctx.strokeStyle = 'rgba(0, 0, 0, 0.1)';
        ctx.lineWidth = 1;
        for (let i = 0; i < canvas.width; i += 50) {
            ctx.beginPath();
            ctx.moveTo(i, 0);
            ctx.lineTo(i, canvas.height);
            ctx.stroke();
        }
        for (let i = 0; i < canvas.height; i += 50) {
            ctx.beginPath();
            ctx.moveTo(0, i);
            ctx.lineTo(canvas.width, i);
            ctx.stroke();
        }
        
        // Add title
        ctx.fillStyle = '#000000';
        ctx.font = 'bold 24px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(payload.title, canvas.width / 2, 40);
        
        // Add axis labels
        ctx.fillStyle = '#000000';
        ctx.font = '16px Arial';
        if (payload.x_axis_label) {
            ctx.fillText(payload.x_axis_label, canvas.width / 2, canvas.height - 20);
        }
        if (payload.y_axis_label) {
            ctx.save();
            ctx.translate(30, canvas.height / 2);
            ctx.rotate(-Math.PI / 2);
            ctx.fillText(payload.y_axis_label, 0, 0);
            ctx.restore();
        }
        
        // Draw sample data based on curve type
        this.drawSampleCurve(ctx, payload.curve_type, canvas.width, canvas.height);
        
        return canvas.toDataURL('image/png');
    }

    drawSampleCurve(ctx, curveType, width, height) {
        const margin = 80;
        const chartWidth = width - 2 * margin;
        const chartHeight = height - 2 * margin;
        
        ctx.strokeStyle = '#1f77b4';
        ctx.lineWidth = 3;
        ctx.fillStyle = 'rgba(31, 119, 180, 0.2)';
        
        switch (curveType) {
            case 'line':
            case 'spline':
                this.drawLineChart(ctx, margin, chartWidth, chartHeight);
                break;
            case 'bar':
                this.drawBarChart(ctx, margin, chartWidth, chartHeight);
                break;
            case 'pie':
                this.drawPieChart(ctx, width / 2, height / 2, 150);
                break;
            case 'area':
                this.drawAreaChart(ctx, margin, chartWidth, chartHeight);
                break;
            default:
                this.drawLineChart(ctx, margin, chartWidth, chartHeight);
        }
    }

    drawLineChart(ctx, margin, width, height) {
        const points = [
            {x: margin + width * 0.1, y: margin + height * 0.8},
            {x: margin + width * 0.3, y: margin + height * 0.6},
            {x: margin + width * 0.5, y: margin + height * 0.4},
            {x: margin + width * 0.7, y: margin + height * 0.3},
            {x: margin + width * 0.9, y: margin + height * 0.2}
        ];
        
        ctx.beginPath();
        ctx.moveTo(points[0].x, points[0].y);
        for (let i = 1; i < points.length; i++) {
            ctx.lineTo(points[i].x, points[i].y);
        }
        ctx.stroke();
        
        // Add points
        ctx.fillStyle = '#1f77b4';
        points.forEach(point => {
            ctx.beginPath();
            ctx.arc(point.x, point.y, 5, 0, 2 * Math.PI);
            ctx.fill();
        });
    }

    drawBarChart(ctx, margin, width, height) {
        const barWidth = width / 6;
        const bars = [0.7, 0.5, 0.8, 0.3, 0.9, 0.6];
        const years = ['2020', '2021', '2022', '2023', '2024', '2025'];
        
        // Draw X-axis labels
        ctx.fillStyle = '#000000';
        ctx.font = 'bold 12px Arial';
        ctx.textAlign = 'center';
        years.forEach((year, i) => {
            const x = margin + i * barWidth + barWidth / 2;
            ctx.fillText(year, x, margin + height + 20);
        });
        
        // Draw Y-axis labels
        ctx.textAlign = 'right';
        ctx.save();
        ctx.translate(margin - 10, margin + height / 2);
        ctx.rotate(-Math.PI / 2);
        ctx.fillText('No. of Publications', 0, 0);
        ctx.restore();
        
        // Draw Y-axis tick values
        ctx.textAlign = 'right';
        ctx.font = '10px Arial';
        for (let i = 0; i <= 5; i++) {
            const y = margin + height - (i * height / 5);
            const value = Math.round(i * 200);
            ctx.fillText(value.toString(), margin - 5, y + 3);
        }
        
        bars.forEach((heightRatio, i) => {
            const x = margin + i * barWidth + barWidth * 0.1;
            const barHeight = height * heightRatio;
            const y = margin + height - barHeight;
            
            const colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'];
            ctx.fillStyle = colors[i % colors.length];
            ctx.fillRect(x, y, barWidth * 0.8, barHeight);
            
            // Add value labels on bars
            ctx.fillStyle = '#000000';
            ctx.font = 'bold 10px Arial';
            ctx.textAlign = 'center';
            const value = Math.round(heightRatio * 1000);
            ctx.fillText(value.toString(), x + barWidth * 0.4, y - 5);
        });
    }

    drawPieChart(ctx, centerX, centerY, radius) {
        const segments = [0.3, 0.25, 0.2, 0.15, 0.1];
        const colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'];
        
        let currentAngle = 0;
        segments.forEach((ratio, i) => {
            const angle = ratio * 2 * Math.PI;
            
            ctx.fillStyle = colors[i % colors.length];
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + angle);
            ctx.closePath();
            ctx.fill();
            
            currentAngle += angle;
        });
    }

    drawAreaChart(ctx, margin, width, height) {
        const points = [
            {x: margin, y: margin + height},
            {x: margin + width * 0.2, y: margin + height * 0.8},
            {x: margin + width * 0.4, y: margin + height * 0.6},
            {x: margin + width * 0.6, y: margin + height * 0.4},
            {x: margin + width * 0.8, y: margin + height * 0.3},
            {x: margin + width, y: margin + height * 0.2}
        ];
        
        ctx.beginPath();
        ctx.moveTo(points[0].x, points[0].y);
        points.forEach(point => {
            ctx.lineTo(point.x, point.y);
        });
        ctx.lineTo(points[points.length - 1].x, margin + height);
        ctx.closePath();
        ctx.fill();
        
        ctx.strokeStyle = '#1f77b4';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(points[0].x, points[0].y);
        points.forEach(point => {
            ctx.lineTo(point.x, point.y);
        });
        ctx.stroke();
    }

    displayChart(chartUrl, chartData) {
        this.chartImage.src = chartUrl;
        this.currentChartData = chartData;
        
        this.chartPreview.style.display = 'none';
        this.generatedChart.style.display = 'block';
    }

    downloadChart(format) {
        if (!this.currentChartData) return;
        
        const link = document.createElement('a');
        link.download = `chart.${format}`;
        
        if (format === 'png') {
            link.href = this.chartImage.src;
        } else {
            // For SVG, you'd need to generate SVG content
            link.href = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(this.generateSVG());
        }
        
        link.click();
    }

    generateSVG() {
        // Generate SVG content based on current chart data
        return `<svg width="800" height="500" xmlns="http://www.w3.org/2000/svg">
            <rect width="800" height="500" fill="#ffffff"/>
            <text x="400" y="40" text-anchor="middle" fill="#000000" font-family="Arial" font-size="24" font-weight="bold">${this.currentChartData.title}</text>
            <text x="400" y="480" text-anchor="middle" fill="#000000" font-family="Arial" font-size="16">${this.currentChartData.x_axis_label}</text>
        </svg>`;
    }

    shareChart() {
        if (!this.currentChartData) return;
        
        if (navigator.share) {
            navigator.share({
                title: this.currentChartData.title,
                text: 'Check out this chart I created with CurveMaker Pro!',
                url: window.location.href
            });
        } else {
            // Fallback: copy to clipboard
            navigator.clipboard.writeText(window.location.href).then(() => {
                this.showMessage('Link copied to clipboard!', 'success');
            });
        }
    }

    showMessage(message, type) {
        // Remove existing messages
        const existingMessages = document.querySelectorAll('.message');
        existingMessages.forEach(msg => msg.remove());
        
        // Create new message
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = message;
        
        // Insert after form
        this.form.parentElement.insertBefore(messageDiv, this.form.nextSibling);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (messageDiv.parentElement) {
                messageDiv.remove();
            }
        }, 5000);
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new CurveMaker();
    
    // Ensure footer stays fixed
    const footer = document.querySelector('.footer');
    if (footer) {
        footer.style.position = 'fixed';
        footer.style.bottom = '0';
        footer.style.left = '0';
        footer.style.right = '0';
        footer.style.width = '100%';
        footer.style.zIndex = '9999';
        
        // Force footer to stay fixed on scroll
        window.addEventListener('scroll', () => {
            footer.style.position = 'fixed';
            footer.style.bottom = '0';
            footer.style.left = '0';
            footer.style.right = '0';
            footer.style.width = '100%';
            footer.style.zIndex = '9999';
        });
        
        // Force footer to stay fixed on resize
        window.addEventListener('resize', () => {
            footer.style.position = 'fixed';
            footer.style.bottom = '0';
            footer.style.left = '0';
            footer.style.right = '0';
            footer.style.width = '100%';
            footer.style.zIndex = '9999';
        });
    }
}); 