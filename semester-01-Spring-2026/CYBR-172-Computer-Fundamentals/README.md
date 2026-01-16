# CYBR 172 – Computer Fundamentals

This folder contains my lab reports, hardware diagrams, and terminology guides for CYBR 172.  
The goal of this class is to understand the "under the hood" mechanics of computing, from physical hardware to networking basics.

## What I’ll Focus On
* **Hardware Architecture** – Identifying components like CPU, RAM, and storage types.
* **Operating Systems** – Learning the basics of Windows, macOS, and Linux environments.
* **Networking Basics** – Understanding how data moves across the internet (TCP/IP, DNS).
* **Security Literacy** – Identifying common threats and basic defense mechanisms.

## How I’ll Use This Folder
* **labs/** – Documentation of hands-on activities and virtual machine setups.
* **glossary/** – Definitions for technical terms and acronyms (BIOS, GUI, SSD, etc.).
* **diagrams/** – Visual representations of system architecture and network topologies.

### System Architecture Overview
```mermaid
graph TD
    subgraph "CPU (The Brain)"
        CU[Control Unit] --- ALU[Arithmetic Logic Unit]
    end
    
    subgraph "Storage Hierarchy"
        RAM[RAM - Volatile Memory]
        SSD[SSD/HDD - Long-term Storage]
    end

    Input[Input Devices: Keyboard/Mouse] --> CU
    CU <--> RAM
    RAM <--> SSD
    ALU --> Output[Output: Monitor/Display]
