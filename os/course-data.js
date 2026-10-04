const subjectName = "os";

const COURSE_DATA = {
  subjectName: "Operating Systems",
  units: [
    {
      unit: "I",
      title: "Introduction to Operating Systems and System Structure",
      topics: [
        "Operating System Objectives and Functions",
        "Computer-System Organization, Computer-System Architecture",
        "Operating-System Operations, Operating-System Structure",
        "Process Management Overview, Memory Management Overview, Storage Management Overview",
        "Protection and Security",
        "System Calls and Types of System Calls"
      ]
    },
    {
      unit: "II",
      title: "Process Management and CPU Scheduling",
      topics: [
        "Process Concept, Operations on Processes, Process States",
        "Process Control Block (PCB)",
        "Threads and Types of Threads, Multicore and Multithreading",
        "CPU Scheduling Concepts and Algorithms",
        "Thread Scheduling"
      ]
    },
    {
      unit: "III",
      title: "Process Synchronization and Concurrency",
      topics: [
        "Principles of Concurrency",
        "Interprocess Communication using Shared Memory and Message Passing",
        "Race Condition, Critical Section Problem",
        "Peterson's Solution, Fork() and Join()",
        "Synchronization Hardware Support",
        "Mutex Locks, Semaphores and their Implementation",
        "Classical Synchronization Problems including Bounded Buffer, Readers-Writers, Dining Philosophers, and Monitors"
      ]
    },
    {
      unit: "IV",
      title: "Deadlocks and Memory Management",
      topics: [
        "Deadlock Characterization, Deadlock Prevention, Ostrich Algorithm",
        "Deadlock Avoidance using Banker's Algorithm",
        "Deadlock Detection and Recovery",
        "Resource Allocation Graph, Wait-for Graph",
        "Address Binding, Swapping",
        "Contiguous Memory Allocation",
        "Segmentation, Paging"
      ]
    },
    {
      unit: "V",
      title: "Virtual Memory, File Systems, and Disk Management",
      topics: [
        "Virtual Memory Concepts, Demand Paging, Copy-on-Write",
        "Page Replacement Algorithms",
        "Allocation of Frames, Thrashing",
        "File and Directory Structure, Unix I-node Structure",
        "Disk Structure, Disk Attachment",
        "Disk Scheduling Algorithms"
      ]
    }
  ]
};

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { COURSE_DATA };
}