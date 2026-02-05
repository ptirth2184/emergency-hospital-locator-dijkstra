# 🚑 Smart Emergency Hospital Locator using Dijkstra Algorithm

A modern, interactive Streamlit application that demonstrates the real-world application of Dijkstra's shortest path algorithm for emergency hospital routing. This college-level Data Structures & Algorithms project simulates a mini Google Maps emergency routing system.

## 🎯 Project Overview

This application creates an interactive system where:
- A person appears on a city map/grid
- Multiple hospitals are strategically placed
- Roads connect locations with realistic distances (weights)
- Dijkstra's algorithm finds the nearest hospital and optimal route
- Visual path highlighting shows the emergency route

## ✨ Key Features

### 🖥️ Modern UI Components
- **Interactive Control Panel**: Adjust hospitals, map complexity
- **Real-time Map Visualization**: Dynamic graph rendering with matplotlib
- **Step-by-step Route Display**: Clear path from location to nearest hospital
- **Distance Analysis**: Complete distance table to all hospitals
- **Algorithm Explanation**: Built-in educational content for viva preparation

### 🧠 Algorithm Implementation
- **Custom Dijkstra Implementation**: Manual implementation using heapq
- **Graph Generation**: Dynamic city-like road networks
- **Weighted Edges**: Realistic distances between locations
- **Path Reconstruction**: Complete route tracking and display

### 🎨 Visual Features
- **Color-coded Nodes**: Green (person), Red (hospitals), Blue (locations)
- **Path Highlighting**: Red thick lines show optimal route
- **Distance Labels**: Edge weights displayed on map
- **Interactive Legend**: Clear node type identification

## 🚀 Installation & Setup

### Prerequisites
```bash
pip install streamlit networkx matplotlib
```

### Running the Application
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 🎮 How to Use

1. **Generate Map**: Click "Generate New Map" to create a random city layout
2. **Adjust Settings**: 
   - Select number of hospitals (3-6)
   - Choose map complexity (simple/medium/complex)
3. **Find Route**: Click "Start Emergency Routing" to run Dijkstra's algorithm
4. **View Results**: See the nearest hospital, distance, and complete route
5. **Reset**: Use "Reset" button to start over

## 🏗️ Technical Architecture

### Core Components

#### 1. EmergencyHospitalLocator Class
```python
- generate_city_graph(): Creates realistic road networks
- dijkstra_algorithm(): Implements shortest path finding
- find_nearest_hospital(): Identifies optimal emergency route
- visualize_graph(): Renders interactive map visualization
```

#### 2. Graph Structure
- **Nodes**: Locations, hospitals, and person position
- **Edges**: Weighted roads with realistic distances (1-15 km)
- **Connectivity**: Ensures all hospitals are reachable

#### 3. Algorithm Implementation
- **Priority Queue**: Using Python's heapq for efficient node selection
- **Distance Tracking**: Maintains shortest distances to all nodes
- **Path Reconstruction**: Builds complete route from start to destination

## 📊 Algorithm Analysis

### Time Complexity: O(E log V)
- **E**: Number of edges (roads)
- **V**: Number of vertices (locations)
- **log V**: Priority queue operations

### Space Complexity: O(V)
- Distance and previous node dictionaries
- Priority queue storage

### Why Dijkstra?
- **Optimal Solution**: Guarantees shortest path for weighted graphs
- **Real-world Applicable**: Handles varying road distances
- **Efficient**: Better than brute force approaches

## 🎓 Educational Value

### Viva Preparation Topics
1. **Algorithm Explanation**: Step-by-step Dijkstra process
2. **Complexity Analysis**: Time and space complexity breakdown
3. **Real-world Applications**: GPS, emergency services, network routing
4. **Comparison**: Dijkstra vs BFS vs DFS
5. **Data Structures**: Graphs, priority queues, hash tables

### Learning Outcomes
- Understanding weighted graph algorithms
- Priority queue implementation and usage
- Graph visualization techniques
- Real-world algorithm applications
- UI development with Streamlit

## 🔧 Customization Options

### Map Complexity Levels
- **Simple**: 8 nodes, 12 connections
- **Medium**: 12 nodes, 18 connections  
- **Complex**: 16 nodes, 25 connections

### Hospital Configuration
- Adjustable number of hospitals (3-6)
- Random placement ensuring connectivity
- Realistic naming convention

### Visual Customization
- Node colors and sizes
- Edge styling and labels
- Path highlighting options
- Legend and layout settings

## 🌟 Advanced Features

### Animation & Feedback
- Loading animations during algorithm execution
- Step-by-step algorithm explanation
- Real-time distance calculations

### Comparison Analysis
- Distance to all hospitals table
- Algorithm complexity display
- Educational content integration

## 📱 Responsive Design

- **Wide Layout**: Optimized for desktop viewing
- **Sidebar Controls**: Organized control panel
- **Column Layout**: Map and results side-by-side
- **Mobile Friendly**: Responsive design elements

## 🎯 Project Evaluation Criteria

### Technical Implementation (40%)
- ✅ Correct Dijkstra implementation
- ✅ Efficient graph generation
- ✅ Proper data structure usage
- ✅ Error handling and edge cases

### User Interface (30%)
- ✅ Modern, attractive design
- ✅ Intuitive navigation
- ✅ Clear result presentation
- ✅ Interactive controls

### Educational Value (20%)
- ✅ Algorithm explanation
- ✅ Complexity analysis
- ✅ Real-world applications
- ✅ Viva preparation content

### Code Quality (10%)
- ✅ Clean, readable code
- ✅ Proper documentation
- ✅ Modular structure
- ✅ Best practices

## 🚀 Future Enhancements

- **Multiple Algorithm Comparison**: A*, Bellman-Ford
- **Real Map Integration**: OpenStreetMap data
- **Traffic Simulation**: Dynamic edge weights
- **Multi-destination Routing**: Visiting multiple hospitals
- **Performance Metrics**: Algorithm execution timing

## 📝 License

This project is created for educational purposes as part of college Data Structures & Algorithms coursework.

## 🤝 Contributing

This is a college project, but suggestions and improvements are welcome for educational enhancement.

---

**Created for**: College DSA Project Demonstration  
**Algorithm**: Dijkstra's Shortest Path  
**Technology Stack**: Python, Streamlit, NetworkX, Matplotlib  
**Purpose**: Emergency Hospital Routing System