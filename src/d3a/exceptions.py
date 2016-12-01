class D3AException(Exception):
    pass


class MarketException(D3AException):
    pass


class MarketReadOnlyException(MarketException):
    pass


class OfferNotFoundException(MarketException):
    pass


class InvalidOffer(MarketException):
    pass