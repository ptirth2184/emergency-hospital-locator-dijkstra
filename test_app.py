#!/usr/bin/env python3
"""
Test script to verify the Emergency Hospital Locator application works correctly.
Run this before your presentation to ensure everything is functioning.
"""

import sys
import importlib.util

def test_imports():
    """Test if all required libraries are installed"""
    print("🔍 Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError:
        print("❌ Streamlit not found. Run: pip install streamlit")
        return False
    
    try:
        import networkx as nx
        print("✅ NetworkX imported successfully")
    except ImportError:
        print("❌ NetworkX not found. Run: pip install networkx")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✅ Matplotlib imported successfully")
    except ImportError:
        print("❌ Matplotlib not found. Run: pip install matplotlib")
        return False
    
    return True

def test_app_syntax():
    """Test if the main app file has correct syntax"""
    print("\n🔍 Testing app.py syntax...")
    
    try:
        spec = importlib.util.spec_from_file_location("app", "app.py")
        app_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_module)
        print("✅ app.py syntax is correct")
        return True
    except Exception as e:
        print(f"❌ Syntax error in app.py: {e}")
        return False

def test_core_functionality():
    """Test core algorithm functionality"""
    print("\n🔍 Testing core functionality...")
    
    try:
        # Import the app module
        spec = importlib.util.spec_from_file_location("app", "app.py")
        app_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_module)
        
        # Test EmergencyHospitalLocator class
        locator = app_module.EmergencyHospitalLocator()
        
        # Test graph generation
        locator.generate_city_graph(4, 'medium')
        print("✅ Graph generation works")
        
        # Test Dijkstra algorithm
        result = locator.find_nearest_hospital()
        if result and 'nearest_hospital' in result:
            print("✅ Dijkstra algorithm works")
            print(f"   Found nearest hospital: {result['nearest_hospital'][1]}")
            print(f"   Distance: {result['distance']:.1f} km")
        else:
            print("❌ Dijkstra algorithm failed")
            return False
        
        # Test visualization
        fig = locator.visualize_graph()
        print("✅ Graph visualization works")
        
        return True
        
    except Exception as e:
        print(f"❌ Core functionality error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚑 Emergency Hospital Locator - Test Suite")
    print("=" * 50)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test syntax
    if not test_app_syntax():
        all_passed = False
    
    # Test functionality
    if not test_core_functionality():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Your application is ready for presentation.")
        print("\n📋 To run the application:")
        print("   streamlit run app.py")
    else:
        print("❌ Some tests failed. Please fix the issues before presenting.")
        sys.exit(1)

if __name__ == "__main__":
    main()