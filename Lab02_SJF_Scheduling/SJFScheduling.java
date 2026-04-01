import java.util.*;

class Process {
    String id;
    int arrivalTime;
    int burstTime;
    int finishTime;
    int turnaroundTime;
    int waitingTime;
    boolean isCompleted;

    public Process(String id, int arrivalTime, int burstTime) {
        this.id = id;
        this.arrivalTime = arrivalTime;
        this.burstTime = burstTime;
        this.isCompleted = false;
    }
}

public class SJFScheduling {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        List<Process> processes = new ArrayList<>();

        System.out.print("Enter the number of processes/jobs: ");
        int numberOfProcesses = scanner.nextInt();

        for (int i = 0; i < numberOfProcesses; i++) {
            String processId = "P" + (i + 1);
            
            System.out.println("\nEnter details for " + processId + ":");
            System.out.print("Arrival Time: ");
            int arrivalTime = scanner.nextInt();
            
            System.out.print("Burst Time: ");
            int burstTime = scanner.nextInt();

            processes.add(new Process(processId, arrivalTime, burstTime));
        }

        System.out.println("\n=================================================================");
        System.out.println("          SHORTEST JOB FIRST (SJF) SCHEDULING ALGORITHM          ");
        System.out.println("=================================================================");
        
        runSJF(processes);
        
        scanner.close();
    }

    public static void runSJF(List<Process> pList) {
        int currentTime = 0;
        int completed = 0;
        int n = pList.size();
        double totalTAT = 0, totalWT = 0;

        while (completed < n) {
            Process shortestJob = null;
            int minBurstTime = Integer.MAX_VALUE;

            // Find all arrived processes and pick the shortest burst time
            for (Process p : pList) {
                if (!p.isCompleted && p.arrivalTime <= currentTime) {
                    
                    if (p.burstTime < minBurstTime) {
                        minBurstTime = p.burstTime;
                        shortestJob = p;
                    } 
                    // TIE-BREAKER use FCFS
                    else if (p.burstTime == minBurstTime) {
                        if (shortestJob != null && p.arrivalTime < shortestJob.arrivalTime) {
                            shortestJob = p;
                        }
                    }
                }
            }

            // Execute job
            if (shortestJob != null) {
                shortestJob.finishTime = currentTime + shortestJob.burstTime;
                shortestJob.turnaroundTime = shortestJob.finishTime - shortestJob.arrivalTime;
                shortestJob.waitingTime = shortestJob.turnaroundTime - shortestJob.burstTime;
                
                currentTime = shortestJob.finishTime;
                shortestJob.isCompleted = true;
                completed++;

                totalTAT += shortestJob.turnaroundTime;
                totalWT += shortestJob.waitingTime;
                
                System.out.printf("Process %s | Arrival: %d | Burst: %d | Finish: %2d | TAT: %2d | WT: %2d\n", 
                          shortestJob.id, shortestJob.arrivalTime, shortestJob.burstTime, 
                          shortestJob.finishTime, shortestJob.turnaroundTime, shortestJob.waitingTime);
            } else {
                // Move the clock forward if no process arrived
                currentTime++;
            }
        }
        
        System.out.println("-----------------------------------------------------------------");
        System.out.printf("Average Turnaround Time = %.2f\n", totalTAT / n);
        System.out.printf("Average Waiting Time    = %.2f\n", totalWT / n);
    }
}
