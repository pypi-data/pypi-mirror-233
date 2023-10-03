"""These functions first calculate the consistency score over time based on
    a list of performance-date pairs using the provided formula.
    Then, they create a plot of the consistency scores
    and save it as an image with the specified title and filename."""

import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def calculate_consistency(data, S=0.5, R=1.0, min_added=1.0, min_deducted=5.0):
    """
    Calculate the consistency score over time based on the provided data.

    Args:
        data (list): A list of tuples containing bool (1 or 0) and date pairs.
        S (float): Scaling factor for score points added on each consecutive day
        R (float): Punishment factor for score points deducted for skipping
        min_added (float): Minimum amount of score points that can be added
        min_deducted (float): Minimum amount of score points that can be deducted

    Returns:
        list: A list of tuples containing the calculated score and date pairs.
    """
    consistency_scores = []
    consistency_score = 0.0
    consecutive_days = 0.0

    for performance, date in data:
        if performance:
            consecutive_days += 1.0
            consistency_score += max(S * consecutive_days, min_added)
        else:
            consistency_score = max(consistency_score - max(R * consecutive_days, min_deducted), 0.0)
            consecutive_days = 0.0
        consistency_scores.append((consistency_score, date))

    return consistency_scores


def save_plot(plot_title, data, filename):
    """
    Create and save a plot of consistency scores over time.

    Args:
        plot_title (str): The title of the graph.
        data (list): A list of tuples containing score and date pairs.
        filename (str): The filename (including file extension) to save the plot.
    """
    scores, dates = zip(*data)  # Separate scores and dates from the input data

    # Create a plot
    plt.figure(figsize=(12, 9))
    plt.plot(dates, scores, marker='o', linestyle='-')
    plt.xlabel("Date")
    plt.ylabel("Consistency Score")
    plt.title(plot_title)
    plt.grid(True)
    plt.xticks(rotation=-45)
    # Save the plot as an image (PNG format)
    plt.savefig(filename)

if __name__ == '__main__':
    # Example usage:
    data = [(1, datetime(2023, 1, 1)), (0, datetime(2023, 1, 2)), (1, datetime(2023, 1, 3)),
            (1, datetime(2023, 1, 4)), (1, datetime(2023, 1, 5)),
            (1, datetime(2023, 1, 6)), (1, datetime(2023, 1, 7)),
            (1, datetime(2023, 1, 8)), (1, datetime(2023, 1, 9))]
    consistency_data = calculate_consistency(data)
    save_plot("Consistency Score Over Time", consistency_data, "consistency_score_plot.png")


