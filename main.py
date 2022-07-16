import streamlit as st
from math import gcd


def main():

    # タイトル
    st.title(".txt file to encrypt or decrypt")
    st.markdown(
        """
        #### 1. Insert number p, q
        #### 2. Upload .txt file
        #### 3. encrypt or decrypt
        """
    )

    # ページ内でp, qを入力
    p = st.number_input("p = ", key=int, step=1)
    q = st.number_input("q = ", key=int, step=1)

    # Streamlitにファイルアップロード
    file = st.file_uploader("Choose a file")

    # ファイルがアップロードされていなければ実行されない
    if file != None:

        # plaintextにfileの中身を代入
        plaintext = readfile(file)
        encrypted_text = plaintext
        decrypted_text = ""

        # 鍵の生成
        public_key, private_key = generate_keys(int(p), int(q))

        # 暗号化
        if st.button("encrypt", key=2):

            # 暗号化処理
            encrypted_text = encrypt(plaintext, public_key)

            # ページ出力
            st.text(
                f"""
            秘密鍵: {public_key}
            公開鍵: {private_key}
            
            平文:
            「{plaintext}」
            
            暗号文:
            「{sanitize(encrypted_text)}」
            
            """
            )

            # ダウンロードリンク
            href = f'<a href="data:text/plain;charset=UTF-8,{sanitize(encrypted_text)}" download="encrypted_file.txt">Download File</a> (right-click and save as encrypted_file.txt)'
            st.markdown(href, unsafe_allow_html=True)

        # 復号化
        if st.button("decrypt", key=3):

            # 復号化処理
            decrypted_text = decrypt(encrypted_text, private_key)

            # ページ出力
            st.text(
                f"""
            秘密鍵: {public_key}
            公開鍵: {private_key}
        
            平文:
            「{plaintext}」
        
            平文 (復号後):
            「{decrypted_text}」
            """
            )

            # ダウンロードリンク
            href = f'<a href="data:text/plain;charset=UTF-8,{decrypted_text}" download="decrypted_file.txt">Download File</a> (right-click and save as decrypted_file.txt)'
            st.markdown(href, unsafe_allow_html=True)


def lcm(p, q):
    """
    最小公倍数を求める。
    """
    return (p * q) // gcd(p, q)


def generate_keys(p, q):
    """
    与えられた 2 つの素数 p, q から秘密鍵と公開鍵を生成する。
    """
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
    """
    公開鍵 public_key を使って平文 plain_text を暗号化する。
    """
    E, N = public_key
    plain_integers = [ord(char) for char in plain_text]
    encrypted_integers = [pow(i, E, N) for i in plain_integers]
    encrypted_text = "".join(chr(i) for i in encrypted_integers)

    return encrypted_text


def decrypt(encrypted_text, private_key):
    """
    秘密鍵 private_key を使って暗号文 encrypted_text を復号する。
    """
    D, N = private_key
    encrypted_integers = [ord(char) for char in encrypted_text]
    decrypted_intergers = [pow(i, D, N) for i in encrypted_integers]
    decrypted_text = "".join(chr(i) for i in decrypted_intergers)

    return decrypted_text


def sanitize(encrypted_text):
    """
    UnicodeEncodeError が置きないようにする。
    """
    return encrypted_text.encode("utf-8", "replace").decode("utf-8")


def readfile(file):
    """
    ファイルをPythonに読み込ませる
    """
    plaintext = str(file.read(), "utf-8")

    return plaintext


if __name__ == "__main__":
    main()
