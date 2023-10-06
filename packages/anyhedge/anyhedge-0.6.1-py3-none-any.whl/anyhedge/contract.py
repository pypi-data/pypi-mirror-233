# Built-in imports
from __future__ import annotations  # allow pre-definition use of types
from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from math import ceil, floor
from typing import Sequence, Type

# Local imports
from . import validators
from .bch_primitives import (
    DUST,
    SATS_PER_BCH,
    SCRIPT_INT_MAX_WHEN_JAVASCRIPT,
    PublicKey,
    Sats,
    ScriptTimestamp,
    UtxoSats,
)
from .fee import (
    aggregate_fee_sats_to_role,
    FeeAgreement,
)
from .javascript import round_half_up
from .oracle import (
    oracle_pubkey_to_unit_class,
    OracleUnit,
    ScriptPriceInOracleUnitsPerBch,
)
from .role import Role


class UnredeemableError(Exception):
    pass


class Side(str, Enum):
    SHORT = 'Short'
    LONG = 'Long'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()

    @property
    def other_side(self) -> Side:
        # use a lookup to ensure KeyError with unknown value
        return {Side.SHORT: Side.LONG, Side.LONG: Side.SHORT}[self]

    @classmethod
    def from_string(cls, side_string: str) -> Side:
        # use a lookup to ensure KeyError with unknown value
        lookup = {
            'short': cls.SHORT,
            'hedge': cls.SHORT,
            'long': cls.LONG,
        }
        return lookup[side_string.lower()]


class NominalOracleUnitsXSatsPerBch(int):
    def __init__(self, value):
        super().__init__()
        validators.instance(value, int)  # i.e. don't allow silent coercion
        validators.less_equal(self, SCRIPT_INT_MAX_WHEN_JAVASCRIPT)
        validators.greater_equal(self, SATS_PER_BCH)  # i.e. minimum is 1 nominal oracle unit


class ShortLeverage(float):
    min_allowed: float = 1.0
    max_allowed: float = 50.0

    def __init__(self, _):
        super().__init__()
        validators.less_equal(self, self.max_allowed * 1.00001)  # some room for floating point error
        validators.greater_equal(self, self.min_allowed)  # strict boundary for flat hedge position, below one is undefined


class LongLeverage(float):
    min_allowed: float = 1.1
    max_allowed: float = 50.0

    def __init__(self, _):
        super().__init__()
        validators.less_equal(self, self.max_allowed * 1.00001)  # some room for floating point error
        validators.greater_equal(self, self.min_allowed * 0.99999)  # some room for floating point error


# TODO: add "forced maturation" to differentiate from normal case in records?
class RedemptionType(str, Enum):
    LIQUIDATION = 'Liquidation'
    MATURATION = 'Maturation'
    MUTUAL = 'Mutual'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_string(cls, redemption_type_string: str) -> RedemptionType:
        # use a strict lookup (with lowercase) to ensure KeyError with unknown value
        lookup = {
            'liquidation': cls.LIQUIDATION,
            'maturation': cls.MATURATION,
            'mutual': cls.MUTUAL,
        }
        redemption_type = lookup[redemption_type_string.lower()]
        return redemption_type


