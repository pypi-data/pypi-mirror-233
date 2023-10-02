import logging

from ecutils.ec import EC
from ecutils.ecdh import ECDH
from ecutils.ecdsa import ECDSA
from ecutils.eck import ECK

logging.basicConfig(level=logging.ERROR)


class ECMO(ECDH, ECK, ECDSA, EC):
    """
    /***********************************************************************
    * Copyright (c) 2021-2023 Isak Ruas                                        *
    * Distributed under the MIT software license, see the accompanying    *
    * https://github.com/isakruas/ecutils/blob/master/LICENSE.md          *
    ***********************************************************************/

    Reference: https://en.wikipedia.org/wiki/Three-pass_protocol
    """

    def __init__(self, private_key: int) -> None:
        super().__init__(private_key=private_key, curve="secp521r1")

    def encrypt(self, message: str, to: tuple, encode: int = 64) -> tuple:
        message_eck_encode = self.encode(message, encode)
        P = message_eck_encode[0:2]
        j = message_eck_encode[-1]
        x, y = self.trapdoor(P, self.to_share(to)[0])
        r, s = self.signature(x)
        return ((x, y), j), (r, s)

    def decrypt(self, message: tuple, got: tuple, encode: int = 64) -> str:
        ((x, y), j), (r, s) = message
        if not self.verify_signature(x, r, s, got):
            raise ValueError("Invalid signature")
        x, y = self.trapdoor((x, y), self.mmi(self.to_share(got)[0], self.n))
        return self.decode((x, y, j), encode)
