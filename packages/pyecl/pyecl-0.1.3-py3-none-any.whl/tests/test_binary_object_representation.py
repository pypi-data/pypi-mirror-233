"""Tests for handling mathematica's binary object representation.

This is primarily useful for dealing with compressed fields.
"""


from pyecl.models import ConstellationFieldParser


def test_decompress_integer():
    """Compress[4] -> 1:eJxTTMoPymRhYGAAAAtUAbI="""
    assert ConstellationFieldParser().decompress_field(b"1:eJxTTMoPymRhYGAAAAtUAbI=") == "4"


def test_decompress_large_integer():
    """
    In[1]:= Compress[90348590834890590349058038945]
    Out[1]:= 1:eJxTTMoP8pRlYGCwNDA2sTC1NLAAUpYGpiAukLIwMLawNDEFAJVXB6k=
    """
    assert (
        ConstellationFieldParser().decompress_field(b"1:eJxTTMoP8pRlYGCwNDA2sTC1NLAAUpYGpiAukLIwMLawNDEFAJVXB6k=")
        == "90348590834890590349058038945"
    )


def test_decompress_simpleFloat():
    """Compress[4.0] -> "1:eJxTTMoPKmIAAwEHABKtAgc=" """
    assert ConstellationFieldParser().decompress_field(b"1:eJxTTMoPKmIAAwEHABKtAgc=") == "4.0"


def test_decompress_complexFloat():
    """Compress[3.432643] -> "1:eJxTTMoPKlLeX9fBW8btAAAgJgRt" """
    assert ConstellationFieldParser().decompress_field(b"1:eJxTTMoPKlLeX9fBW8btAAAgJgRt") == "3.432643"


def test_decompress_string():
    """Compress["Hi There!"] -> "1:eJxTTMoPCuZkYGDwyFQIyUgtSlUEACgoBIs=" """
    assert ConstellationFieldParser().decompress_field(b"1:eJxTTMoPCuZkYGDwyFQIyUgtSlUEACgoBIs=") == "Hi There!"


def test_decompress_symbol():
    """Compress[Login] -> "1:eJxTTMoPKmZlYGDwyU/PzAMAGegDtg==" """
    assert ConstellationFieldParser().decompress_field(b"1:eJxTTMoPKmZlYGDwyU/PzAMAGegDtg==") == "Login"


def test_decompress_empty_list():
    """Compress[{}] -> "1:eJxTTMoPSmMAgmIWIOGTWVwCACIoA74=" """
    assert ConstellationFieldParser().decompress_field(b"1:eJxTTMoPSmMAgmIWIOGTWVwCACIoA74=") == "List[]"


def test_decompress_list_of_numbers():
    """Compress[{1, 2}] -> "1:eJxTTMoPSmNiYGAoZgESPpnFJZmMQEYmSAgATfoElQ==" """
    assert (
        ConstellationFieldParser().decompress_field(b"1:eJxTTMoPSmNiYGAoZgESPpnFJZmMQEYmSAgATfoElQ==") == "List[1, 2]"
    )


def test_decompress_large_matrix():
    """Large matricies of real numbers get compresed into a special format, which we test here"""
    with open("tests/decompress-large-matrix.dat", "rb") as handle:
        parsed_field = ConstellationFieldParser().parse_variable_unit_field(handle.read())

    # The result should look like:
    # {{0.min,-87.529Lsus},{0.016667min,-96.7016Lsus},<<357>>,{5.98333min,1742.05Lsus},{6.min,1009.1Lsus}}

    assert len(parsed_field) == 361
    assert parsed_field[0][0].value == 0.0
    assert parsed_field[0][0].unit == "Minutes"
    assert parsed_field[0][1].value == -87.528984
    assert parsed_field[0][1].unit == "IndependentUnit[Lsus]"
    assert parsed_field[-1][0].value == 6.0
    assert parsed_field[-1][0].unit == "Minutes"
    assert parsed_field[-1][1].value == 1009.098328
    assert parsed_field[-1][1].unit == "IndependentUnit[Lsus]"
