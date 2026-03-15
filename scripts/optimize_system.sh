#!/bin/bash
# System optimization script for low-noise benchmark execution
# Disables Turbo Boost, Hyper-Threading, ASLR, and non-essential services

echo "=== System Optimization for Benchmarking ==="

# Disable Turbo Boost
echo "Disabling Turbo Boost..."
echo 1 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo

# Disable Hyper-Threading (CPUs 5-9 for a 10 CPU system with HT)
echo "Disabling Hyper-Threading (CPUs 5-9)..."
for cpu in {5..9}; do 
    echo 0 | sudo tee /sys/devices/system/cpu/cpu$cpu/online
done

# Disable ASLR
echo "Disabling ASLR..."
echo 0 | sudo tee /proc/sys/kernel/randomize_va_space

# Set CPU governor to performance
echo "Setting CPU governor to performance..."
for cpu in /sys/devices/system/cpu/cpu[0-4]/cpufreq/scaling_governor; do
    if [ -f "$cpu" ]; then
        echo performance | sudo tee "$cpu"
    fi
done

# Stop non-essential services
echo "Stopping non-essential services..."
sudo systemctl stop bluetooth.service 2>/dev/null || true
sudo systemctl stop cups.service 2>/dev/null || true
sudo systemctl stop packagekit.service 2>/dev/null || true

echo ""
echo "=== Optimization Complete ==="
echo "Active CPUs:"
grep -H . /sys/devices/system/cpu/cpu*/online 2>/dev/null | grep ":1"
echo ""
echo "Turbo Boost status (1=disabled):"
cat /sys/devices/system/cpu/intel_pstate/no_turbo
echo ""
echo "ASLR status (0=disabled):"
cat /proc/sys/kernel/randomize_va_space
