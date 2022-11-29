import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;

/**
 * DNA sequence converter
 * Input file is read by L bytes. Each byte of input file is considered to contain A-C-G-T base in 2 most
 * significant bits. The rest 6 bits contain quality score.
 * Input binary file is printed in FASTQ format.
 * Takes two arguments - file name and number L
 */
public class Main {

    static void convert_dna(String fileName, int L) {

        // bases alphabet
        final char[] BASES = {'A', 'C', 'G', 'T'};

        try (
            // open file
            InputStream inputStream = new FileInputStream(fileName)
        ) {
            int index = 1;
            byte[] data = new byte[L];
            int bytesRead;

            // read L bytes and write converted data
            while ((bytesRead = inputStream.read(data)) > 0) {
                System.out.println("@READ_" + index);

                // write 2 most significant bits of each byte converted to bases alphabet
                StringBuilder output = new StringBuilder(L);
                for (int i = 0; i < bytesRead; i++) {
                    output.append(BASES[Byte.toUnsignedInt(data[i]) >> 6]);
                }
                System.out.println(output);

                System.out.println("+READ_" + index);

                // write bytes without 2 most significant bits increased by 33
                output = new StringBuilder(L);
                for (int i = 0; i < bytesRead; i++) {
                    output.append((char)((data[i] & 0b00111111) + 33));
                }
                System.out.println(output);

                index++;

            }
        } catch (FileNotFoundException e) {
            System.out.println("Error: File not found: " + e);
            System.exit(10);
        } catch (IOException e) {
            System.out.println("Error: I/O Exception: " + e);
            System.exit(12);
        } catch (SecurityException e) {
            System.out.println("Error: Security exception: " + e);
            System.exit(11);
        }

    }

    public static void main(String[] args) {

        // check we have exaclty two parameters
        if (args.length != 2) {
            System.out.println("Error: Exactly two parameters must be specified: file name and positive number L.");
            System.exit(2);
        }

        // check second parameter L is positive number
        int L = -1;
        try {
            L = Integer.parseInt(args[1]);
        } catch (NumberFormatException e) {
            System.out.println("Error: Second parameter must be a positive number L.");
            System.exit(2);
        }
        if (L <= 0) {
            System.out.println("Error: Number L must be a positive number.");
            System.exit(12);
        }

        convert_dna(args[0], L);
    }
}