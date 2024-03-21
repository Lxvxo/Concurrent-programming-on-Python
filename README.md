# Concurrent-programming-on-Python

# Table of Contents

1. [Introduction](#introduction)
2. [Horse Racing](#horse-racing)
3. [Estimation of PI using Arc-Tangent Method](#estimation-of-pi-using-arc-tangent-method)
4. [Ball Manager](#ball-manager)
5. [Merge Sort](#merge-sort)
6. [Restaurant Management](#restaurant-management)
7. [Temperature and Pressure Controller](#temperature-and-pressure-controller)
8. [Conclusion](#conclusion)

## INTRODUCTION

During this project, we had to complete various exercises to become familiar with parallel computing in Python. We completed 6 exercises, totaling 25 points. Initially, we each chose exercises to work on, and then we refined the programs together when they were nearly finished. We tried to adhere to the instructions provided and for better visibility, each of our exercises is decomposed into 3 sub-files: the main program, the file containing all the functions used, and the modifiable constants file.

## HORSE RACING

The horse racing exercise involved creating a referee to obtain real-time rankings of runners. A substantial part of the program was already provided. We created a process for our referee and initialized an array as a shared variable to store the positions of all players in real-time. Then, the referee distinguishes between arrived runners and runners still in the race, upon which it performs an insertion sort algorithm to determine the ranking. A betting system is also available where users can bet on a horse with a simple input. A personalized message is sent if their horse finishes in the top 3; otherwise, a defeat message is sent.

## ESTIMATION OF PI USING ARC-TANGENT METHOD

For the estimation of pi, we opted for an approximation using the arc-tangent method. By distributing the calculations across multiple processes (modifiable number of processes in constants), we assigned each process a list of integers for its calculations. Using a shared variable, we obtained the result.

## BALL MANAGER

We implemented a ball manager using multiple processes. We utilized a mutex and another semaphore. Additionally, we stored the number of available balls at all times so that each process could determine whether they could retrieve balls. Each process performs the tasks of requesting and returning balls. A controller is also present to display the available balls and terminate the program when all processes have finished their work.

## MERGE SORT

The exercise on merge sort was probably where we spent the most time. We modified the sort to divide the list into slices rather than two as usual. We attempted various methods such as separating the initial list into multiple processes or using a Pool, but without success. We found another method using pipes, which works correctly.

## RESTAURANT MANAGEMENT

Restaurant management is done by a main process (the head waiter) coordinating server processes. They use several shared variables to simulate necessary information. For example, the "buffer" variable stores customer orders and their numbers, and another variable stores server numbers along with their associated orders. The code is detailed, and we won't dwell on the specifics here.

## TEMPERATURE AND PRESSURE CONTROLLER

For the temperature and pressure controller, we use exactly 6 processes:
- The controller: the main process, which activates or deactivates heating or the pump using shared variables as booleans.
- A process simulating a decrease in temperature.
- A process simulating an increase in pressure.
- The heater: increases the temperature when activated.
- The pump: decreases the pressure when activated.
- A final process displaying the temperature in degrees Celsius and the pressure in bar. All constants are modifiable in the corresponding folder.

## CONCLUSION

In conclusion, all these exercises allowed us to experiment extensively with multiprocessing. Understanding semaphores, especially the concept of mutual exclusion, was well understood.

