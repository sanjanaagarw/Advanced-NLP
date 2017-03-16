import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class Entropy {
    public static void main(String args[]) throws IOException{
        Map<String, Integer> entropyMap = new HashMap<>();
        BufferedReader inputFile = null;
        String s;
        int startIndex, noOfPOSTags=0;
        String POSTag;
        float entropy = 0;
        for (int i = 1;i<=16;i++) {
            try {
                //File read
                inputFile = new BufferedReader(new FileReader("/Users/sanjanaagarwal/Desktop/Advanced NLP/fc2/A" + i));
            } catch (FileNotFoundException f) {
                System.out.println("File not found");
                f.printStackTrace();
            }
            while ((s = inputFile.readLine()) != null) {

                //Starting index of the POS tag. Taking substring of the tag
                startIndex = s.indexOf("\t", 14);
                POSTag = s.substring(14, startIndex);

                if (entropyMap.get(POSTag) == null) {
                    entropyMap.put(POSTag, 1);
                } else {
                    entropyMap.put(POSTag, entropyMap.get(POSTag) + 1);
                }
            }
        }
                for (String s1 : entropyMap.keySet()) {
                    System.out.println(s1 + ": " + entropyMap.get(s1));
                    noOfPOSTags++;
                }
                System.out.println("The total number of POS tags are: " + noOfPOSTags);

                //Entropy calculation
                for (String s1 : entropyMap.keySet()) {
                    entropy += (((float) entropyMap.get(s1)) / noOfPOSTags) *
                            (Math.log(((float) entropyMap.get(s1)) / noOfPOSTags) / Math.log(2));
                }
                System.out.println("Entropy of POS for the sub-corpora is: " + entropy);
                inputFile.close();
    }
}