import time
import hashlib
import hmac
import secrets

def main():
    a = "Welcome to Mercy HMAC checker\n"
    for ch in a:
        print(ch, end="", flush=True)
        time.sleep(.2)

    u = input("Please enter your secret message: ").encode()
    
    while True:
        k_l = input("Please enter how long you would like the key to be: ")

        if any(char.isalpha() for char in k_l):
            print("Key length does not accept any alpha characters")
            continue
        if not k_l.isdigit():
            print("Key length must only contain numbers")
            continue

        k_l = int(k_l)
        break
    
    match k_l:
        case e if e > 64:
            y = "Key length is greater than 64"
            for ch in y:
                print(ch, end="", flush=True)
                time.sleep(.2)
        case _:
            less = "Key length will have padded bytes added to it prior to hashing\n"
            for ch in less:
                print(ch, end="", flush=True)
                time.sleep(.1)

    k = secrets.token_bytes(k_l)
    h = hmac.new(k, u, hashlib.sha256)
    t = h.hexdigest()
    print("HMAC Digest: ", t)
    compare(t, k)

def compare(t, k):
    r = "Lets verify the authenticity of your message\n"
    for ch in r:
        print(ch, end="", flush=True)
        time.sleep(.2)
    rr = input("Please reenter the same message for authentication purposes: ").encode()

    new_hmac = hmac.new(k, rr, hashlib.sha256).hexdigest()

    if hmac.compare_digest(new_hmac, t):
        print("HMACs are the same. Integrity checked passed")
        print("HMAC Digest: ", t)
    else:
        print("HMACs are not the same. Integrity checked failed\n")
        print("Real HMAC: \n", t)
        print("Fake HMAC: \n", new_hmac)


if __name__ == "__main__":
    main()
