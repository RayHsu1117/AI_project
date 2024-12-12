#!/bin/zsh

# Activate the Python environment if needed
source /path/to/your/env/bin/activate  # Adjust this path to your Python environment

# Loop to run the simulation 100 times
for i in {1..1000}
do
  echo "Running simulation $i..."
  python main.py $i --no-draw
done

echo "All simulations completed!"

# Analyze simulation_results.txt for success and collision rates
simulation_results_file="simulation_results.txt"
successful_count=0
collision_count=0

while IFS= read -r line; do
  if [[ $line == *"Successful"* ]]; then
    successful_count=$((successful_count + 1))
  elif [[ $line == *"Collision"* ]]; then
    collision_count=$((collision_count + 1))
  fi
done < "$simulation_results_file"

total_simulations=$((successful_count + collision_count))
success_rate=$(echo "scale=2; $successful_count / $total_simulations * 100" | bc)
collision_rate=$(echo "scale=2; $collision_count / $total_simulations * 100" | bc)

echo "Calculating Success and Collision Rates..."
echo -e "\nSuccess Rate: $success_rate%" >> "$simulation_results_file"
echo "Collision Rate: $collision_rate%" >> "$simulation_results_file"
echo "Success and Collision Rates appended to $simulation_results_file."

# Analyze simulation_time_analysis.txt for average metrics
simulation_time_file="simulation_time_analysis.txt"
total_avg_time=0
total_max_time=0
total_min_time=0
record_count=0

while IFS= read -r line; do
  if [[ $line == *"Average Time:"* ]]; then
    avg_time=$(echo $line | awk -F'Average Time: ' '{print $2}' | awk '{print $1}')
    total_avg_time=$(echo "$total_avg_time + $avg_time" | bc)
    record_count=$((record_count + 1))
  elif [[ $line == *"Max Time:"* ]]; then
    max_time=$(echo $line | awk -F'Max Time: ' '{print $2}' | awk '{print $1}')
    total_max_time=$(echo "$total_max_time + $max_time" | bc)
  elif [[ $line == *"Min Time:"* ]]; then
    min_time=$(echo $line | awk -F'Min Time: ' '{print $2}' | awk '{print $1}')
    total_min_time=$(echo "$total_min_time + $min_time" | bc)
  fi
done < "$simulation_time_file"

if [[ $record_count -gt 0 ]]; then
  avg_avg_time=$(echo "scale=2; $total_avg_time / $record_count" | bc)
  avg_max_time=$(echo "scale=2; $total_max_time / $record_count" | bc)
  avg_min_time=$(echo "scale=2; $total_min_time / $record_count" | bc)

  echo "Calculating Average Metrics..."
  echo -e "\nOverall Simulation Metrics:" >> "$simulation_time_file"
  echo "  Average of Average Time: $avg_avg_time frames" >> "$simulation_time_file"
  echo "  Average of Max Time: $avg_max_time frames" >> "$simulation_time_file"
  echo "  Average of Min Time: $avg_min_time frames" >> "$simulation_time_file"
  echo "Metrics appended to $simulation_time_file."
else
  echo "No records found in $simulation_time_file to calculate metrics."
fi