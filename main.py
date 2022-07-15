import streamlit as st
from math import gcd
import numpy as np

def main():

    st.markdown(
        """
        1. txtファイルアップロード
        2. readfile
        3. download
        """
    )

    #Streamlitにファイルアップロード
    file = st.file_uploader("Choose a file")
    plaintext = ""

    # ファイルの読み込み
    if st.button("readfile"):
        plaintext = readfile(file)
        #st.text("plaintext")
        #st.text(plaintext)

        public_key, private_key = generate_keys(101, 3259)

        encrypted_text = encrypt(plaintext, public_key)
        decrypted_text = decrypt(encrypted_text, private_key)

        st.text(f'''
        秘密鍵: {public_key}
        公開鍵: {private_key}
    
        平文:
        「{plaintext}」
    
        暗号文:
        「{sanitize(encrypted_text)}」
    
        平文 (復号後):
        「{decrypted_text}」
        '''[1:-1])

        href = f'<a href="data:text/plain;charset=UTF-8,{sanitize(encrypted_text)}" download="popopo.txt">Download File</a> (right-click and save as popopo.txt)'
        st.markdown(href, unsafe_allow_html=True)

def lcm(p, q):
  '''
  最小公倍数を求める。
  '''
  return (p * q) // gcd(p, q)


def generate_keys(p, q):
  '''
  与えられた 2 つの素数 p, q から秘密鍵と公開鍵を生成する。
  '''
  N = p * q
  L = lcm(p - 1, q - 1)

  for i in range(2, L):
    if gcd(i, L) == 1:
      E = i
      break

  for i in range(2, L):
    if (E * i) % L == 1:
      D = i
      break

  return (E, N), (D, N)


def encrypt(plain_text, public_key):
  '''
  公開鍵 public_key を使って平文 plain_text を暗号化する。
  '''
  E, N = public_key
  plain_integers = [ord(char) for char in plain_text]
  encrypted_integers = [pow(i, E, N) for i in plain_integers]
  encrypted_text = ''.join(chr(i) for i in encrypted_integers)

  return encrypted_text


def decrypt(encrypted_text, private_key):
  '''
  秘密鍵 private_key を使って暗号文 encrypted_text を復号する。
  '''
  D, N = private_key
  encrypted_integers = [ord(char) for char in encrypted_text]
  decrypted_intergers = [pow(i, D, N) for i in encrypted_integers]
  decrypted_text = ''.join(chr(i) for i in decrypted_intergers)

  return decrypted_text


def sanitize(encrypted_text):
  '''
  UnicodeEncodeError が置きないようにする。
  '''
  return encrypted_text.encode('utf-8', 'replace').decode('utf-8')


def readfile(file):
    '''
    ファイルをPythonに読み込ませる
    '''
    plaintext = str(file.read(), "utf-8")

    return plaintext

if __name__ == '__main__':
    main()