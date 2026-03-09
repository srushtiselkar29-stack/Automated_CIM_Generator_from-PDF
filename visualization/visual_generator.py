class VisualGenerator:

    def generate(self, slide):

        if slide["visual"] == "chart":
            return "generate_chart"

        if slide["visual"] == "diagram":
            return "generate_diagram"

        if slide["visual"] == "image":
            return "add_image"

        if slide["visual"] == "metrics":
            return "metric_block"

        return None