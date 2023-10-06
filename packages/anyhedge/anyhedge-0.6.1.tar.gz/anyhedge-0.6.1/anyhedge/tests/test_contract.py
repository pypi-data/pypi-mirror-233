# Built-in imports
import unittest
from typing import Sequence

# Library imports
from arrow import Arrow

# Local imports
from ..bch_primitives import (
    SATS_PER_BCH,
    Sats,
    ScriptTimestamp,
    UtxoSats,
)
from ..contract import (
    ContractFunding,
    ContractProposal,
    ContractRedemption,
    LongLeverage,
    NominalOracleUnitsXSatsPerBch,
    RedemptionType,
    ShortLeverage,
    Side,
    UnredeemableError,
)
from ..fee import FeeAgreement
from ..oracle import (
    OracleUnit,
    ScriptPriceInOracleUnitsPerBch,
    UsdEM2Beta,
)
from ..role import Role


###################
# Contract Tests
###################
# Generic intent values, not always perfectly reproducible from the contract
START_TIMESTAMP = ScriptTimestamp(Arrow(year=2021, month=10, day=21).int_timestamp)
MATURITY_TIMESTAMP = ScriptTimestamp(Arrow(year=2021, month=10, day=23).int_timestamp)  # 2 days later
NOMINAL_VALUE_USDEM2 = UsdEM2Beta(100_00.0)  # $100.00
LONG_LEVERAGE = LongLeverage(4.5)
SHORT_LEVERAGE_1_AS_HEDGE = ShortLeverage(1)
SHORT_LEVERAGE_NOT_1 = ShortLeverage(2.2)
START_PRICE_USDEM2_PER_BCH = ScriptPriceInOracleUnitsPerBch(200_00)  # $200.00 / BCH

# Derived values

# The cost of the short position at start is equal to the hedge input for a pure hedge.
# However, they are not equal for a leveraged short.
# Calculated as round_half_up((NOMINAL_VALUE_USDEM2 / START_PRICE_USDEM2_PER_BCH) * SATS_PER_BCH)
COST_SATS_FOR_NOMINAL_VALUE_AT_START = UtxoSats(50_000_000)

# The compound nominal value is a giant number stored in the original AnyHedge contract and needed
# to get around the lack of multiplication by optimizing the contract into a single division operation
# = NominalOracleUnitsXSatsPerBch(round(NOMINAL_VALUE_USDEM2 * SATS_PER_BCH))
NOMINAL_UNITS_X_SATS_PER_BCH = NominalOracleUnitsXSatsPerBch(1_000_000_000_000)

# The contract stores the compound nominal value but not the original value. Therefore, the nominal value
# of a contract exists only as an effective value back-calculated from the parameters.
# Calculated as NOMINAL_UNITS_X_SATS_PER_BCH / SATS_PER_BCH
EFFECTIVE_NOMINAL_VALUE_ORALCEUNITS = UsdEM2Beta(100_00.0)

# Low liquidation Price is the price where all of long's input is consumed to cover short's agreed payout
# Calculate in terms of leverage intent as round(START_PRICE_USDEM2_PER_BCH * (1 - 1 / LONG_LEVERAGE))
# 15556 cents/BCH ($155.56 / BCH)
LOW_LIQUIDATION_PRICE = ScriptPriceInOracleUnitsPerBch(155_56)

# High liquidation Price is the price where all of short's input is consumed to cover long's agreed payout
# When short is exactly a 1x short, there is no meaningful liquidation price (infinity) but the stored liquidation price is still
# used to trigger early settlement. By definition, we set it to the max possible price in the 4 byte oracle price message scheme.
HIGH_LIQUIDATION_PRICE_AS_HEDGE = ScriptPriceInOracleUnitsPerBch.largest_allowed()
# In the case of a leveraged short, it is calculated as round(START_PRICE_USDEM2_PER_BCH * (1 + 1 / (SHORT_LEVERAGE_NOT_1 - 1)))
# 36667 cents/BCH ($366.67 / BCH)
HIGH_LIQUIDATION_PRICE_AS_LEVERAGED_SHORT = ScriptPriceInOracleUnitsPerBch(366_67)

# Cost of nominal value at high liquidation is a new value that was always zero for pure hedges
# and therefore not documented explicitly anywhere. With leveraged shorts, short does not always
# pay the full cost of the nominal value and so the contract needs to track the cost.
# Fixed for pure hedge at 0
ZERO_COST_OF_NOMINAL_VALUE_AT_HEDGE_LIQUIDATION = Sats(0)
# Calculated for leveraged short as floor(NOMINAL_UNITS_X_SATS_PER_BCH / HIGH_LIQUIDATION_PRICE_FOR_LEVERAGED_SHORT)
COST_SATS_FOR_NOMINAL_VALUE_AT_LEVERAGED_HIGH_LIQUIDATION = Sats(27_272_479)

# The bch amount to cover the short's payout obligations to long
# For a pure hedge, it is the full cost of the nominal contract at starting price,
# effectively allowing the price to increase to any value and still be able to pay out
SHORT_INPUT_SATS_AS_HEDGE = COST_SATS_FOR_NOMINAL_VALUE_AT_START
# For a leveraged short, it is the cost at starting price less the cost at high liquidation price
# Calculated as SHORT_INPUT_SATS_AS_HEDGE - COST_SATS_FOR_NOMINAL_VALUE_AT_LEVERAGED_HIGH_LIQUIDATION
SHORT_INPUT_SATS_AS_LEVERAGED_SHORT = UtxoSats(22_727_521)

# Similar to cost at high liquidation, there is also the cost at low liquidation.
# In the contract, this is not stored anywhere, but it is a useful intermediary for confirming tests.
# It is the amount needed to cover the nominal unit value at low liquidation price
# Calculated as ceil((NOMINAL_UNITS_X_SATS_PER_BCH) / DERIVED_LIQUIDATION_PRICE_UNITS_PER_BCH)
COST_SATS_FOR_NOMINAL_VALUE_AT_LOW_LIQUIDATION = UtxoSats(64_283_878)

# The total input sats needed to cover all positions is the sum of the short and long inputs.
# However, from base contract values, it is the difference between the cost at the two liquidation points
# For a pure hedge, it has to cover the cost between low liquidation and zero
TOTAL_INPUT_SATS_AS_HEDGE = COST_SATS_FOR_NOMINAL_VALUE_AT_LOW_LIQUIDATION - 0
# For a leveraged short, it has to cover the cost between low liquidation and high liquidation (which also might be zero)
# Calculated as COST_SATS_FOR_NOMINAL_VALUE_AT_LOW_LIQUIDATION - COST_SATS_FOR_NOMINAL_VALUE_AT_HIGH_LIQUIDATION
TOTAL_INPUT_SATS_AS_LEVERAGED_SHORT = UtxoSats(37_011_399)

