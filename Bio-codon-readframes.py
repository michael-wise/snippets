# A student I tutored on pythontutor.com wrote this code
# under loose guidance from me.

# It takes an mRNA sequence (containing valid start/stop codons).
# The first for loop scans until a start codon "AUG" is found.
# Once found, it uses a second for loop on all proceeding base pairs after AUG
# to find a valid stop codon.

# Version 1.0 (unmodified student version) 9-30-18

sequence = input("Enter mRNA sequence: ")
# mRNA = "ACCUAUGAUAACCUAAGCAGUUUGACG"
# mRNA = "AUGAUGAUGAUGAUGUGAUGAUGAUGA"
# mRNA = "UAUUUGUUAUAUGUAUUUGUUAUUAAAUUAAU"
# non_valid_stopCodon = "UAUUUGUUAUAUGUAUUUGUUAUUAAAUUUAU"

count = 0
for protein in sequence:
    proteinSeq = sequence[count:count+3]
    if "AUG" in proteinSeq:
        remainingSeq = sequence[count+3:]
        print(remainingSeq)
        break
    count += 1

codonCount = 0
count = 0
for protein in remainingSeq:
    proteinSeq = remainingSeq[count:count+3]
    if count%3 == 0:
        codonCount += 1
        if ('UAA' == proteinSeq) or ('UAG' == proteinSeq) or ('UGA' == proteinSeq):
            print("counted a codon")
            break
    count += 1

print(codonCount)