from ecutils.ec import EC


class ECDH(EC):
    """
    /***********************************************************************
    * Copyright (c) 2021-2023 Isak Ruas                                      *
    * Distributed under the MIT software license, see the accompanying    *
    * https://github.com/isakruas/ecutils/blob/master/LICENSE.md          *
    ***********************************************************************/

    Reference: https://en.wikipedia.org/wiki/Elliptic-curve_Diffie-Hellman
    """

    def __init__(self, private_key: int, curve: str = None, **kwargs) -> None:
        super().__init__(curve=curve)
        self.__private_key = private_key
        self.__public_key = None

    @property
    def private_key(self) -> int:
        return self.__private_key

    @property
    def public_key(self) -> tuple:
        if self.__public_key is None:
            self.__public_key = self.trapdoor(self.G, self.__private_key)
            return self.__public_key
        return self.__public_key

    def to_share(self, public_key: tuple) -> tuple:
        return self.trapdoor(public_key, self.__private_key)