# The bch amount to provide volatility protection as specified by the multiplier
# This is the amount to cover the difference between payout bch at start and payout bch at long's liquidation price
# Calculated as DERIVED_TOTAL_INPUT_SATS - SHORT_INPUT_SATS_AS_HEDGE
LONG_INPUT_SATS = UtxoSats(14_283_878)

# Converting the input amounts into ORACLE units at start
# for pure hedge, it's NOMINAL_UNITS_X_SATS_PER_BCH / SATS_PER_BCH
SHORT_INPUT_ORACLE_UNITS_AS_HEDGE_AT_START = UsdEM2Beta(100_00.0)
# for long, it's LONG_INPUT_SATS * START_PRICE_USDEM2_PER_BCH / SATS_PER_BCH
LONG_INPUT_ORACLE_UNITS_AT_START = UsdEM2Beta(2856.7756)
TOTAL_INPUT_ORACLE_UNITS_AS_HEDGE_AT_START = UsdEM2Beta(SHORT_INPUT_ORACLE_UNITS_AS_HEDGE_AT_START + LONG_INPUT_ORACLE_UNITS_AT_START)
# TODO: Need another set of these established at the redemption price


def standard_contract_proposal(
    start_timestamp: ScriptTimestamp = START_TIMESTAMP,
    maturity_timestamp: ScriptTimestamp = MATURITY_TIMESTAMP,
    nominal_oracleUnits: OracleUnit = NOMINAL_VALUE_USDEM2,
    long_leverage: LongLeverage = LONG_LEVERAGE,
    start_price_oracleUnits_per_bch: ScriptPriceInOracleUnitsPerBch = START_PRICE_USDEM2_PER_BCH,
    maker_side: Side = Side.SHORT,
    short_leverage: ShortLeverage = SHORT_LEVERAGE_1_AS_HEDGE,
) -> ContractProposal:
    return ContractProposal.new_from_intent(
        start_timestamp=start_timestamp,
        maturity_timestamp=maturity_timestamp,
        nominal_oracleUnits=nominal_oracleUnits,
        long_leverage=long_leverage,
        start_price_oracleUnits_per_bch=start_price_oracleUnits_per_bch,
        maker_side=maker_side,
        short_leverage=short_leverage,
    )


class TestContractProposalDerivedValues(unittest.TestCase):
    ######################
    # Exact contract parameters, some root values, some derived from root values
    ######################
    def test_nominal_oracleUnits_x_satsPerBch(self):
        self.assertEqual(standard_contract_proposal().nominal_oracleUnits_x_satsPerBch, NOMINAL_UNITS_X_SATS_PER_BCH)

    def test_total_input_sats(self):
        self.assertEqual(standard_contract_proposal().total_input_sats, TOTAL_INPUT_SATS_AS_HEDGE)

    def test_low_liquidation_price_oracleUnits_per_bch(self):
        self.assertEqual(standard_contract_proposal().low_liquidation_price_oracleUnits_per_bch, LOW_LIQUIDATION_PRICE)

    def test_high_liquidation_price_oracleUnits_per_bch(self):
        self.assertEqual(standard_contract_proposal().high_liquidation_price_oracleUnits_per_bch, HIGH_LIQUIDATION_PRICE_AS_HEDGE)

    def test_maker_taker_side(self):
        maker_short = standard_contract_proposal(maker_side=Side.SHORT)
        self.assertEqual(maker_short.maker_side, Side.SHORT)
        self.assertEqual(maker_short.taker_side, Side.LONG)

        maker_long = standard_contract_proposal(maker_side=Side.LONG)
        self.assertEqual(maker_long.maker_side, Side.LONG)
        self.assertEqual(maker_long.taker_side, Side.SHORT)

    def test_short_long_role(self):
        maker_short = standard_contract_proposal(maker_side=Side.SHORT)
        self.assertEqual(maker_short.short_role, Role.MAKER)
        self.assertEqual(maker_short.long_role, Role.TAKER)

        maker_long = standard_contract_proposal(maker_side=Side.LONG)
        self.assertEqual(maker_long.long_role, Role.MAKER)
        self.assertEqual(maker_long.short_role, Role.TAKER)

    ######################
    # Exact secondary values derived from contract parameters
    ######################
    def test_short_input_sats(self):
        self.assertEqual(standard_contract_proposal().short_input_sats, SHORT_INPUT_SATS_AS_HEDGE)

    def test_long_input_sats(self):
        self.assertEqual(standard_contract_proposal().long_input_sats, LONG_INPUT_SATS)

    ######################
    # Reverse calculated intent values from the contract's perspective
    ######################
    def test_effective_long_leverage(self):
        self.assertAlmostEqual(standard_contract_proposal().effective_long_leverage, LONG_LEVERAGE, delta=.001)

    ######################
    # Unit values
    ######################
    def test_total_input_oracleUnits(self):
        self.assertEqual(standard_contract_proposal().total_input_oracleUnits, TOTAL_INPUT_ORACLE_UNITS_AS_HEDGE_AT_START)

    def test_short_input_oracleUnits(self):
        self.assertEqual(standard_contract_proposal().short_input_oracleUnits, SHORT_INPUT_ORACLE_UNITS_AS_HEDGE_AT_START)

    def test_long_input_oracleUnits(self):
        self.assertEqual(standard_contract_proposal().long_input_oracleUnits, LONG_INPUT_ORACLE_UNITS_AT_START)

    ######################
    # Role versions of values
    ######################
    def test_all_sided_values(self):
        short_maker_contract = standard_contract_proposal(maker_side=Side.SHORT)
        self.assertEqual(short_maker_contract.maker_side, Side.SHORT)
        self.assertEqual(short_maker_contract.taker_side, Side.LONG)
        self.assertEqual(short_maker_contract.maker_input_sats, SHORT_INPUT_SATS_AS_HEDGE)
        self.assertEqual(short_maker_contract.taker_input_sats, LONG_INPUT_SATS)
        self.assertEqual(short_maker_contract.maker_input_oracleUnits, SHORT_INPUT_ORACLE_UNITS_AS_HEDGE_AT_START)
        self.assertEqual(short_maker_contract.taker_input_oracleUnits, LONG_INPUT_ORACLE_UNITS_AT_START)

        long_maker_contract = standard_contract_proposal(maker_side=Side.LONG)
        self.assertEqual(long_maker_contract.maker_side, Side.LONG)
        self.assertEqual(long_maker_contract.taker_side, Side.SHORT)
        self.assertEqual(long_maker_contract.maker_input_sats, LONG_INPUT_SATS)
        self.assertEqual(long_maker_contract.taker_input_sats, SHORT_INPUT_SATS_AS_HEDGE)
        self.assertEqual(long_maker_contract.maker_input_oracleUnits, LONG_INPUT_ORACLE_UNITS_AT_START)
        self.assertEqual(long_maker_contract.taker_input_oracleUnits, SHORT_INPUT_ORACLE_UNITS_AS_HEDGE_AT_START)

    ######################
    # Role versions of values
    ######################
    def test_parameterized_lookup_error_on_invalid_combinations(self):
        maker_short_contract = standard_contract_proposal(maker_side=Side.SHORT)
        with self.assertRaises(ValueError):
            maker_short_contract.input_sats(role=Role.MAKER, side=Side.LONG)
        with self.assertRaises(ValueError):
            maker_short_contract.input_sats(role=Role.TAKER, side=Side.SHORT)

        taker_short_contract = standard_contract_proposal(maker_side=Side.LONG)
        with self.assertRaises(ValueError):
            taker_short_contract.input_sats(role=Role.TAKER, side=Side.LONG)
        with self.assertRaises(ValueError):
            taker_short_contract.input_sats(role=Role.MAKER, side=Side.SHORT)


