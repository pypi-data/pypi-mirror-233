

class ApitExceptions(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UnknownException(ApitExceptions):
    """Retrun when an unknown exception is raised"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class MinQuantityExceeded(ApitExceptions)

    def MinQuantityExceeded(self) -> dict:
        """
        handle MinQuantityExceeded response.
        """

        value = float(self.data["context"]["min"]) # minimum trade quantity

        result = {"code": self.code, "type": self.type, "quantity": value}

        return result

    def InsufficientFundsMaxSell(self) -> dict:
        """
        handle InsufficientFundsMaxSell response.
        """

        value = float(self.data["context"]["max"]) # maximum trade quantity

        result = {"code": self.code, "type": self.type, "quantity": value}

        return result

    def NoPriceException(self) -> dict:
        """
        handle NoPriceException response
        """

        result = {"code": self.code, "type": self.type}

        return result

    def InstrumentNotSupported(self) -> dict:
        """
        handle InstrumentNotSupported response.
        """

        result = {"code": self.code, "type": self.type}

        return result

    def SpreadIsBiggerThanMinDistance(self) -> dict:
        """
        handle SpreadIsBiggerThanMinDistance response.
        """

        result = {"code": self.code, "type": self.type}

        return result
    
    def InstrumentDisabled(self) -> dict:
        """
        handle InstrumentDisabled response.
        """

        result = {"code": self.code, "type": self.type}

        return result

    def StopLossMustBeBelowCurrentPrice(self) -> dict:
        """
        handle StopLossMustBeBelowCurrentPrice response.
        """

        result = {"code": self.code, "type": self.type}

        return result

    def InsufficientFundsMaxBuy(self) -> dict:
        """
        handle InsufficientFundsMaxBuy response.
        """

        result = {"code": self.code, "type": self.type}

        return result

    def MarketStillNotOpen(self) -> dict:
        """
        handle MarketStillNotOpen response.
        """

        opentime = self.data["context"]["opens"] # get opentime

        result = {"code": self.code, "type": self.type, "openTime": opentime}

        return result

    def MarketClosedAtWeekend(self) -> dict:
        """
        handle MarketClosedAtWeekend response.
        """
        result = {"code": self.code, "type": self.type}

        return result

    def QuantityPrecisionMismatch(self) -> dict:
        """
        handle QuantityPrecisionMismatch response.
        """

        result = {"code": self.code, "type": self.type}

        return result

    def InternalError(self):
        """
        handle InternalError response.
        """

        result = {"code": self.code, "type": self.type}

        return result

    def account(self):
        """
        returns the last order in the list.
        """
        orders = self.data['account']['positions'] # list of orders.

        return orders

    def InvalidSession(self) -> None:
        """
        """
        result = {"code": self.code, "type": self.type}

        return result
        