@dataclass(frozen=True)
class ContractProposal:
    """Details of a proposed contract between a maker and taker. Does not include any funding oriented details such as fees."""
    # Address (unvalidated, use empty string when unknown)
    address: str

    # Time
    start_timestamp: ScriptTimestamp
    maturity_timestamp: ScriptTimestamp

    # Position settings
    nominal_oracleUnits_x_satsPerBch: NominalOracleUnitsXSatsPerBch
    cost_sats_for_nominal_value_at_high_liquidation: Sats
    total_input_sats: UtxoSats

    # Start price is not an actual contract parameter, but one of start price, leverage,
    # or separated side inputs are needed in order for the contract to be fully specified.
    start_price_oracleUnits_per_bch: ScriptPriceInOracleUnitsPerBch

    # Liquidation prices
    high_liquidation_price_oracleUnits_per_bch: ScriptPriceInOracleUnitsPerBch
    low_liquidation_price_oracleUnits_per_bch: ScriptPriceInOracleUnitsPerBch

    # Price oracle
    oracle_public_key: PublicKey

    # Relationship between Roles and Sides
    maker_side: Side

    def __post_init__(self):
        # Note: can make validation a switch with unsafe construction if needed
        self.validate()

    ###############
    # Parameterized Input Values
    ###############
    @cached_property
    def _input_sats_lookup(self) -> dict[(Role | None, Side | None), UtxoSats | None]:
        # Total sats is a hard contract parameter established by whatever method during construction.
        # Here we split it back into its two parts: short side, and for strict numerical safety, everything else as long side

        # The definition of short's input is that it needs to be enough to fully cover the worst case outcome of selling low
        # and buying high. That amount is the difference between the cost of the nominal assets at short/high liquidation vs
        # the cost at the start price. Note that in our inverted price scheme of BCH/Asset, the lower cost is at the higher price.
        short_input_sats = UtxoSats(self.cost_sats_for_nominal_value_at_start - self.cost_sats_for_nominal_value_at_high_liquidation)

        # Long input sats is everything needed to cover the rest of the total
        long_input_sats = UtxoSats(self.total_input_sats - short_input_sats)

        return {
            (None,       None):       self.total_input_sats,
            (None,       Side.SHORT): short_input_sats,
            (None,       Side.LONG):  long_input_sats,
            (Role.MAKER, None):       short_input_sats if self.maker_side == Side.SHORT else long_input_sats,
            (Role.MAKER, Side.SHORT): short_input_sats if self.maker_side == Side.SHORT else None,
            (Role.MAKER, Side.LONG):  long_input_sats  if self.maker_side == Side.LONG  else None,
            (Role.TAKER, None):       short_input_sats if self.taker_side == Side.SHORT else long_input_sats,
            (Role.TAKER, Side.SHORT): short_input_sats if self.taker_side == Side.SHORT else None,
            (Role.TAKER, Side.LONG):  long_input_sats  if self.taker_side == Side.LONG  else None,
        }

    def input_sats(self, role: Role | None = None, side: Side | None = None) -> UtxoSats:
        key = (role, side)
        value = self._input_sats_lookup[key]
        if value is None:
            raise ValueError(f'mismatch of role and side query ({key}) with actual contract roles (maker={self.maker_side})')
        return value

    def input_oracleUnits(self, role: Role | None = None, side: Side | None = None) -> OracleUnit:
        unit = self.oracle_unit_cls
        bch = self.input_sats(side=side, role=role).bch
        return unit(bch * float(self.start_price_oracleUnits_per_bch))

    ###############
    # Derivative values
    ###############
    @property
    def oracle_unit_cls(self) -> Type[OracleUnit]:
        return oracle_pubkey_to_unit_class[self.oracle_public_key]

    @property
    def duration_seconds(self) -> int:
        return self.maturity_timestamp - self.start_timestamp

    @property
    def effective_nominal_value_oracleUnits(self) -> OracleUnit:
        return self.oracle_unit_cls(self.nominal_oracleUnits_x_satsPerBch / SATS_PER_BCH)

    @property
    def cost_sats_for_nominal_value_at_start(self) -> UtxoSats:
        return UtxoSats(round_half_up(float(self.nominal_oracleUnits_x_satsPerBch) / float(self.start_price_oracleUnits_per_bch)))

    @property
    def effective_short_leverage(self) -> ShortLeverage:
        # There is a special case where even if the liquidation price must be recorded at some max value,
        # The fundamental cost for the position at liquidation is hard-lined at zero. That is the definition
        # of a hard hedge position, emulating the original anyhedge contract behavior.
        if self.cost_sats_for_nominal_value_at_high_liquidation == 0:
            return ShortLeverage(1)

        # Derivation of the calculation:
        #   short liq price = high liq price = start price (1 + 1 / (short leverage - 1))
        #   1 + 1 / (short leverage - 1) = short liq price / start price
        #   1 / (short leverage - 1) = (short liq price / start price) - 1
        #   short leverage - 1 = 1 / ((short liq price / start price) - 1)
        #   short leverage = 1 + 1 / ((short liq price / start price) - 1)
        return ShortLeverage(1 + 1 / (self.high_liquidation_price_oracleUnits_per_bch / self.start_price_oracleUnits_per_bch - 1))

    @property
    def effective_long_leverage(self) -> LongLeverage:
        # Derivation of the calculation:
        #   long liq price = low liq price = start price (1 - 1 / long leverage)
        #   1 - 1 / long leverage = long liq price / start price
        #   1 / long leverage = 1 - (long liq price / start price)
        #   long leverage = 1 / (1 - (long liq price / start price))
        return LongLeverage(1 / (1 - self.low_liquidation_price_oracleUnits_per_bch / self.start_price_oracleUnits_per_bch))

    @property
    def taker_side(self) -> Side:
        return self.maker_side.other_side

    @property
    def short_role(self) -> Role:
        if self.maker_side == Side.SHORT:
            return Role.MAKER
        return Role.TAKER

    @property
    def long_role(self) -> Role:
        if self.maker_side == Side.LONG:
            return Role.MAKER
        return Role.TAKER

    ###############
    # Property access to input sats
    ###############
    @property
    def short_input_sats(self) -> UtxoSats:
        return self.input_sats(side=Side.SHORT)

    @property
    def long_input_sats(self) -> UtxoSats:
        return self.input_sats(side=Side.LONG)

    @property
    def maker_input_sats(self) -> UtxoSats:
        return self.input_sats(role=Role.MAKER)

    @property
    def taker_input_sats(self) -> UtxoSats:
        return self.input_sats(role=Role.TAKER)

    ###############
    # Property access to unit conversions of inputs
    ###############
    @property
    def total_input_oracleUnits(self) -> OracleUnit:
        return self.input_oracleUnits()

    @property
    def short_input_oracleUnits(self) -> OracleUnit:
        return self.input_oracleUnits(side=Side.SHORT)

    @property
    def long_input_oracleUnits(self) -> OracleUnit:
        return self.input_oracleUnits(side=Side.LONG)

    @property
    def maker_input_oracleUnits(self) -> OracleUnit:
        return self.input_oracleUnits(role=Role.MAKER)

    @property
    def taker_input_oracleUnits(self) -> OracleUnit:
        return self.input_oracleUnits(role=Role.TAKER)

    ###############
    # Constructors
    ###############
    @staticmethod
    def new_from_intent(start_timestamp: ScriptTimestamp,
                        maturity_timestamp: ScriptTimestamp,
                        nominal_oracleUnits: OracleUnit,
                        long_leverage: LongLeverage,
                        start_price_oracleUnits_per_bch: ScriptPriceInOracleUnitsPerBch,
                        maker_side: Side,
                        # For upgrade to leveraged shorts, we establish a default of 1 representing the pure hedge position
                        short_leverage: ShortLeverage = ShortLeverage(1),
                        address: str = '',
                        ) -> ContractProposal:
        nominal_oracleUnits_x_satsPerBch = NominalOracleUnitsXSatsPerBch(round_half_up(nominal_oracleUnits * SATS_PER_BCH))

        try:
            # High liquidation price is a hard contract parameter, and is also used as a base number to derive other contract details.
            # We calculate high liquidation price from the more abstract leverage input and then discard leverage.
            # High liquidation price is rounded for accuracy - in the contract it's used as for testing, but not calculations
            high_liquidation_price_oracleUnits_per_bch = ScriptPriceInOracleUnitsPerBch(round_half_up(float(start_price_oracleUnits_per_bch) * (1 + 1 / (short_leverage - 1))))

            # Each side of the contract has a worst-case price (the liquidation price) at which it needs to be able to settle the contract.
            # In nominal terms, there is a full cost for that position, but in input/output terms, the counterparties only need to cover the difference in cost.
            # In order to achieve the simplest possible in-contract calculation, we use the full cost for high liquidation price as a contract parameter.
            # cost is floored for safety - it's a hard contract value subtracted from another during contract execution, and that result must never be a negative number
            cost_sats_for_nominal_value_at_high_liquidation = Sats(floor(nominal_oracleUnits_x_satsPerBch / high_liquidation_price_oracleUnits_per_bch))
        except ZeroDivisionError:
            # For short leverage exactly 1 (or any floating point result that still causes the error), the implication
            # is that high liquidation is at infinity on a continuous number line. However, for the contract purposes,
            # we need a concrete test price for liquidation and the cost value. We establish those directly:
            high_liquidation_price_oracleUnits_per_bch = ScriptPriceInOracleUnitsPerBch.largest_allowed()
            cost_sats_for_nominal_value_at_high_liquidation = Sats(0)

        # Low liquidation has the same considerations as high liquidation above, except long leverage of 1 is strictly disallowed,
        # avoiding the problem of a zero price, infinite cost. Note that a short leverage of 1 is useful in the sense that it gives the short
        # party the equivalent of simply holding another asset, while long leverage of 1 is nonsensical in that it gives the long
        # the equivalent of simply holding the underlying asset (BCH) which by definition they already have.
        low_liquidation_price_oracleUnits_per_bch = ScriptPriceInOracleUnitsPerBch(round_half_up(float(start_price_oracleUnits_per_bch) * (1 - 1 / long_leverage)))

        # Cost at low liquidation has the same considerations as high liquidation above, except we are on the opposite side so we use ceil to be conservative instead of floor
        cost_sats_for_nominal_value_at_low_liquidation = UtxoSats(ceil(nominal_oracleUnits_x_satsPerBch / low_liquidation_price_oracleUnits_per_bch))

        # Total input sats is the total of the two party's required amounts. In the contract base terms that we are using, it is the difference between
        # the cost at the two liquidation points
        total_input_sats = UtxoSats(cost_sats_for_nominal_value_at_low_liquidation - cost_sats_for_nominal_value_at_high_liquidation)

        return ContractProposal(
            address=address,
            start_timestamp=start_timestamp,
            maturity_timestamp=maturity_timestamp,
            nominal_oracleUnits_x_satsPerBch=nominal_oracleUnits_x_satsPerBch,
            cost_sats_for_nominal_value_at_high_liquidation=cost_sats_for_nominal_value_at_high_liquidation,
            total_input_sats=total_input_sats,
            start_price_oracleUnits_per_bch=start_price_oracleUnits_per_bch,
            high_liquidation_price_oracleUnits_per_bch=high_liquidation_price_oracleUnits_per_bch,
            low_liquidation_price_oracleUnits_per_bch=low_liquidation_price_oracleUnits_per_bch,
            oracle_public_key=nominal_oracleUnits.public_key,
            maker_side=maker_side,
        )

    def neutralize(self,
                   current_price_oracleUnitsPerBch: ScriptPriceInOracleUnitsPerBch,
                   current_timestamp: ScriptTimestamp,
                   ) -> ContractProposal:
        neutralizing_proposal = ContractProposal(
            # reset / unimplemented
            address='',

            # update to settlement timing / price
            start_timestamp=current_timestamp,
            start_price_oracleUnits_per_bch=current_price_oracleUnitsPerBch,

            # swap sides
            maker_side=self.taker_side,

            # the rest remains the same
            maturity_timestamp=self.maturity_timestamp,
            nominal_oracleUnits_x_satsPerBch=self.nominal_oracleUnits_x_satsPerBch,
            cost_sats_for_nominal_value_at_high_liquidation=self.cost_sats_for_nominal_value_at_high_liquidation,
            total_input_sats=self.total_input_sats,
            high_liquidation_price_oracleUnits_per_bch=self.high_liquidation_price_oracleUnits_per_bch,
            low_liquidation_price_oracleUnits_per_bch=self.low_liquidation_price_oracleUnits_per_bch,
            oracle_public_key=self.oracle_public_key,
        )
        return neutralizing_proposal

    def fund(self, fee_agreements: Sequence[FeeAgreement]) -> ContractFunding:
        return ContractFunding(
            base_proposal=self,
            fee_agreements=tuple(fee_agreements),
        )

    def validate(self):
        # Timing
        min_contract_duration_seconds = 60
        if not (self.duration_seconds >= min_contract_duration_seconds):
            raise ValueError(f'contract duration is {self.duration_seconds} s but it must be >= {min_contract_duration_seconds} s')