class TestContractProposalNeutralize(unittest.TestCase):
    def test_neutralize_creates_an_opposite_virtual_hedge_at_current_price(self):
        # Use a base case and hand-constructed neutralizing contract to confirm actual result

        # Construct the base case
        base_proposal = ContractProposal.new_from_intent(
            start_timestamp=START_TIMESTAMP,
            maturity_timestamp=MATURITY_TIMESTAMP,
            nominal_oracleUnits=NOMINAL_VALUE_USDEM2,
            long_leverage=LongLeverage(5.0),
            start_price_oracleUnits_per_bch=START_PRICE_USDEM2_PER_BCH,
            maker_side=Side.SHORT,
            short_leverage=ShortLeverage(1.0),
            address='',
        )

        # Manually construct the neutralizing contract
        neutralizing_price = ScriptPriceInOracleUnitsPerBch(190_00)
        neutralizing_timestamp = ScriptTimestamp(round((START_TIMESTAMP + MATURITY_TIMESTAMP) / 2))
        expected_neutralizing_contract = ContractProposal(
            address='',
            start_timestamp=neutralizing_timestamp,
            maturity_timestamp=base_proposal.maturity_timestamp,
            nominal_oracleUnits_x_satsPerBch=base_proposal.nominal_oracleUnits_x_satsPerBch,
            cost_sats_for_nominal_value_at_high_liquidation=base_proposal.cost_sats_for_nominal_value_at_high_liquidation,
            total_input_sats=base_proposal.total_input_sats,
            start_price_oracleUnits_per_bch=neutralizing_price,
            high_liquidation_price_oracleUnits_per_bch=base_proposal.high_liquidation_price_oracleUnits_per_bch,
            low_liquidation_price_oracleUnits_per_bch=base_proposal.low_liquidation_price_oracleUnits_per_bch,
            oracle_public_key=base_proposal.oracle_public_key,
            maker_side=base_proposal.taker_side,
        )

        # Get the function result from the base contract
        neutralizing_contract = base_proposal.neutralize(neutralizing_price, neutralizing_timestamp)

        # Confirm the function result matches expected
        self.assertEqual(neutralizing_contract, expected_neutralizing_contract)


class TestContractProposalValidation(unittest.TestCase):
    def test_ValueError_if_duration_too_short(self):
        with self.assertRaises(ValueError):
            too_short_maturity_timestamp = ScriptTimestamp(START_TIMESTAMP + 60 - 1)
            standard_contract_proposal(maturity_timestamp=too_short_maturity_timestamp)


# Create a set of fees to be used in funding and redemption
FEE_100000_TAKER_TO_MAKER = FeeAgreement(name='fee type a', amount_sats=Sats(100000), receiving=Role.MAKER, paying=Role.TAKER)
FEE_200000_TAKER_TO_MAKER = FeeAgreement(name='fee type b', amount_sats=Sats(200000), receiving=Role.MAKER, paying=Role.TAKER)
FEE_400000_TAKER_TO_SETTLEMENT_SERVICE = FeeAgreement(name='fee type ss', amount_sats=Sats(400000), receiving=Role.SETTLEMENT_SERVICE, paying=Role.TAKER)

# Create the set of funding fees
FUNDING_FEES = (FEE_100000_TAKER_TO_MAKER, FEE_200000_TAKER_TO_MAKER, FEE_400000_TAKER_TO_SETTLEMENT_SERVICE)

# Manually group them by side and unit
TOTAL_FUNDING_FEES_TO_MAKER_SATS = Sats(
    + FEE_100000_TAKER_TO_MAKER.amount_sats
    + FEE_200000_TAKER_TO_MAKER.amount_sats
)
TOTAL_FUNDING_FEES_TO_TAKER_SATS = Sats(
    - FEE_100000_TAKER_TO_MAKER.amount_sats
    - FEE_200000_TAKER_TO_MAKER.amount_sats
    - FEE_400000_TAKER_TO_SETTLEMENT_SERVICE.amount_sats
)


def standard_contract_funding(proposal: ContractProposal | None = None) -> ContractFunding:
    proposal = proposal or standard_contract_proposal()
    return proposal.fund(fee_agreements=FUNDING_FEES)


