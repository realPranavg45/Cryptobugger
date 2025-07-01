export const mockPythonCode = `def montgomery_reduce(a):
    """Montgomery reduction implementation - BUGGY VERSION"""
    t = (a * QINV) & ((1 << 16) - 1)
    t = (a - t * Q) >> 16
    return t

def generate_zetas():
    """Generate NTT twiddle factors"""
    KYBER_Q = 3329
    KYBER_ROOT_OF_UNITY = 17
    
    zetas = []
    for i in range(256):
        # Issue: Missing proper Montgomery form conversion
        zeta = pow(KYBER_ROOT_OF_UNITY, bit_reverse(i, 8), KYBER_Q)
        zetas.append(montgomery_reduce(zeta * R_MOD_Q))
    
    return zetas

def bit_reverse(n, bits):
    """Bit reversal for NTT ordering"""
    result = 0
    for _ in range(bits):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result

# Constants (may be incorrect)
QINV = 62209  # Q^(-1) mod 2^16
Q = 3329
R_MOD_Q = 2285  # 2^16 mod Q`;

export const mockCCode = `// Reference C implementation
#define KYBER_Q 3329
#define QINV 62209 // q^(-1) mod 2^16
#define MONT 2285  // 2^16 mod q

static int16_t montgomery_reduce(int32_t a) {
    int16_t t;
    t = (int16_t)a * QINV;
    t = (a - (int32_t)t * KYBER_Q) >> 16;
    return t;
}

void generate_zetas(int16_t zetas[256]) {
    unsigned int i;
    const int16_t root = 17; // primitive 512th root of unity
    
    for(i = 0; i < 256; i++) {
        zetas[i] = montgomery_reduce(
            (int32_t)pow_mod(root, bit_reverse(i, 8), KYBER_Q) * MONT
        );
    }
}

static unsigned int bit_reverse(unsigned int n, int bits) {
    unsigned int r = 0;
    int i;
    for(i = 0; i < bits; i++) {
        r = (r << 1) | (n & 1);
        n >>= 1;
    }
    return r;
}`;

// Mock data for zetas arrays - these would normally come from actual implementations
export const mockPythonZetas = [
  2285, 2571, 2970, 1812, 1493, 1422, 287, 202, 3158, 622, 1577, 182, 962,
  2127, 1855, 1468, 573, 2004, 264, 383, 2500, 1458, 1727, 3199, 2648, 1017,
  732, 608, 1787, 411, 3124, 1758, 1223, 652, 2777, 1015, 2036, 1491, 3047,
  1785, 516, 3321, 3009, 2663, 1711, 2167, 126, 1469, 2476, 3239, 3058, 830,
  107, 1908, 3082, 2378, 2931, 961, 1821, 2604, 448, 2264, 677, 2054, 2226
];

export const mockCZetas = [
  2285, 2571, 2970, 1812, 1493, 1422, 287, 202, 3158, 622, 1577, 182, 962,
  2127, 1855, 1468, 573, 2004, 264, 383, 2500, 1458, 1727, 3199, 2648, 1017,
  732, 608, 1787, 411, 3124, 1758, 1223, 652, 2777, 1015, 2036, 1491, 3047,
  1785, 516, 3321, 3009, 2663, 1711, 2167, 126, 1469, 2476, 3239, 3058, 830,
  107, 1908, 3082, 2378, 2931, 961, 1821, 2604, 448, 2264, 677, 2054, 2227  // Note: last value differs
];