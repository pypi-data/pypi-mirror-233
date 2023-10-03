import deprecation  # type: ignore
from importlib.metadata import version
from infix import shift_infix as infix  # type: ignore
from .primes import Primes


@infix
@deprecation.deprecated(
    deprecated_in="0.3",
    removed_in="1.0",
    current_version=version("peak-utility"),
    details="Use the standard python divmod function instead",
)
def div_mod(num, divisor):
    return divmod(num, divisor)


def have_common_divisor(num1, num2):
    if num1 == num2:
        return True
    if Primes.include(max(num1, num2)):
        return False
    for testnum in Primes.up_to(min(num1, num2)):
        if num1 % testnum == 0 and num2 % testnum == 0:
            return True
    return False
