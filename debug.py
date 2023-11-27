def caesar_cipher_decode(ciphertext, shift):
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():  # Only perform decryption on alphabets
            if char.isupper():
                start = ord('A')
            else:
                start = ord('a')

            decrypted_char = chr((ord(char) - start - shift) % 26 + start)
            plaintext += decrypted_char
        else:
            plaintext += char

    return plaintext

ciphertext = "Naljnl, Pnrfne jnf n fxvyyrq pbzzhavpngbe, naq ur hfrq n inevrgl bs zrgubqf gb xrrc uvf zrffntrf frperg sebz uvf rarzvrf. Bar bs gurfr zrgubqf jnf gur Pnrfne pvcure, n fvzcyr grpuavdhr gb boshfpngr pbzzhavpngvbaf. SYNT{ebgngr_gung_nycunorg}"

result_list = []

for shift in range(1, 27):  # Iterate through shifts from 1 to 26
    plain_text = caesar_cipher_decode(ciphertext, shift)
    result_list.append(plain_text)

with open("results.txt", "w") as file:
    # Write each result to the text file
    for result in result_list:
        file.write(result + "\n")

print("Results have been saved to results.txt")
