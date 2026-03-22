#!/bin/bash
# Restore system to normal operation after benchmarking

echo "=== Restoring System to Normal ==="

# Re-enable Hyper-Threading
echo "Re-enabling Hyper-Threading..."
for cpu in {5..9}; do 
    echo 1 | sudo tee /sys/devices/system/cpu/cpu$cpu/online
done

# Re-enable Turbo Boost
echo "Re-enabling Turbo Boost..."
echo 0 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo

# Re-enable ASLR
echo "Re-enabling ASLR..."
echo 2 | sudo tee /proc/sys/kernel/randomize_va_space

# Restore CPU governor
echo "Restoring CPU governor to powersave..."
for cpu in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
    if [ -f "$cpu" ]; then
        echo powersave | sudo tee "$cpu"
    fi
done

# Restart services
echo "Restarting services..."
sudo systemctl start bluetooth.service 2>/dev/null || true
sudo systemctl start cups.service 2>/dev/null || true

echo ""
echo "=== System Restored ==="