@dataclass(frozen=True)
class ContractFunding:
    """Funding details and actions, typically derived from a contract proposal."""
    base_proposal: ContractProposal
    fee_agreements: tuple[FeeAgreement, ...]

    @property
    def fee_sats_to_maker(self) -> Sats:
        return aggregate_fee_sats_to_role(self.fee_agreements, Role.MAKER)

    @property
    def fee_sats_to_taker(self) -> Sats:
        return aggregate_fee_sats_to_role(self.fee_agreements, Role.TAKER)

    @property
    def fee_sats_to_short(self) -> Sats:
        if self.base_proposal.maker_side == Side.SHORT:
            return self.fee_sats_to_maker
        return self.fee_sats_to_taker

    @property
    def fee_sats_to_long(self) -> Sats:
        if self.base_proposal.maker_side == Side.LONG:
            return self.fee_sats_to_maker
        return self.fee_sats_to_taker

    ###############
    # Unit value calculations
    ###############
    @property
    def fee_oracleUnits_to_maker(self) -> OracleUnit:
        fee_bch = self.fee_sats_to_maker.bch
        fee_oracleUnits = self.base_proposal.oracle_unit_cls(fee_bch * float(self.base_proposal.start_price_oracleUnits_per_bch))
        return fee_oracleUnits

    @property
    def fee_oracleUnits_to_taker(self) -> OracleUnit:
        fee_bch = self.fee_sats_to_taker.bch
        fee_oracleUnits = self.base_proposal.oracle_unit_cls(fee_bch * float(self.base_proposal.start_price_oracleUnits_per_bch))
        return fee_oracleUnits

    @property
    def fee_oracleUnits_to_short(self) -> OracleUnit:
        if self.base_proposal.maker_side == Side.SHORT:
            return self.fee_oracleUnits_to_maker
        return self.fee_oracleUnits_to_taker

    @property
    def fee_oracleUnits_to_long(self) -> OracleUnit:
        if self.base_proposal.maker_side == Side.LONG:
            return self.fee_oracleUnits_to_maker
        return self.fee_oracleUnits_to_taker

    ###############
    # Actions
    ###############
    def redeem(self,
               price_timestamp: ScriptTimestamp,
               price_oracleUnits_per_bch: ScriptPriceInOracleUnitsPerBch,
               force_maturity: bool,
               is_mutual_redemption: bool = False,
               fee_agreements: Sequence[FeeAgreement] = tuple(),
               ) -> ContractRedemption:
        """
        Redeem the contract according to market conditions or raise an unredeemable error for invalid conditions.
        Note that is_mutual_redemption takes precedence over force_maturity.
        """
        reached_maturity_time = price_timestamp >= self.base_proposal.maturity_timestamp
        reached_liquidation_price = (
                price_oracleUnits_per_bch <= self.base_proposal.low_liquidation_price_oracleUnits_per_bch
                or
                price_oracleUnits_per_bch >= self.base_proposal.high_liquidation_price_oracleUnits_per_bch
        )

        if is_mutual_redemption:
            # Mutual redemption
            redemption_type = RedemptionType.MUTUAL
        elif reached_maturity_time or force_maturity:
            # Maturation, even in the case of a liquidation price
            redemption_type = RedemptionType.MATURATION
        elif reached_liquidation_price:
            # Liquidation
            redemption_type = RedemptionType.LIQUIDATION
        else:
            raise UnredeemableError

        return ContractRedemption(
            base_funding=self,
            end_price_timestamp=price_timestamp,
            naive_end_price_oracleUnits_per_bch=price_oracleUnits_per_bch,
            redemption_type=redemption_type,
            fee_agreements=tuple(fee_agreements),
        )


