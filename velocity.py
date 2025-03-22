import sqlite3
from rosidl_runtime_py.utilities import get_message
from rclpy.serialization import deserialize_message
import matplotlib.pyplot as plt

class BagFileParser():
    def __init__(self, bag_file):
        self.conn = sqlite3.connect(bag_file)
        self.cursor = self.conn.cursor()

        topics_data = self.cursor.execute("SELECT id, name, type FROM topics").fetchall()
        self.topic_type = {name_of: type_of for id_of, name_of, type_of in topics_data}
        self.topic_id = {name_of: id_of for id_of, name_of, type_of in topics_data}
        self.topic_msg_message = {name_of: get_message(type_of) for id_of, name_of, type_of in topics_data}

    def __del__(self):
        self.conn.close()

    def get_messages(self, topic_name):
        topic_id = self.topic_id[topic_name]
        rows = self.cursor.execute(f"SELECT timestamp, data FROM messages WHERE topic_id = {topic_id}").fetchall()
        return [(timestamp, deserialize_message(data, self.topic_msg_message[topic_name])) for timestamp, data in rows]

def plot_velocity_from_bag_files(bag_files):
    plt.figure(figsize=(10, 5))

    colors = ['r', 'r', 'b', 'b']
    message = '/vehicle/status/velocity_status'

    for idx, bag_file in enumerate(bag_files):

        parser = BagFileParser(bag_file)

        time = '/clock'
        clock_start = parser.get_messages(time)[0][0]
        time_start = clock_start / 1e9

        data = parser.get_messages(message)

        time_seconds = []
        velocities = []

        for timestamp, velocity_msg in data:

            time_seconds.append(timestamp / 1e9 - time_start)  # Relative time in seconds
            velocities.append(velocity_msg.longitudinal_velocity)

        run_num = bag_file.split('.')[0][-4:-2]
        plt.plot(time_seconds, velocities, linestyle='-', color=colors[idx % len(colors)], label=f"Run {run_num}")

    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Vehicle Velocity Over Time (Multiple Runs)")
    plt.grid(True)
    plt.legend()
    plt.savefig('velocity.png')
    plt.show()

if __name__ == "__main__":
    bag_files = [
        "/home/lucas/scenario_test_runner/sample_awsim/sample_awsim_30/sample_awsim_30_0.db3",
        "/home/lucas/scenario_test_runner/sample_awsim/sample_awsim_31/sample_awsim_31_0.db3",
        "/home/lucas/scenario_test_runner/sample_awsim/sample_awsim_15/sample_awsim_15_0.db3",
        "/home/lucas/scenario_test_runner/sample_awsim/sample_awsim_35/sample_awsim_35_0.db3",
    ]  
    plot_velocity_from_bag_files(bag_files)