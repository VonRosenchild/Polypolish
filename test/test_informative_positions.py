"""
This module contains some tests for Poligner. To run them, execute `pytest` from the root Poligner
directory.

Copyright 2021 Ryan Wick (rrwick@gmail.com)
https://github.com/rrwick/Poligner

This file is part of Poligner. Poligner is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version. Poligner is distributed
in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details. You should have received a copy of the GNU General Public License along with Poligner.
If not, see <http://www.gnu.org/licenses/>.
"""

import poligner.informative_positions
import test.test_alignment


def test_get_pileup_1():
    """
    Tests a pileup from an unmasked read sequence.
    """
    a = test.test_alignment.prep_alignment()
    ref_seq = 'ATCGCAATTGTAGAAGGACCTAGGAAGCAAAAGTTTC' \
              'CTCTATGACGAGACGAACGTCGCTAACGAGCGACCTATAGCGTTTAAAATA' \
              'GGATTATCGAACACCGGTAG'
    alignments = {'read': [a]}
    pileup = poligner.informative_positions.get_pileup(['read'], alignments, 'ref', ref_seq)
    for i in range(37):
        assert pileup[i] == []
    assert pileup[37] == ['C']
    assert pileup[38] == ['T']
    assert pileup[39] == ['C']
    assert pileup[40] == ['T']
    assert pileup[41] == ['A']
    assert pileup[42] == ['T']
    assert pileup[43] == ['G']
    assert pileup[44] == ['A']
    assert pileup[45] == ['C']
    assert pileup[46] == ['G']
    assert pileup[47] == ['AC']
    assert pileup[48] == ['G']
    assert pileup[49] == ['A']
    assert pileup[50] == ['-']
    assert pileup[51] == ['-']
    assert pileup[52] == ['A']
    assert pileup[53] == ['A']
    assert pileup[54] == ['C']
    assert pileup[55] == ['G']
    assert pileup[56] == ['T']
    assert pileup[57] == ['C']
    assert pileup[58] == ['G']
    assert pileup[59] == ['C']
    assert pileup[60] == ['T']
    assert pileup[61] == ['CTGT']
    assert pileup[62] == ['A']
    assert pileup[63] == ['C']
    assert pileup[64] == ['G']
    assert pileup[65] == ['A']
    assert pileup[66] == ['G']
    assert pileup[67] == ['C']
    assert pileup[68] == ['G']
    assert pileup[69] == ['A']
    assert pileup[70] == ['C']
    assert pileup[71] == ['-']
    assert pileup[72] == ['T']
    assert pileup[73] == ['A']
    assert pileup[74] == ['T']
    assert pileup[75] == ['A']
    assert pileup[76] == ['G']
    assert pileup[77] == ['C']
    assert pileup[78] == ['G']
    assert pileup[79] == ['T']
    assert pileup[80] == ['T']
    assert pileup[81] == ['-']
    assert pileup[82] == ['A']
    assert pileup[83] == ['A']
    assert pileup[84] == ['A']
    assert pileup[85] == ['A']
    assert pileup[86] == ['T']
    assert pileup[87] == ['A']
    for i in range(88, 109):
        assert pileup[i] == []


def test_get_pileup_2():
    """
    Tests a pileup from a read sequence with a couple masked bases.
    """
    a = test.test_alignment.prep_alignment()
    ref_seq = 'ATCGCAATTGTAGAAGGACCTAGGAAGCAAAAGTTTC' \
              'CTCTATGACGAGACGAACGTCGCTAACGAGCGACCTATAGCGTTTAAAATA' \
              'GGATTATCGAACACCGGTAG'
    alignments = {'read': [a]}
    a.masked_read_positions = {6, 16}
    pileup = poligner.informative_positions.get_pileup(['read'], alignments, 'ref', ref_seq)
    assert pileup[41] == ['A']
    assert pileup[42] == ['T']
    assert pileup[43] == []
    assert pileup[44] == ['A']
    assert pileup[45] == ['C']
    assert pileup[46] == ['G']
    assert pileup[47] == ['AC']
    assert pileup[48] == ['G']
    assert pileup[49] == ['A']
    assert pileup[50] == ['-']
    assert pileup[51] == ['-']
    assert pileup[52] == ['A']
    assert pileup[53] == ['A']
    assert pileup[54] == []
    assert pileup[55] == ['G']
    assert pileup[56] == ['T']


def test_get_pileup_3():
    """
    Tests a pileup from a read sequence with masked base in an indel.
    """
    a = test.test_alignment.prep_alignment()
    ref_seq = 'ATCGCAATTGTAGAAGGACCTAGGAAGCAAAAGTTTC' \
              'CTCTATGACGAGACGAACGTCGCTAACGAGCGACCTATAGCGTTTAAAATA' \
              'GGATTATCGAACACCGGTAG'
    alignments = {'read': [a]}

    a.masked_read_positions = {10}
    pileup = poligner.informative_positions.get_pileup(['read'], alignments, 'ref', ref_seq)
    assert pileup[45] == ['C']
    assert pileup[46] == ['G']
    assert pileup[47] == []
    assert pileup[48] == ['G']
    assert pileup[49] == ['A']
    assert pileup[50] == ['-']
    assert pileup[51] == ['-']
    assert pileup[52] == ['A']
    assert pileup[53] == ['A']


def test_get_pileup_4():
    """
    Tests a pileup from a read sequence with masked base in an indel.
    """
    a = test.test_alignment.prep_alignment()
    ref_seq = 'ATCGCAATTGTAGAAGGACCTAGGAAGCAAAAGTTTC' \
              'CTCTATGACGAGACGAACGTCGCTAACGAGCGACCTATAGCGTTTAAAATA' \
              'GGATTATCGAACACCGGTAG'
    alignments = {'read': [a]}

    a.masked_read_positions = {11}
    pileup = poligner.informative_positions.get_pileup(['read'], alignments, 'ref', ref_seq)
    assert pileup[45] == ['C']
    assert pileup[46] == ['G']
    assert pileup[47] == []
    assert pileup[48] == ['G']
    assert pileup[49] == ['A']
    assert pileup[50] == ['-']
    assert pileup[51] == ['-']
    assert pileup[52] == ['A']
    assert pileup[53] == ['A']


def test_get_pileup_5():
    """
    Tests a pileup from a read sequence with masked base in an indel.
    """
    a = test.test_alignment.prep_alignment()
    ref_seq = 'ATCGCAATTGTAGAAGGACCTAGGAAGCAAAAGTTTC' \
              'CTCTATGACGAGACGAACGTCGCTAACGAGCGACCTATAGCGTTTAAAATA' \
              'GGATTATCGAACACCGGTAG'
    alignments = {'read': [a]}

    a.masked_read_positions = {13}
    pileup = poligner.informative_positions.get_pileup(['read'], alignments, 'ref', ref_seq)
    assert pileup[45] == ['C']
    assert pileup[46] == ['G']
    assert pileup[47] == ['AC']
    assert pileup[48] == ['G']
    assert pileup[49] == []
    assert pileup[50] == []
    assert pileup[51] == []
    assert pileup[52] == ['A']
    assert pileup[53] == ['A']