@dataclass(frozen=True)
class ContractRedemption:
    """Outcome of a redeemed contract, especially with respect to the two counterparties."""
    base_funding: ContractFunding
    end_price_timestamp: ScriptTimestamp
    naive_end_price_oracleUnits_per_bch: ScriptPriceInOracleUnitsPerBch
    redemption_type: RedemptionType
    fee_agreements: tuple[FeeAgreement, ...]

    ###############
    # Parameterized Payout Values
    ###############
    @cached_property
    def _payout_sats_lookup(self) -> dict[(Role | None, Side | None), UtxoSats | None]:
        # Hedge payout sats is the payout side of the fundamental definition of an AnyHedge contract
        # Note that due to dust safety in the contract, the total actual payout can be greater than total inputs.
        # In reality, the extra dust is covered by an amount sitting on the contract that the contract is not aware of.
        # Use divmod (instead of //) to make it crystal clear this represents integer division of the contract.
        _unsafe_hedge_payout_sats, _ = divmod(self.base_funding.base_proposal.nominal_oracleUnits_x_satsPerBch, self.clamped_end_price_oracleUnits_per_bch)

        # With leveraged shorts, the short is no longer necessarily paying out the full value of the nominal position.
        # If short leverage is not 1, the short only pays up to the planned liquidation point
        unsafe_short_payout_sats = _unsafe_hedge_payout_sats - self.base_funding.base_proposal.cost_sats_for_nominal_value_at_high_liquidation
        short_payout_sats = UtxoSats(max(DUST, unsafe_short_payout_sats))

        # Long Payout Sats
        unsafe_long_payout_sats = self.base_funding.base_proposal.total_input_sats - short_payout_sats
        long_payout_sats = UtxoSats(max(DUST, unsafe_long_payout_sats))

        # Total payout sats is just the combination of short and long
        # Note: This can be different from total input in the case of liquidation where dust protection is pulled in from outside the contract
        # Any extra dust is covered by an amount sitting on the contract's utxo that the contract is not aware of.
        total_payout_sats = UtxoSats(short_payout_sats + long_payout_sats)

        # visual shortcut for the maker/taker sides
        maker_side = self.base_funding.base_proposal.maker_side
        taker_side = self.base_funding.base_proposal.taker_side

        return {
            (None,       None):       total_payout_sats,
            (None,       Side.SHORT): short_payout_sats,
            (None,       Side.LONG):  long_payout_sats,
            (Role.MAKER, None):       short_payout_sats if maker_side == Side.SHORT else long_payout_sats,
            (Role.MAKER, Side.SHORT): short_payout_sats if maker_side == Side.SHORT else None,
            (Role.MAKER, Side.LONG):  long_payout_sats  if maker_side == Side.LONG  else None,
            (Role.TAKER, None):       short_payout_sats if taker_side == Side.SHORT else long_payout_sats,
            (Role.TAKER, Side.SHORT): short_payout_sats if taker_side == Side.SHORT else None,
            (Role.TAKER, Side.LONG):  long_payout_sats  if taker_side == Side.LONG  else None,
        }

    def payout_sats(self, role: Role | None = None, side: Side | None = None) -> UtxoSats:
        key = (role, side)
        value = self._payout_sats_lookup[key]
        if value is None:
            raise ValueError(f'mismatch of role and side query ({key}) with actual contract roles (maker={self.base_funding.base_proposal.maker_side})')
        return value

    def payout_oracleUnits(self, role: Role | None = None, side: Side | None = None) -> OracleUnit:
        unit = self.base_funding.base_proposal.oracle_unit_cls
        bch = self.payout_sats(side=side, role=role).bch
        # NOTE: using actual end price, not clamped, to determine unit value including any potential slippage
        return unit(bch * float(self.naive_end_price_oracleUnits_per_bch))

    ###############
    # Derivative values
    ###############
    @property
    def clamped_end_price_oracleUnits_per_bch(self) -> ScriptPriceInOracleUnitsPerBch:
        return max(self.naive_end_price_oracleUnits_per_bch, self.base_funding.base_proposal.low_liquidation_price_oracleUnits_per_bch)

    @property
    def cost_sats_for_nominal_value_at_redemption(self) -> Sats:
        return Sats(round_half_up(SATS_PER_BCH * (self.base_funding.base_proposal.effective_nominal_value_oracleUnits / float(self.clamped_end_price_oracleUnits_per_bch))))

    ###############
    # Property access to payout sats
    ###############
    @property
    def total_payout_sats(self) -> UtxoSats:
        return self.payout_sats()

    @property
    def short_payout_sats(self) -> UtxoSats:
        return self.payout_sats(side=Side.SHORT)

    @property
    def long_payout_sats(self) -> UtxoSats:
        return self.payout_sats(side=Side.LONG)

    @property
    def maker_payout_sats(self) -> UtxoSats:
        return self.payout_sats(role=Role.MAKER)

    @property
    def taker_payout_sats(self) -> UtxoSats:
        return self.payout_sats(role=Role.TAKER)

    ###############
    # Property access to unit conversions of payouts
    ###############
    @property
    def total_payout_oracleUnits(self) -> OracleUnit:
        return self.payout_oracleUnits()

    @property
    def short_payout_oracleUnits(self) -> OracleUnit:
        return self.payout_oracleUnits(side=Side.SHORT)

    @property
    def long_payout_oracleUnits(self) -> OracleUnit:
        return self.payout_oracleUnits(side=Side.LONG)

    @property
    def maker_payout_oracleUnits(self) -> OracleUnit:
        return self.payout_oracleUnits(role=Role.MAKER)

    @property
    def taker_payout_oracleUnits(self) -> OracleUnit:
        return self.payout_oracleUnits(role=Role.TAKER)

    ###############
    # Gains - see funding class for details of fee and gain calculations
    # TODO: These could also be parameterized with a lookup
    ###############
    @property
    def short_gain_sats(self) -> Sats:
        payout_sats = self.short_payout_sats
        input_sats = self.base_funding.base_proposal.short_input_sats
        fee_sats = self.base_funding.fee_sats_to_short + self.fee_sats_to_short
        return Sats(payout_sats - input_sats + fee_sats)

    @property
    def long_gain_sats(self) -> Sats:
        payout_sats = self.long_payout_sats
        input_sats = self.base_funding.base_proposal.long_input_sats
        fee_sats = self.base_funding.fee_sats_to_long + self.fee_sats_to_long
        return Sats(payout_sats - input_sats + fee_sats)

    @property
    def short_gain_oracleUnits(self) -> OracleUnit:
        # Note that this is not the same as (end sats - start sats) * end price. start value depends on start price.
        # Note that we use naive end price. This represents reality of slippage in liquidations.
        payout_oracleUnits = self.short_payout_oracleUnits
        input_oracleUnits = self.base_funding.base_proposal.short_input_oracleUnits
        fee_oracleUnits = self.base_funding.fee_oracleUnits_to_short + self.fee_oracleUnits_to_short
        return self.base_funding.base_proposal.oracle_unit_cls(payout_oracleUnits - input_oracleUnits + fee_oracleUnits)

    @property
    def long_gain_oracleUnits(self) -> OracleUnit:
        # Note that this is not the same as (end sats - start sats) * end price. start value depends on start price.
        # Note that we use naive end price. This represents reality of slippage in liquidations.
        payout_oracleUnits = self.long_payout_oracleUnits
        input_oracleUnits = self.base_funding.base_proposal.long_input_oracleUnits
        fee_oracleUnits = self.base_funding.fee_oracleUnits_to_long + self.fee_oracleUnits_to_long
        return self.base_funding.base_proposal.oracle_unit_cls(payout_oracleUnits - input_oracleUnits + fee_oracleUnits)

    ###############
    # Relative gains
    ###############
    @property
    def short_gain_percent_of_own_input(self) -> float:
        return 100.0 * float(self.short_gain_sats) / float(self.base_funding.base_proposal.short_input_sats)

    @property
    def long_gain_percent_of_own_input(self) -> float:
        return 100.0 * float(self.long_gain_sats) / float(self.base_funding.base_proposal.long_input_sats)

    ###############
    # Sided views on gains
    ###############
    @property
    def maker_gain_sats(self) -> Sats:
        if self.base_funding.base_proposal.maker_side == Side.SHORT:
            return self.short_gain_sats
        return self.long_gain_sats

    @property
    def taker_gain_sats(self) -> Sats:
        if self.base_funding.base_proposal.taker_side == Side.SHORT:
            return self.short_gain_sats
        return self.long_gain_sats

    @property
    def maker_gain_oracleUnits(self) -> OracleUnit:
        if self.base_funding.base_proposal.maker_side == Side.SHORT:
            return self.short_gain_oracleUnits
        return self.long_gain_oracleUnits

    @property
    def taker_gain_oracleUnits(self) -> OracleUnit:
        if self.base_funding.base_proposal.taker_side == Side.SHORT:
            return self.short_gain_oracleUnits
        return self.long_gain_oracleUnits

    @property
    def maker_gain_percent_of_own_input(self) -> float:
        if self.base_funding.base_proposal.maker_side == Side.SHORT:
            return self.short_gain_percent_of_own_input
        return self.long_gain_percent_of_own_input

    @property
    def taker_gain_percent_of_own_input(self) -> float:
        if self.base_funding.base_proposal.taker_side == Side.SHORT:
            return self.short_gain_percent_of_own_input
        return self.long_gain_percent_of_own_input

    ###############
    # Redemption Fees (Especially for early redemption)
    ###############
    @property
    def fee_sats_to_maker(self) -> Sats:
        return aggregate_fee_sats_to_role(self.fee_agreements, Role.MAKER)

    @property
    def fee_sats_to_taker(self) -> Sats:
        return aggregate_fee_sats_to_role(self.fee_agreements, Role.TAKER)

    @property
    def fee_sats_to_short(self) -> Sats:
        if self.base_funding.base_proposal.maker_side == Side.SHORT:
            return self.fee_sats_to_maker
        return self.fee_sats_to_taker

    @property
    def fee_sats_to_long(self) -> Sats:
        if self.base_funding.base_proposal.maker_side == Side.LONG:
            return self.fee_sats_to_maker
        return self.fee_sats_to_taker

    ###############
    # Unit value of fees
    ###############
    @property
    def fee_oracleUnits_to_maker(self) -> OracleUnit:
        fee_bch = self.fee_sats_to_maker.bch
        # NOTE: using actual end price, not clamped, to determine unit value including any potential slippage
        fee_oracleUnits = self.base_funding.base_proposal.oracle_unit_cls(fee_bch * float(self.naive_end_price_oracleUnits_per_bch))
        return fee_oracleUnits

    @property
    def fee_oracleUnits_to_taker(self) -> OracleUnit:
        fee_bch = self.fee_sats_to_taker.bch
        # NOTE: using actual end price, not clamped, to determine unit value including any potential slippage
        fee_oracleUnits = self.base_funding.base_proposal.oracle_unit_cls(fee_bch * float(self.naive_end_price_oracleUnits_per_bch))
        return fee_oracleUnits

    @property
    def fee_oracleUnits_to_short(self) -> OracleUnit:
        if self.base_funding.base_proposal.maker_side == Side.SHORT:
            return self.fee_oracleUnits_to_maker
        return self.fee_oracleUnits_to_taker

    @property
    def fee_oracleUnits_to_long(self) -> OracleUnit:
        if self.base_funding.base_proposal.maker_side == Side.LONG:
            return self.fee_oracleUnits_to_maker
        return self.fee_oracleUnits_to_taker
