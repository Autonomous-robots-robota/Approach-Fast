from pynput import keyboard
import time
import matplotlib.pyplot as plt

# Global variables
channels = [0.0 for _ in range(16)]
path = []  # To store the path commands with timestamps


def set_channels(roll, pitch, throttle, yaw, arm, aux):
    # Clamp the throttle value to be within -0.1 to 0.1
    throttle = min(0.1, max(-0.1, throttle))
    channels[15] = roll  # Roll
    channels[14] = pitch  # Pitch
    channels[13] = throttle  # Throttle
    channels[12] = yaw  # Yaw
    channels[11] = arm  # Arm
    channels[10] = aux  # Auxiliary control (extra variable for another channel)


def on_press(key):
    timestamp = time.time()  # Capture the current time
    try:
        if key == keyboard.Key.up:
            command = "Up arrow key pressed"
            set_channels(0, 0, 0.1, 0, 1, 0)
        elif key == keyboard.Key.down:
            command = "Down arrow key pressed"
            set_channels(0, 0, -0.1, 0, 1, 0)
        elif key == keyboard.Key.left:
            command = "Left arrow key pressed"
            set_channels(-0.1, 0, 0, 0, 1, 0)
        elif key == keyboard.Key.right:
            command = "Right arrow key pressed"
            set_channels(0.1, 0, 0, 0, 1, 0)
        elif key == keyboard.KeyCode.from_char('w'):
            command = "W key pressed - Moving forward"
            set_channels(0, 0.1, 0, 0, 1, 0)
        elif key == keyboard.KeyCode.from_char('s'):
            command = "S key pressed - Moving backward"
            set_channels(0, -0.1, 0, 0, 1, 0)
        else:
            command = None

        if command:
            print(command)
            path.append((timestamp, channels[:]))  # Record the timestamp and channels state
    except AttributeError:
        print(f"Special key {key} pressed")


def on_release(key):
    if key == keyboard.Key.esc:
        print("Exiting...")
        # Stop listener
        return False


def plot_path():
    if path:
        timestamps = [p[0] for p in path]
        roll = [p[1][15] for p in path]
        pitch = [p[1][14] for p in path]
        throttle = [p[1][13] for p in path]
        yaw = [p[1][12] for p in path]

        plt.figure(figsize=(12, 10))

        # Plot Roll
        plt.subplot(4, 1, 1)
        plt.plot(timestamps, roll, label='Roll')
        plt.xlabel('Time (s)')
        plt.ylabel('Roll')
        plt.legend()

        # Plot Pitch
        plt.subplot(4, 1, 2)
        plt.plot(timestamps, pitch, label='Pitch')
        plt.xlabel('Time (s)')
        plt.ylabel('Pitch')
        plt.legend()

        # Plot Throttle
        plt.subplot(4, 1, 3)
        plt.plot(timestamps, throttle, label='Throttle')
        plt.xlabel('Time (s)')
        plt.ylabel('Throttle')
        plt.legend()

        # Plot Yaw
        plt.subplot(4, 1, 4)
        plt.plot(timestamps, yaw, label='Yaw')
        plt.xlabel('Time (s)')
        plt.ylabel('Yaw')
        plt.legend()

        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    print("Press any arrow key to control the drone, 'w' and 's' for FORWARD and BACKWARD (press 'Esc' to quit)...")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    # Print the path with time durations and plot the graph
    if path:
        print("\nFlight Path:")
        start_time = path[0][0]
        for i, (timestamp, _) in enumerate(path):
            elapsed_time = timestamp - start_time
            print(f"Time: {elapsed_time:.2f} seconds - Command {i + 1}")
            start_time = timestamp

        # Plot the path
        plot_path()
