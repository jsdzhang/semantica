#!/usr/bin/env python3
"""Fix remaining notebooks with calculate_centrality calls"""

import json
import os

# List of notebooks to fix
notebooks = [
    "cookbook/use_cases/trading/01_Market_Data_Analysis.ipynb",
    "cookbook/use_cases/trading/03_Real_Time_Monitoring.ipynb",
    "cookbook/use_cases/trading/05_Strategy_Backtesting.ipynb",
    "cookbook/use_cases/healthcare/02_Disease_Network_Analysis.ipynb",
    "cookbook/use_cases/healthcare/03_Drug_Interactions_Analysis.ipynb",
    "cookbook/use_cases/renewable_energy/01_Energy_Market_Analysis.ipynb",
    "cookbook/use_cases/renewable_energy/03_Grid_Management.ipynb",
    "cookbook/use_cases/finance/01_Financial_Data_Integration.ipynb",
    "cookbook/use_cases/finance/02_Financial_Reports_Analysis.ipynb",
    "cookbook/use_cases/cybersecurity/01_Anomaly_Detection_Real_Time.ipynb",
    "cookbook/use_cases/cybersecurity/02_Incident_Analysis.ipynb",
    "cookbook/use_cases/supply_chain/01_Supply_Chain_Data_Integration.ipynb",
]

old_pattern = 'calculate_centrality('
new_code = [
    'centrality_result = centrality_calculator.calculate_degree_centrality(',
    "centrality_scores = centrality_result.get('centrality', {})"
]

for notebook_path in notebooks:
    if not os.path.exists(notebook_path):
        print(f"Skipping {notebook_path} - file not found")
        continue
        
    print(f"Processing {notebook_path}...")
    
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    modified = False
    for cell in nb['cells']:
        if cell.get('cell_type') == 'code':
            source = cell.get('source', [])
            if isinstance(source, list):
                # Check if any line contains the pattern
                for i, line in enumerate(source):
                    if old_pattern in line and 'measure="degree"' in line:
                        # Extract the graph variable name
                        if 'market_kg' in line:
                            graph_var = 'market_kg'
                        elif 'trading_kg' in line:
                            graph_var = 'trading_kg'
                        elif 'historical_kg' in line:
                            graph_var = 'historical_kg'
                        elif 'disease_kg' in line:
                            graph_var = 'disease_kg'
                        elif 'drug_kg' in line:
                            graph_var = 'drug_kg'
                        elif 'energy_market_kg' in line:
                            graph_var = 'energy_market_kg'
                        elif 'grid_kg' in line:
                            graph_var = 'grid_kg'
                        elif 'financial_kg' in line:
                            graph_var = 'financial_kg'
                        elif 'temporal_kg' in line:
                            graph_var = 'temporal_kg'
                        elif 'incident_kg' in line:
                            graph_var = 'incident_kg'
                        elif 'supply_chain_kg' in line:
                            graph_var = 'supply_chain_kg'
                        else:
                            print(f"  Warning: Could not identify graph variable in line: {line}")
                            continue
                        
                        # Replace the line
                        new_lines = [
                            f"centrality_result = centrality_calculator.calculate_degree_centrality({graph_var})\n",
                            f"centrality_scores = centrality_result.get('centrality', {{}})\n"
                        ]
                        cell['source'][i:i+1] = new_lines
                        modified = True
                        print(f"  Fixed calculate_centrality call with {graph_var}")
                        break
    
    if modified:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
        print(f"  ✓ Updated {notebook_path}")
    else:
        print(f"  - No changes needed in {notebook_path}")

print("\nDone!")

