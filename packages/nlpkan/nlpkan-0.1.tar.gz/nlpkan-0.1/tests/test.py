import sys
sys.path.append('../')
from main import *

print("""{}\n{}\n{}""".format("_"*60, "Only Kannada Characters", "_"*60))

print(contains_only_kannada("ನಮsddಸ್ಕಾರ")) 
print(contains_only_kannada("ನಮಸ್ಕಾರ"))

print("""{}\n{}\n{}""".format("_"*60, "Remove Non Kannada Characters", "_"*60))

print(remove_non_kannada_characters("ನಮsddಸ್ಕಾರ")) 
print(remove_non_kannada_characters("ನಮಸ್ಕಾರddds")) 
print(remove_non_kannada_characters("ನಮ,ಸ್ಕಾರ")) 
print(remove_non_kannada_characters("$ನಮಸ್$ಕಾರ")) 
print(remove_non_kannada_characters("ನಮ ಸ್ಕಾರ"))
print(remove_non_kannada_characters("ನಮsssಸ್ಕಾರ")) 
print(remove_non_kannada_characters("ನಮಸ್ಕಾರ")) 
print(remove_non_kannada_characters("234543"))
print(remove_non_kannada_characters("safdjst4ds"))
print(remove_non_kannada_characters("ನಮಸ್ಕಾರ"))


print("""{}\n{}\n{}""".format("_"*60, "Remove Special Characters", "_"*60))

print(remove_special_characters("ನಮs,,ddಸ್ಕಾರ")) # ನಮsddಸಕರ
print(remove_special_characters("ನಮಸ್ಕಾರddds")) # True
print(remove_special_characters("ನಮ,ಸ್ಕಾರ")) # True
print(remove_special_characters("$ನಮಸ್$ಕಾರ")) # True
print(remove_special_characters("ನಮ ಸ್ಕಾರ")) # True
print(remove_special_characters("ನಮsssಸ್ಕಾರ")) # True
print(remove_special_characters("ನಮಸ್ಕಾರ")) # True
print(remove_special_characters("234543")) # True
print(remove_special_characters("safdjst4ds")) # True
print(remove_special_characters("ನಮಸ್ಕಾರ")) # True


print("""{}\n{}\n{}""".format("_"*60, "Remove Special Characters", "_"*60))

print(is_kannada_words("ನಮs,,ddಸ್ಕಾರ")) 
print(is_kannada_words("ನಮ dಸ್ಕಾರ")) 
print(is_kannada_words("ನಮs,ddಸ್ಕಾರ")) 
print(is_kannada_words("ನಮಸ್ಕಾರ")) 
print(is_kannada_words("ನಮಸ್ಕಾರ$")) 
print(is_kannada_words("SSನಮಸ್ಕರ")) 