class TestContractFundingDerivedValues(unittest.TestCase):
    def test_fee_sats_to_side(self):
        # Confirm short maker and long taker
        short_maker_contract = standard_contract_funding(standard_contract_proposal(maker_side=Side.SHORT))
        long_maker_contract = standard_contract_funding(standard_contract_proposal(maker_side=Side.LONG))

        expected_fees_sats_to_maker = TOTAL_FUNDING_FEES_TO_MAKER_SATS
        expected_fees_sats_to_taker = TOTAL_FUNDING_FEES_TO_TAKER_SATS

        # Short Maker
        self.assertEqual(short_maker_contract.fee_sats_to_short, expected_fees_sats_to_maker)
        self.assertEqual(short_maker_contract.fee_sats_to_maker, expected_fees_sats_to_maker)

        # Long Taker
        self.assertEqual(short_maker_contract.fee_sats_to_long, expected_fees_sats_to_taker)
        self.assertEqual(short_maker_contract.fee_sats_to_taker, expected_fees_sats_to_taker)

        # Long Maker
        self.assertEqual(long_maker_contract.fee_sats_to_long, expected_fees_sats_to_maker)
        self.assertEqual(long_maker_contract.fee_sats_to_maker, expected_fees_sats_to_maker)

        # Short Taker
        self.assertEqual(long_maker_contract.fee_sats_to_short, expected_fees_sats_to_taker)
        self.assertEqual(long_maker_contract.fee_sats_to_taker, expected_fees_sats_to_taker)

    def test_fee_oracleUnits_to_side(self):
        # Confirm short maker and long taker
        short_maker_contract = standard_contract_funding(standard_contract_proposal(maker_side=Side.SHORT))
        long_maker_contract = standard_contract_funding(standard_contract_proposal(maker_side=Side.LONG))
        oracle_class = short_maker_contract.base_proposal.oracle_unit_cls

        expected_fee_oracleUnits_to_maker_at_funding = oracle_class(TOTAL_FUNDING_FEES_TO_MAKER_SATS * START_PRICE_USDEM2_PER_BCH / SATS_PER_BCH)
        expected_fee_oracleUnits_to_taker_at_funding = oracle_class(TOTAL_FUNDING_FEES_TO_TAKER_SATS * START_PRICE_USDEM2_PER_BCH / SATS_PER_BCH)

        # Short Maker
        self.assertEqual(short_maker_contract.fee_oracleUnits_to_short, expected_fee_oracleUnits_to_maker_at_funding)
        self.assertEqual(short_maker_contract.fee_oracleUnits_to_maker, expected_fee_oracleUnits_to_maker_at_funding)

        # Long Taker
        self.assertEqual(short_maker_contract.fee_oracleUnits_to_long, expected_fee_oracleUnits_to_taker_at_funding)
        self.assertEqual(short_maker_contract.fee_oracleUnits_to_taker, expected_fee_oracleUnits_to_taker_at_funding)

        # Long Maker
        self.assertEqual(long_maker_contract.fee_oracleUnits_to_long, expected_fee_oracleUnits_to_maker_at_funding)
        self.assertEqual(long_maker_contract.fee_oracleUnits_to_maker, expected_fee_oracleUnits_to_maker_at_funding)

        # Short Taker
        self.assertEqual(long_maker_contract.fee_oracleUnits_to_short, expected_fee_oracleUnits_to_taker_at_funding)
        self.assertEqual(long_maker_contract.fee_oracleUnits_to_taker, expected_fee_oracleUnits_to_taker_at_funding)


# Valid timestamp, just before maturity
BEFORE_MATURITY_TIMESTAMP = ScriptTimestamp(MATURITY_TIMESTAMP - 1)

# A valid maturity price, just somewhat over the start price so no chance of low liquidation
NAIVE_MATURITY_PRICE_USDEM2_PER_BCH = ScriptPriceInOracleUnitsPerBch(220_00)  # $220.00
BELOW_LIQUIDATING_PRICE_USDEM2_PER_BCH = ScriptPriceInOracleUnitsPerBch(LOW_LIQUIDATION_PRICE - 10)


class TestRedemption(unittest.TestCase):
    def test_matures_at_maturity_time(self):
        redemption = standard_contract_funding().redeem(
            price_timestamp=MATURITY_TIMESTAMP,
            price_oracleUnits_per_bch=NAIVE_MATURITY_PRICE_USDEM2_PER_BCH,
            force_maturity=False,
        )
        self.assertEqual(redemption.redemption_type, RedemptionType.MATURATION)

    def test_matures_at_maturity_time_even_if_liquidating_price(self):
        redemption = standard_contract_funding().redeem(
            price_timestamp=MATURITY_TIMESTAMP,
            price_oracleUnits_per_bch=LOW_LIQUIDATION_PRICE,
            force_maturity=False,
        )
        self.assertEqual(redemption.redemption_type, RedemptionType.MATURATION)

    def test_fails_to_mature_before_maturity_time(self):
        with self.assertRaises(UnredeemableError):
            standard_contract_funding().redeem(
                price_timestamp=BEFORE_MATURITY_TIMESTAMP,
                price_oracleUnits_per_bch=NAIVE_MATURITY_PRICE_USDEM2_PER_BCH,
                force_maturity=False,
            )

    def test_liquidates_before_maturity_time_at_low_liquidation_price(self):
        redemption = standard_contract_funding().redeem(
            price_timestamp=BEFORE_MATURITY_TIMESTAMP,
            price_oracleUnits_per_bch=LOW_LIQUIDATION_PRICE,
            force_maturity=False,
        )
        self.assertEqual(redemption.redemption_type, RedemptionType.LIQUIDATION)

    def test_fails_to_liquidate_before_maturity_time_at_one_over_low_liquidation_price(self):
        valid_liquidation_timestamp = ScriptTimestamp(MATURITY_TIMESTAMP - 1)
        one_over_liquidation_price = ScriptPriceInOracleUnitsPerBch(LOW_LIQUIDATION_PRICE + 1)
        with self.assertRaises(UnredeemableError):
            standard_contract_funding().redeem(
                price_timestamp=valid_liquidation_timestamp,
                price_oracleUnits_per_bch=one_over_liquidation_price,
                force_maturity=False,
            )

    def test_maturation_works_if_force(self):
        too_early_maturation_timestamp = ScriptTimestamp(MATURITY_TIMESTAMP - 1)
        redemption = standard_contract_funding().redeem(
            price_timestamp=too_early_maturation_timestamp,
            price_oracleUnits_per_bch=NAIVE_MATURITY_PRICE_USDEM2_PER_BCH,
            force_maturity=True,
        )
        self.assertEqual(redemption.redemption_type, RedemptionType.MATURATION)

    def test_mutual_redemption_works_if_indicated(self):
        too_early_maturation_timestamp = ScriptTimestamp(MATURITY_TIMESTAMP - 1)
        redemption = standard_contract_funding().redeem(
            price_timestamp=too_early_maturation_timestamp,
            price_oracleUnits_per_bch=NAIVE_MATURITY_PRICE_USDEM2_PER_BCH,
            force_maturity=False,
            is_mutual_redemption=True,
        )
        self.assertEqual(redemption.redemption_type, RedemptionType.MUTUAL)

    def test_mutual_redemption_takes_precedence_over_forced_redemption(self):
        too_early_maturation_timestamp = ScriptTimestamp(MATURITY_TIMESTAMP - 1)
        redemption = standard_contract_funding().redeem(
            price_timestamp=too_early_maturation_timestamp,
            price_oracleUnits_per_bch=NAIVE_MATURITY_PRICE_USDEM2_PER_BCH,
            force_maturity=True,
            is_mutual_redemption=True,
        )
        self.assertEqual(redemption.redemption_type, RedemptionType.MUTUAL)


