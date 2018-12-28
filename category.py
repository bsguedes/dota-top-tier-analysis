class Category:
    def __init__(self, weight, param, text=None, reverse=True, has_avg=True, unit='',
                 has_max=True, apply_transform=None, rule=None):
        self.weight = weight
        self.parameter = param
        self.text = text
        self.unit = unit
        self.reverse = reverse
        self.has_avg = has_avg
        self.has_max = has_max
        self.rule = rule
        self.transform = apply_transform if apply_transform is not None else lambda y: y