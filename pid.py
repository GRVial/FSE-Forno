from pid import PID
import time

# Create a new PID controller
pid = PID(1, 0.1, 0.05)

# Set the target temperature
pid.setpoint = 50

# Get the current temperature from the heating system
current_temp = 25

# Update the PID controller with the current temperature
pid.update(current_temp)

# Get the control output from the PID controller
control_output = pid.output

# Use the control output to control the heating system
# For example, if control_output is positive, increase the heating power
# If control_output is negative, decrease the heating power

# Continuously update the PID controller with the current temperature
# and use the control output to adjust the heating system
while True:
    current_temp = get_current_temp()
    pid.update(current_temp)
    control_output = pid.output
    set_heating_power(control_output)
    time.sleep(1)
