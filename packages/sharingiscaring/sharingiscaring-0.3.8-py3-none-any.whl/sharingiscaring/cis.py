from __future__ import annotations
from pydantic import BaseModel, Extra, Field
import datetime as dt
from typing import Union
from enum import Enum
import io
import base58
from sharingiscaring.GRPCClient import GRPCClient
from sharingiscaring.GRPCClient.CCD_Types import *
from sharingiscaring.mongodb import Collections
from pymongo.collection import Collection
from pymongo import ReplaceOne, DESCENDING, ASCENDING
from sharingiscaring.enums import NET
from rich import print
from rich.console import Console
import math
import leb128

console = Console()

LEN_ACCOUNT_ADDRESS = 50


# Metadata classes
class TokenAttribute(BaseModel):
    type: str
    name: str
    value: str


class TokenURLJSON(BaseModel):
    url: str
    hash: str = None


class TokenMetaData(BaseModel):
    name: str = None
    symbol: str = None
    unique: bool = None
    decimals: int = None
    description: str = None
    thumbnail: TokenURLJSON = None
    display: TokenURLJSON = None
    artifact: TokenURLJSON = None
    assets: list[TokenMetaData] = None
    attributes: list[TokenAttribute] = None
    localization: dict[str, TokenURLJSON] = None


# class MongoTypeTokenHolder(BaseModel):
#     account_address: CCD_AccountAddress
#     token_amount: str


class MongoTypeTokenForAddress(BaseModel):
    token_address: str
    contract: str
    token_id: str
    token_amount: str


class MongoTypeTokenHolderAddress(BaseModel):
    id: str = Field(..., alias="_id")
    tokens: dict[str, MongoTypeTokenForAddress]


class MongoTypeLoggedEvent(BaseModel):
    id: str = Field(..., alias="_id")
    logged_event: str
    result: dict
    tag: int
    event_type: str
    block_height: int
    slot_time: dt.datetime = None
    tx_index: int  ###########################################################################
    ordering: int
    tx_hash: str
    token_address: str
    contract: str


class MongoTypeTokensTag(BaseModel):
    id: str = Field(..., alias="_id")
    contracts: list[str]
    tag_template: bool = None
    single_use_contract: bool = None
    logo_url: str = None
    decimals: int = None
    exchange_rate: float = None
    logged_events_count: int = None
    owner: str = None
    module_name: str = None
    token_type: str = None
    display_name: str = None


class MongoTypeTokenAddress(BaseModel):
    id: str = Field(..., alias="_id")
    contract: str
    token_id: str
    token_amount: str = None
    metadata_url: str = None
    last_height_processed: int
    token_holders: dict[str, str] = None
    tag_information: MongoTypeTokensTag = None
    exchange_rate: float = None
    domain_name: str = None
    token_metadata: TokenMetaData = None


# CIS
class StandardIdentifiers(Enum):
    CIS_0 = "CIS-0"
    CIS_1 = "CIS-1"
    CIS_2 = "CIS-2"
    CIS_3 = "CIS-3"


class LoggedEvents(Enum):
    transfer_event = 255
    mint_event = 254
    burn_event = 253
    operator_event = 252
    metadata_event = 251
    nonce_event = 250


# CIS-2 Logged Event Types


class transferEvent(BaseModel):
    tag: int
    token_id: str = None
    token_amount: int = None
    from_address: str = None
    to_address: str = None


class mintEvent(BaseModel):
    tag: int
    token_id: str = None
    token_amount: int = None
    to_address: str = None


class burnEvent(BaseModel):
    tag: int
    token_id: str = None
    token_amount: int = None
    from_address: str = None


class updateOperatorEvent(BaseModel):
    tag: int
    operator_update: str = None
    owner: str = None
    operator: str = None


class MetadataUrl(BaseModel):
    url: str
    checksum: str = None


class tokenMetadataEvent(BaseModel):
    tag: int
    token_id: str
    metadata: MetadataUrl


class nonceEvent(BaseModel):
    tag: int
    nonce: int = None
    sponsoree: str = None


