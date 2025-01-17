import pytest

from zkevm_specs.evm_circuit import (
    ExecutionState,
    StepState,
    verify_steps,
    Tables,
    Block,
    Bytecode,
    RWDictionary,
)
from zkevm_specs.util import Word, U64, U160, U256
from typing import Union
from common import rand_address, rand_range


TESTING_DATA_U160 = (0x030201, rand_address())


@pytest.mark.parametrize("coinbase", TESTING_DATA_U160)
def test_coinbase(coinbase: U160):
    block = Block(coinbase=coinbase)

    bytecode = Bytecode().coinbase()

    verify_block_ctx(
        block,
        bytecode,
        coinbase,
    )


TESTING_DATA_U64 = (0, 1, 2**63 - 1, rand_range(2**63))


@pytest.mark.parametrize("timestamp", TESTING_DATA_U64)
def test_timestamp(timestamp: U64):
    block = Block(timestamp=timestamp)

    bytecode = Bytecode().timestamp()

    verify_block_ctx(
        block,
        bytecode,
        timestamp,
    )


@pytest.mark.parametrize("number", TESTING_DATA_U64)
def test_number(number: U64):
    block = Block(number=number)

    bytecode = Bytecode().number()

    verify_block_ctx(
        block,
        bytecode,
        number,
    )


@pytest.mark.parametrize("gaslimit", TESTING_DATA_U64)
def test_gaslimit(gaslimit: U64):
    block = Block(gas_limit=gaslimit)

    bytecode = Bytecode().gaslimit()

    verify_block_ctx(
        block,
        bytecode,
        gaslimit,
    )


TESTING_DATA_U256 = (0, 1, 2**256 - 1)


@pytest.mark.parametrize("prev_randao", TESTING_DATA_U256)
def test_prev_randao(prev_randao: U256):
    block = Block(prev_randao=prev_randao)

    bytecode = Bytecode().prevrandao()

    verify_block_ctx(
        block,
        bytecode,
        prev_randao,
    )


@pytest.mark.parametrize("basefee", TESTING_DATA_U256)
def test_basefee(basefee: U256):
    block = Block(base_fee=basefee)

    bytecode = Bytecode().basefee()

    verify_block_ctx(
        block,
        bytecode,
        basefee,
    )


@pytest.mark.parametrize("chainid", TESTING_DATA_U64)
def test_chainid(chainid: U64):
    block = Block(chainid=chainid)

    bytecode = Bytecode().chainid()

    verify_block_ctx(
        block,
        bytecode,
        chainid,
    )


def verify_block_ctx(
    block: Block,
    bytecode: Bytecode,
    op: Union[U64, U160, U256],
):
    bytecode_hash = Word(bytecode.hash())

    tables = Tables(
        block_table=set(block.table_assignments()),
        tx_table=set(),
        bytecode_table=set(bytecode.table_assignments()),
        rw_table=set(RWDictionary(9).stack_write(1, 1023, Word(op)).rws),
    )

    verify_steps(
        tables=tables,
        steps=[
            StepState(
                execution_state=ExecutionState.BlockCtx,
                rw_counter=9,
                call_id=1,
                is_root=True,
                is_create=False,
                code_hash=bytecode_hash,
                program_counter=0,
                stack_pointer=1024,
                gas_left=2,
            ),
            StepState(
                execution_state=ExecutionState.STOP,
                rw_counter=10,
                call_id=1,
                is_root=True,
                is_create=False,
                code_hash=bytecode_hash,
                program_counter=1,
                stack_pointer=1023,
                gas_left=0,
            ),
        ],
    )
