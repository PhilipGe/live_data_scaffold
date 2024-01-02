class GraphColors:
    colors = [
            (1.0, 0.0, 0.0, 1.0),  # Red
            (0.0, 1.0, 0.0, 1.0),  # Green
            (0.0, 0.0, 1.0, 1.0),  # Blue
            (1.0, 1.0, 0.0, 1.0),  # Yellow
            
            (1.0, 0.0, 1.0, 1.0),  # Magenta
            (0.0, 1.0, 1.0, 1.0),  # Cyan
            (1.0, 0.5, 0.0, 1.0),  # Orange
            (0.5, 0.0, 1.0, 1.0),  # Purple
            
            (0.0, 0.5, 1.0, 1.0),  # Light Blue
            (0.5, 0.5, 0.5, 1.0),  # Gray
            (1.0, 0.5, 0.5, 1.0),  # Light Red
            (0.5, 1.0, 0.5, 1.0),  # Light Green
            
            (0.5, 0.5, 1.0, 1.0),  # Lavender
            (0.75, 0.25, 0.0, 1.0),  # Brown
            (0.25, 0.75, 0.0, 1.0),  # Olive
            (0.0, 0.75, 0.25, 1.0),  # Forest Green
            
            (0.75, 0.0, 0.75, 1.0),  # Dark Magenta
            (0.0, 0.75, 0.75, 1.0),  # Teal
            (0.75, 0.75, 0.0, 1.0),  # Chartreuse
            (0.25, 0.25, 0.25, 1.0),  # Dark Gray
    ]

    curr_index = 0

    @classmethod 
    def get_next_plot_color(cls):
        cls.curr_index += 1
        cls.curr_index %= len(cls.colors)
        return cls.colors[cls.curr_index-1]