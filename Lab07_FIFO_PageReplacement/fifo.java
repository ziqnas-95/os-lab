import java.util.*;

public class fifo {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int numPageFrame;
        String[] pages;

        System.out.print("Enter number of page frames : ");
        numPageFrame = sc.nextInt();
        sc.nextLine();

        System.out.print("Enter page sequence : ");
        pages = sc.nextLine().split(" ");
        sc.close();

        simulateFIFO(numPageFrame, pages);
    }

    public static void simulateFIFO(int numPageFrame, String[] pages){
        String[] frames = new String[numPageFrame];
        Arrays.fill(frames, "-");

        int replaceIndex = 0;
        int pageFaultCount = 0;

        //HEADER 
        System.out.printf("%-8s", "Time");
        System.out.printf("%-15s","Requested");
        for (int i = 0; i < numPageFrame; i++) {
            System.out.printf("%-10s", "Frame" + (i + 1));
        }
        System.out.printf("%-10s\n","Status");

        //ALGORITHM
        for (int t = 0; t < pages.length; t++) {

            String currentPage = pages[t];
            boolean hit = false;

            //CHECK PAGE HIT
            for (String frame : frames) {
                if (frame.equals(currentPage)) {
                    hit = true;
                    break;
                }
            }

            //PAGE FAULT
            if (!hit) {
                boolean inserted = false;
                pageFaultCount++;
                //SEARCH EMPTY SLOT
                for (int i = 0; i < numPageFrame; i++) {
                    if (frames[i].equals("-")) {
                        frames[i] = currentPage;
                        inserted = true;
                        break;
                    }
                }

                //IF NO EMPTY SLOT, FIFO REPLACEMENT
                if (!inserted) {
                    frames[replaceIndex] = currentPage;
                    replaceIndex = (replaceIndex + 1) % numPageFrame;
                }
            }

            //PRINT LINE BY LINE 
            System.out.printf("%-8s", "T" + (t + 1));
            System.out.printf("%-15s",currentPage);
            for (String frame : frames) {
                System.out.printf("%-10s", frame);
            }
            if(hit) System.out.printf("%-10s\n","Page Hit");
            else System.out.printf("%-10s\n","Page Fault");
        }
        System.out.println("Total page faults: " + pageFaultCount);
    }


}