###################
# Redeemed Contract Tests
###################
# Derived short payout sats and units
# For pure hedge, calculated as max(dust, HEDGE_COMPOSITE // CLAMPED_PRICE - 0) (Note the integer division //)
SHORT_PAYOUT_SATS_AS_HEDGE = UtxoSats(45_454_545)  # 0.45454545... Bch
# For leveraged short, same calculation but the cost at high liquidation is not zero
# Calculated as SHORT_PAYOUT_SATS_AS_HEDGE - COST_SATS_FOR_NOMINAL_VALUE_AT_LEVERAGED_HIGH_LIQUIDATION
# Due to integer math, this *can* be zero like a perfect hedge in some extreme values.
SHORT_PAYOUT_SATS_AS_LEVERAGED_SHORT = UtxoSats(18_182_066)

# Calculated as SHORT_PAYOUT_SATS_AS_HEDGE * MATURITY_PRICE / SATS_PER_BCH
SHORT_PAYOUT_ORACLE_UNITS_AS_HEDGE_AT_REDEMPTION = UsdEM2Beta(9999.999900)  # 99.99999900000 USD

# Derived long payout sats and units
# Calculated as max(dust, TOTAL_INPUT - HEDGE_PAYOUT)
LONG_PAYOUT_SATS = UtxoSats(18_829_333)  # 0.18829... Bch
# Calculated as LONG_PAYOUT_SATS * MATURITY_PRICE / SATS_PER_BCH
LONG_PAYOUT_ORACLE_UNITS_AT_REDEMPTION = UsdEM2Beta(4142.45326)

# Derived total payout sats and units
# Calculated as SHORT_PAYOUT_SATS_AS_HEDGE + LONG_PAYOUT_SATS
TOTAL_PAYOUT_SATS_AS_HEDGE = UtxoSats(64283878)
# Calculated as SHORT_PAYOUT_ORACLE_UNITS_AS_HEDGE + LONG_PAYOUT_ORACLE_UNITS
TOTAL_PAYOUT_ORACLE_UNITS_AS_HEDGE_AT_REDEMPTION = UsdEM2Beta(14142.4532)

# Nominal value at payout
# Calculated as round_half_up(NOMINAL_VALUE_USDEM2 / float(CLAMPED_PRICE)) * SATS_PER_BCH
COST_SATS_FOR_NOMINAL_VALUE_AT_REDEMPTION = Sats(45_454_545)

# Create the set of redemption fees
REDEMPTION_FEES = (
    FEE_200000_TAKER_TO_MAKER,
)

# Manually group them by side and unit
TOTAL_REDEMPTION_FEES_TO_MAKER_SATS = Sats(FEE_200000_TAKER_TO_MAKER.amount_sats)
TOTAL_REDEMPTION_FEES_TO_TAKER_SATS = Sats(-FEE_200000_TAKER_TO_MAKER.amount_sats)

# Manually calculate total funding and redemption fees in oracle unit terms for checking gains
# TODO: these shouldn't be useful after reworking assumptions
TOTAL_FUNDING_FEES_TO_MAKER_ORACLE_UNITS_AT_START = UsdEM2Beta(TOTAL_FUNDING_FEES_TO_MAKER_SATS * START_PRICE_USDEM2_PER_BCH / SATS_PER_BCH)
TOTAL_FUNDING_FEES_TO_TAKER_ORACLE_UNITS_AT_START = UsdEM2Beta(TOTAL_FUNDING_FEES_TO_TAKER_SATS * START_PRICE_USDEM2_PER_BCH / SATS_PER_BCH)

# TODO: these should be the only ones we need after reworking assumptions
TOTAL_FUNDING_FEES_TO_MAKER_ORACLE_UNITS_AT_REDEMPTION = UsdEM2Beta(TOTAL_FUNDING_FEES_TO_MAKER_SATS * NAIVE_MATURITY_PRICE_USDEM2_PER_BCH / SATS_PER_BCH)
TOTAL_FUNDING_FEES_TO_TAKER_ORACLE_UNITS_AT_REDEMPTION = UsdEM2Beta(TOTAL_FUNDING_FEES_TO_TAKER_SATS * NAIVE_MATURITY_PRICE_USDEM2_PER_BCH / SATS_PER_BCH)
TOTAL_REDEMPTION_FEES_TO_MAKER_ORACLE_UNITS_AT_REDEMPTION = UsdEM2Beta(TOTAL_REDEMPTION_FEES_TO_MAKER_SATS * NAIVE_MATURITY_PRICE_USDEM2_PER_BCH / SATS_PER_BCH)
TOTAL_REDEMPTION_FEES_TO_TAKER_ORACLE_UNITS_AT_REDEMPTION = UsdEM2Beta(TOTAL_REDEMPTION_FEES_TO_TAKER_SATS * NAIVE_MATURITY_PRICE_USDEM2_PER_BCH / SATS_PER_BCH)


def standard_maturation(
        funding: ContractFunding | None = None,
        fee_agreements: Sequence[FeeAgreement] = REDEMPTION_FEES,
) -> ContractRedemption:
    funding = funding if funding is not None else standard_contract_funding()
    return funding.redeem(
        price_timestamp=MATURITY_TIMESTAMP,
        price_oracleUnits_per_bch=NAIVE_MATURITY_PRICE_USDEM2_PER_BCH,
        force_maturity=False,
        fee_agreements=fee_agreements,
    )


def standard_liquidation(
    price_timestamp: ScriptTimestamp = MATURITY_TIMESTAMP,
    price_oracleUnits_per_bch: ScriptPriceInOracleUnitsPerBch = LOW_LIQUIDATION_PRICE,
    fee_agreements: Sequence[FeeAgreement] = REDEMPTION_FEES,
) -> ContractRedemption:
    return standard_contract_funding().redeem(
        price_timestamp=price_timestamp,
        price_oracleUnits_per_bch=price_oracleUnits_per_bch,
        force_maturity=False,
        fee_agreements=fee_agreements,
    )


