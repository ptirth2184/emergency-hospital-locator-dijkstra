import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import time
from collections import defaultdict
import heapq

# Set page configuration
st.set_page_config(
    page_title="🚑 Smart Emergency Hospital Locator",
    page_icon="🚑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme styling
st.markdown("""
<style>
    .stApp {
        background-color: #2E2E2E;
        color: #FFFFFF;
    }
    
    .main-header {
        font-size: 2.5rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .result-box {
        background-color: #3A3A3A;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #FF6B6B;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        border: 1px solid #4A4A4A;
        color: #FFFFFF;
    }
    
    .info-box {
        background-color: #3A3A3A;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #4ECDC4;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        border: 1px solid #4A4A4A;
        color: #FFFFFF;
    }
    
    .success-box {
        background-color: #3A3A3A;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #FFE66D;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        border: 1px solid #4A4A4A;
        color: #FFFFFF;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1E1E1E;
    }
    
    /* Main content area */
    .css-18e3th9 {
        background-color: #2E2E2E;
    }
    
    /* Text color overrides */
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #FF6B6B;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background-color: #FF5252;
        box-shadow: 0 4px 8px rgba(255, 107, 107, 0.3);
    }
    
    /* Selectbox and input styling */
    .stSelectbox > div > div {
        background-color: #3A3A3A;
        color: #FFFFFF;
        border: 1px solid #4A4A4A;
    }
    
    /* Table styling */
    .stTable {
        background-color: #3A3A3A;
        color: #FFFFFF;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #3A3A3A;
        color: #FFFFFF;
        border: 1px solid #4A4A4A;
    }
    
    .streamlit-expanderContent {
        background-color: #3A3A3A;
        color: #FFFFFF;
        border: 1px solid #4A4A4A;
    }
</style>
""", unsafe_allow_html=True)

class EmergencyHospitalLocator:
    def __init__(self):
        self.graph = nx.Graph()
        self.person_location = None
        self.hospitals = []
        self.all_locations = []
        self.shortest_paths = {}
        self.distances = {}
        
    def generate_city_graph(self, num_hospitals, complexity):
        """Generate a realistic city-like graph with roads and locations"""
        self.graph.clear()
        self.hospitals = []
        self.all_locations = []
        
        # Define complexity parameters
        complexity_params = {
            'simple': {'nodes': 8, 'connections': 12},
            'medium': {'nodes': 12, 'connections': 18},
            'complex': {'nodes': 16, 'connections': 25}
        }
        
        total_nodes = complexity_params[complexity]['nodes']
        total_connections = complexity_params[complexity]['connections']
        
        # Generate location names
        location_names = [
            'Central Square', 'Park Avenue', 'Main Street', 'Downtown',
            'Riverside', 'Hillview', 'Market Place', 'University Area',
            'Industrial Zone', 'Residential Area', 'Shopping Mall', 'Airport Road',
            'Business District', 'Old Town', 'New City', 'Suburb'
        ]
        
        hospital_names = [
            'City General Hospital', 'Emergency Medical Center', 'St. Mary Hospital',
            'Regional Medical Center', 'Community Hospital', 'Trauma Center'
        ]
        
        # Create nodes
        for i in range(total_nodes):
            location_name = location_names[i % len(location_names)]
            self.graph.add_node(i, name=location_name, type='location')
            self.all_locations.append((i, location_name))
        
        # Designate hospitals
        hospital_indices = random.sample(range(1, total_nodes), num_hospitals)
        for i, hospital_idx in enumerate(hospital_indices):
            hospital_name = hospital_names[i % len(hospital_names)]
            self.graph.nodes[hospital_idx]['name'] = hospital_name
            self.graph.nodes[hospital_idx]['type'] = 'hospital'
            self.hospitals.append((hospital_idx, hospital_name))
        
        # Set person location (always at node 0)
        self.person_location = (0, 'Your Location')
        self.graph.nodes[0]['name'] = 'Your Location'
        self.graph.nodes[0]['type'] = 'person'
        
        # Create realistic road connections with distances
        edges_added = 0
        attempts = 0
        max_attempts = total_connections * 3
        
        while edges_added < total_connections and attempts < max_attempts:
            node1 = random.randint(0, total_nodes - 1)
            node2 = random.randint(0, total_nodes - 1)
            
            if node1 != node2 and not self.graph.has_edge(node1, node2):
                # Generate realistic distance (1-15 km)
                distance = round(random.uniform(1.0, 15.0), 1)
                self.graph.add_edge(node1, node2, weight=distance)
                edges_added += 1
            
            attempts += 1
        
        # Ensure all nodes are connected (especially hospitals)
        if not nx.is_connected(self.graph):
            components = list(nx.connected_components(self.graph))
            for i in range(len(components) - 1):
                node1 = random.choice(list(components[i]))
                node2 = random.choice(list(components[i + 1]))
                distance = round(random.uniform(2.0, 8.0), 1)
                self.graph.add_edge(node1, node2, weight=distance)
    
    def dijkstra_algorithm(self, start_node):
        """
        Implement Dijkstra's Algorithm to find shortest paths
        Returns: distances dictionary and previous nodes dictionary
        """
        # Initialize distances and previous nodes
        distances = {node: float('infinity') for node in self.graph.nodes()}
        previous = {node: None for node in self.graph.nodes()}
        distances[start_node] = 0
        
        # Priority queue: (distance, node)
        pq = [(0, start_node)]
        visited = set()
        
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            if current_node in visited:
                continue
                
            visited.add(current_node)
            
            # Check all neighbors
            for neighbor in self.graph.neighbors(current_node):
                if neighbor not in visited:
                    edge_weight = self.graph[current_node][neighbor]['weight']
                    new_distance = current_distance + edge_weight
                    
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        previous[neighbor] = current_node
                        heapq.heappush(pq, (new_distance, neighbor))
        
        return distances, previous
    
    def get_shortest_path(self, previous, start, end):
        """Reconstruct shortest path from previous nodes dictionary"""
        path = []
        current = end
        
        while current is not None:
            path.append(current)
            current = previous[current]
        
        path.reverse()
        return path if path[0] == start else []
    
    def find_nearest_hospital(self):
        """Find the nearest hospital using Dijkstra's algorithm"""
        person_node = self.person_location[0]
        
        # Run Dijkstra's algorithm
        distances, previous = self.dijkstra_algorithm(person_node)
        
        # Find nearest hospital
        nearest_hospital = None
        min_distance = float('infinity')
        
        for hospital_node, hospital_name in self.hospitals:
            if distances[hospital_node] < min_distance:
                min_distance = distances[hospital_node]
                nearest_hospital = (hospital_node, hospital_name)
        
        # Get shortest path to nearest hospital
        if nearest_hospital:
            shortest_path = self.get_shortest_path(previous, person_node, nearest_hospital[0])
            
            # Store results
            self.distances = distances
            self.shortest_paths = previous
            
            return {
                'nearest_hospital': nearest_hospital,
                'distance': min_distance,
                'path': shortest_path,
                'all_hospital_distances': {name: distances[node] for node, name in self.hospitals}
            }
        
        return None
    
    def visualize_graph(self, highlight_path=None):
        """Create an attractive dark-themed visualization of the graph"""
        plt.figure(figsize=(14, 10))
        plt.style.use('dark_background')  # Use dark matplotlib theme
        
        # Create layout
        pos = nx.spring_layout(self.graph, k=3, iterations=50, seed=42)
        
        # Draw all edges (roads) in light gray
        nx.draw_networkx_edges(self.graph, pos, edge_color='#CCCCCC', 
                              width=2, alpha=0.7)
        
        # Draw edge labels (distances)
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        edge_labels = {k: f"{v} km" for k, v in edge_labels.items()}
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels, 
                                    font_size=8, font_color='#FFFFFF')
        
        # Draw nodes with different colors based on type
        node_colors = []
        node_sizes = []
        
        for node in self.graph.nodes():
            node_type = self.graph.nodes[node].get('type', 'location')
            if node_type == 'person':
                node_colors.append('#4ECDC4')  # Teal for person
                node_sizes.append(800)
            elif node_type == 'hospital':
                node_colors.append('#FF6B6B')  # Coral red for hospitals
                node_sizes.append(600)
            else:
                node_colors.append('#95A5A6')  # Light gray for other locations
                node_sizes.append(400)
        
        nx.draw_networkx_nodes(self.graph, pos, node_color=node_colors, 
                              node_size=node_sizes, alpha=0.9, edgecolors='white', linewidths=2)
        
        # Draw node labels
        labels = {node: self.graph.nodes[node]['name'][:15] + '...' 
                 if len(self.graph.nodes[node]['name']) > 15 
                 else self.graph.nodes[node]['name'] 
                 for node in self.graph.nodes()}
        
        nx.draw_networkx_labels(self.graph, pos, labels, font_size=8, 
                               font_weight='bold', font_color='white')
        
        # Highlight shortest path if provided
        if highlight_path and len(highlight_path) > 1:
            path_edges = [(highlight_path[i], highlight_path[i+1]) 
                         for i in range(len(highlight_path)-1)]
            nx.draw_networkx_edges(self.graph, pos, edgelist=path_edges, 
                                  edge_color='#FFE66D', width=5, alpha=1.0)
        
        # Add legend with dark theme colors
        legend_elements = [
            patches.Patch(color='#4ECDC4', label='👤 Your Location'),
            patches.Patch(color='#FF6B6B', label='🏥 Hospitals'),
            patches.Patch(color='#95A5A6', label='📍 Other Locations'),
            patches.Patch(color='#FFE66D', label='🛣️ Shortest Path')
        ]
        plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1),
                  facecolor='#2E2E2E', edgecolor='white', labelcolor='white')
        
        plt.title("🗺️ Emergency Hospital Locator Map", fontsize=16, fontweight='bold', color='white')
        plt.axis('off')
        
        # Set dark background
        plt.gca().set_facecolor('#2E2E2E')
        plt.gcf().patch.set_facecolor('#2E2E2E')
        
        plt.tight_layout()
        
        return plt

