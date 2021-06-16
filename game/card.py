class Card:
    def __init__(self, card_class, card_type, card_num,is_beast, function, initiation):
        self.card_class = card_class
        self.card_type = card_type
        self.card_num = card_num,

        self.is_beast = is_beast,
        self.initiation = initiation,

        self.function = function

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Card):
            return ((self.card_class == other.card_class)
                    and (self.card_type == other.card_type)
                    and (self.card_num == self.card_num))
        return False