class TestNewRedemptionDerivedValues(unittest.TestCase):
    ######################
    # Exact secondary values derived from contract parameters
    ######################
    def test_price_is_not_clamped_at_liquidation_price(self):
        liquidation = standard_liquidation()
        self.assertEqual(liquidation.clamped_end_price_oracleUnits_per_bch, liquidation.naive_end_price_oracleUnits_per_bch)

    def test_price_is_clamped_below_liquidation(self):
        liquidation = standard_liquidation(price_oracleUnits_per_bch=BELOW_LIQUIDATING_PRICE_USDEM2_PER_BCH)
        self.assertGreater(liquidation.clamped_end_price_oracleUnits_per_bch, liquidation.naive_end_price_oracleUnits_per_bch)

    def test_total_payout_sats_has_correct_value(self):
        self.assertEqual(standard_maturation().total_payout_sats, TOTAL_PAYOUT_SATS_AS_HEDGE)

    def test_short_payout_sats_has_correct_value(self):
        self.assertEqual(standard_maturation().short_payout_sats, SHORT_PAYOUT_SATS_AS_HEDGE)

    def test_long_payout_sats_has_correct_value(self):
        self.assertEqual(standard_maturation().long_payout_sats, LONG_PAYOUT_SATS)

    ######################
    # Exact secondary unit values
    ######################
    def test_total_payout_units_has_correct_value(self):
        self.assertAlmostEqual(standard_maturation().total_payout_oracleUnits, TOTAL_PAYOUT_ORACLE_UNITS_AS_HEDGE_AT_REDEMPTION, delta=.001)

    def test_short_payout_units_has_correct_value(self):
        self.assertAlmostEqual(standard_maturation().short_payout_oracleUnits, SHORT_PAYOUT_ORACLE_UNITS_AS_HEDGE_AT_REDEMPTION, delta=.001)

    def test_long_payout_units_has_correct_value(self):
        self.assertAlmostEqual(standard_maturation().long_payout_oracleUnits, LONG_PAYOUT_ORACLE_UNITS_AT_REDEMPTION, delta=.001)

    ######################
    # Exact secondary gain values
    ######################
    def test_gain_sats(self):
        # Short Maker / Long Taker
        expected_gain_sats_to_short_maker_at_redemption = SHORT_PAYOUT_SATS_AS_HEDGE - SHORT_INPUT_SATS_AS_HEDGE + TOTAL_FUNDING_FEES_TO_MAKER_SATS + TOTAL_REDEMPTION_FEES_TO_MAKER_SATS
        expected_gain_sats_to_long_taker_at_redemption = LONG_PAYOUT_SATS - LONG_INPUT_SATS + TOTAL_FUNDING_FEES_TO_TAKER_SATS + TOTAL_REDEMPTION_FEES_TO_TAKER_SATS
        short_maker_contract = standard_maturation(standard_contract_funding(standard_contract_proposal(maker_side=Side.SHORT)))

        # Short Maker
        self.assertEqual(short_maker_contract.short_gain_sats, expected_gain_sats_to_short_maker_at_redemption)
        self.assertEqual(short_maker_contract.maker_gain_sats, expected_gain_sats_to_short_maker_at_redemption)

        # Long Taker
        self.assertEqual(short_maker_contract.long_gain_sats, expected_gain_sats_to_long_taker_at_redemption)
        self.assertEqual(short_maker_contract.taker_gain_sats, expected_gain_sats_to_long_taker_at_redemption)

        # Long Maker / Short Taker
        expected_gain_sats_to_long_maker_at_redemption = LONG_PAYOUT_SATS - LONG_INPUT_SATS + TOTAL_FUNDING_FEES_TO_MAKER_SATS + TOTAL_REDEMPTION_FEES_TO_MAKER_SATS
        expected_gain_sats_to_short_taker_at_redemption = SHORT_PAYOUT_SATS_AS_HEDGE - SHORT_INPUT_SATS_AS_HEDGE + TOTAL_FUNDING_FEES_TO_TAKER_SATS + TOTAL_REDEMPTION_FEES_TO_TAKER_SATS
        long_maker_contract = standard_maturation(standard_contract_funding(standard_contract_proposal(maker_side=Side.LONG)))

        # Long Maker
        self.assertEqual(long_maker_contract.long_gain_sats, expected_gain_sats_to_long_maker_at_redemption)
        self.assertEqual(long_maker_contract.maker_gain_sats, expected_gain_sats_to_long_maker_at_redemption)

        # Short Taker
        self.assertEqual(long_maker_contract.short_gain_sats, expected_gain_sats_to_short_taker_at_redemption)
        self.assertEqual(long_maker_contract.taker_gain_sats, expected_gain_sats_to_short_taker_at_redemption)

    def test_gain_oracleUnits(self):
        # Short Maker / Long Taker
        # TODO: this reveals the ambiguity between asset value at start and redemption.... we should assume the earlier fees are kept in BCH, not ASSET............
        # TODO: do a major update to py-anyhedge to reflect this after this update
        expected_gain_oracleUnits_to_short_maker_at_redemption = UsdEM2Beta(
            SHORT_PAYOUT_ORACLE_UNITS_AS_HEDGE_AT_REDEMPTION - SHORT_INPUT_ORACLE_UNITS_AS_HEDGE_AT_START + TOTAL_FUNDING_FEES_TO_MAKER_ORACLE_UNITS_AT_START + TOTAL_REDEMPTION_FEES_TO_MAKER_ORACLE_UNITS_AT_REDEMPTION
        )
        expected_gain_oracleUnits_to_long_taker_at_redemption = UsdEM2Beta(
            LONG_PAYOUT_ORACLE_UNITS_AT_REDEMPTION - LONG_INPUT_ORACLE_UNITS_AT_START + TOTAL_FUNDING_FEES_TO_TAKER_ORACLE_UNITS_AT_START + TOTAL_REDEMPTION_FEES_TO_TAKER_ORACLE_UNITS_AT_REDEMPTION
        )
        short_maker_contract = standard_maturation(standard_contract_funding(standard_contract_proposal(maker_side=Side.SHORT)))

        # Short Maker
        self.assertAlmostEqual(short_maker_contract.short_gain_oracleUnits, expected_gain_oracleUnits_to_short_maker_at_redemption)
        self.assertAlmostEqual(short_maker_contract.maker_gain_oracleUnits, expected_gain_oracleUnits_to_short_maker_at_redemption)

        # Long Taker
        self.assertAlmostEqual(short_maker_contract.long_gain_oracleUnits, expected_gain_oracleUnits_to_long_taker_at_redemption)
        self.assertAlmostEqual(short_maker_contract.taker_gain_oracleUnits, expected_gain_oracleUnits_to_long_taker_at_redemption)

        # Long Maker / Short Taker
        expected_gain_oracleUnits_to_long_maker_at_redemption = UsdEM2Beta(
            LONG_PAYOUT_ORACLE_UNITS_AT_REDEMPTION - LONG_INPUT_ORACLE_UNITS_AT_START + TOTAL_FUNDING_FEES_TO_MAKER_ORACLE_UNITS_AT_START + TOTAL_REDEMPTION_FEES_TO_MAKER_ORACLE_UNITS_AT_REDEMPTION
        )
        expected_gain_oracleUnits_to_short_taker_at_redemption = UsdEM2Beta(
            SHORT_PAYOUT_ORACLE_UNITS_AS_HEDGE_AT_REDEMPTION - SHORT_INPUT_ORACLE_UNITS_AS_HEDGE_AT_START + TOTAL_FUNDING_FEES_TO_TAKER_ORACLE_UNITS_AT_START + TOTAL_REDEMPTION_FEES_TO_TAKER_ORACLE_UNITS_AT_REDEMPTION
        )
        long_maker_contract = standard_maturation(standard_contract_funding(standard_contract_proposal(maker_side=Side.LONG)))

        # Long Maker
        self.assertAlmostEqual(long_maker_contract.long_gain_oracleUnits, expected_gain_oracleUnits_to_long_maker_at_redemption)
        self.assertAlmostEqual(long_maker_contract.maker_gain_oracleUnits, expected_gain_oracleUnits_to_long_maker_at_redemption)

        # Short Taker
        self.assertAlmostEqual(long_maker_contract.short_gain_oracleUnits, expected_gain_oracleUnits_to_short_taker_at_redemption)
        self.assertAlmostEqual(long_maker_contract.taker_gain_oracleUnits, expected_gain_oracleUnits_to_short_taker_at_redemption)

    ######################
    # Fee values
    ######################
    def test_fee_sats_to_side(self):
        # Confirm short maker and long taker
        short_maker_redemption = standard_maturation(standard_contract_funding(standard_contract_proposal(maker_side=Side.SHORT)))
        long_maker_redemption = standard_maturation(standard_contract_funding(standard_contract_proposal(maker_side=Side.LONG)))

        expected_fees_sats_to_maker = TOTAL_REDEMPTION_FEES_TO_MAKER_SATS
        expected_fees_sats_to_taker = TOTAL_REDEMPTION_FEES_TO_TAKER_SATS

        # Short Maker
        self.assertEqual(short_maker_redemption.fee_sats_to_short, expected_fees_sats_to_maker)
        self.assertEqual(short_maker_redemption.fee_sats_to_maker, expected_fees_sats_to_maker)

        # Long Taker
        self.assertEqual(short_maker_redemption.fee_sats_to_long, expected_fees_sats_to_taker)
        self.assertEqual(short_maker_redemption.fee_sats_to_taker, expected_fees_sats_to_taker)

        # Long Maker
        self.assertEqual(long_maker_redemption.fee_sats_to_long, expected_fees_sats_to_maker)
        self.assertEqual(long_maker_redemption.fee_sats_to_maker, expected_fees_sats_to_maker)

        # Short Taker
        self.assertEqual(long_maker_redemption.fee_sats_to_short, expected_fees_sats_to_taker)
        self.assertEqual(long_maker_redemption.fee_sats_to_taker, expected_fees_sats_to_taker)

    def test_fee_oracleUnits_to_side(self):
        # Confirm short maker and long taker
        short_maker_redemption = standard_maturation(standard_contract_funding(standard_contract_proposal(maker_side=Side.SHORT)))
        long_maker_redemption = standard_maturation(standard_contract_funding(standard_contract_proposal(maker_side=Side.LONG)))

        expected_fee_oracleUnits_to_maker_at_redemption = TOTAL_REDEMPTION_FEES_TO_MAKER_ORACLE_UNITS_AT_REDEMPTION
        expected_fee_oracleUnits_to_taker_at_redemption = TOTAL_REDEMPTION_FEES_TO_TAKER_ORACLE_UNITS_AT_REDEMPTION

        # Short Maker
        self.assertEqual(short_maker_redemption.fee_oracleUnits_to_short, expected_fee_oracleUnits_to_maker_at_redemption)
        self.assertEqual(short_maker_redemption.fee_oracleUnits_to_maker, expected_fee_oracleUnits_to_maker_at_redemption)

        # Long Taker
        self.assertEqual(short_maker_redemption.fee_oracleUnits_to_long, expected_fee_oracleUnits_to_taker_at_redemption)
        self.assertEqual(short_maker_redemption.fee_oracleUnits_to_taker, expected_fee_oracleUnits_to_taker_at_redemption)

        # Long Maker
        self.assertEqual(long_maker_redemption.fee_oracleUnits_to_long, expected_fee_oracleUnits_to_maker_at_redemption)
        self.assertEqual(long_maker_redemption.fee_oracleUnits_to_maker, expected_fee_oracleUnits_to_maker_at_redemption)

        # Short Taker
        self.assertEqual(long_maker_redemption.fee_oracleUnits_to_short, expected_fee_oracleUnits_to_taker_at_redemption)
        self.assertEqual(long_maker_redemption.fee_oracleUnits_to_taker, expected_fee_oracleUnits_to_taker_at_redemption)

    ######################
    # Sided versions of values
    ######################
    def test_all_sided_values(self):
        c = standard_maturation()
        self.assertEqual(c.maker_payout_sats, c.short_payout_sats)
        self.assertEqual(c.taker_payout_sats, c.long_payout_sats)
        self.assertEqual(c.maker_payout_oracleUnits, c.short_payout_oracleUnits)
        self.assertEqual(c.taker_payout_oracleUnits, c.long_payout_oracleUnits)
        self.assertEqual(c.maker_gain_sats, c.short_gain_sats)
        self.assertEqual(c.taker_gain_sats, c.long_gain_sats)
        self.assertEqual(c.maker_gain_oracleUnits, c.short_gain_oracleUnits)
        self.assertEqual(c.taker_gain_oracleUnits, c.long_gain_oracleUnits)
        self.assertEqual(c.maker_gain_percent_of_own_input, c.short_gain_percent_of_own_input)
        self.assertEqual(c.taker_gain_percent_of_own_input, c.long_gain_percent_of_own_input)

        c = standard_maturation(standard_contract_funding(standard_contract_proposal(maker_side=Side.LONG)))
        self.assertEqual(c.maker_payout_sats, c.long_payout_sats)
        self.assertEqual(c.taker_payout_sats, c.short_payout_sats)
        self.assertEqual(c.maker_payout_oracleUnits, c.long_payout_oracleUnits)
        self.assertEqual(c.taker_payout_oracleUnits, c.short_payout_oracleUnits)
        self.assertEqual(c.maker_gain_sats, c.long_gain_sats)
        self.assertEqual(c.taker_gain_sats, c.short_gain_sats)
        self.assertEqual(c.maker_gain_oracleUnits, c.long_gain_oracleUnits)
        self.assertEqual(c.taker_gain_oracleUnits, c.short_gain_oracleUnits)
        self.assertEqual(c.maker_gain_percent_of_own_input, c.long_gain_percent_of_own_input)
        self.assertEqual(c.taker_gain_percent_of_own_input, c.short_gain_percent_of_own_input)

    def test_parameterized_lookup_error_on_invalid_combinations(self):
        maker_short_maturation = standard_maturation(standard_contract_funding(standard_contract_proposal(maker_side=Side.SHORT)))
        with self.assertRaises(ValueError):
            maker_short_maturation.payout_sats(role=Role.MAKER, side=Side.LONG)
        with self.assertRaises(ValueError):
            maker_short_maturation.payout_sats(role=Role.TAKER, side=Side.SHORT)

        taker_short_maturation = standard_maturation(standard_contract_funding(standard_contract_proposal(maker_side=Side.LONG)))
        with self.assertRaises(ValueError):
            taker_short_maturation.payout_sats(role=Role.TAKER, side=Side.LONG)
        with self.assertRaises(ValueError):
            taker_short_maturation.payout_sats(role=Role.MAKER, side=Side.SHORT)


