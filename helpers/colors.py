import random


class MColors:
    RED = {
        'lighten-5': '#ffebee',
        'lighten-4': '#ffcdd2',
        'lighten-3': '#ef9a9a',
        'lighten-2': '#e57373',
        'lighten-1': '#ef5350',
        'base': '#f44336',
        'darken-1': '#e53935',
        'darken-2': '#d32f2f',
        'darken-3': '#c62828',
        'darken-4': '#b71c1c',
        'accent-1': '#ff8a80',
        'accent-2': '#ff5252',
        'accent-3': '#ff1744',
        'accent-4': '#d50000',
    }

    PINK = {
        'lighten-5': '#fce4ec',
        'lighten-4': '#f8bbd0',
        'lighten-3': '#f48fb1',
        'lighten-2': '#f06292',
        'lighten-1': '#ec407a',
        'base': '#e91e63',
        'darken-1': '#d81b60',
        'darken-2': '#c2185b',
        'darken-3': '#ad1457',
        'darken-4': '#880e4f',
        'accent-1': '#ff80ab',
        'accent-2': '#ff4081',
        'accent-3': '#f50057',
        'accent-4': '#c51162',
    }

    PURPLE = {
        'lighten-5': '#f3e5f5',
        'lighten-4': '#e1bee7',
        'lighten-3': '#ce93d8',
        'lighten-2': '#ba68c8',
        'lighten-1': '#ab47bc',
        'base': '#9c27b0',
        'darken-1': '#8e24aa',
        'darken-2': '#7b1fa2',
        'darken-3': '#6a1b9a',
        'darken-4': '#4a148c',
        'accent-1': '#ea80fc',
        'accent-2': '#e040fb',
        'accent-3': '#d500f9',
        'accent-4': '#aa00ff',
    }

    DEEP_PURPLE = {
        'lighten-5': '#ede7f6',
        'lighten-4': '#d1c4e9',
        'lighten-3': '#b39ddb',
        'lighten-2': '#9575cd',
        'lighten-1': '#7e57c2',
        'base': '#673ab7',
        'darken-1': '#5e35b1',
        'darken-2': '#512da8',
        'darken-3': '#4527a0',
        'darken-4': '#311b92',
        'accent-1': '#b388ff',
        'accent-2': '#7c4dff',
        'accent-3': '#651fff',
        'accent-4': '#6200ea',
    }

    INDIGO = {
        'lighten-5': '#e8eaf6',
        'lighten-4': '#c5cae9',
        'lighten-3': '#9fa8da',
        'lighten-2': '#7986cb',
        'lighten-1': '#5c6bc0',
        'base': '#3f51b5',
        'darken-1': '#3949ab',
        'darken-2': '#303f9f',
        'darken-3': '#283593',
        'darken-4': '#1a237e',
        'accent-1': '#8c9eff',
        'accent-2': '#536dfe',
        'accent-3': '#3d5afe',
        'accent-4': '#304ffe',
    }

    BLUE = {
        'lighten-5': '#e3f2fd',
        'lighten-4': '#bbdefb',
        'lighten-3': '#90caf9',
        'lighten-2': '#64b5f6',
        'lighten-1': '#42a5f5',
        'base': '#2196f3',
        'darken-1': '#1e88e5',
        'darken-2': '#1976d2',
        'darken-3': '#1565c0',
        'darken-4': '#0d47a1',
        'accent-1': '#82b1ff',
        'accent-2': '#448aff',
        'accent-3': '#2979ff',
        'accent-4': '#2962ff',
    }

    LIGHT_BLUE = {
        'lighten-5': '#e1f5fe',
        'lighten-4': '#b3e5fc',
        'lighten-3': '#81d4fa',
        'lighten-2': '#4fc3f7',
        'lighten-1': '#29b6f6',
        'base': '#03a9f4',
        'darken-1': '#039be5',
        'darken-2': '#0288d1',
        'darken-3': '#0277bd',
        'darken-4': '#01579b',
        'accent-1': '#80d8ff',
        'accent-2': '#40c4ff',
        'accent-3': '#00b0ff',
        'accent-4': '#0091ea',
    }

    CYAN = {
        'lighten-5': '#e0f7fa',
        'lighten-4': '#b2ebf2',
        'lighten-3': '#80deea',
        'lighten-2': '#4dd0e1',
        'lighten-1': '#26c6da',
        'base': '#00bcd4',
        'darken-1': '#00acc1',
        'darken-2': '#0097a7',
        'darken-3': '#00838f',
        'darken-4': '#006064',
        'accent-1': '#84ffff',
        'accent-2': '#18ffff',
        'accent-3': '#00e5ff',
        'accent-4': '#00b8d4',
    }

    TEAL = {
        'lighten-5': '#e0f2f1',
        'lighten-4': '#b2dfdb',
        'lighten-3': '#80cbc4',
        'lighten-2': '#4db6ac',
        'lighten-1': '#26a69a',
        'base': '#009688',
        'darken-1': '#00897b',
        'darken-2': '#00796b',
        'darken-3': '#00695c',
        'darken-4': '#004d40',
        'accent-1': '#a7ffeb',
        'accent-2': '#64ffda',
        'accent-3': '#1de9b6',
        'accent-4': '#00bfa5',
    }

    GREEN = {
        'lighten-5': '#e8f5e9',
        'lighten-4': '#c8e6c9',
        'lighten-3': '#a5d6a7',
        'lighten-2': '#81c784',
        'lighten-1': '#66bb6a',
        'base': '#4caf50',
        'darken-1': '#43a047',
        'darken-2': '#388e3c',
        'darken-3': '#2e7d32',
        'darken-4': '#1b5e20',
        'accent-1': '#b9f6ca',
        'accent-2': '#69f0ae',
        'accent-3': '#00e676',
        'accent-4': '#00c853',
    }

    LIGHT_GREEN = {
        'lighten-5': '#f1f8e9',
        'lighten-4': '#dcedc8',
        'lighten-3': '#c5e1a5',
        'lighten-2': '#aed581',
        'lighten-1': '#9ccc65',
        'base': '#8bc34a',
        'darken-1': '#7cb342',
        'darken-2': '#689f38',
        'darken-3': '#558b2f',
        'darken-4': '#33691e',
        'accent-1': '#ccff90',
        'accent-2': '#b2ff59',
        'accent-3': '#76ff03',
        'accent-4': '#64dd17',
    }

    LIME = {
        'lighten-5': '#f9fbe7',
        'lighten-4': '#f0f4c3',
        'lighten-3': '#e6ee9c',
        'lighten-2': '#dce775',
        'lighten-1': '#d4e157',
        'base': '#cddc39',
        'darken-1': '#c0ca33',
        'darken-2': '#afb42b',
        'darken-3': '#9e9d24',
        'darken-4': '#827717',
        'accent-1': '#f4ff81',
        'accent-2': '#eeff41',
        'accent-3': '#c6ff00',
        'accent-4': '#aeea00',
    }

    YELLOW = {
        'lighten-5': '#fffde7',
        'lighten-4': '#fff9c4',
        'lighten-3': '#fff59d',
        'lighten-2': '#fff176',
        'lighten-1': '#ffee58',
        'base': '#ffeb3b',
        'darken-1': '#fdd835',
        'darken-2': '#fbc02d',
        'darken-3': '#f9a825',
        'darken-4': '#f57f17',
        'accent-1': '#ffff8d',
        'accent-2': '#ffff00',
        'accent-3': '#ffea00',
        'accent-4': '#ffd600',
    }

    AMBER = {
        'lighten-5': '#fff8e1',
        'lighten-4': '#ffecb3',
        'lighten-3': '#ffe082',
        'lighten-2': '#ffd54f',
        'lighten-1': '#ffca28',
        'base': '#ffc107',
        'darken-1': '#ffb300',
        'darken-2': '#ffa000',
        'darken-3': '#ff8f00',
        'darken-4': '#ff6f00',
        'accent-1': '#ffe57f',
        'accent-2': '#ffd740',
        'accent-3': '#ffc400',
        'accent-4': '#ffab00',
    }

    ORANGE = {
        'lighten-5': '#fff3e0',
        'lighten-4': '#ffe0b2',
        'lighten-3': '#ffcc80',
        'lighten-2': '#ffb74d',
        'lighten-1': '#ffa726',
        'base': '#ff9800',
        'darken-1': '#fb8c00',
        'darken-2': '#f57c00',
        'darken-3': '#ef6c00',
        'darken-4': '#e65100',
        'accent-1': '#ffd180',
        'accent-2': '#ffab40',
        'accent-3': '#ff9100',
        'accent-4': '#ff6d00',
    }

    DEEP_ORANGE = {
        'lighten-5': '#fbe9e7',
        'lighten-4': '#ffccbc',
        'lighten-3': '#ffab91',
        'lighten-2': '#ff8a65',
        'lighten-1': '#ff7043',
        'base': '#ff5722',
        'darken-1': '#f4511e',
        'darken-2': '#e64a19',
        'darken-3': '#d84315',
        'darken-4': '#bf360c',
        'accent-1': '#ff9e80',
        'accent-2': '#ff6e40',
        'accent-3': '#ff3d00',
        'accent-4': '#dd2c00',
    }

    BROWN = {
        'lighten-5': '#efebe9',
        'lighten-4': '#d7ccc8',
        'lighten-3': '#bcaaa4',
        'lighten-2': '#a1887f',
        'lighten-1': '#8d6e63',
        'base': '#795548',
        'darken-1': '#6d4c41',
        'darken-2': '#5d4037',
        'darken-3': '#4e342e',
        'darken-4': '#3e2723',
    }

    GREY = {
        'lighten-5': '#fafafa',
        'lighten-4': '#f5f5f5',
        'lighten-3': '#eeeeee',
        'lighten-2': '#e0e0e0',
        'lighten-1': '#bdbdbd',
        'base': '#9e9e9e',
        'darken-1': '#757575',
        'darken-2': '#616161',
        'darken-3': '#424242',
        'darken-4': '#212121',
    }

    BLUE_GREY = {
        'lighten-5': '#eceff1',
        'lighten-4': '#cfd8dc',
        'lighten-3': '#b0bec5',
        'lighten-2': '#90a4ae',
        'lighten-1': '#78909c',
        'base': '#607d8b',
        'darken-1': '#546e7a',
        'darken-2': '#455a64',
        'darken-3': '#37474f',
        'darken-4': '#263238',
    }

    FULL = [
        RED, PINK, PURPLE, DEEP_PURPLE, INDIGO, BLUE, LIGHT_BLUE, CYAN, TEAL, GREEN, LIGHT_GREEN, LIME, YELLOW, AMBER,
        ORANGE, DEEP_ORANGE, BROWN, GREY, BLUE_GREY
    ]

    WARM = [PINK, RED, DEEP_ORANGE, ORANGE, AMBER, YELLOW]
    COOL = [CYAN, LIGHT_BLUE, BLUE, INDIGO, DEEP_PURPLE, BLUE_GREY]
    NATURE = [BROWN, DEEP_ORANGE, AMBER, YELLOW, LIGHT_GREEN, GREEN]
    TECH = [LIGHT_BLUE, CYAN, TEAL, BLUE_GREY]
    ODD = [PINK, CYAN, BROWN, AMBER, LIGHT_GREEN, DEEP_PURPLE, RED]

    SCHEME_REGISTRY = [
        WARM,
        COOL,
        NATURE,
        TECH
    ]

    def __init__(self, colorset=None):
        if not colorset:
            self.colorset = self.FULL
        else:
            self.colorset = colorset

    def get_colors(self, variant='base'):
        colors = []

        for color in self.colorset:
            if variant == 'all':
                for key, __variant in color.items():
                    colors.append(__variant)
            else:
                try:
                    colors.append(color[variant])
                except KeyError:
                    colors.append(color['base'])
        return colors

    def get_color(self, color=None, variant=None):
        if not color:
            selected_color = random.sample(self.colorset, len(self.colorset)).pop()
        else:
            if type(color) == list:
                if color in self.SCHEME_REGISTRY:
                    selected_color = random.sample(color, len(color)).pop()
                else:
                    return False
            elif type(color) == dict:
                selected_color = color
            else:
                selected_color = random.sample(self.colorset, len(self.colorset)).pop()

        if not variant:
            selected_variant = random.choice(list(selected_color.keys()))
        else:
            if variant == 'dark':
                selected_variant = "darken-{}".format(random.randint(1, 5))
            elif variant == 'light':
                selected_variant = "lighten-{}".format(random.randint(1, 5))
            else:
                selected_variant = variant

        try:
            return selected_color[selected_variant]
        except KeyError:
            return selected_color['base']
