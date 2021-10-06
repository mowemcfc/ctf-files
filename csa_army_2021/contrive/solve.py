string = "srnwhpsrnrxieptkczusxaejvaxwhphkxbyorxisrntpnmxctpnsed"
d = {'a':'nco', 
    'b':'tev',  'c':'twp',  'd':'cro',  'e':'yre',  'f':'lyd',  'g':'aem',  'h':'bib',  'i':'dhs',  'j':'hyt',  'k':'ulq',  'l':'weq',  'm':'jlm',  'n':'vdr',  'o':'ewk',  'p':'ysf',  'q':'izd',  'r':'mfo',  's':'bcg',  't':'anw',  'u':'nnr',  'v':'bsw',  'w':'zte',  'x':'ihp',  'y':'qxv',  'z':'odq',  'A':'vax',  'B':'uix',  'C':'byo',  'D':'kcz',  'E':'uwj',  'F':'srn',  'G':'tpd',  'H':'ept',  'I':'whp',  'J':'rgi',  'K':'rdp',  'L':'oea',  'M':'aej',  'N':'hkx',  'O':'usx',  'P':'esv',  'Q':'rci',  'R':'gsq',  'S':'juu',  'T':'rxi',  'U':'myn',  'V':'kgk',  'W':'doz',  'X':'bda',  'Y':'ipl',  'Z':'ulg',  '0':'mxc',  '1':'sed',  '2':'tpn',  '3':'jxm',  '4':'uqf',  '5':'qsr',  '6':'hyx',  '7':'esb',  '8':'ent',  '9':'gxg'}
dict = {value:key for key, value in d.items()}
for i in range(0,len(string), 3):
    print(dict[string[i:i+3]], end='')
print('\n')
