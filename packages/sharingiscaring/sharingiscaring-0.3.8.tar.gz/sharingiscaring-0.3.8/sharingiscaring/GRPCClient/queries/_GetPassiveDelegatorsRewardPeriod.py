from __future__ import annotations
from sharingiscaring.GRPCClient.types_pb2 import *
from sharingiscaring.enums import NET
from enum import Enum
from sharingiscaring.GRPCClient.service_pb2_grpc import QueriesStub
from sharingiscaring.GRPCClient.queries._SharedConverters import (
    Mixin as _SharedConverters,
)
from typing import Iterator
from sharingiscaring.GRPCClient.CCD_Types import CCD_DelegatorRewardPeriodInfo
from typing import TYPE_CHECKING
import sys

if TYPE_CHECKING:
    from sharingiscaring.GRPCClient import GRPCClient


class Mixin(_SharedConverters):
    def get_delegators_for_passive_delegation_in_reward_period(
        self: GRPCClient,
        block_hash: str,
        net: Enum = NET.MAINNET,
    ) -> list[CCD_DelegatorRewardPeriodInfo]:
        result = []
        blockHashInput = self.generate_block_hash_input_from(block_hash)

        self.check_connection(net, sys._getframe().f_code.co_name)
        if net == NET.MAINNET:
            grpc_return_value: Iterator[
                DelegatorInfo
            ] = self.stub_mainnet.GetPassiveDelegatorsRewardPeriod(
                request=blockHashInput
            )
        else:
            grpc_return_value: Iterator[
                DelegatorInfo
            ] = self.stub_testnet.GetPassiveDelegatorsRewardPeriod(
                request=blockHashInput
            )

        for delegator in list(grpc_return_value):
            result.append(
                CCD_DelegatorRewardPeriodInfo(
                    **{
                        "account": self.convertAccountAddress(delegator.account),
                        "stake": self.convertAmount(delegator.stake),
                    }
                )
            )

        return result
