# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Plain BNF codes to SQL format conversion
# Enter BNF codes without formatting to return SQL compatible result

def SQLformatBNFcodes(bnfcodeslist):
    #Convert to list
    bnfcodeslist = bnfcodes.split('\n')

    #Remove empty list items
    bnfcodeslist = list(filter(None, bnfcodeslist))

    #Remove duplicate codes
    bnfcodeslist = list(set(bnfcodeslist))
    
    #Resort codes
    bnfcodeslist.sort()

    #Convert to quoted, comma seperated list
    bnfcodesstring = ', '.join(f'"{code}"' for code in bnfcodeslist)

    return bnfcodesstring


# +
bnfcodes = '''
0803042B0AAAAAA
0803042B0BBAAAA
0803042K0AAAAAA
0803042K0AAAAAA
0803042K0AAABAB
0803042K0BBAAAA
0803042K0BBABAB
0803042K0BCAAAA
0803042N0AAAAAA
0803042N0AAABAB
0803042N0AAACAC
0803042N0AAADAD
0803042N0AAAEAE
0803042N0AAAFAF
0803042N0BBAAAA
0803042N0BBABAB
0803042N0BBACAC
0803042N0BBADAD
0803042N0BCAAAA
0803042N0BCABAE
0803042N0BDAAAF
0803042P0AAAAAA
0803042P0AAABAB
0803042P0BBAAAA
0803042P0BCAAAB
0803042R0AAAAAA
0803042R0AAABAB
0803042R0BBAAAA
0803042R0BBABAB
0803042S0AAABAB
0803042S0BCAAAB
0803042W0AAAAAA
0803042W0BBAAAA
'''

bnfcodesstring = SQLformatBNFcodes(bnfcodes)
bnfcodesstring

# -