def main():
    # Initialize session state
    if 'locator' not in st.session_state:
        st.session_state.locator = EmergencyHospitalLocator()
        st.session_state.map_generated = False
        st.session_state.route_calculated = False
        st.session_state.result = None
    
    # Main header
    st.markdown('<h1 class="main-header">🚑 Smart Emergency Hospital Locator using Dijkstra Algorithm</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar controls
    st.sidebar.header("🎛️ Control Panel")
    
    # Location selector (for future enhancement)
    st.sidebar.subheader("📍 Your Location")
    st.sidebar.info("Your current location is set to: **Your Location**")
    
    # Hospital settings
    st.sidebar.subheader("🏥 Hospital Settings")
    num_hospitals = st.sidebar.slider("Number of Hospitals", 3, 6, 4)
    
    # Map complexity
    st.sidebar.subheader("🗺️ Map Complexity")
    complexity = st.sidebar.selectbox("Select Complexity", 
                                     ['simple', 'medium', 'complex'], 
                                     index=1)
    
    # Control buttons
    st.sidebar.subheader("🎮 Controls")
    
    if st.sidebar.button("🔄 Generate New Map", type="primary"):
        st.session_state.locator.generate_city_graph(num_hospitals, complexity)
        st.session_state.map_generated = True
        st.session_state.route_calculated = False
        st.session_state.result = None
        st.rerun()
    
    if st.sidebar.button("🚑 Start Emergency Routing", type="secondary", 
                        disabled=not st.session_state.map_generated):
        with st.spinner("🔍 Calculating shortest path using Dijkstra Algorithm..."):
            time.sleep(2)  # Simulation delay
            st.session_state.result = st.session_state.locator.find_nearest_hospital()
            st.session_state.route_calculated = True
        st.rerun()
    
    if st.sidebar.button("🔄 Reset", type="secondary"):
        st.session_state.map_generated = False
        st.session_state.route_calculated = False
        st.session_state.result = None
        st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🗺️ Interactive Map")
        
        if st.session_state.map_generated:
            # Show map with or without highlighted path
            highlight_path = None
            if st.session_state.route_calculated and st.session_state.result:
                highlight_path = st.session_state.result['path']
            
            fig = st.session_state.locator.visualize_graph(highlight_path)
            st.pyplot(fig)
            plt.close()
        else:
            st.info("👆 Click 'Generate New Map' to create a new city map with hospitals!")
    
    with col2:
        st.subheader("📊 Results & Information")
        
        if st.session_state.route_calculated and st.session_state.result:
            result = st.session_state.result
            
            # Main result box
            st.markdown(f"""
            <div class="result-box">
                <h3>🚑 Emergency Route Found!</h3>
                <p><strong>🏥 Nearest Hospital:</strong> {result['nearest_hospital'][1]}</p>
                <p><strong>📏 Total Distance:</strong> {result['distance']:.1f} km</p>
                <p><strong>🛣️ Route:</strong></p>
                <ul>
            """, unsafe_allow_html=True)
            
            # Show step-by-step path
            path_names = []
            for node in result['path']:
                node_name = st.session_state.locator.graph.nodes[node]['name']
                path_names.append(node_name)
            
            for i, location in enumerate(path_names):
                if i == 0:
                    st.markdown(f"<li>🚀 Start: {location}</li>", unsafe_allow_html=True)
                elif i == len(path_names) - 1:
                    st.markdown(f"<li>🏥 Destination: {location}</li>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<li>➡️ Via: {location}</li>", unsafe_allow_html=True)
            
            st.markdown("</ul></div>", unsafe_allow_html=True)
            
            # Distance to all hospitals table
            st.subheader("📋 All Hospital Distances")
            hospital_data = []
            for hospital_name, distance in result['all_hospital_distances'].items():
                status = "🎯 NEAREST" if hospital_name == result['nearest_hospital'][1] else ""
                hospital_data.append({
                    "Hospital": hospital_name,
                    "Distance (km)": f"{distance:.1f}",
                    "Status": status
                })
            
            st.table(hospital_data)
        
        elif st.session_state.map_generated:
            st.markdown("""
            <div class="info-box">
                <h4>🎯 Ready for Emergency Routing!</h4>
                <p>Map generated successfully. Click <strong>'Start Emergency Routing'</strong> to find the nearest hospital using Dijkstra's algorithm.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Algorithm information
        st.subheader("🧠 Algorithm Information")
        
        with st.expander("📚 About Dijkstra's Algorithm"):
            st.markdown("""
            **What is Dijkstra's Algorithm?**
            - A graph search algorithm that finds the shortest path between nodes
            - Uses a greedy approach with a priority queue
            - Guarantees the optimal solution for non-negative edge weights
            
            **Why use Dijkstra here?**
            - Perfect for finding shortest routes in road networks
            - Handles weighted edges (distances between locations)
            - More efficient than exploring all possible paths
            
            **Time Complexity:** O(E log V)
            - E = number of edges (roads)
            - V = number of vertices (locations)
            
            **Real-life Applications:**
            - GPS Navigation systems (Google Maps, Waze)
            - Network routing protocols
            - Flight path optimization
            - Emergency services routing
            
            **Difference from BFS/DFS:**
            - BFS: Finds shortest path in unweighted graphs only
            - DFS: Doesn't guarantee shortest path
            - Dijkstra: Finds shortest path in weighted graphs
            """)
        
        with st.expander("🔬 Step-by-step Process"):
            if st.session_state.route_calculated:
                st.markdown("""
                **Dijkstra's Algorithm Steps:**
                1. **Initialize:** Set distance to start = 0, all others = ∞
                2. **Priority Queue:** Add start node to queue
                3. **Visit:** Remove node with minimum distance
                4. **Update:** Check all neighbors, update distances if shorter path found
                5. **Repeat:** Until all nodes visited or destination reached
                6. **Result:** Shortest path and distance found!
                """)
            else:
                st.info("Run the algorithm to see step-by-step explanation!")

if __name__ == "__main__":
    main()

