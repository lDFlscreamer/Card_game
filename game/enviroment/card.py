class Card:
    def __init__(self, id, card_class, card_type, card_num, is_beast, function, initiation):
        self.id = id
        self.card_class = card_class
        self.card_type = card_type
        self.card_num = card_num,

        self.is_Beast = is_beast,
        self.initiation = initiation,

        self.function = function

    def get_id(self):
        return self.id

    def get_card_class(self):
        return self.card_class

    def get_card_type(self):
        return self.card_type

    def is_beast(self):
        return self.is_Beast

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Card):
            return ((self.card_class == other.card_class)
                    and (self.card_type == other.card_type)
                    and (self.card_num == self.card_num))
        return False
