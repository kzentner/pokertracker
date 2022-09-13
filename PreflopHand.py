from Ignition_Processing import *
import ipywidgets as widgets
import Decision_Types as Decision

class PreflopHand:
    # static variables
    Suited = 0
    Pair = 1
    Offsuit = 2

    def __init__(self, text, status):
        self.text = text
        self.status = status
        self._process_hand_type()


    def _process_hand_type(self):
        if self.text[-1] == 'o':
            self.hand_type = PreflopHand.Offsuit
        elif self.text[-1] == 's':
            self.hand_type = PreflopHand.Suited
        else:
            self.hand_type = PreflopHand.Pair


    def get_display(self):
        size = 55
        html = f'''<style>
            .{self.status} {{
                border: 1px solid black;
                height: {size}px;
                width: {size}px;
                display: flex;
                align-items: center;
                justify-content: center;
                background-color: {self.getBackgroundStyle()};
            }}
            </style>
            <h3 class="{self.status}">{self.text}</h3>
        '''
        return widgets.HTML(html)

    
    def getBackgroundStyle(self):
        if self.status == Decision.Calls:
            return 'green'
        elif self.status == Decision.Raises:
            return 'red'

        return None