class CIS:
    def __init__(
        self,
        grpcclient: GRPCClient = None,
        instance_index=None,
        instance_subindex=None,
        entrypoint=None,
        net: NET.MAINNET = None,
    ):
        self.grpcclient = grpcclient
        self.instance_index = instance_index
        self.instance_subindex = instance_subindex
        self.entrypoint = entrypoint
        self.net = net

    ###############

    def execute_save(self, collection: Collection, replacement, _id: str):
        repl_dict = replacement.dict()
        if "id" in repl_dict:
            del repl_dict["id"]

        # sort tokens and token_holders
        if "tokens" in repl_dict:
            sorted_tokens = list(repl_dict["tokens"].keys())
            sorted_tokens.sort()
            tokens_sorted = {i: repl_dict["tokens"][i] for i in sorted_tokens}
            repl_dict["tokens"] = tokens_sorted

        if "token_holders" in repl_dict:
            sorted_holders = list(repl_dict["token_holders"].keys())
            sorted_holders.sort()
            token_holders_sorted = {
                i: repl_dict["token_holders"][i] for i in sorted_holders
            }
            repl_dict["token_holders"] = token_holders_sorted

        _ = collection.bulk_write(
            [
                ReplaceOne(
                    {"_id": _id},
                    replacement=repl_dict,
                    upsert=True,
                )
            ]
        )

    def restore_state_for_token_address(
        self,
        db_to_use: dict[Collections, Collection],
        token_address: str,
    ):
        d: dict = db_to_use[Collections.tokens_token_addresses].find_one(
            {"_id": token_address}
        )

        d.update(
            {
                "token_amount": str(int(0)),  # mongo limitation on int size
                "token_holders": {},  # {CCD_AccountAddress, str(token_amount)}
                "last_height_processed": 0,
            }
        )

        d = MongoTypeTokenAddress(**d)
        self.execute_save(
            db_to_use[Collections.tokens_token_addresses], d, token_address
        )

    def copy_token_holders_state_to_address_and_save(
        self,
        db_to_use: dict[Collections, Collection],
        token_address_info: MongoTypeTokenAddress,
        address: str,
    ):
        token_address = token_address_info.id
        d = db_to_use[Collections.tokens_accounts].find_one({"_id": address})
        # if this account doesn't have tokens, create empty dict.
        if not d:
            d = MongoTypeTokenHolderAddress(
                **{
                    "_id": address,
                    "tokens": {},
                }
            )  # keyed on token_address
        else:
            d = MongoTypeTokenHolderAddress(**d)

        token_to_save = MongoTypeTokenForAddress(
            **{
                "token_address": token_address,
                "contract": token_address_info.contract,
                "token_id": token_address_info.token_id,
                "token_amount": str(token_address_info.token_holders.get(address, 0)),
            }
        )

        d.tokens[token_address] = token_to_save

        if token_to_save.token_amount == str(0):
            del d.tokens[token_address]

        self.execute_save(db_to_use[Collections.tokens_accounts], d, address)

    def save_mint(
        self,
        db_to_use: dict[Collections, Collection],
        instance_address: str,
        result: mintEvent,
        height: int,
    ):
        token_address = f"{instance_address}-{result.token_id}"
        d = db_to_use[Collections.tokens_token_addresses].find_one(
            {"_id": token_address}
        )
        if not d:
            d = MongoTypeTokenAddress(
                **{
                    "_id": token_address,
                    "contract": instance_address,
                    "token_id": result.token_id,
                    "token_amount": str(int(0)),  # mongo limitation on int size
                    "token_holders": {},  # {CCD_AccountAddress, str(token_amount)}
                    "last_height_processed": height,
                }
            )
        else:
            d = MongoTypeTokenAddress(**d)

        token_holders: dict[CCD_AccountAddress, str] = d.token_holders
        token_holders[result.to_address] = str(
            int(token_holders.get(result.to_address, "0")) + result.token_amount
        )
        d.token_amount = str((int(d.token_amount) + result.token_amount))
        d.token_holders = token_holders

        self.execute_save(
            db_to_use[Collections.tokens_token_addresses], d, token_address
        )
        self.copy_token_holders_state_to_address_and_save(
            db_to_use, d, result.to_address
        )

    def save_metadata(
        self,
        db_to_use: dict[Collections, Collection],
        instance_address: str,
        result: tokenMetadataEvent,
        height: int,
    ):
        token_address = f"{instance_address}-{result.token_id}"
        d = db_to_use[Collections.tokens_token_addresses].find_one(
            {"_id": token_address}
        )
        if not d:
            d = MongoTypeTokenAddress(
                **{
                    "_id": token_address,
                    "contract": instance_address,
                    "token_id": result.token_id,
                    "last_height_processed": height,
                }
            )
        else:
            d = MongoTypeTokenAddress(**d)

        d.metadata_url = result.metadata.url

        self.execute_save(
            db_to_use[Collections.tokens_token_addresses], d, token_address
        )

    def save_operator(
        self,
        db_to_use: dict[Collections, Collection],
        instance_address: str,
        result: tokenMetadataEvent,
        height: int,
    ):
        token_address = f"{instance_address}-{result.token_id}"
        d = db_to_use[Collections.tokens_token_addresses].find_one(
            {"_id": token_address}
        )
        if not d:
            d = MongoTypeTokenAddress(
                **{
                    "_id": token_address,
                    "contract": instance_address,
                    "token_id": result.token_id,
                    "last_height_processed": height,
                }
            )
        else:
            d = MongoTypeTokenAddress(**d)

        d.metadata_url = result.metadata.url

        self.execute_save(
            db_to_use[Collections.tokens_token_addresses], d, token_address
        )

    def save_transfer(
        self,
        db_to_use: dict[Collections, Collection],
        instance_address: str,
        result: transferEvent,
        height: int,
    ):
        token_address = f"{instance_address}-{result.token_id}"
        d = db_to_use[Collections.tokens_token_addresses].find_one(
            {"_id": token_address}
        )
        if not d:
            return None

        d = MongoTypeTokenAddress(**d)

        try:
            token_holders: dict[CCD_AccountAddress, str] = d.token_holders
        except:
            console.log(
                f"{result.tag}: {token_address} | {d} has no field token_holders?"
            )
            Exception(
                console.log(
                    f"{result.tag}: {token_address} | {d} has no field token_holders?"
                )
            )

        token_holders[result.to_address] = str(
            int(token_holders.get(result.to_address, "0")) + result.token_amount
        )
        try:
            token_holders[result.from_address] = str(
                int(token_holders.get(result.from_address, None)) - result.token_amount
            )
            if int(token_holders[result.from_address]) >= 0:
                d.token_holders = token_holders
                d.last_height_processed = height
                self.execute_save(
                    db_to_use[Collections.tokens_token_addresses], d, token_address
                )

                self.copy_token_holders_state_to_address_and_save(
                    db_to_use, d, result.from_address
                )
                self.copy_token_holders_state_to_address_and_save(
                    db_to_use, d, result.to_address
                )

        except:
            if result.token_amount > 0:
                console.log(
                    f"{result.tag}: {result.from_address} is not listed as token holder for {token_address}?"
                )

    def save_burn(
        self,
        db_to_use: dict[Collections, Collection],
        instance_address: str,
        result: burnEvent,
        height: int,
    ):
        token_address = f"{instance_address}-{result.token_id}"

        d = MongoTypeTokenAddress(
            **db_to_use[Collections.tokens_token_addresses].find_one(
                {"_id": token_address}
            )
        )

        token_holders: dict[CCD_AccountAddress, str] = d.token_holders
        try:
            token_holders[result.from_address] = str(
                int(token_holders.get(result.from_address, "0")) - result.token_amount
            )
            if token_holders[result.from_address] == str(0):
                del token_holders[result.from_address]

            d.token_amount = str((int(d.token_amount) - result.token_amount))
            d.token_holders = token_holders
            d.last_height_processed = height

            if int(d.token_amount) >= 0:
                self.execute_save(
                    db_to_use[Collections.tokens_token_addresses], d, token_address
                )
                self.copy_token_holders_state_to_address_and_save(
                    db_to_use, d, result.from_address
                )

        except:
            console.log(
                f"{result.tag}: {result.from_address} is not listed as token holder for {token_address}?"
            )
            # exit

    def save_logged_event(
        self,
        db_to_use,
        tag_: int,
        result: Union[
            mintEvent, burnEvent, transferEvent, updateOperatorEvent, tokenMetadataEvent
        ],
        instance_address: str,
        event: str,
        height: int,
        tx_hash: str,
        tx_index: int,
        ordering: int,
        _id_postfix: str,
    ) -> Union[ReplaceOne, None]:
        if tag_ in [255, 254, 253, 252, 251, 250]:
            if tag_ == 252:
                token_address = f"{instance_address}-operator"
            elif tag_ == 250:
                token_address = f"{instance_address}-nonce"
            else:
                token_address = f"{instance_address}-{result.token_id}"
            _id = f"{height}-{token_address}-{event}-{_id_postfix}"
            if result:
                result_dict = result.dict()
            else:
                result_dict = {}
            if "token_amount" in result_dict:
                result_dict["token_amount"] = str(result_dict["token_amount"])

            d = {
                "_id": _id,
                "logged_event": event,
                "result": result_dict,
                "tag": tag_,
                "event_type": LoggedEvents(tag_).name,
                "block_height": height,
                "tx_hash": tx_hash,
                "tx_index": tx_index,
                "ordering": ordering,
                "token_address": token_address,
                "contract": instance_address,
            }
            return ReplaceOne(
                {"_id": _id},
                replacement=d,
                upsert=True,
            )

        else:
            return None

    def execute_logged_event(
        self,
        db_to_use,
        tag_: int,
        result: Union[mintEvent, burnEvent, transferEvent, tokenMetadataEvent],
        instance_address: str,
        height: int,
    ):
        if tag_ == 255:
            self.save_transfer(db_to_use, instance_address, result, height)
        elif tag_ == 254:
            self.save_mint(db_to_use, instance_address, result, height)
        elif tag_ == 253:
            self.save_burn(db_to_use, instance_address, result, height)
        elif tag_ == 252:
            pass
            # we only save the logged event, but to not process this in
            # token_address or accounts.
            # save_operator(db_to_use, instance_address, result, height)
        elif tag_ == 251:
            self.save_metadata(db_to_use, instance_address, result, height)
        elif tag_ == 250:
            pass  # nonceEvent

    def process_event(
        self,
        db_to_use,
        instance_address: str,
        event: str,
        height: int,
        tx_hash: str,
        tx_index: int,
        ordering: int,
        _id_postfix: str,
    ):
        tag_, result = self.process_log_events(event)
        logged_event = None
        token_address = None
        if result:
            # if tag_ in [255, 254, 253, 252, 251, 250]:
            if tag_ in [255, 254, 253, 251]:
                # if tag_ == 252:
                #     token_address = f"{instance_address}-operator"
                # elif tag_ == 250:
                #     token_address = f"{instance_address}-nonce"

                # else:
                token_address = f"{instance_address}-{result.token_id}"
                logged_event_id = f"{height}-{token_address}-{event}-{_id_postfix}"
                # stored_logged_event = db_to_use[Collections.tokens_logged_events].find_one(
                #     {"_id": logged_event_id}
                # )
                # if not stored_logged_event:
                # we have not processed this log event before,
                # so we can safely process the current logged event
                logged_event = self.save_logged_event(
                    db_to_use,
                    tag_,
                    result,
                    instance_address,
                    event,
                    height,
                    tx_hash,
                    tx_index,
                    ordering,
                    _id_postfix,
                )

        return tag_, logged_event, token_address
        #     # self.execute_logged_event(db_to_use, tag_, result, instance_address, height)

        # else:
        #     console.log(f"Re-processing logged event: {logged_event_id}")
        #     # we are (re-) processing a block that is earlier than the last block
        #     # on which the state is based. We need to recalculate state from the beginning.
        #     self.save_logged_event(
        #         db_to_use,
        #         tag_,
        #         result,
        #         instance_address,
        #         event,
        #         height,
        #         tx_hash,
        #         tx_index,
        #         ordering,
        #         _id_postfix,
        #     )
        # self.restore_state_for_token_address(db_to_use, token_address)

        # # we will read all logged events for this token address from the collection
        # # and process them in order.

        # stored_logged_events_for_token_address = [
        #     MongoTypeLoggedEvent(**x)
        #     for x in db_to_use[Collections.tokens_logged_events]
        #     .find({"token_address": token_address})
        #     .sort(
        #         [
        #             ("block_height", ASCENDING),
        #             ("tx_index", ASCENDING),
        #             ("ordering", ASCENDING),
        #         ]
        #     )
        # ]
        # for logged_event in stored_logged_events_for_token_address:
        #     if logged_event.tag == 255:
        #         result = transferEvent(**logged_event.result)
        #     elif logged_event.tag == 254:
        #         result = mintEvent(**logged_event.result)
        #     elif logged_event.tag == 253:
        #         result = burnEvent(**logged_event.result)
        #     elif logged_event.tag == 252:
        #         result = updateOperatorEvent(**logged_event.result)
        #     elif logged_event.tag == 251:
        #         result = tokenMetadataEvent(**logged_event.result)

        #     self.execute_logged_event(
        #         db_to_use,
        #         logged_event.tag,
        #         result,
        #         logged_event.contract,
        #         logged_event.block_height,
        #     )

    ###############

    def standard_identifier(self, identifier: StandardIdentifiers) -> bytes:
        si = io.BytesIO()
        # write the length of ASCII characters for the identifier
        number = len(identifier.value)
        byte_array = number.to_bytes(1, "little")
        si.write(byte_array)
        # write the identifier
        si.write(bytes(identifier.value, encoding="ASCII"))
        # convert to bytes
        return si.getvalue()

    def supports_parameter(self, standard_identifier: StandardIdentifiers) -> bytes:
        sp = io.BytesIO()
        # write the number of standardIdentifiers present
        number = 1
        byte_array = number.to_bytes(2, "little")
        sp.write(byte_array)
        # write the standardIdentifier
        sp.write(self.standard_identifier(standard_identifier))
        # convert to bytes
        return sp.getvalue()

    def support_result(self, bs: io.BytesIO):
        t = int.from_bytes(bs.read(2), byteorder="little")
        if t == 0:
            return t, "Standard is not supported"
        elif t == 1:
            return t, "Standard is supported by this contract"
        elif t == 2:
            contracts = []
            n = int.from_bytes(bs.read(1), byteorder="little")
            for _ in range(n):
                contracts.append(self.contract_address(bs))
                return (
                    t,
                    "Standard is supported by using one of these contract addresses: "
                    + [x for x in contracts],
                )

    def supports_response(self, res: bytes):
        bs = io.BytesIO(bytes.fromhex(res.decode()))
        if bs.getbuffer().nbytes > 0:
            n = int.from_bytes(bs.read(2), byteorder="big")
            responses = []
            for _ in range(n):
                responses.append(self.support_result(bs))
            if len(responses) > 0:
                return responses[0]
            else:
                return False, "Lookup Failure"
        else:
            return False, "Lookup Failure"

    def supports_standard(self, standard_identifier: StandardIdentifiers) -> bool:
        parameter_bytes = self.supports_parameter(standard_identifier)

        ii = self.grpcclient.invoke_instance(
            "last_final",
            self.instance_index,
            self.instance_subindex,
            self.entrypoint,
            parameter_bytes,
            self.net,
        )

        res = ii.success.return_value
        support_result, support_result_text = self.supports_response(res)

        return support_result == 1

    def supports_standards(
        self, standard_identifiers: list[StandardIdentifiers]
    ) -> bool:
        support = False
        for si in standard_identifiers:
            parameter_bytes = self.supports_parameter(si)

            ii = self.grpcclient.invoke_instance(
                "last_final",
                self.instance_index,
                self.instance_subindex,
                self.entrypoint,
                parameter_bytes,
                self.net,
            )

            res = ii.success.return_value
            support_result, support_result_text = self.supports_response(res)

            support = support_result == 1
        return support

    def balanceOf(self, block_hash: str, tokenID: str, account_id: str):
        parameter_bytes = self.balanceOfParameter(tokenID, account_id)

        ii = self.grpcclient.invoke_instance(
            block_hash,
            self.instance_index,
            self.instance_subindex,
            self.entrypoint,
            parameter_bytes,
            self.net,
        )

        res = ii.success.return_value
        support_result = self.balanceOfResponse(res)

        return support_result, ii

    # def supports_parameter(self, standard_identifier: StandardIdentifiers) -> bytes:
    #     sp = io.BytesIO()
    #     # write the number of standardIdentifiers present
    #     number = 2
    #     byte_array = number.to_bytes(1, "little")
    #     sp.write(byte_array)

    #     # write the standardIdentifier
    #     si = io.BytesIO()
    #     # write the length of ASCII characters for the identifier
    #     identifier = StandardIdentifiers.CIS_1
    #     number = len(identifier.value)
    #     byte_array = number.to_bytes(1, "little")
    #     si.write(byte_array)
    #     # write the identifier
    #     si.write(bytes(identifier.value, encoding="ASCII"))
    #     sp.write(si)
    #     si = io.BytesIO()
    #     identifier = StandardIdentifiers.CIS_1
    #     # write the length of ASCII characters for the identifier
    #     number = len(identifier.value)
    #     byte_array = number.to_bytes(1, "little")
    #     si.write(byte_array)
    #     # write the identifier
    #     si.write(bytes(identifier.value, encoding="ASCII"))
    #     sp.write(si)
    #     # convert to bytes
    #     return sp.getvalue()

    # def supportsParameter(self) -> bytes:
    #     sp = io.BytesIO()
    #     # write the number of standardIdentifiers present
    #     number = len(StandardIdentifiers)
    #     byte_array = number.to_bytes(2, "little")
    #     sp.write(byte_array)

    #     for standard in StandardIdentifiers:
    #         # write the standardIdentifier
    #         sp.write(self.standardIdentifier(standard.value))
    #     # convert to bytes
    #     return sp.getvalue()

    def account_address(self, bs: io.BytesIO):
        addr = bs.read(32)
        return base58.b58encode_check(b"\x01" + addr).decode()

    def contract_address(self, bs: io.BytesIO):
        return int.from_bytes(bs.read(8), byteorder="little"), int.from_bytes(
            bs.read(8), byteorder="little"
        )

    def address(self, bs: io.BytesIO):
        t = int.from_bytes(bs.read(1), byteorder="little")
        if t == 0:
            return self.account_address(bs)
        elif t == 1:
            return self.contract_address(bs)
        else:
            raise Exception("invalid type")

    def receiver(self, bs: io.BytesIO):
        t = int.from_bytes(bs.read(1), byteorder="little")
        if t == 0:
            return self.account_address(bs)
        elif t == 1:
            return self.contract_address(bs), self.receiveHookName(bs)
        else:
            raise Exception("invalid type")

    def url(self, n: int, bs: io.BytesIO):
        data = bs.read(n)
        return data

    def metadataChecksum(self, bs: io.BytesIO):
        t = int.from_bytes(bs.read(1), byteorder="little")
        if t == 0:
            return None
        elif t == 1:
            return bs.read(32)
        else:
            raise Exception("invalid type")

    def metadataUrl(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(2), byteorder="little")
        url = bs.read(n).decode()
        # checksum = self.metadataChecksum(bs)
        return MetadataUrl(**{"url": url, "checksum": None})

    def tokenAmount(self, bs: io.BytesIO):
        return int.from_bytes(bs.read(8), byteorder="little")

    def receiveHookName(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(2), byteorder="little")
        name = bs.read(n)
        return bytes.decode(name, "UTF-8")

    def additionalData(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(2), byteorder="little")
        data = bs.read(n)
        return data

    def tokenID(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(1), byteorder="little")
        return bytes.hex(bs.read(n))

    def balanceOfQuery(self, tokenID: str, address: str):
        sp = io.BytesIO()

        tokenID = self.generate_tokenID(tokenID)
        address = self.generate_address(address)
        sp.write(tokenID)
        sp.write(address)
        return sp.getvalue()

    def balanceOfParameter(self, tokenID: str, address: str):
        sp = io.BytesIO()

        sp.write(int(1).to_bytes(2, "little"))
        sp.write(self.balanceOfQuery(tokenID, address))
        # convert to bytes
        return sp.getvalue()

    def balanceOfResponse(self, res: bytes):
        bs = io.BytesIO(bytes.fromhex(res.decode()))
        n = int.from_bytes(bs.read(2), byteorder="little")
        result = self.tokenAmount(bs)

        return result

    def generate_tokenID(self, tokenID: str):
        sp = io.BytesIO()
        tokenID_in_bytes = bytes.fromhex(tokenID)
        sp.write(int(len(tokenID_in_bytes)).to_bytes(1, "little"))
        sp.write(tokenID_in_bytes)
        return sp.getvalue()

    def generate_account_address(self, address: str):
        return bytearray(base58.b58decode_check(address)[1:])

    def generate_contract_address(self, address: str):
        # TODO
        sp = io.BytesIO()

        address_in_bytes = bytes.fromhex(address.encode("utf-8"))

        sp.write(address_in_bytes)
        return sp.getvalue()

    def generate_address(self, address: str):
        sp = io.BytesIO()

        if len(address) == 50:
            sp.write(int(0).to_bytes(1, "little"))
            sp.write(self.generate_account_address(address))
        else:
            sp.write(int(1).to_bytes(1, "little"))
            sp.write(self.generate_contract_address(address))

        return sp.getvalue()

    def invoke_token_metadataUrl(self, tokenID: str) -> bool:
        parameter_bytes = self.tokenMetadataParameter(tokenID)

        ii = self.grpcclient.invoke_instance(
            "last_final",
            self.instance_index,
            self.instance_subindex,
            self.entrypoint,
            parameter_bytes,
            self.net,
        )

        res = ii.success.return_value
        return self.tokenMetadataResultParameter(res)

    def viewOwnerHistoryRequest(self, tokenID: str):
        return self.generate_tokenID(tokenID)

    def viewOwnerHistoryResponse(self, res: bytes):
        bs = io.BytesIO(bytes.fromhex(res.decode()))
        n = int.from_bytes(bs.read(1), byteorder="little")
        own_str = bs.read(3)
        results = []
        for _ in range(0, n):
            results.append(self.address(bs))

        return results

    def tokenMetadataParameter(self, tokenID: str):
        sp = io.BytesIO()
        sp.write(int(1).to_bytes(2, "little"))
        sp.write(self.generate_tokenID(tokenID))
        return sp.getvalue()

    def metadata_result(self, bs: bytes):
        n = int(bs[:2].decode("ASCII"))
        bs = io.BytesIO(bs)
        bs.read(2)
        url = self.url(n, bs)
        return url

    def metadata_response(self, bs: bytes):
        # bs: io.BytesIO = io.BytesIO(bs)
        if len(bs) > 0:
            n = int(bs[:2].decode("ASCII"))
            # n = int.from_bytes(bs.read(2), byteorder="big")
            responses = []
            for _ in range(n):
                responses.append(self.metadata_result(bs))
            return responses[0]
        else:
            return False, "Lookup Failure"

    def tokenMetadataResultParameter(self, res: bytes):
        bs = io.BytesIO(bytes.fromhex(res.decode()))
        n = int.from_bytes(bs.read(2), byteorder="little")
        results = []
        for _ in range(0, n):
            results.append(self.metadataUrl(bs))

        return results

    def operator_update(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(1), byteorder="little")
        if n == 0:
            return "Remove operator"
        elif n == 1:
            return "Add operator"

    def token_id(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(1), byteorder="little")
        return bytes.hex(bs.read(n))

    def nonce(self, bs: io.BytesIO):
        return bytes.hex(bs.read(8))

    def token_amount(self, bs: io.BytesIO):
        x = int.from_bytes(bs.read(1), byteorder="little")
        if x < math.pow(2, 7):
            return x
        else:
            m = self.token_amount(bs)
            return (x - math.pow(2, 7)) + (math.pow(2, 7) * m)

    def transferEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        token_id_ = self.token_id(bs)
        amount_ = self.token_amount(bs)

        from_ = self.address(bs)
        if type(from_) is not tuple:
            # it's an account address
            if len(from_) != LEN_ACCOUNT_ADDRESS:
                return None

        if type(from_) == tuple:
            from_ = f"<{from_[0]},{from_[1]}>"
        to_ = self.address(bs)
        if type(to_) is not tuple:
            # it's an account address
            if len(to_) != LEN_ACCOUNT_ADDRESS:
                return None

        if type(to_) == tuple:
            to_ = f"<{to_[0]},{to_[1]}>"

        return transferEvent(
            **{
                "tag": tag_,
                "token_id": token_id_,
                "token_amount": amount_,
                "from_address": from_,
                "to_address": to_,
            }
        )

    def updateOperatorEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        # token_id_ = self.token_id(bs)
        update_ = self.operator_update(bs)

        owner_ = self.address(bs)
        if type(owner_) is not tuple:
            # it's an account address
            if len(owner_) != LEN_ACCOUNT_ADDRESS:
                return None

        if type(owner_) == tuple:
            owner_ = f"<{owner_[0]},{owner_[1]}>"
        operator_ = self.address(bs)
        if type(operator_) is not tuple:
            # it's an account address
            if len(operator_) != LEN_ACCOUNT_ADDRESS:
                return None

        if type(operator_) == tuple:
            operator_ = f"<{operator_[0]},{operator_[1]}>"

        return updateOperatorEvent(
            **{
                "tag": tag_,
                "operator_update": update_,
                "owner": owner_,
                "operator": operator_,
            }
        )

    def mintEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        token_id_ = self.token_id(bs)
        amount_ = self.token_amount(bs)
        to_ = self.address(bs)
        if type(to_) is not tuple:
            # it's an account address
            if len(to_) != LEN_ACCOUNT_ADDRESS:
                return None

        if type(to_) == tuple:
            to_ = f"<{to_[0]},{to_[1]}>"

        return mintEvent(
            **{
                "tag": tag_,
                "token_id": token_id_,
                "token_amount": amount_,
                "to_address": to_,
            }
        )

    def burnEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        token_id_ = self.token_id(bs)
        amount_ = self.token_amount(bs)
        from_ = self.address(bs)
        if type(from_) is not tuple:
            # it's an account address
            if len(from_) != LEN_ACCOUNT_ADDRESS:
                return None

        if type(from_) == tuple:
            from_ = f"<{from_[0]},{from_[1]}>"

        return burnEvent(
            **{
                "tag": tag_,
                "token_id": token_id_,
                "token_amount": amount_,
                "from_address": from_,
            }
        )

    def tokenMetaDataEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")

        token_id_ = self.token_id(bs)
        metadata_ = self.metadataUrl(bs)

        return tokenMetadataEvent(
            **{
                "tag": tag_,
                "token_id": token_id_,
                "metadata": metadata_,
            }
        )

    def nonceEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")

        nonce_ = self.nonce(bs)
        sponsoree_ = self.account_address(bs)

        return nonceEvent(
            **{
                "tag": tag_,
                "nonce": nonce_,
                "sponsoree": sponsoree_,
            }
        )

    def process_log_events(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        if tag_ == 255:
            try:
                event = self.transferEvent(hexParameter)
                return tag_, event
            except:
                return tag_, None
        elif tag_ == 254:
            try:
                event = self.mintEvent(hexParameter)
                return tag_, event
            except:
                return tag_, None
        elif tag_ == 253:
            try:
                event = self.burnEvent(hexParameter)
                return tag_, event
            except:
                return tag_, None
        elif tag_ == 252:
            try:
                event = self.updateOperatorEvent(hexParameter)
                return tag_, event
            except:
                return tag_, None
        elif tag_ == 251:
            try:
                event = self.tokenMetaDataEvent(hexParameter)
                return tag_, event
            except:
                return tag_, None
        elif tag_ == 250:
            try:
                event = self.nonceEvent(hexParameter)
                return tag_, event
            except:
                return tag_, None
        else:
            return tag_, f"Custom even with tag={tag_}."