class TestHedgeVsLeveragedShort(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hedge_short = standard_contract_proposal()
        cls.leveraged_short = standard_contract_proposal(short_leverage=SHORT_LEVERAGE_NOT_1)

    def test_effective_nominal_value_oracleUnits(self):
        # The asset value is the same in both pure hedge and leveraged short
        self.assertEqual(self.hedge_short.effective_nominal_value_oracleUnits, EFFECTIVE_NOMINAL_VALUE_ORALCEUNITS)
        self.assertEqual(self.leveraged_short.effective_nominal_value_oracleUnits, EFFECTIVE_NOMINAL_VALUE_ORALCEUNITS)

    def test_cost_of_nominal_value_at_start_not_equivalent_to_short_input(self):
        # in the pure hedge case so far on AnyHedge, hedge input is equal to cost of nominal value at the start
        self.assertEqual(self.hedge_short.short_input_sats, self.hedge_short.cost_sats_for_nominal_value_at_start)

        # For leveraged shorts, they are not equal.
        self.assertNotEqual(self.leveraged_short.short_input_sats, self.leveraged_short.cost_sats_for_nominal_value_at_start)

        # Confirm that the new cost at start is correct
        self.assertEqual(self.leveraged_short.cost_sats_for_nominal_value_at_start, COST_SATS_FOR_NOMINAL_VALUE_AT_START)

    def test_high_liquidation_price_for_leveraged_short(self):
        self.assertEqual(self.leveraged_short.high_liquidation_price_oracleUnits_per_bch, HIGH_LIQUIDATION_PRICE_AS_LEVERAGED_SHORT)

    def test_cost_at_high_liquidation_for_hedge_vs_leveraged_short(self):
        self.assertEqual(self.hedge_short.cost_sats_for_nominal_value_at_high_liquidation, ZERO_COST_OF_NOMINAL_VALUE_AT_HEDGE_LIQUIDATION)
        self.assertEqual(self.leveraged_short.cost_sats_for_nominal_value_at_high_liquidation, COST_SATS_FOR_NOMINAL_VALUE_AT_LEVERAGED_HIGH_LIQUIDATION)

    def test_short_input_sats_for_leveraged_short(self):
        self.assertEqual(self.leveraged_short.short_input_sats, SHORT_INPUT_SATS_AS_LEVERAGED_SHORT)

    def test_total_input_sats_for_leveraged_short(self):
        self.assertEqual(self.leveraged_short.total_input_sats, TOTAL_INPUT_SATS_AS_LEVERAGED_SHORT)

    def test_effective_short_leverage_when_hedge_vs_leveraged_short(self):
        # Should report as exactly 1 for pure hedge
        self.assertEqual(self.hedge_short.effective_short_leverage, SHORT_LEVERAGE_1_AS_HEDGE)

        # Should report according to calculation for leveraged short (which can also be 1)
        self.assertAlmostEqual(self.leveraged_short.effective_short_leverage, SHORT_LEVERAGE_NOT_1, delta=.001)

    def test_short_payout_for_leveraged_short(self):
        leveraged_short_redemption = standard_maturation(standard_contract_funding(self.leveraged_short))
        self.assertEqual(leveraged_short_redemption.short_payout_sats, SHORT_PAYOUT_SATS_AS_LEVERAGED_SHORT)

    def test_cost_at_redemption_for_hedge_vs_leveraged_short(self):
        hedge_redemption = standard_maturation(standard_contract_funding(self.hedge_short))
        leveraged_short_redemption = standard_maturation(standard_contract_funding(self.leveraged_short))

        # hedge redemption should just be the short payout
        self.assertEqual(hedge_redemption.cost_sats_for_nominal_value_at_redemption, hedge_redemption.short_payout_sats)

        # leveraged short redemption is different from short payout
        self.assertNotEqual(leveraged_short_redemption.cost_sats_for_nominal_value_at_redemption, leveraged_short_redemption.short_payout_sats)
        self.assertEqual(leveraged_short_redemption.cost_sats_for_nominal_value_at_redemption, COST_SATS_FOR_NOMINAL_VALUE_AT_REDEMPTION)


class TestContractSide(unittest.TestCase):
    def test_from_string_works_for_known_api_values(self):
        self.assertEqual(Side.from_string('short'), Side.SHORT)
        self.assertEqual(Side.from_string('hedge'), Side.SHORT)
        self.assertEqual(Side.from_string('long'), Side.LONG)


if __name__ == '__main__':
    unittest.main()
