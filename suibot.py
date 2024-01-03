from pysui import SuiConfig, SyncClient, ObjectID
from pysui.sui.sui_config import SuiConfig, SignatureScheme
from pysui.sui.sui_builders.get_builders import *
from pysui.sui.sui_txn import SyncTransaction
from pysui.sui.sui_txresults.package_meta import (
    SuiMoveScalarArgument,
    SuiMoveVector,
    SuiParameterReference,
    SuiParameterStruct
)
from pysui.sui.sui_types.scalars import (
    SuiString,
    SuiU8,
    SuiU16,
    SuiU32,
    SuiU64,
    SuiU128,
    SuiU256,
)
from typing import Any
import json
import time

# Lookup untuk tipe skalar integer
_INT_SCALAR_LOOKUP: dict[str, Any] = {
    "U8": SuiU8,
    "U16": SuiU16,
    "U32": SuiU32,
    "U64": SuiU64,
    "U128": SuiU128,
    "U1256": SuiU256,
}

class Mint:
    def __init__(self, mint_fee) -> None:
        self.keys = []
        self.addresses = []
        for k in keys:
            self.keys.append(k['key'])
            self.addresses.append(k['address'])
        
        self.mint_fee = mint_fee

    def init_address(self):
        self.set_action_address(0)
        balance = self.get_balance()
        sui_ob = []
        for b in balance:
            if b['coinType'] == '0x2::sui::SUI':
                sui_ob.append(b)
        if len(sui_ob) > 2:
            primary_coin = sui_ob[1]['coinObjectId']
            coin_to_merge = []
            for i in range(2, len(sui_ob)):
                coin_to_merge.append(sui_ob[i]['coinObjectId'])
            self.merge_coin(primary_coin, coin_to_merge)
            
        balance = self.get_balance()
        self.transfer_coin(balance)
        print("Inisialisasi alamat selesai")

    def set_action_address(self, number):
        self.cfg = SuiConfig.user_config(rpc_url=rpc_url, prv_keys=[{
                    'wallet_key': self.keys[number],
                    'key_scheme': SignatureScheme.ED25519
                }], ws_url=ws_url)
        self.client = SyncClient(self.cfg)

    def get_balance(self):
        result = self.client.execute(GetAllCoins(owner=self.cfg.active_address))
        if result.is_ok():
            re = json.loads(result.result_data.to_json(indent=2))
            return re['data']

    def merge_coin(self, primary_coin, coin_to_merge):
        for_owner = self.client.config.active_address
        
        txn = SyncTransaction(client=self.client, initial_sender=for_owner)
        txn.merge_coins(merge_to=primary_coin, merge_from=coin_to_merge)
        txn.execute()

    def transfer_coin(self, balance):
        sui_ob = []
        for b in balance:
            if b['coinType'] == '0x2::sui::SUI':
                sui_ob.append(b)
        addresses_amount = len(self.addresses)
        if len(sui_ob) == 1:
            one_address_amount = int(int(sui_ob[0]['balance']) / addresses_amount)
            for a in self.addresses[1:]:
                self.do_transfer(a, sui_ob[0]['coinObjectId'], one_address_amount)
        if len(sui_ob) == 2:
            larger_object = max(sui_ob, key=lambda obj: int(obj['balance']))
            one_address_amount = int(int(larger_object['balance']) / addresses_amount)
            for a in self.addresses[1:]:
                self.do_transfer(a, larger_object['coinObjectId'], one_address_amount)
        
        print("Pembagian SUI selesai")

    def do_transfer(self, recipient, from_coin, amount):
        for_owner = self.client.config.active_address
        txn = SyncTransaction(client=self.client, initial_sender=for_owner)
        txn.transfer_sui(
            recipient=ObjectID(recipient),
            from_coin=from_coin,
            amount=int(amount),
        )
        txn.execute()
        time.sleep(5)

    def select_sui_ob(self, balance):
        sui_ob = []
        for b in balance:
            if b['coinType'] == '0x2::sui::SUI':
                sui_ob.append(b)
        return sui_ob
    
    def select_max_object(self, sui_ob):
        max_obj = {
            'id': '',
            'balance': 0
        }
        for obj in sui_ob:
            if int(obj['balance']) > max_obj['balance']:
                max_obj = {
                    'id': obj['coinObjectId'],
                    'balance': int(obj['balance'])
                }
        
        return max_obj
                
    def mint(self, mint_interval):
        for i in range(0, len(keys)):
            try:
                print(f"Proses mint ke alamat ke-{i}")
                self.set_action_address(i)
                self.do_mint(keys[i])
                time.sleep(mint_interval)
            except Exception as e:
                print(f'Error: {e}')
            
    def do_mint(self, address):
        print(f'Minting saat ini: {self.client.config.active_address}')
        coins = self.get_balance()
        sui_ob = self.select_sui_ob(coins)
        if len(sui_ob) >= 2:
            max_obj = self.select_max_object(sui_ob)
            if max_obj['balance'] > int(self.mint_fee * 10**9):
                self.move_call(max_obj)
            else:
                print("Jumlah SUI dalam alamat kurang dari 0.1")
                
        else:
            print("Tidak cukup objek SUI, harap kirim SUI ke alamat ini sebagai gasfee")
        
    def _recon_args(self, args: list[str], parms: list) -> list[Any]:
        """."""
        assert len(args) == len(parms)
        res_args: list[Any] = []
        for index, parm in enumerate(parms):
            if isinstance(parm, SuiParameterReference):
                res_args.append(ObjectID(args[index]))
            elif isinstance(parm, SuiMoveScalarArgument):
                if parm.scalar_type[0] == "U":
                    res_args.append(_INT_SCALAR_LOOKUP[parm.scalar_type](int(args[index])))
                else:
                    res_args.append(args[index])
            elif isinstance(parm, SuiParameterStruct):
                res_args.append(ObjectID(args[index]))
            elif isinstance(parm, SuiMoveVector):
                res_args.append(SuiString(args[index]))
        return res_args

    def move_call(self, max_obj):
        """Invoke a Sui move smart contract function."""
        for_owner = self.client.config.active_address

        target = '0x830fe26674dc638af7c3d84030e2575f44a2bdc1baa1f4757cfe010a4b106b6a::movescription::mint'
        arguments = [
            '0xfa6f8ab30f91a3ca6f969d117677fb4f669e08bbeed815071cf38f4d19284199',
            'MOVE',
            max_obj['id'],
            '0x0000000000000000000000000000000000000000000000000000000000000006'
        ]
        
        txn = SyncTransaction(client=self.client, initial_sender=for_owner)
        (
            _target_id,
            _module_id,
            _function_id,
            parameters,
            _res_count,
        ) = txn._move_call_target_cache(target)
        
        arguments = self._recon_args(arguments, parameters[:-1])
        
        res = txn.move_call(
            target=target, arguments=arguments)
        
        txn.execute()

# URL untuk node blockchain, ganti jika node tidak tersedia
rpc_url = "https://sui-rpc.publicnode.com"
ws_url = "wss://sui-rpc.publicnode.com/websocket"

# Parameter input
mint_fee = 0.1
daily_mint_times = 10

# Isi dengan key dan alamat yang sesuai
keys = [
    {
        'key': 'private_key_1',
        'address': '0x1234567890abcdefABCDEF1234567890abcdefAB'
    },
    # Tambahkan kunci dan alamat lainnya jika diperlukan
]



mint_interval = 60 / daily_mint_times
print(f'Melakukan mint setiap {mint_interval} detik')

# Inisialisasi dan minting
m = Mint(mint_fee) 
m.init_address()
while True:
    m.mint(mint_interval)
    ## Setiap kali seluruh alamat melakukan mint
