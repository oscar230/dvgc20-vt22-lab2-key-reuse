using System.Text;

namespace Lab2
{
    internal class OTPHelper
    {
        private const int DefaultSeed = 1337;

        internal static byte[] TextToBytes(string text) => Encoding.Unicode.GetBytes(text);

        internal static string BytesToText(byte[] bytes) => Encoding.Unicode.GetString(bytes);

        internal static byte[] GeneratePad(int size, int seed = DefaultSeed)
        {
            Random random = new(seed);
            var pad = new byte[size];
            random.NextBytes(pad);
            return pad;
        }

        internal static byte[] Encrypt(byte[] plaintext, byte[] pad)
        {
            var result = new byte[plaintext.Length];
            for (int i = 0; i < plaintext.Length; i++)
            {
                var sum = (int)plaintext[i] + (int)pad[i];
                if (sum > 255)
                    sum -= 255;
                result[i] = (byte)sum;
            }
            return result;
        }

        internal static byte[] Decrypt(byte[] ciphertext, byte[] pad)
        {
            var result = new byte[ciphertext.Length];
            for (int i = 0; i < ciphertext.Length; i++)
            {
                var dif = (int)ciphertext[i] - (int)pad[i];
                if (dif < 0)
                    dif += 255;
                result[i] = (byte)dif;
            }
            return result;
        }
    }
}
