def bin_seq(n, seq="1"):
    if n <= 0:
        print(seq)
        return
    bin_seq(n - 1, seq + '0')
    bin_seq(n - 1, seq + '1')

bin_seq(int(input()) - 1)
